from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

class ModulePage(QWidget):
    def __init__(self, title, description):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        eyebrow = QLabel("MÓDULO DEL LABORATORIO")
        eyebrow.setObjectName("Eyebrow")
        heading = QLabel(title)
        heading.setObjectName("PageTitle")
        subtitle = QLabel(description)
        subtitle.setObjectName("MutedText")
        layout.addWidget(eyebrow)
        layout.addWidget(heading)
        layout.addWidget(subtitle)

        panel = QFrame()
        panel.setObjectName("Panel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(28, 28, 28, 28)
        panel_layout.setAlignment(Qt.AlignCenter)

        icon = QLabel("◈")
        icon.setObjectName("PlaceholderIcon")
        icon.setAlignment(Qt.AlignCenter)
        message = QLabel("MÓDULO PREPARADO PARA DESARROLLO")
        message.setObjectName("PanelHeading")
        message.setAlignment(Qt.AlignCenter)
        detail = QLabel(
            "La navegación ya está funcionando. La lógica de este módulo se incorporará "
            "en su fase correspondiente, manteniendo la arquitectura modular de SIRE."
        )
        detail.setObjectName("BodyText")
        detail.setWordWrap(True)
        detail.setMaximumWidth(560)
        detail.setAlignment(Qt.AlignCenter)

        panel_layout.addStretch()
        panel_layout.addWidget(icon)
        panel_layout.addWidget(message)
        panel_layout.addWidget(detail, 0, Qt.AlignHCenter)
        panel_layout.addStretch()
        layout.addWidget(panel, 1)
