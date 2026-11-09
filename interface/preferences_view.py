from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QDoubleSpinBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from config.preferences import (
    DEFAULT_PREFERENCES,
    MAX_AMPLITUDE,
    MAX_SAMPLING_RATE,
    MAX_SIGNAL_FREQUENCY,
    MIN_AMPLITUDE,
    MIN_SAMPLING_RATE,
    MIN_SIGNAL_FREQUENCY,
    load_preferences,
    save_preferences,
)


class PreferencesView(QWidget):
    """Permite definir parámetros iniciales compartidos por las prácticas."""

    preferences_changed = Signal()

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._load_values()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        title = QLabel("Preferencias de simulación")
        title.setObjectName("PageTitle")
        description = QLabel(
            "Define los valores iniciales para las señales. También puedes "
            "ajustarlos individualmente en cada simulador. La frecuencia de "
            "muestreo mínima permite representar señales de hasta 400 Hz "
            "respetando el criterio de Nyquist."
        )
        description.setObjectName("MutedText")
        description.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(description)

        group = QGroupBox("Parámetros predeterminados")
        group.setStyleSheet("QGroupBox { color: #4cc9f0; font-weight: bold; }")
        form = QFormLayout(group)

        self.sampling_rate_input = QSpinBox()
        self.sampling_rate_input.setRange(MIN_SAMPLING_RATE, MAX_SAMPLING_RATE)
        self.sampling_rate_input.setSingleStep(500)
        self.sampling_rate_input.setSuffix(" Hz")
        form.addRow("Frecuencia de muestreo:", self.sampling_rate_input)

        self.amplitude_input = QDoubleSpinBox()
        self.amplitude_input.setRange(MIN_AMPLITUDE, MAX_AMPLITUDE)
        self.amplitude_input.setSingleStep(0.1)
        self.amplitude_input.setDecimals(1)
        self.amplitude_input.setSuffix(" V")
        form.addRow("Amplitud:", self.amplitude_input)

        self.signal_frequency_input = QSpinBox()
        self.signal_frequency_input.setRange(
            MIN_SIGNAL_FREQUENCY, MAX_SIGNAL_FREQUENCY
        )
        self.signal_frequency_input.setSuffix(" Hz")
        form.addRow("Frecuencia base / portadora:", self.signal_frequency_input)
        layout.addWidget(group)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self.reset_button = QPushButton("Restablecer valores iniciales")
        self.reset_button.clicked.connect(self._reset_defaults)
        buttons.addWidget(self.reset_button)

        self.save_button = QPushButton("Guardar preferencias")
        self.save_button.setObjectName("ActionButton")
        self.save_button.clicked.connect(self._save)
        buttons.addWidget(self.save_button)
        layout.addLayout(buttons)
        layout.addStretch()

    def _load_values(self):
        preferences = load_preferences()
        self.sampling_rate_input.setValue(preferences["sampling_rate"])
        self.amplitude_input.setValue(preferences["amplitude"])
        self.signal_frequency_input.setValue(preferences["signal_frequency"])

    def _save(self):
        try:
            save_preferences(
                self.sampling_rate_input.value(),
                self.amplitude_input.value(),
                self.signal_frequency_input.value(),
            )
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "Error al guardar", str(error))
            return

        self.preferences_changed.emit()
        QMessageBox.information(
            self,
            "Preferencias guardadas",
            "Los simuladores activos ya usan los nuevos valores predeterminados.",
        )

    def _reset_defaults(self):
        self.sampling_rate_input.setValue(DEFAULT_PREFERENCES["sampling_rate"])
        self.amplitude_input.setValue(DEFAULT_PREFERENCES["amplitude"])
        self.signal_frequency_input.setValue(
            DEFAULT_PREFERENCES["signal_frequency"]
        )
        self._save()
