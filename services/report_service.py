import os
from datetime import datetime
from services.experiment_service import ExperimentService

class ReportService:
    """Servicio dedicado a compilar y exportar reportes de laboratorio en formatos estándar."""

    @staticmethod
    def generate_markdown_report_content() -> str:
        """Compila todos los experimentos del historial en un archivo estructurado en Markdown."""
        experiments = ExperimentService.load_all_experiments()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        markdown = []
        markdown.append("# SIRE — SISTEMA DE INTERFERENCIA Y RECUPERACIÓN DE SEÑALES")
        markdown.append("### REPORTE EJECUTIVO DE PRÁCTICAS DE LABORATORIO")
        markdown.append(f"**Fecha de Emisión:** {fecha_actual}")
        markdown.append(f"**Total de Experimentos Registrados:** {len(experiments)}")
        markdown.append("\n" + "="*60 + "\n")
        
        if not experiments:
            markdown.append("*No se encontraron experimentos registrados en el historial local.*")
            return "\n".join(markdown)
            
        # La tabla resume todos los registros; la sección siguiente agrega contexto
        # para que el reporte sirva tanto para comparar como para documentar ensayos.
        markdown.append("## 1. Resumen de Ejecuciones")
        markdown.append("| ID | Fecha / Hora | Nombre de la Práctica | Esquema de Señal | Perturbación | SNR Medida |")
        markdown.append("|---|---|---|---|---|---|")
        
        for exp in experiments:
            markdown.append(f"| {exp.id} | {exp.timestamp} | {exp.name} | {exp.signal_type} | {exp.applied_noise} | {exp.measured_snr} dB |")
            
        markdown.append("\n## 2. Detalle de Observaciones por Práctica")
        for exp in experiments:
            markdown.append(f"### Práctica {exp.id}: {exp.name}")
            markdown.append(f"- **Estampa de Tiempo:** {exp.timestamp}")
            markdown.append(f"- **Configuración de Onda:** {exp.signal_type} (Frecuencia Central: {exp.carrier_freq} Hz)")
            markdown.append(f"- **Condición del Canal:** {exp.applied_noise}")
            markdown.append(f"- **Calidad de Recepción (SNR):** {exp.measured_snr} dB")
            markdown.append(f"- **Notas de Laboratorio:** {exp.notes}")
            markdown.append("\n" + "-"*40)
            
        markdown.append("\n**Fin del Reporte Académico.**")
        return "\n".join(markdown)

    @staticmethod
    def export_to_file(file_path: str, content: str) -> bool:
        """Escribe físicamente el string del reporte en la ruta seleccionada por el usuario."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False
