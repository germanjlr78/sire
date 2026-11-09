import numpy as np
from typing import List

class SignalMetrics:
    """Cálculo de métricas e indicadores de rendimiento de la señal."""

    @staticmethod
    def calculate_measured_snr(clean_vector: np.ndarray, noisy_vector: np.ndarray) -> float:
        """Calcula la SNR medida en dB comparando la señal limpia con la ruidosa."""
        # Al restar la referencia limpia se estima la perturbación introducida por el canal.
        power_signal = np.mean(clean_vector ** 2)
        noise_vector = noisy_vector - clean_vector
        power_noise = np.mean(noise_vector ** 2)
        
        if power_noise == 0:
            return 40.0 # Techo de rendimiento por aproximación
        return float(10 * np.log10(power_signal / power_noise))

    @staticmethod
    def calculate_ber(tx_bits: List[int], rx_bits: List[int]) -> float:
        """Calcula la Tasa de Error de Bit (BER)."""
        if not tx_bits or not rx_bits or len(tx_bits) != len(rx_bits):
            return 0.5 # Máxima incertidumbre si no hay sincronismo
        
        # BER es la fracción de posiciones distintas entre transmisión y recepción.
        errors = np.sum(np.array(tx_bits) != np.array(rx_bits))
        return float(errors / len(tx_bits))
