import numpy as np
from typing import List
from models.signal_model import SignalModel

class ModulationEngine:
    """Motor de simulación matemática para modulaciones analógicas y digitales."""

    @staticmethod
    def generate_sinusoidal(amplitude: float, frequency: float, duration: float, sampling_rate: float, phase: float = 0.0) -> SignalModel:
        """Genera una señal sinusoidal pura."""
        # El intervalo entre muestras es 1/Fs; Fs debe superar el doble de la
        # frecuencia máxima para representar la onda sin aliasing (Nyquist).
        t = np.arange(0, duration, 1.0 / sampling_rate)
        s = amplitude * np.sin(2 * np.pi * frequency * t + phase)
        return SignalModel(t, s, sampling_rate, 'Sinusoidal', frequency, amplitude)

    @staticmethod
    def modulate_am(modulating_freq: float, carrier_freq: float, mu: float, amplitude_c: float, duration: float, sampling_rate: float) -> SignalModel:
        """Modulación en Amplitud (AM-DSB-FC) estándar."""
        t = np.arange(0, duration, 1.0 / sampling_rate)
        m_t = np.cos(2 * np.pi * modulating_freq * t)
        # mu controla cuánto varía la envolvente; mu <= 1 evita sobremodulación ideal.
        s_t = amplitude_c * (1.0 + mu * m_t) * np.cos(2 * np.pi * carrier_freq * t)
        return SignalModel(t, s_t, sampling_rate, 'AM', carrier_freq, amplitude_c, metadata={'mu': mu, 'fm': modulating_freq})

    @staticmethod
    def modulate_fm(modulating_freq: float, carrier_freq: float, beta: float, amplitude_c: float, duration: float, sampling_rate: float) -> SignalModel:
        """Modulación en Frecuencia (FM) analógica."""
        t = np.arange(0, duration, 1.0 / sampling_rate)
        # s(t) = Ac * cos(2*pi*fc*t + beta * sin(2*pi*fm*t))
        s_t = amplitude_c * np.cos(2 * np.pi * carrier_freq * t + beta * np.sin(2 * np.pi * modulating_freq * t))
        return SignalModel(t, s_t, sampling_rate, 'FM', carrier_freq, amplitude_c, metadata={'beta': beta, 'fm': modulating_freq})

    @staticmethod
    def _generate_digital_baseband(bits: List[int], bit_duration: float, sampling_rate: float) -> tuple:
        """Helper para mapear una lista de bits a muestras temporales."""
        # Cada bit ocupa un número entero de muestras; el recorte alinea ambas
        # secuencias cuando la duración no produce exactamente un entero de muestras.
        samples_per_bit = int(bit_duration * sampling_rate)
        t = np.arange(0, len(bits) * bit_duration, 1.0 / sampling_rate)
        
        # Extender el flujo de bits a un arreglo con la misma longitud que el tiempo
        bit_stream = np.repeat(bits, samples_per_bit)
        # Sincronizar dimensiones si hay pequeñas variaciones por redondeo
        bit_stream = bit_stream[:len(t)]
        return t, bit_stream, samples_per_bit

    @classmethod
    def modulate_ask(cls, bits: List[int], carrier_freq: float, amplitude: float, bit_duration: float, sampling_rate: float) -> SignalModel:
        """Modulación por Conmutación de Amplitud (ASK)."""
        t, bit_stream, _ = cls._generate_digital_baseband(bits, bit_duration, sampling_rate)
        s_t = bit_stream * amplitude * np.cos(2 * np.pi * carrier_freq * t)
        return SignalModel(t, s_t, sampling_rate, 'ASK', carrier_freq, amplitude, digital_data=bits)

    @classmethod
    def modulate_fsk(cls, bits: List[int], freq_0: float, freq_1: float, amplitude: float, bit_duration: float, sampling_rate: float) -> SignalModel:
        """Modulación por Conmutación de Frecuencia (FSK)."""
        t, bit_stream, _ = cls._generate_digital_baseband(bits, bit_duration, sampling_rate)
        # Frecuencia instantánea controlada por el flujo de bits
        frequencies = np.where(bit_stream == 1, freq_1, freq_0)
        # La fase es la suma discreta de la frecuencia instantánea; así cada
        # cambio de bit altera la pendiente de fase sin reiniciar la portadora.
        phase = 2 * np.pi * np.cumsum(frequencies) / sampling_rate
        s_t = amplitude * np.cos(phase)
        return SignalModel(t, s_t, sampling_rate, 'FSK', freq_1, amplitude, digital_data=bits, metadata={'freq_0': freq_0})

    @classmethod
    def modulate_psk(cls, bits: List[int], carrier_freq: float, amplitude: float, bit_duration: float, sampling_rate: float) -> SignalModel:
        """Modulación por Conmutación de Fase (BPSK)."""
        t, bit_stream, _ = cls._generate_digital_baseband(bits, bit_duration, sampling_rate)
        # Bit 1 -> Fase 0, Bit 0 -> Fase Pi (Inversión de fase / multiplicación por esquema NRZ)
        nrz_stream = np.where(bit_stream == 1, 1, -1)
        s_t = amplitude * nrz_stream * np.cos(2 * np.pi * carrier_freq * t)
        return SignalModel(t, s_t, sampling_rate, 'PSK', carrier_freq, amplitude, digital_data=bits)

    @staticmethod
    def modulate_qam16(bits: List[int], carrier_freq: float, bit_duration: float, sampling_rate: float, amplitude: float = 3.0) -> SignalModel:
        """Modulación por Amplitud en Cuadratura (16-QAM). Requiere múltiplos de 4 bits."""
        if len(bits) % 4 != 0:
            raise ValueError("El flujo de bits para 16-QAM debe ser múltiplo de 4.")
            
        # Cada grupo de 4 bits selecciona un punto (I, Q) de la constelación;
        # el orden Gray hace que puntos vecinos difieran en un solo bit.
        qam_map = {
            (0,0,0,0): (-3, 3), (0,0,0,1): (-3, 1), (0,0,1,1): (-3, -1), (0,0,1,0): (-3, -3),
            (0,1,0,0): (-1, 3), (0,1,0,1): (-1, 1), (0,1,1,1): (-1, -1), (0,1,1,0): (-1, -3),
            (1,1,0,0): (3, 3),  (1,1,0,1): (3, 1),  (1,1,1,1): (3, -1),  (1,1,1,0): (3, -3),
            (1,0,0,0): (1, 3),  (1,0,0,1): (1, 1),  (1,0,1,1): (1, -1),  (1,0,1,0): (1, -3)
        }
        
        samples_per_symbol = int((bit_duration * 4) * sampling_rate)
        num_symbols = len(bits) // 4
        t = np.arange(0, num_symbols * (bit_duration * 4), 1.0 / sampling_rate)
        
        i_components = []
        q_components = []
        
        for idx in range(num_symbols):
            chunk = tuple(bits[idx*4 : (idx+1)*4])
            I, Q = qam_map[chunk]
            i_components.extend([I] * samples_per_symbol)
            q_components.extend([Q] * samples_per_symbol)
            
        # La constelación usa niveles hasta 3; escalar por amplitude/3 conserva
        # su forma y permite que la preferencia controle el nivel de salida.
        scale = amplitude / 3.0
        i_signal = np.array(i_components)[:len(t)] * scale
        q_signal = np.array(q_components)[:len(t)] * scale
        
        # Las componentes I y Q usan portadoras en cuadratura (90°) y se suman
        # para transportar dos coordenadas del símbolo en una misma frecuencia.
        s_t = i_signal * np.cos(2 * np.pi * carrier_freq * t) - q_signal * np.sin(2 * np.pi * carrier_freq * t)
        return SignalModel(t, s_t, sampling_rate, 'QAM', carrier_freq, amplitude, digital_data=bits)
