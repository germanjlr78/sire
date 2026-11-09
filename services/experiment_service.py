import os
import json
from typing import List
from models.experiment_model import ExperimentModel

class ExperimentService:
    """Servicio para gestionar el almacenamiento local de las prácticas de laboratorio."""
    
    # Estas rutas son relativas al directorio desde donde se inicia la aplicación.
    DATA_DIR = os.path.join("data", "experiments")
    FILE_PATH = os.path.join(DATA_DIR, "history.json")

    @classmethod
    def _ensure_storage_exists(cls):
        """Garantiza la existencia del directorio de datos."""
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR, exist_ok=True)
        if not os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f)

    @classmethod
    def save_experiment(cls, experiment: ExperimentModel) -> bool:
        """Guarda un experimento en el archivo JSON local."""
        try:
            cls._ensure_storage_exists()
            experiments = cls.load_all_experiments()
            experiments.append(experiment)
            
            # JSON legible facilita inspeccionar y compartir el historial en prácticas.
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump([e.to_dict() for e in experiments], f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    @classmethod
    def load_all_experiments(cls) -> List[ExperimentModel]:
        """Carga el historial completo de experimentos."""
        cls._ensure_storage_exists()
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                return [ExperimentModel.from_dict(item) for item in data_list]
        except Exception:
            return []
