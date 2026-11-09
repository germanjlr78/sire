import numpy as np
from models.signal_model import SignalModel

class InterferenceEngine:
    """Motor matemático para inyectar ruido e interferencias en las señales de SIRE."""

    @staticmethod
    def apply_awgn(signal: SignalModel, snr_db: float) -> SignalModel:
        """
        Inyecta Ruido Blanco Gaussiano Aditivo (AWGN) basado en una SNR (dB) objetivo.
        Fórmula: SNR_dB = 10 * log10(Potencia_Señal / Potencia_Ruido)
        """
        s_t = signal.amplitude_vector
        
        # 1. Calcular la potencia media de la señal: P = (1/N) * sum(s(t)^2)
        signal_power = np.mean(s_t ** 2)
        if signal_power == 0:
            # Evitar división por cero si la señal está vacía o es nula
            signal_power = 1e-12 
            
        # Los decibelios son logarítmicos: 10^(SNR/10) convierte la razón de
        # potencias a escala lineal antes de calcular la potencia de ruido.
        snr_linear = 10 ** (snr_db / 10.0)
        
        # 3. Calcular la potencia requerida para el ruido
        noise_power = signal_power / snr_linear
        
        # Una variable gaussiana de media cero tiene potencia igual a su varianza;
        # por eso la desviación estándar requerida es la raíz de esa potencia.
        standard_deviation = np.sqrt(noise_power)
        noise = np.random.normal(0, standard_deviation, len(s_t))
        
        # 5. Sumar el ruido a la señal original
        noisy_amplitude = s_t + noise
        
        # Clonar metadatos y registrar la alteración
        updated_metadata = signal.metadata.copy()
        updated_metadata.update({'applied_noise': 'AWGN', 'snr_db': snr_db})
        
        return SignalModel(
            time_vector=signal.time_vector,
            amplitude_vector=noisy_amplitude,
            sampling_rate=signal.sampling_rate,
            signal_type=signal.signal_type,
            frequency=signal.frequency,
            amplitude=signal.amplitude,
            digital_data=signal.digital_data,
            metadata=updated_metadata
        )

    @staticmethod
    def apply_single_tone_interference(signal: SignalModel, interference_freq: float, interference_amplitude: float, phase: float = 0.0) -> SignalModel:
        """
        Suma una interferencia sinusoidal de tono único a la señal original.
        Útil para simular interferencias por canales adyacentes o armónicos no deseados.
        """
        t = signal.time_vector
        # Generar el tono no deseado
        i_t = interference_amplitude * np.sin(2 * np.pi * interference_freq * t + phase)
        
        # En un canal aditivo, la muestra recibida es la suma de señal e interferencia.
        interfered_amplitude = signal.amplitude_vector + i_t
        
        updated_metadata = signal.metadata.copy()
        updated_metadata.update({
            'applied_interference': 'Single Tone',
            'int_freq': interference_freq,
            'int_amp': interference_amplitude
        })
        
        return SignalModel(
            time_vector=t,
            amplitude_vector=interfered_amplitude,
            sampling_rate=signal.sampling_rate,
            signal_type=signal.signal_type,
            frequency=signal.frequency,
            amplitude=signal.amplitude,
            digital_data=signal.digital_data,
            metadata=updated_metadata
        )

    @staticmethod
    def apply_amplitude_attenuation(signal: SignalModel, attenuation_factor: float) -> SignalModel:
        """
        Simula pérdidas en el trayecto o desvanecimiento multiplicativo plano.
        attenuation_factor: Escala entre 0.0 (pérdida total) y 1.0 (sin degradación).
        """
        if not (0.0 <= attenuation_factor <= 1.0):
            raise ValueError("El factor de atenuación debe estar comprendido entre 0.0 y 1.0")
            
        attenuated_amplitude = signal.amplitude_vector * attenuation_factor
        
        updated_metadata = signal.metadata.copy()
        updated_metadata.update({'attenuation_factor': attenuation_factor})
        
        return SignalModel(
            time_vector=signal.time_vector,
            amplitude_vector=attenuated_amplitude,
            sampling_rate=signal.sampling_rate,
            signal_type=signal.signal_type,
            frequency=signal.frequency,
            amplitude=signal.amplitude,
            digital_data=signal.digital_data,
            metadata=updated_metadata
        )
