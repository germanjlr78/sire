import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QComboBox, QGroupBox, QSplitter)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.modulation import ModulationEngine
from core.interference import InterferenceEngine
from core.spectrum_analyzer import SpectrumAnalyzer
from config.preferences import load_preferences

class MplSpectrumCanvas(FigureCanvas):
    """Contenedor de doble gráfica: Dominio del Tiempo y Dominio de la Frecuencia."""
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#1e1e24')
        
        # Gráfica superior: Tiempo
        self.ax_time = fig.add_subplot(211)
        self.ax_time.set_facecolor('#121214')
        self.ax_time.tick_params(colors='white')
        self.ax_time.xaxis.label.set_color('white')
        self.ax_time.yaxis.label.set_color('white')
        
        # Gráfica inferior: Espectro de Frecuencia
        self.ax_freq = fig.add_subplot(212)
        self.ax_freq.set_facecolor('#121214')
        self.ax_freq.tick_params(colors='white')
        self.ax_freq.xaxis.label.set_color('white')
        self.ax_freq.yaxis.label.set_color('white')
        
        fig.tight_layout(pad=3.0)
        super().__init__(fig)

class SpectrumView(QWidget):
    """Módulo Analizador de Espectro de SIRE (Fase 4)."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Panel lateral de controles
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        controls_layout.setSpacing(16)
        
        # Configuración de señal bajo prueba
        group_input = QGroupBox("Señal bajo Análisis")
        group_input.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        input_layout = QVBoxLayout()
        
        input_layout.addWidget(QLabel("Tipo de Señal:"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Sinusoidal Pura", "Modulación AM", "Señal con Ruido AWGN"])
        self.combo_type.currentIndexChanged.connect(self.update_analysis)
        input_layout.addWidget(self.combo_type)
        
        self.lbl_freq = QLabel("Frecuencia Central: 100 Hz")
        input_layout.addWidget(self.lbl_freq)
        self.slider_freq = QSlider(Qt.Orientation.Horizontal)
        self.slider_freq.setRange(10, 400)
        self.slider_freq.setValue(load_preferences()["signal_frequency"])
        self.slider_freq.valueChanged.connect(self.update_analysis)
        input_layout.addWidget(self.slider_freq)
        
        group_input.setLayout(input_layout)
        controls_layout.addWidget(group_input)
        
        main_layout.addLayout(controls_layout, stretch=1)
        
        # Lienzo de gráficas duales
        self.canvas = MplSpectrumCanvas(self)
        main_layout.addWidget(self.canvas, stretch=3)
        
        self.update_analysis()

    def update_analysis(self):
        stype = self.combo_type.currentText()
        freq = self.slider_freq.value()
        self.lbl_freq.setText(f"Frecuencia Central: {freq} Hz")
        
        # Nyquist exige Fs > 2*Fmax. Se mantiene margen para las bandas laterales
        # AM (fc + fm) y para el ruido que se observe en el espectro.
        preferences = load_preferences()
        fs = float(preferences["sampling_rate"])
        amplitude = preferences["amplitude"]
        duration = 0.2
        
        # 1. Generar la señal temporal
        if stype == "Sinusoidal Pura":
            signal = ModulationEngine.generate_sinusoidal(amplitude=amplitude, frequency=freq, duration=duration, sampling_rate=fs)
        elif stype == "Modulación AM":
            # Genera bandas laterales a fc - fm y fc + fm (fm = 30Hz)
            signal = ModulationEngine.modulate_am(modulating_freq=30, carrier_freq=freq, mu=1.0, amplitude_c=amplitude, duration=duration, sampling_rate=fs)
        elif stype == "Señal con Ruido AWGN":
            base_sig = ModulationEngine.generate_sinusoidal(amplitude=amplitude, frequency=freq, duration=duration, sampling_rate=fs)
            signal = InterferenceEngine.apply_awgn(base_sig, snr_db=5.0)

        # Separar el cálculo de la FFT de la interfaz permite reutilizarlo y probarlo.
        frequencies, magnitude_db = SpectrumAnalyzer.calculate_fft(signal)

        # 3. Renderizar Dominio del Tiempo
        self.canvas.ax_time.clear()
        self.canvas.ax_time.plot(signal.time_vector, signal.amplitude_vector, color='#4cc9f0', linewidth=1.5)
        self.canvas.ax_time.set_title("Osciloscopio (Dominio del Tiempo)", color='white')
        self.canvas.ax_time.set_xlabel("Tiempo (s)")
        self.canvas.ax_time.set_ylabel("Amplitud (V)")
        self.canvas.ax_time.grid(True, color='#2a2a35')

        # 4. Renderizar Dominio de la Frecuencia (Analizador de Espectro)
        self.canvas.ax_freq.clear()
        self.canvas.ax_freq.stem(frequencies, magnitude_db, linefmt='#f72585', markerfmt=' ', basefmt=' ')
        self.canvas.ax_freq.plot(frequencies, magnitude_db, color='#f72585', linewidth=1.2)
        self.canvas.ax_freq.set_title("Analizador de Espectro (Dominio de la Frecuencia)", color='white')
        self.canvas.ax_freq.set_xlabel("Frecuencia (Hz)")
        self.canvas.ax_freq.set_ylabel("Magnitud Normalizada (dB)")
        self.canvas.ax_freq.set_ylim([-80, 5])  # Rango dinámico estándar de visualización
        self.canvas.ax_freq.grid(True, color='#2a2a35')

        self.canvas.draw()

    def apply_preferences(self):
        """Actualiza la frecuencia de análisis y recalcula el espectro."""
        self.slider_freq.setValue(load_preferences()["signal_frequency"])
        self.update_analysis()
