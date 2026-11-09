from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QLabel, QFileDialog, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from services.report_service import ReportService

class ReportsView(QWidget):
    """Módulo de Visualización y Exportación de Reportes de SIRE (Fase 7)."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        
        # Título del panel
        header = QLabel("<b>Módulo de Exportación de Resultados</b>")
        header.setStyleSheet("font-size: 16px; color: white;")
        main_layout.addWidget(header)
        
        # Contenedor de previsualización
        group_preview = QGroupBox("Previsualización del Reporte de Prácticas")
        group_preview.setStyleSheet("QGroupBox { color: #4cc9f0; font-weight: bold; }")
        preview_layout = QVBoxLayout()
        
        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(True)
        self.txt_preview.setStyleSheet("background-color: #121214; color: #e0e0e0; font-family: 'Consolas', 'Courier New'; font-size: 12px;")
        preview_layout.addWidget(self.txt_preview)
        
        group_preview.setLayout(preview_layout)
        main_layout.addWidget(group_preview, stretch=1)
        
        # Barra de acciones (Botones)
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        self.btn_refresh = QPushButton("⟳ Actualizar Vista")
        self.btn_refresh.setStyleSheet("padding: 8px 16px; background-color: #2a2a35; color: white;")
        self.btn_refresh.clicked.connect(self.refresh_report_preview)
        actions_layout.addWidget(self.btn_refresh)
        
        self.btn_export = QPushButton("💾 Exportar Reporte (.md)")
        self.btn_export.setStyleSheet("padding: 8px 24px; background-color: #4cc9f0; color: #121214; font-weight: bold;")
        self.btn_export.clicked.connect(self.handle_export_file)
        actions_layout.addWidget(self.btn_export)
        
        main_layout.addLayout(actions_layout)
        
        # Cargar datos iniciales
        self.refresh_report_preview()

    def refresh_report_preview(self):
        """Genera el contenido dinámico actual del historial y lo despliega en pantalla."""
        self.current_report_content = ReportService.generate_markdown_report_content()
        self.txt_preview.setPlainText(self.current_report_content)

    def handle_export_file(self):
        """Abre el diálogo nativo de Windows para que el alumno guarde su reporte."""
        if not hasattr(self, 'current_report_content') or not self.current_report_content:
            QMessageBox.warning(self, "Exportación", "El reporte está vacío.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte Académico",
            "Reporte_Laboratorio_SIRE.md",
            "Markdown Files (*.md);;Text Files (*.txt)"
        )
        
        if file_path:
            if ReportService.export_to_file(file_path, self.current_report_content):
                QMessageBox.information(self, "Éxito", "El archivo de reporte fue exportado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar el archivo en la ruta especificada.")
