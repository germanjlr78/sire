import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QGroupBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.modulation import ModulationEngine
from core.interference import InterferenceEngine
from core.signal_recovery import SignalRecovery
from core.signal_metrics import SignalMetrics
from config.preferences import load_preferences

class MplRecoveryCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#1e1e24')
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#121214')
        self.axes.tick_params(colors='white')
        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        super().__init__(fig)

class RecoveryView(QWidget):
    """Módulo de Recuperación de Señales de SIRE (Fase 5)."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Panel Izquierdo
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        controls_layout.setSpacing(16)
        
        group_filter = QGroupBox("Control de Filtro FIR")
        group_filter.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        filter_layout = QVBoxLayout()
        
        self.lbl_cutoff = QLabel("Frecuencia de Corte: 40 Hz")
        filter_layout.addWidget(self.lbl_cutoff)
        self.slider_cutoff = QSlider(Qt.Orientation.Horizontal)
        preferences = load_preferences()
        self.slider_cutoff.setRange(10, int(preferences["sampling_rate"] * 0.4))
        self.slider_cutoff.setValue(min(200, int(preferences["signal_frequency"] * 1.5)))
        self.slider_cutoff.valueChanged.connect(self.update_simulation)
        filter_layout.addWidget(self.slider_cutoff)
        
        group_filter.setLayout(filter_layout)
        controls_layout.addWidget(group_filter)
        
        # Cuadro de Métricas
        group_metrics = QGroupBox("Métricas de Calidad de Señal")
        group_metrics.setStyleSheet("QGroupBox { color: #4cc9f0; font-weight: bold; }")
        metrics_layout = QVBoxLayout()
        self.lbl_snr_val = QLabel("SNR Medida: -- dB")
        self.lbl_snr_val.setStyleSheet("font-size: 14px; color: white;")
        metrics_layout.addWidget(self.lbl_snr_val)
        group_metrics.setLayout(metrics_layout)
        controls_layout.addWidget(group_metrics)
        
        main_layout.addLayout(controls_layout, stretch=1)
        
        # Panel Derecho Gráfico
        self.canvas = MplRecoveryCanvas(self)
        main_layout.addWidget(self.canvas, stretch=3)
        
        self.update_simulation()

    def update_simulation(self):
        cutoff = self.slider_cutoff.value()
        self.lbl_cutoff.setText(f"Frecuencia de Corte: {cutoff} Hz")
        
        preferences = load_preferences()
        fs = float(preferences["sampling_rate"])
        amplitude = preferences["amplitude"]
        signal_frequency = preferences["signal_frequency"]
        self.slider_cutoff.setRange(10, int(fs * 0.4))
        cutoff = self.slider_cutoff.value()
        duration = 0.4
        
        clean = ModulationEngine.generate_sinusoidal(
            amplitude=amplitude,
            frequency=signal_frequency,
            duration=duration,
            sampling_rate=fs,
        )
        
        # Mantener la interferencia por encima del corte permite mostrar el efecto
        # del filtro al variar la frecuencia útil predeterminada.
        interference_frequency = min(
            max(signal_frequency * 4, cutoff * 2),
            int(fs * 0.45),
        )
        interfered = InterferenceEngine.apply_single_tone_interference(
            clean,
            interference_freq=interference_frequency,
            interference_amplitude=amplitude * 0.6,
        )
        
        # 3. Escenario Receptor: Filtrar la señal
        recovered = SignalRecovery.apply_lowpass_fir(interfered, cutoff_freq=cutoff)
        
        # La referencia limpia permite medir el error residual después del filtrado.
        measured_snr = SignalMetrics.calculate_measured_snr(clean.amplitude_vector, recovered.amplitude_vector)
        self.lbl_snr_val.setText(f"SNR Post-Filtrado: {measured_snr:.2f} dB")
        
        # Renderizado
        self.axes = self.canvas.axes
        self.axes.clear()
        self.axes.plot(interfered.time_vector, interfered.amplitude_vector, color='#ff5555', alpha=0.4, label='Señal Ruidosa (Canal)')
        self.axes.plot(clean.time_vector, clean.amplitude_vector, color='#ffffff', linestyle='--', alpha=0.6, label='Señal Original')
        self.axes.plot(recovered.time_vector, recovered.amplitude_vector, color='#4cc9f0', linewidth=2, label='Señal Filtrada / Recuperada')
        
        self.axes.set_title("Proceso de Recuperación y Limpieza de la Señal", color='white')
        self.canvas.axes.set_xlabel("Tiempo (s)")
        self.canvas.axes.set_ylabel("Amplitud (V)")
        self.axes.legend(loc='upper right', facecolor='#121214', edgecolor='none', labelcolor='white')
        self.axes.grid(True, color='#2a2a35')
        self.canvas.draw()

    def apply_preferences(self):
        """Ajusta el corte inicial junto con los parámetros globales de señal."""
        preferences = load_preferences()
        max_cutoff = int(preferences["sampling_rate"] * 0.4)
        self.slider_cutoff.setRange(10, max_cutoff)
        self.slider_cutoff.setValue(
            min(max_cutoff, max(10, int(preferences["signal_frequency"] * 1.5)))
        )
        self.update_simulation()
