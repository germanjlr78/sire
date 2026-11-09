from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget, QStatusBar
)
from config.settings import APP_NAME, APP_VERSION, MODULES
from interface.dashboard import DashboardPage
from interface.module_page import ModulePage

from interface.signal_view import SignalView
from interface.interference_view import InterferenceView  
from interface.spectrum_view import SpectrumView 
from interface.recovery_view import RecoveryView 
from interface.laboratory_view import LaboratoryView
from interface.reports_view import ReportsView
from interface.preferences_view import PreferencesView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setObjectName("MainWindow")
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = self._build_sidebar()
        root.addWidget(sidebar)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 22, 28, 18)
        content_layout.setSpacing(16)

        self.page_stack = QStackedWidget()
        self.dashboard = DashboardPage()
        self.page_stack.addWidget(self.dashboard)

        self.pages = {"Dashboard": 0}
        self.preferences_page = PreferencesView()
        
        # Cada sección tiene un índice en el stack; las vistas especializadas
        # reemplazan la plantilla genérica cuando el módulo ya tiene funcionalidad.
        for name, _icon, description in MODULES[1:]:
            if name == "Generador de señales":
                page = SignalView()

            elif name == "Simulador de interferencias":
                page = InterferenceView()
            elif name == "Analizador de espectro":
                page = SpectrumView()
            elif name in ["Calidad de señal", "Recuperación de señales"]:
                page = RecoveryView()
            elif name in ["Laboratorio de prácticas", "Historial de experimentos"]:
                page = LaboratoryView()
            elif name == "Reportes":
                page = ReportsView()
            elif name == "Configuración":
                page = self.preferences_page
            else:
                # La plantilla conserva la navegación para secciones aún no implementadas.
                page = ModulePage(name, description)
                
            index = self.page_stack.addWidget(page)
            self.pages[name] = index

        # Las vistas escuchan los cambios para volver a generar su señal al guardar.
        for index in range(self.page_stack.count()):
            page = self.page_stack.widget(index)
            apply_preferences = getattr(page, "apply_preferences", None)
            if callable(apply_preferences):
                self.preferences_page.preferences_changed.connect(apply_preferences)

        content_layout.addWidget(self.page_stack)
        root.addWidget(content, 1)
        self.setCentralWidget(central)

        status = QStatusBar()
        status.showMessage(f"SIRE v{APP_VERSION}  |  Simulación educativa: no transmite señales de radiofrecuencia.")
        self.setStatusBar(status)

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(258)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 24, 18, 18)
        layout.setSpacing(10)

        brand = QLabel("SIRE")
        brand.setObjectName("Brand")
        subtitle = QLabel("LABORATORIO DE TELECOMUNICACIONES")
        subtitle.setObjectName("BrandSubtitle")
        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(22)

        section = QLabel("MENÚ PRINCIPAL")
        section.setObjectName("SectionLabel")
        layout.addWidget(section)

        self.nav_buttons = {}
        for name, icon, _description in MODULES:
            button = QPushButton(f"{icon}    {name}")
            button.setObjectName("NavButton")
            button.setCursor(Qt.PointingHandCursor)
            button.setCheckable(True)
            # El argumento por defecto captura el nombre actual; sin él, todos los
            # botones podrían terminar navegando a la última sección del bucle.
            button.clicked.connect(lambda checked=False, page=name: self.navigate(page))
            layout.addWidget(button)
            self.nav_buttons[name] = button

        layout.addStretch()
        note = QLabel("ENTORNO ACADÉMICO\nVersión 0.1.0")
        note.setObjectName("SidebarFooter")
        note.setWordWrap(True)
        layout.addWidget(note)

        exit_button = QPushButton("⏻    Salir")
        exit_button.setObjectName("ExitButton")
        exit_button.setCursor(Qt.PointingHandCursor)
        exit_button.setToolTip("Cerrar SIRE")
        exit_button.clicked.connect(lambda checked=False: self.close())
        layout.addWidget(exit_button)

        self.nav_buttons["Dashboard"].setChecked(True)
        return sidebar

    def navigate(self, page_name):
        if page_name not in self.pages:
            return
        self.page_stack.setCurrentIndex(self.pages[page_name])
        for name, button in self.nav_buttons.items():
            button.setChecked(name == page_name)
