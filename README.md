# SIRE — Fase 1

Sistema de Interferencia y Recuperación de Señales. Aplicación educativa de escritorio construida con Python y PySide6.

## Requisitos
- Python 3.10 o superior (probado con Python 3.14.7).
- Windows 10/11, Linux o macOS.

## Instalación en Windows
Abre PowerShell en la carpeta `SIRE_Fase1` y ejecuta:

```powershell
py -3.14 -m venv .venv-1
.\.venv-1\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Si PowerShell bloquea la activación del entorno, puedes ejecutar directamente:

```powershell
.\.venv-1\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-1\Scripts\python.exe main.py
```

## Ejecutar posteriormente
Con el entorno virtual activado:

```powershell
python main.py
```

## Preferencias de simulación
En la sección **Configuración** puedes guardar la frecuencia de muestreo, la amplitud
y la frecuencia base/portadora. Los valores iniciales son 5000 Hz, 2 V y 50 Hz,
respectivamente; sus rangos son 2000–20000 Hz, 0.1–10 V y 10–400 Hz. Estos valores
se aplican al generador, interferencias, analizador de espectro, recuperación y
prácticas; cada vista permite ajustes propios mientras se usa. El muestreo mínimo
permite representar señales de hasta 400 Hz respetando el criterio de Nyquist.
Las preferencias se guardan en la configuración del usuario mediante Qt (Registro
de Windows o el directorio de configuración del sistema operativo) y se conservan
al cerrar la aplicación.

## Estructura
- `main.py`: punto de entrada.
- `GUIA_USO_SIRE.md`: instrucciones de uso y descripción de las secciones.
- `config/`: configuración general.
- `interface/`: ventana principal, dashboard y páginas.
- `resources/styles/`: tema visual.
- `tests/`: reservado para pruebas de las siguientes fases.

## Alcance de esta fase
Incluye ventana principal, navegación entre diez secciones, dashboard y páginas preparadas. Los módulos funcionales de procesamiento de señales se implementarán en las fases siguientes.

**Aviso:** SIRE es un simulador educativo por software. Esta fase no transmite ni bloquea señales de radiofrecuencia.
