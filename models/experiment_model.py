import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional, List

@dataclass
class ExperimentModel:
    """Representa el registro de una práctica o simulación realizada en SIRE."""
    id: str
    name: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    signal_type: str = "Sinusoidal"
    carrier_freq: float = 0.0
    applied_noise: str = "Ninguno"
    measured_snr: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict:
        # Convertir el dataclass a tipos simples facilita su serialización como JSON.
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        # Centralizar la reconstrucción mantiene el formato del historial ligado al modelo.
        return cls(**data)
