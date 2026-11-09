import sys
import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QComboBox, QDoubleSpinBox, QGroupBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.modulation import ModulationEngine
from core.interference import InterferenceEngine
from config.preferences import load_preferences

class MplCanvas(FigureCanvas):
    """Lienzo para incrustar gráficas de Matplotlib en PySide6 para simulación de interferencias."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#1e1e24')  # Fondo oscuro a juego con tu Dashboard
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#121214')
        self.axes.tick_params(colors='white')
        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        super().__init__(fig)

class InterferenceView(QWidget):
    """Módulo de Simulación de Interferencias de SIRE (Fase 3)."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # ==========================================
        # PANEL IZQUIERDO: CONTROLES DE CONFIGURACIÓN
        # ==========================================
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        controls_layout.setSpacing(14)
        
        # 1. Configuración de la Señal Base
        group_base = QGroupBox("Señal Base Deseada")
        group_base.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        base_layout = QVBoxLayout()
        
        base_layout.addWidget(QLabel("Tipo de Señal:"))
        self.combo_base_type = QComboBox()
        self.combo_base_type.addItems(["Sinusoidal", "AM", "FM"])
        self.combo_base_type.currentIndexChanged.connect(self.update_simulation)
        base_layout.addWidget(self.combo_base_type)
        
        self.lbl_base_freq = QLabel("Frecuencia Base: 20 Hz")
        base_layout.addWidget(self.lbl_base_freq)
        self.slider_base_freq = QSlider(Qt.Orientation.Horizontal)
        self.slider_base_freq.setRange(10, 400)
        self.slider_base_freq.setValue(load_preferences()["signal_frequency"])
        self.slider_base_freq.valueChanged.connect(self.update_simulation)
        base_layout.addWidget(self.slider_base_freq)
        
        group_base.setLayout(base_layout)
        controls_layout.addWidget(group_base)
        
        # 2. Configuración de la Perturbación (Interferencia)
        group_noise = QGroupBox("Inyección de Interferencia / Ruido")
        group_noise.setStyleSheet("QGroupBox { color: #ff5555; font-weight: bold; }")
        noise_layout = QVBoxLayout()
        
        noise_layout.addWidget(QLabel("Tipo de Canal/Ruido:"))
        self.combo_noise_type = QComboBox()
        self.combo_noise_type.addItems(["Ruido Blanco (AWGN)", "Interferencia Tono Único", "Atenuación de Canal"])
        self.combo_noise_type.currentIndexChanged.connect(self.update_simulation)
        noise_layout.addWidget(self.combo_noise_type)
        
        # Control para SNR (AWGN)
        self.lbl_snr = QLabel("Relación Señal/Ruido (SNR): 15 dB")
        noise_layout.addWidget(self.lbl_snr)
        self.slider_snr = QSlider(Qt.Orientation.Horizontal)
        self.slider_snr.setRange(-5, 40)
        self.slider_snr.setValue(15)
        self.slider_snr.valueChanged.connect(self.update_simulation)
        noise_layout.addWidget(self.slider_snr)
        
        # Controles para Tono Parásito / Atenuación
        self.lbl_int_freq = QLabel("Frecuencia del Tono Parásito: 60 Hz")
        noise_layout.addWidget(self.lbl_int_freq)
        self.slider_int_freq = QSlider(Qt.Orientation.Horizontal)
        self.slider_int_freq.setRange(10, 200)
        self.slider_int_freq.setValue(60)
        self.slider_int_freq.valueChanged.connect(self.update_simulation)
        noise_layout.addWidget(self.slider_int_freq)
        
        self.lbl_int_amp = QLabel("Amplitud / Atenuación:")
        noise_layout.addWidget(self.lbl_int_amp)
        self.spin_int_amp = QDoubleSpinBox()
        self.spin_int_amp.setRange(0.0, 3.0)
        self.spin_int_amp.setSingleStep(0.1)
        self.spin_int_amp.setValue(1.0)
        self.spin_int_amp.valueChanged.connect(self.update_simulation)
        noise_layout.addWidget(self.spin_int_amp)
        
        group_noise.setLayout(noise_layout)
        controls_layout.addWidget(group_noise)
        
        main_layout.addLayout(controls_layout, stretch=1)
        
        # ==========================================
        # PANEL DERECHO: CANVAS DE MATPLOTLIB
        # ==========================================
        self.canvas = MplCanvas(self, width=7, height=5, dpi=100)
        main_layout.addWidget(self.canvas, stretch=3)
        
        # Ejecutar simulación inicial
        self.update_simulation()

    def update_simulation(self):
        # 1. Recuperar Parámetros de la interfaz
        base_type = self.combo_base_type.currentText()
        base_freq = self.slider_base_freq.value()
        noise_type = self.combo_noise_type.currentText()
        snr_db = self.slider_snr.value()
        int_freq = self.slider_int_freq.value()
        amp_val = self.spin_int_amp.value()
        
        self.lbl_base_freq.setText(f"Frecuencia Base: {base_freq} Hz")
        
        # Configuración fija de muestreo
        preferences = load_preferences()
        fs = float(preferences["sampling_rate"])
        amplitude = preferences["amplitude"]
        duration = 0.3
        
        # 2. Generar Señal Base Limpia
        if base_type == "Sinusoidal":
            clean_signal = ModulationEngine.generate_sinusoidal(amplitude=amplitude, frequency=base_freq, duration=duration, sampling_rate=fs)
        elif base_type == "AM":
            clean_signal = ModulationEngine.modulate_am(modulating_freq=5, carrier_freq=base_freq, mu=0.8, amplitude_c=amplitude, duration=duration, sampling_rate=fs)
        elif base_type == "FM":
            clean_signal = ModulationEngine.modulate_fm(modulating_freq=3, carrier_freq=base_freq, beta=4.0, amplitude_c=amplitude, duration=duration, sampling_rate=fs)
            
        # 3. Aplicar Perturbación según el tipo seleccionado
        if noise_type == "Ruido Blanco (AWGN)":
            self.lbl_snr.setVisible(True)
            self.slider_snr.setVisible(True)
            self.lbl_int_freq.setVisible(False)
            self.slider_int_freq.setVisible(False)
            self.lbl_int_amp.setText("Amplitud Ruido (Inactivo):")
            self.spin_int_amp.setEnabled(False)
            self.lbl_snr.setText(f"Relación Señal/Ruido (SNR): {snr_db} dB")
            
            perturbed_signal = InterferenceEngine.apply_awgn(clean_signal, snr_db)
            
        elif noise_type == "Interferencia Tono Único":
            self.lbl_snr.setVisible(False)
            self.slider_snr.setVisible(False)
            self.lbl_int_freq.setVisible(True)
            self.slider_int_freq.setVisible(True)
            self.spin_int_amp.setEnabled(True)
            self.lbl_int_amp.setText("Amplitud del Tono:")
            self.lbl_int_freq.setText(f"Frecuencia del Tono Parásito: {int_freq} Hz")
            
            perturbed_signal = InterferenceEngine.apply_single_tone_interference(clean_signal, int_freq, amp_val)
            
        elif noise_type == "Atenuación de Canal":
            self.lbl_snr.setVisible(False)
            self.slider_snr.setVisible(False)
            self.lbl_int_freq.setVisible(False)
            self.slider_int_freq.setVisible(False)
            self.spin_int_amp.setEnabled(True)
            self.lbl_int_amp.setText("Factor de Atenuación (0.0 a 1.0):")
            if amp_val > 1.0: 
                amp_val = 1.0
                self.spin_int_amp.setValue(1.0)
                
            perturbed_signal = InterferenceEngine.apply_amplitude_attenuation(clean_signal, amp_val)

        # 4. Renderizar gráficas comparativas en el Canvas
        self.canvas.axes.clear()
        
        # Graficar señal original degradada (atrás) y señal original limpia (adelante)
        self.canvas.axes.plot(perturbed_signal.time_vector, perturbed_signal.amplitude_vector, 
                               color='#ff5555', alpha=0.7, linewidth=1.2, label='Señal con Interferencia')
        self.canvas.axes.plot(clean_signal.time_vector, clean_signal.amplitude_vector, 
                               color='#4cc9f0', linewidth=1.8, label='Señal Original Limpia')
        
        self.canvas.axes.set_title(f"Canal de Simulación - Efecto del Entorno", color='white', fontsize=12)
        self.canvas.axes.set_xlabel("Tiempo (s)")
        self.canvas.axes.set_ylabel("Amplitud (V)")
        self.canvas.axes.grid(True, color='#2a2a35')
        self.canvas.axes.legend(loc='upper right', facecolor='#121214', edgecolor='none', labelcolor='white')
        self.canvas.draw()

    def apply_preferences(self):
        """Actualiza los valores iniciales cuando se guardan preferencias globales."""
        self.slider_base_freq.setValue(load_preferences()["signal_frequency"])
        self.update_simulation()
