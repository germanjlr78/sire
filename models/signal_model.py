import numpy as np
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class SignalModel:
    """Señal discreta: muestras, frecuencia de muestreo y parámetros descriptivos."""
    time_vector: np.ndarray
    amplitude_vector: np.ndarray
    sampling_rate: float
    signal_type: str  # 'Sinusoidal', 'AM', 'FM', 'ASK', 'FSK', 'PSK', 'QAM'
    frequency: float
    amplitude: float
    digital_data: Optional[List[int]] = None  # Almacena la secuencia de bits si es digital
    # Los metadatos permiten registrar parámetros adicionales sin alterar la estructura base.
    metadata: dict = field(default_factory=dict)
