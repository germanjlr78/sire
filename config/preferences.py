"""Lectura y persistencia de preferencias compartidas por los simuladores."""

from PySide6.QtCore import QSettings


DEFAULT_PREFERENCES = {
    "sampling_rate": 5000,
    "amplitude": 2.0,
    "signal_frequency": 50,
}

MIN_SAMPLING_RATE = 2000
MAX_SAMPLING_RATE = 20000
MIN_AMPLITUDE = 0.1
MAX_AMPLITUDE = 10.0
MIN_SIGNAL_FREQUENCY = 10
MAX_SIGNAL_FREQUENCY = 400


def load_preferences() -> dict:
    """Carga las preferencias del usuario y usa valores iniciales si aún no existen."""
    settings = QSettings("SIRE", "SIRE")
    return {
        "sampling_rate": settings.value(
            "sampling_rate", DEFAULT_PREFERENCES["sampling_rate"], type=int
        ),
        "amplitude": settings.value(
            "amplitude", DEFAULT_PREFERENCES["amplitude"], type=float
        ),
        "signal_frequency": settings.value(
            "signal_frequency", DEFAULT_PREFERENCES["signal_frequency"], type=int
        ),
    }


def save_preferences(sampling_rate: int, amplitude: float, signal_frequency: int) -> None:
    """Valida y guarda las preferencias; informa si el sistema no pudo persistirlas."""
    if not MIN_SAMPLING_RATE <= sampling_rate <= MAX_SAMPLING_RATE:
        raise ValueError("La frecuencia de muestreo debe estar entre 2000 y 20000 Hz.")
    if not MIN_AMPLITUDE <= amplitude <= MAX_AMPLITUDE:
        raise ValueError("La amplitud debe estar entre 0.1 y 10 V.")
    if not MIN_SIGNAL_FREQUENCY <= signal_frequency <= MAX_SIGNAL_FREQUENCY:
        raise ValueError("La frecuencia de señal debe estar entre 10 y 400 Hz.")

    settings = QSettings("SIRE", "SIRE")
    settings.setValue("sampling_rate", sampling_rate)
    settings.setValue("amplitude", amplitude)
    settings.setValue("signal_frequency", signal_frequency)
    settings.sync()
    if settings.status() != QSettings.Status.NoError:
        raise OSError("No se pudieron guardar las preferencias del usuario.")
