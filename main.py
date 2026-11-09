import sys
from PySide6.QtWidgets import QApplication
from config.settings import APP_NAME, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from interface.main_window import MainWindow
from pathlib import Path

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    # La hoja QSS aplica el tema de forma global sin acoplar estilos a cada widget.
    style_path = Path(__file__).parent / "resources" / "styles" / "dark.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    window.show()
    # Qt procesa eventos (clics, teclado y repintado) mientras este bucle está activo.
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
