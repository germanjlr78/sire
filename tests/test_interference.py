import unittest
import numpy as np
from core.modulation import ModulationEngine
from core.interference import InterferenceEngine

class TestInterferenceAndNoise(unittest.TestCase):

    def setUp(self):
        self.fs = 10000.0
        self.duration = 1.0
        # Generamos una señal sinusoidal limpia de referencia (Amplitud = 2.0 -> Potencia Teórica = A^2 / 2 = 2.0)
        self.clean_signal = ModulationEngine.generate_sinusoidal(
            amplitude=2.0, frequency=10.0, duration=self.duration, sampling_rate=self.fs
        )

    def test_awgn_snr_calculation(self):
        """Prueba que el ruido inyectado corresponda estadísticamente a la SNR solicitada."""
        target_snr_db = 10.0  # SNR lineal de 10
        noisy_signal = InterferenceEngine.apply_awgn(self.clean_signal, target_snr_db)
        
        # Extraer el perfil del ruido restando la señal limpia de la señal ruidosa
        extracted_noise = noisy_signal.amplitude_vector - self.clean_signal.amplitude_vector
        
        # Calcular potencias experimentales
        p_signal = np.mean(self.clean_signal.amplitude_vector ** 2)
        p_noise = np.mean(extracted_noise ** 2)
        
        calculated_snr_db = 10 * np.log10(p_signal / p_noise)
        
        # Al ser un proceso estocástico (aleatorio), permitimos un pequeño margen de tolerancia delta
        self.assertAlmostEqual(calculated_snr_db, target_snr_db, delta=0.5)

    def test_single_tone_interference_pockets(self):
        """Valida la adición lineal algebraica de una señal parásita."""
        int_freq = 50.0
        int_amp = 1.5
        
        interfered = InterferenceEngine.apply_single_tone_interference(
            self.clean_signal, interference_freq=int_freq, interference_amplitude=int_amp
        )
        
        # El límite dinámico absoluto teórico máximo de la suma de ambas ondas es 2.0 + 1.5 = 3.5
        self.assertTrue(np.max(np.abs(interfered.amplitude_vector)) <= 3.5001)

    def test_attenuation_bounds(self):
        """Asegura que el factor multiplicativo disminuya correctamente la potencia de la señal."""
        factor = 0.5
        attenuated = InterferenceEngine.apply_amplitude_attenuation(self.clean_signal, factor)
        
        # La amplitud máxima debe verse reducida exactamente a la mitad (2.0 * 0.5 = 1.0)
        self.assertAlmostEqual(np.max(np.abs(attenuated.amplitude_vector)), 1.0, places=4)

if __name__ == '__main__':
    unittest.main()
