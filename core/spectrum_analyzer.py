import numpy as np
from models.signal_model import SignalModel

class SpectrumAnalyzer:
    """Motor matemático para calcular la FFT y transformar señales al dominio de la frecuencia."""

    @staticmethod
    def calculate_fft(signal: SignalModel) -> tuple:
        """
        Calcula la FFT unilateral de una señal y devuelve el vector de frecuencias y magnitudes en dB.
        
        Regresa:
            frequencies (np.ndarray): Eje X en Hz.
            magnitude_db (np.ndarray): Eje Y en dB (normalizado respecto al pico).
        """
        y = signal.amplitude_vector
        n = len(y)
        fs = signal.sampling_rate

        if n == 0:
            return np.array([]), np.array([])

        # La FFT descompone las muestras en componentes de frecuencia discretas.
        fft_values = np.fft.fft(y)
        
        # 2. Obtener la magnitud absoluta y normalizarla por el número de muestras
        frequencies = np.fft.fftfreq(n, 1.0 / fs)
        magnitude = np.abs(fft_values) / n

        # Para señales reales, la mitad negativa es redundante (simetría conjugada).
        half_n = n // 2
        frequencies = frequencies[:half_n]
        magnitude = magnitude[:half_n]

        # Multiplicar por 2 para conservar la energía (excepto la componente DC)
        if len(magnitude) > 1:
            magnitude[1:] = 2 * magnitude[1:]

        # 4. Convertir a Decibelios (dB). Añadimos un pequeño offset para evitar log10(0)
        # Se normaliza respecto al valor máximo para que el pico más alto sea 0 dB de forma estándar
        max_val = np.max(magnitude) if np.max(magnitude) > 0 else 1e-12
        magnitude_db = 20 * np.log10(magnitude / max_val + 1e-12)

        return frequencies, magnitude_db
