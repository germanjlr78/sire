import numpy as np
from models.signal_model import SignalModel

class SignalRecovery:
    """Algoritmos de filtrado y recuperación de señales degradadas."""

    @staticmethod
    def apply_lowpass_fir(signal: SignalModel, cutoff_freq: float, num_taps: int = 61) -> SignalModel:
        """
        Aplica un filtro pasa-bajas FIR usando una ventana de Hamming.
        """
        fs = signal.sampling_rate
        nyquist = fs / 2.0
        norm_cutoff = cutoff_freq / nyquist
        
        if norm_cutoff >= 1.0:
            norm_cutoff = 0.99

        # Crear la respuesta al impulso ideal de un filtro pasa-bajas (Sinc)
        # El corte se normaliza respecto a Nyquist porque la sinc trabaja en ciclos/muestra.
        alpha = 0.5 * (num_taps - 1)
        m = np.arange(num_taps) - alpha
        # Evitar división entre cero en el centro
        h = np.zeros(num_taps)
        h[m == 0] = 2 * norm_cutoff
        h[m != 0] = np.sin(2 * np.pi * norm_cutoff * m[m != 0]) / (np.pi * m[m != 0])
        
        # La ventana de Hamming reduce las ondulaciones laterales que aparecen
        # al truncar la respuesta infinita ideal del filtro.
        window = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(num_taps) / (num_taps - 1))
        h = h * window
        h = h / np.sum(h) # Normalizar ganancia a 0 dB
        
        # La convolución FIR combina muestras vecinas con los coeficientes h.
        # 'same' conserva la longitud para poder comparar y graficar las señales.
        filtered_amplitude = np.convolve(signal.amplitude_vector, h, mode='same')
        
        return SignalModel(
            time_vector=signal.time_vector,
            amplitude_vector=filtered_amplitude,
            sampling_rate=fs,
            signal_type=f"Filtrada ({signal.signal_type})",
            frequency=signal.frequency,
            amplitude=signal.amplitude,
            digital_data=signal.digital_data,
            metadata=signal.metadata.copy()
        )
