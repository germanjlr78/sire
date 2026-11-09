import uuid
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QGroupBox, QComboBox, QSlider)
from PySide6.QtCore import Qt
from models.experiment_model import ExperimentModel
from services.experiment_service import ExperimentService
from core.modulation import ModulationEngine
from core.interference import InterferenceEngine
from core.signal_metrics import SignalMetrics
from config.preferences import load_preferences

class LaboratoryView(QWidget):
    """Módulo del Laboratorio de Prácticas e Historial de Experimentos de SIRE (Fase 6)."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(18)

        # ==========================================
        # SECCIÓN SUPERIOR: FORMULARIO DE PRÁCTICA
        # ==========================================
        group_experiment = QGroupBox("Ejecución de Práctica Guiada")
        group_experiment.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        exp_layout = QHBoxLayout()

        # Configuración rápida para la simulación
        vbox_inputs = QVBoxLayout()
        vbox_inputs.addWidget(QLabel("Nombre de la Práctica:"))
        self.txt_exp_name = QLineEdit("Práctica 1: Atenuación por Ruido Térmico")
        vbox_inputs.addWidget(self.txt_exp_name)

        vbox_inputs.addWidget(QLabel("Esquema de Señal:"))
        self.combo_sig = QComboBox()
        self.combo_sig.addItems(["Sinusoidal", "AM", "FM"])
        vbox_inputs.addWidget(self.combo_sig)
        self.lbl_defaults = QLabel()
        self.lbl_defaults.setWordWrap(True)
        self.lbl_defaults.setStyleSheet("color: #a0a0a0;")
        vbox_inputs.addWidget(self.lbl_defaults)

        exp_layout.addLayout(vbox_inputs, stretch=2)

        vbox_noise = QVBoxLayout()
        vbox_noise.addWidget(QLabel("Inyectar Ruido AWGN (SNR objetivo):"))
        self.slider_snr = QSlider(Qt.Orientation.Horizontal)
        self.slider_snr.setRange(0, 30)
        self.slider_snr.setValue(12)
        vbox_noise.addWidget(self.slider_snr)

        self.btn_run_save = QPushButton("✓ Ejecutar y Guardar en Historial")
        self.btn_run_save.setStyleSheet("background-color: #4cc9f0; color: #121214; font-weight: bold; padding: 8px;")
        self.btn_run_save.clicked.connect(self.execute_and_log_experiment)
        vbox_noise.addWidget(self.btn_run_save)

        exp_layout.addLayout(vbox_noise, stretch=2)
        group_experiment.setLayout(exp_layout)
        main_layout.addWidget(group_experiment)

        # ==========================================
        # SECCIÓN INFERIOR: TABLA DE HISTORIAL
        # ==========================================
        group_history = QGroupBox("Historial Local de Experimentos Registrados")
        group_history.setStyleSheet("QGroupBox { color: #4cc9f0; font-weight: bold; }")
        history_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha / Hora", "Nombre del Experimento", "Señal", "Ruido Inyectado", "SNR Medida"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("QTableWidget { color: white; background-color: #121214; }")
        history_layout.addWidget(self.table)

        group_history.setLayout(history_layout)
        main_layout.addWidget(group_history, stretch=1)

        # Cargar los datos guardados al iniciar la vista
        self.apply_preferences()
        self.refresh_history_table()

    def execute_and_log_experiment(self):
        """Simula la señal seleccionada, calcula métricas y persiste el resultado."""
        name = self.txt_exp_name.text().strip()
        sig_type = self.combo_sig.currentText()
        target_snr = self.slider_snr.value()

        if not name:
            QMessageBox.warning(self, "Validación", "Por favor ingresa un nombre para el experimento.")
            return

        # La práctica usa los valores globales y el tipo de señal seleccionado.
        preferences = load_preferences()
        fs = float(preferences["sampling_rate"])
        amplitude = preferences["amplitude"]
        frequency = preferences["signal_frequency"]
        if sig_type == "AM":
            clean = ModulationEngine.modulate_am(
                modulating_freq=5,
                carrier_freq=frequency,
                mu=0.7,
                amplitude_c=amplitude,
                duration=0.2,
                sampling_rate=fs,
            )
        elif sig_type == "FM":
            clean = ModulationEngine.modulate_fm(
                modulating_freq=4,
                carrier_freq=frequency,
                beta=5.0,
                amplitude_c=amplitude,
                duration=0.2,
                sampling_rate=fs,
            )
        else:
            clean = ModulationEngine.generate_sinusoidal(
                amplitude=amplitude,
                frequency=frequency,
                duration=0.2,
                sampling_rate=fs,
            )
        noisy = InterferenceEngine.apply_awgn(clean, snr_db=float(target_snr))
        measured_snr = SignalMetrics.calculate_measured_snr(clean.amplitude_vector, noisy.amplitude_vector)

        # El modelo reúne parámetros y resultado para guardar una instantánea del ensayo.
        new_experiment = ExperimentModel(
            id=str(uuid.uuid4())[:8].upper(),
            name=name,
            signal_type=sig_type,
            carrier_freq=frequency,
            applied_noise=f"AWGN ({target_snr} dB)",
            measured_snr=round(measured_snr, 2),
            notes="Simulación educativa automatizada."
        )

        # La vista delega la persistencia para separar interfaz y acceso a archivos.
        if ExperimentService.save_experiment(new_experiment):
            self.refresh_history_table()
            QMessageBox.information(self, "Éxito", f"Experimento '{name}' guardados en el historial de forma exitosa.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo escribir el archivo de datos local.")

    def apply_preferences(self):
        """Muestra los parámetros globales que utilizará la próxima práctica."""
        preferences = load_preferences()
        self.lbl_defaults.setText(
            "Predeterminados: "
            f"{preferences['signal_frequency']} Hz · "
            f"{preferences['amplitude']:.1f} V · "
            f"muestreo {preferences['sampling_rate']} Hz"
        )

    def refresh_history_table(self):
        """Lee el archivo JSON de persistencia y rellena la tabla de PySide6."""
        experiments = ExperimentService.load_all_experiments()
        self.table.setRowCount(0)

        for idx, exp in enumerate(experiments):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(exp.id))
            self.table.setItem(idx, 1, QTableWidgetItem(exp.timestamp))
            self.table.setItem(idx, 2, QTableWidgetItem(exp.name))
            self.table.setItem(idx, 3, QTableWidgetItem(exp.signal_type))
            self.table.setItem(idx, 4, QTableWidgetItem(exp.applied_noise))
            self.table.setItem(idx, 5, QTableWidgetItem(f"{exp.measured_snr} dB"))
