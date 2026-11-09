import unittest
import numpy as np
from core.modulation import ModulationEngine
from core.interference import InterferenceEngine
from core.signal_recovery import SignalRecovery
from core.signal_metrics import SignalMetrics

class TestSignalRecovery(unittest.TestCase):

    def setUp(self):
        self.fs = 2000.0
        self.duration = 0.5
        # Señal deseada de 10 Hz
        self.clean = ModulationEngine.generate_sinusoidal(1.0, 10.0, self.duration, self.fs)
        # Inyectamos tono parásito de alta frecuencia (300 Hz)
        self.interfered = InterferenceEngine.apply_single_tone_interference(self.clean, 300.0, 1.5)

    def test_lowpass_attenuation(self):
        """Verifica que el filtro atenúe las altas frecuencias y mejore la calidad medida."""
        # Filtrar con frecuencia de corte a 50 Hz (dejando pasar los 10 Hz y bloqueando los 300 Hz)
        recovered = SignalRecovery.apply_lowpass_fir(self.interfered, cutoff_freq=50.0)
        
        snr_antes = SignalMetrics.calculate_measured_snr(self.clean.amplitude_vector, self.interfered.amplitude_vector)
        snr_despues = SignalMetrics.calculate_measured_snr(self.clean.amplitude_vector, recovered.amplitude_vector)
        
        # La SNR medida debió mejorar (aumentar en dB) tras remover el tono parásito
        self.assertGreater(snr_despues, snr_antes)

if __name__ == '__main__':
    unittest.main()
