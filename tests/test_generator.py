import unittest
import numpy as np
from core.modulation import ModulationEngine

class TestSignalGenerationAndModulation(unittest.TestCase):

    def setUp(self):
        self.fs = 10000.0  # Frecuencia de muestreo estándar para pruebas
        self.duration = 1.0

    def test_sinusoidal_mathematics(self):
        """Valida que los picos máximos coincidan con la amplitud parametrizada."""
        amplitude = 5.0
        frequency = 10.0
        signal = ModulationEngine.generate_sinusoidal(amplitude, frequency, self.duration, self.fs)
        
        self.assertEqual(len(signal.time_vector), len(signal.amplitude_vector))
        self.assertAlmostEqual(np.max(signal.amplitude_vector), amplitude, places=4)

    def test_am_modulation_index(self):
        """Valida matemáticamente la envolvente de la modulación AM."""
        mu = 0.5
        ac = 2.0
        signal = ModulationEngine.modulate_am(modulating_freq=5, carrier_freq=100, mu=mu, amplitude_c=ac, duration=self.duration, sampling_rate=self.fs)
        
        # El valor máximo teórico de AM con mu=0.5 y Ac=2 es Ac*(1 + mu) = 3.0
        self.assertAlmostEqual(np.max(signal.amplitude_vector), ac * (1.0 + mu), places=2)

    def test_ask_amplitude_states(self):
        """Verifica que ASK conmuta correctamente la amplitud a 0 cuando el bit es 0."""
        bits = [1, 0, 1, 0]
        signal = ModulationEngine.modulate_ask(bits, carrier_freq=50, amplitude=1.0, bit_duration=0.25, sampling_rate=self.fs)
        
        # Dividir la señal en el bloque correspondiente al segundo bit (índice 1, que vale 0)
        samples_per_bit = int(0.25 * self.fs)
        second_bit_samples = signal.amplitude_vector[samples_per_bit : 2 * samples_per_bit]
        
        self.assertTrue(np.allclose(second_bit_samples, 0.0, atol=1e-5))

    def test_qam_amplitude_parameter_scales_signal(self):
        """Comprueba que la amplitud configurada escale la constelación 16-QAM."""
        bits = [1, 1, 0, 0]
        reference = ModulationEngine.modulate_qam16(
            bits, carrier_freq=50, bit_duration=0.05, sampling_rate=self.fs, amplitude=3.0
        )
        scaled = ModulationEngine.modulate_qam16(
            bits, carrier_freq=50, bit_duration=0.05, sampling_rate=self.fs, amplitude=1.0
        )

        self.assertTrue(np.allclose(scaled.amplitude_vector, reference.amplitude_vector / 3))

if __name__ == '__main__':
    unittest.main()
