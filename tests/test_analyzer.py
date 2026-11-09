import unittest
import numpy as np
from core.modulation import ModulationEngine
from core.spectrum_analyzer import SpectrumAnalyzer

class TestSpectrumAnalyzer(unittest.TestCase):

    def setUp(self):
        self.fs = 2000.0  # Frecuencia de muestreo
        self.duration = 1.0

    def test_fft_peak_detection(self):
        """Valida que el analizador detecte el pico máximo exactamente en la frecuencia de la señal."""
        target_frequency = 150.0  # Hz
        
        # Generar señal limpia de 150 Hz
        signal = ModulationEngine.generate_sinusoidal(
            amplitude=1.0, frequency=target_frequency, duration=self.duration, sampling_rate=self.fs
        )
        
        # Calcular espectro
        frequencies, magnitude_db = SpectrumAnalyzer.calculate_fft(signal)
        
        # Encontrar el índice donde se encuentra la máxima magnitud en dB
        peak_index = np.argmax(magnitude_db)
        detected_frequency = frequencies[peak_index]
        
        # Validar con un delta de tolerancia según la resolución del contenedor FFT
        self.assertAlmostEqual(detected_frequency, target_frequency, delta=1.0)

if __name__ == '__main__':
    unittest.main()
