import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QComboBox, QLineEdit, QPushButton)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.modulation import ModulationEngine
from config.preferences import load_preferences

class MplCanvas(FigureCanvas):
    """Lienzo para incrustar gráficas de Matplotlib en PySide6."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#1e1e24') # Estilo oscuro adaptado a tu UI original
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#121214')
        self.axes.tick_params(colors='white')
        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        super().__init__(fig)

class SignalView(QWidget):
    """Módulo de simulación y vista de señales de SIRE (Fase 2)."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Panel Izquierdo de Parámetros
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        controls_layout.addWidget(QLabel("<b>Tipo de Señal / Modulación:</b>"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Sinusoidal", "AM", "FM", "ASK", "FSK", "PSK", "QAM"])
        # Las señales de Qt vuelven a calcular y dibujar la simulación al cambiar controles.
        self.combo_type.currentIndexChanged.connect(self.update_simulation)
        controls_layout.addWidget(self.combo_type)
        
        # Controles Dinámicos (Frecuencia)
        self.lbl_freq = QLabel("Frecuencia Portadora: 50 Hz")
        controls_layout.addWidget(self.lbl_freq)
        self.slider_freq = QSlider(Qt.Orientation.Horizontal)
        self.slider_freq.setRange(10, 400)
        self.slider_freq.setValue(load_preferences()["signal_frequency"])
        self.slider_freq.valueChanged.connect(self.update_simulation)
        controls_layout.addWidget(self.slider_freq)

        # Entrada de datos binarios (para ASK/FSK/PSK/QAM)
        controls_layout.addWidget(QLabel("Flujo de Bits (separados por comas):"))
        self.txt_bits = QLineEdit("1,0,1,1,0,1,0,0")
        self.txt_bits.textChanged.connect(self.update_simulation)
        controls_layout.addWidget(self.txt_bits)
        
        main_layout.addLayout(controls_layout, stretch=1)
        
        # Panel Derecho de Visualización (Gráfica)
        self.canvas = MplCanvas(self, width=7, height=5, dpi=100)
        main_layout.addWidget(self.canvas, stretch=3)
        
        self.update_simulation()

    def _parse_bits(self) -> list:
        try:
            return [int(b.strip()) for b in self.txt_bits.text().split(",") if b.strip() in ['0', '1']]
        except ValueError:
            return [1, 0, 1, 1]

    def update_simulation(self):
        stype = self.combo_type.currentText()
        freq = self.slider_freq.value()
        self.lbl_freq.setText(f"Frecuencia Portadora: {freq} Hz")
        
        preferences = load_preferences()
        fs = float(preferences["sampling_rate"])
        amplitude = preferences["amplitude"]
        duration = 0.5
        
        # Enrutamiento de lógica matemática según selección en la UI
        if stype == "Sinusoidal":
            signal = ModulationEngine.generate_sinusoidal(amplitude=amplitude, frequency=freq, duration=duration, sampling_rate=fs)
        elif stype == "AM":
            signal = ModulationEngine.modulate_am(modulating_freq=5, carrier_freq=freq, mu=0.7, amplitude_c=amplitude, duration=duration, sampling_rate=fs)
        elif stype == "FM":
            signal = ModulationEngine.modulate_fm(modulating_freq=4, carrier_freq=freq, beta=5.0, amplitude_c=amplitude, duration=duration, sampling_rate=fs)
        else:
            bits = self._parse_bits()
            if stype == "ASK":
                signal = ModulationEngine.modulate_ask(bits, carrier_freq=freq, amplitude=amplitude, bit_duration=0.05, sampling_rate=fs)
            elif stype == "FSK":
                signal = ModulationEngine.modulate_fsk(bits, freq_0=freq//2, freq_1=freq, amplitude=amplitude, bit_duration=0.05, sampling_rate=fs)
            elif stype == "PSK":
                signal = ModulationEngine.modulate_psk(bits, carrier_freq=freq, amplitude=amplitude, bit_duration=0.05, sampling_rate=fs)
            elif stype == "QAM":
                # 16-QAM agrupa bits de cuatro en cuatro; completar con ceros
                # garantiza un último símbolo completo para poder visualizarlo.
                while len(bits) % 4 != 0:
                    bits.append(0)
                signal = ModulationEngine.modulate_qam16(bits, carrier_freq=freq, bit_duration=0.05, sampling_rate=fs, amplitude=amplitude)

        # El motor entrega muestras; la vista solo decide cómo representarlas.
        self.canvas.axes.clear()
        self.canvas.axes.plot(signal.time_vector, signal.amplitude_vector, color='#4cc9f0', linewidth=1.5)
        self.canvas.axes.set_title(f"Visualización de Señal - {signal.signal_type}", color='white')
        self.canvas.axes.set_xlabel("Tiempo (s)")
        self.canvas.axes.set_ylabel("Amplitud (V)")
        self.canvas.axes.grid(True, color='#2a2a35')
        self.canvas.draw()

    def apply_preferences(self):
        """Aplica frecuencia predeterminada guardada y actualiza la gráfica."""
        self.slider_freq.setValue(load_preferences()["signal_frequency"])
        self.update_simulation()
