# Guía de uso del simulador SIRE

## 1. ¿Qué es SIRE?

SIRE (Sistema de Interferencia y Recuperación de Señales) es una aplicación
educativa de escritorio para explorar conceptos de telecomunicaciones mediante
señales generadas por software. Permite generar modulaciones, simular efectos de
canal, observar espectros, probar un filtro pasa-bajas y registrar prácticas.

**SIRE no transmite ni recibe señales de radiofrecuencia real.** Los gráficos y
resultados corresponden a simulaciones numéricas.

## 2. Inicio del programa

En Windows, abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
.\.venv-1\Scripts\python.exe main.py
```

También puedes activar el entorno y luego ejecutar la aplicación:

```powershell
.\.venv-1\Scripts\Activate.ps1
python main.py
```

Al iniciar aparece el Dashboard. Usa el menú lateral para cambiar de sección.
Los controles de cada vista actualizan la simulación y sus gráficas. Para cerrar
el programa, pulsa **Salir** al pie del menú lateral; también puedes cerrar la
ventana con la X o usar **Alt + F4**.

## 3. Secciones

### Dashboard

Es la pantalla de inicio y ofrece accesos rápidos al generador, al simulador de
interferencias y al analizador de espectro. Incluye una descripción general del
laboratorio y del estado del proyecto.

Las tarjetas y la hoja de ruta son informativas; algunos valores visibles, como
el contador de experimentos, no se actualizan automáticamente con el historial.

### Generador de señales

Permite visualizar una señal en el dominio del tiempo.

1. Selecciona el tipo de señal o modulación.
2. Ajusta la frecuencia portadora con el control deslizante.
3. Para ASK, FSK, PSK o QAM, edita la secuencia de bits separada por comas
   (por ejemplo, `1,0,1,1,0,1,0,0`).
4. Observa cómo cambia la forma de onda en la gráfica.

Se incluyen:

- **Sinusoidal:** señal periódica básica.
- **AM:** la amplitud de la portadora varía según una señal moduladora.
- **FM:** la fase instantánea varía según la señal moduladora, produciendo
  cambios en la frecuencia instantánea.
- **ASK:** los bits controlan la amplitud de la portadora.
- **FSK:** los bits seleccionan una de dos frecuencias.
- **PSK/BPSK:** los bits seleccionan entre dos fases.
- **QAM/16-QAM:** cada grupo de cuatro bits selecciona un punto de la
  constelación; si la secuencia no es múltiplo de cuatro, se completa con ceros
  para formar el último símbolo.

La amplitud y la frecuencia de muestreo se toman de Configuración. La frecuencia
del control deslizante de esta sección es local y no cambia la preferencia global.

### Simulador de interferencias

Permite comparar una señal base limpia con su versión alterada.

1. Elige una señal base sinusoidal, AM o FM.
2. Ajusta su frecuencia.
3. Selecciona el efecto del canal:
   - **Ruido blanco (AWGN):** usa el control SNR en dB. Una SNR más alta
     representa menos potencia de ruido respecto a la señal.
   - **Interferencia de tono único:** establece la frecuencia y amplitud del
     tono no deseado.
   - **Atenuación de canal:** reduce la amplitud mediante un factor entre 0
     (pérdida total) y 1 (sin atenuación).
4. Compara las curvas de señal limpia y señal afectada.

La frecuencia de muestreo y amplitud base provienen de Configuración. Los
parámetros del canal se controlan en esta misma sección.

### Analizador de espectro

Muestra dos gráficas de la señal seleccionada:

- **Osciloscopio:** amplitud de las muestras con respecto al tiempo.
- **Espectro:** magnitud normalizada en decibelios con respecto a la frecuencia.

Selecciona una señal sinusoidal, AM o una sinusoidal con ruido AWGN, y ajusta la
frecuencia central. En AM pueden observarse la portadora y las bandas laterales.
La FFT usada en esta vista es unilateral, apropiada para visualizar señales reales.

La frecuencia de muestreo y amplitud se toman de Configuración. La escala del
espectro está normalizada respecto al pico más alto, por lo que 0 dB indica ese
pico y no una potencia absoluta en dBm.

### Calidad de señal

Esta entrada abre la misma vista que **Recuperación de señales**. En ella se
muestra la métrica SNR calculada entre una señal de referencia limpia y la señal
recuperada después del filtro. No es un panel independiente de métricas generales:
por ahora, la interfaz no presenta BER ni un conjunto de mediciones configurables.

### Recuperación de señales

Compara la señal original, la señal con interferencia y la señal después de un
filtro FIR pasa-bajas con ventana de Hamming.

1. Ajusta la frecuencia de corte.
2. Revisa las tres curvas y la SNR posterior al filtrado.
3. Cambia la frecuencia de corte para observar el compromiso entre conservar la
   señal útil y atenuar la interferencia.

La señal útil, la amplitud y la frecuencia de muestreo provienen de Configuración.
La interferencia se sitúa por encima de la frecuencia de corte para mostrar el
efecto del filtro. Una elección de corte demasiado baja puede atenuar parte de la
señal útil; una demasiado alta puede dejar pasar más interferencia.

### Laboratorio de prácticas

Permite ejecutar una simulación AWGN y guardar un registro en el historial.

1. Escribe el nombre de la práctica.
2. Selecciona Sinusoidal, AM o FM.
3. Ajusta la SNR objetivo.
4. Pulsa **Ejecutar y Guardar en Historial**.
5. La aplicación calcula una SNR medida y agrega el experimento a la tabla.

La práctica usa la frecuencia de muestreo, amplitud y frecuencia base de
Configuración. El resultado se guarda localmente en
`data/experiments/history.json`, relativo al directorio desde donde se ejecuta
SIRE. La SNR medida puede diferir ligeramente del objetivo porque AWGN es
aleatorio.

### Historial de experimentos

Esta entrada abre la misma vista del **Laboratorio de prácticas** y muestra su
tabla de registros. Cada fila incluye identificador, fecha y hora, nombre,
señal, ruido aplicado y SNR medida. Los registros se cargan desde el archivo JSON
local indicado arriba.

### Reportes

Presenta una vista previa del reporte Markdown generado a partir del historial.

1. Pulsa **Actualizar Vista** para volver a leer los experimentos guardados.
2. Pulsa **Exportar Reporte (.md)**.
3. Elige el nombre y la ubicación del archivo en el diálogo.

El reporte resume los experimentos y añade el detalle de las notas y parámetros
registrados. La vista previa no se actualiza al guardar una práctica en otra
sección; usa el botón de actualización antes de exportar.

### Configuración

Define valores predeterminados que se guardan y se conservan al cerrar SIRE:

| Preferencia | Valor inicial | Rango permitido |
|---|---:|---:|
| Frecuencia de muestreo | 5000 Hz | 2000–20000 Hz |
| Amplitud | 2 V | 0.1–10 V |
| Frecuencia base / portadora | 50 Hz | 10–400 Hz |

Pulsa **Guardar preferencias** para aplicarlas a las vistas de generador,
interferencias, espectro, recuperación y prácticas. Los cambios actualizan las
gráficas abiertas. Los controles específicos de cada simulador siguen permitiendo
ajustes locales. **Restablecer valores iniciales** recupera los valores de la
tabla y los guarda.

La frecuencia de muestreo mínima permite representar hasta 400 Hz según el
criterio de Nyquist (al menos el doble de la frecuencia máxima); en la práctica,
usar una frecuencia de muestreo mayor suele dar una representación más detallada.

## 4. Secuencia sugerida para una práctica

1. En **Configuración**, establece la frecuencia base, amplitud y frecuencia de
   muestreo.
2. En **Generador de señales**, observa la señal sin perturbaciones y compara
   distintos tipos de modulación.
3. En **Simulador de interferencias**, aplica AWGN, un tono o atenuación y
   compara la salida con la señal limpia.
4. En **Analizador de espectro**, observa cómo el tipo de señal y el ruido se
   reflejan en frecuencia.
5. En **Recuperación de señales**, ajusta el filtro y compara la señal recibida
   con la recuperada.
6. En **Laboratorio de prácticas**, ejecuta y guarda un ensayo con nombre y SNR
   objetivo.
7. En **Reportes**, actualiza la vista previa y exporta los resultados.

## 5. Interpretación y límites

- La frecuencia de muestreo determina cuántas muestras por segundo se calculan.
  Si es insuficiente respecto a las frecuencias presentes, aparece aliasing.
- La SNR se expresa en dB y compara potencias. En general, más dB significa una
  señal relativamente menos afectada por ruido.
- Las gráficas son resultados de modelos discretos ideales/simplificados; no
  incluyen todas las características de un transmisor, receptor o canal físico.
- El historial se guarda en el equipo local. Copia el archivo JSON si necesitas
  respaldarlo o llevarlo a otra computadora.
- Configuración e Historial son funciones locales de esta versión; no hay cuentas
  de usuario ni sincronización en la nube.

## 6. Estructura del proyecto

Este árbol muestra los archivos propios del proyecto. Se excluyen `.venv-1` (el
entorno virtual) y las carpetas `__pycache__` (caché generada por Python), porque
no forman parte del código fuente que se debe mantener o compartir.

```text
SIRE_Fase1/
├── .gitignore
├── GUIA_USO_SIRE.md
├── README.md
├── Reporte_Laboratorio_SIRE.md
├── main.py
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── preferences.py
│   └── settings.py
├── core/
│   ├── interference.py
│   ├── modulation.py
│   ├── signal_generator.py
│   ├── signal_metrics.py
│   ├── signal_recovery.py
│   └── spectrum_analyzer.py
├── data/
│   └── experiments/
│       └── history.json
├── interface/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── interference_view.py
│   ├── laboratory_view.py
│   ├── main_window.py
│   ├── module_page.py
│   ├── preferences_view.py
│   ├── recovery_view.py
│   ├── reports_view.py
│   ├── signal_view.py
│   └── spectrum_view.py
├── models/
│   ├── experiment_model.py
│   └── signal_model.py
├── resources/
│   └── styles/
│       └── dark.qss
├── services/
│   ├── experiment_service.py
│   ├── export_service.py
│   └── report_service.py
└── tests/
    ├── test_analyzer.py
    ├── test_generator.py
    ├── test_interference.py
    ├── test_preferences.py
    └── test_recovery.py
```

### Responsabilidad de las carpetas

- `config/`: constantes generales y preferencias persistentes del usuario.
- `core/`: cálculos de señales, modulaciones, interferencias, métricas,
  recuperación y análisis espectral.
- `data/`: datos locales de la aplicación; `experiments/history.json` contiene
  el historial de prácticas guardadas.
- `interface/`: ventanas, controles, navegación y gráficas de PySide6.
- `models/`: estructuras de datos para señales y experimentos.
- `resources/styles/`: hoja de estilo visual de la aplicación.
- `services/`: persistencia de experimentos y generación/exportación de reportes.
- `tests/`: pruebas automáticas de los cálculos y las preferencias.

`core/signal_generator.py` y `services/export_service.py` están vacíos en esta
versión. La generación funcional de señales está implementada en
`core/modulation.py`; la exportación del reporte Markdown está implementada en
`services/report_service.py`.
