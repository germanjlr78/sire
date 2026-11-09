from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGridLayout
from PySide6.QtCore import Qt

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        header = QHBoxLayout()
        titles = QVBoxLayout()
        eyebrow = QLabel("CENTRO DE CONTROL")
        eyebrow.setObjectName("Eyebrow")
        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        description = QLabel("Bienvenido al entorno de simulación y análisis de señales.")
        description.setObjectName("MutedText")
        titles.addWidget(eyebrow)
        titles.addWidget(title)
        titles.addWidget(description)
        header.addLayout(titles)
        header.addStretch()
        status = QLabel("●  SISTEMA PREPARADO")
        status.setObjectName("ReadyBadge")
        status.setAlignment(Qt.AlignCenter)
        header.addWidget(status, 0, Qt.AlignTop)
        layout.addLayout(header)

        cards = QGridLayout()
        cards.setSpacing(14)
        cards.addWidget(self._metric_card("01", "Módulos disponibles", "10", "Secciones del laboratorio"), 0, 0)
        cards.addWidget(self._metric_card("02", "Experimentos ejecutados", "0", "Aún no hay experimentos"), 0, 1)
        cards.addWidget(self._metric_card("03", "Estado del entorno", "Listo", "Interfaz inicial cargada"), 0, 2)
        layout.addLayout(cards)

        body = QHBoxLayout()
        body.setSpacing(14)

        overview = QFrame()
        overview.setObjectName("Panel")
        ov = QVBoxLayout(overview)
        ov.setContentsMargins(20, 20, 20, 20)
        heading = QLabel("INICIO RÁPIDO")
        heading.setObjectName("PanelHeading")
        ov.addWidget(heading)
        intro = QLabel(
            "SIRE permitirá generar señales, introducir interferencias de forma matemática, "
            "analizar su espectro y evaluar técnicas de recuperación."
        )
        intro.setObjectName("BodyText")
        intro.setWordWrap(True)
        ov.addWidget(intro)
        ov.addSpacing(8)

        actions = [
            ("Abrir generador de señales", "Generador de señales"),
            ("Explorar simulador de interferencias", "Simulador de interferencias"),
            ("Abrir analizador de espectro", "Analizador de espectro"),
        ]
        for text, target in actions:
            btn = QPushButton("→   " + text)
            btn.setObjectName("ActionButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, p=target: self.window().navigate(p))
            ov.addWidget(btn)
        ov.addStretch()
        body.addWidget(overview, 2)

        roadmap = QFrame()
        roadmap.setObjectName("Panel")
        rd = QVBoxLayout(roadmap)
        rd.setContentsMargins(20, 20, 20, 20)
        roadmap_title = QLabel("ESTADO DEL PROYECTO")
        roadmap_title.setObjectName("PanelHeading")
        rd.addWidget(roadmap_title)
        for label, state in [
            ("Fase 1 · Interfaz y navegación", "EN DESARROLLO"),
            ("Fase 2 · Generación de señales", "PENDIENTE"),
            ("Fase 3 · Interferencias", "PENDIENTE"),
            ("Fase 4 · Análisis y métricas", "PENDIENTE"),
            ("Fase 5 · Recuperación", "PENDIENTE"),
        ]:
            row = QHBoxLayout()
            item = QLabel(label)
            item.setObjectName("BodyText")
            tag = QLabel(state)
            tag.setObjectName("RoadmapTag")
            row.addWidget(item, 1)
            row.addWidget(tag)
            rd.addLayout(row)
        rd.addStretch()
        body.addWidget(roadmap, 3)
        layout.addLayout(body, 1)

        disclaimer = QLabel("SIMULACIÓN EDUCATIVA · No genera ni transmite señales de radiofrecuencia.")
        disclaimer.setObjectName("Disclaimer")
        layout.addWidget(disclaimer)

    def _metric_card(self, number, title, value, detail):
        card = QFrame()
        card.setObjectName("MetricCard")
        box = QVBoxLayout(card)
        box.setContentsMargins(18, 16, 18, 16)
        top = QHBoxLayout()
        n = QLabel(number)
        n.setObjectName("MetricNumber")
        top.addWidget(n)
        top.addStretch()
        box.addLayout(top)
        t = QLabel(title)
        t.setObjectName("MutedText")
        v = QLabel(value)
        v.setObjectName("MetricValue")
        d = QLabel(detail)
        d.setObjectName("SmallMuted")
        box.addWidget(t)
        box.addWidget(v)
        box.addWidget(d)
        return card
