import re
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURACIÓN GENERAL Y ESTILOS
# =====================================================
st.set_page_config(
    page_title="Calidad y Capacitación | Contactel",
    page_icon="📊",
    layout="wide"
)

VERDE_PRINCIPAL = "#30b44e"
VERDE_OSCURO = "#1e7e34"
GRIS_DESPLEGABLE = "#f1f5f9"
GRIS_HOVER = "#dcfce7"
ROJO_CRITICO = "#dc2626"

MESES_ES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

MESES_CORTO = {
    "Enero": "Ene",
    "Febrero": "Feb",
    "Marzo": "Mar",
    "Abril": "Abr",
    "Mayo": "May",
    "Junio": "Jun",
    "Julio": "Jul",
    "Agosto": "Ago",
    "Septiembre": "Sep",
    "Octubre": "Oct",
    "Noviembre": "Nov",
    "Diciembre": "Dic"
}

ORDEN_MESES = {nombre: num for num, nombre in MESES_ES.items()}

MAPA_MES_TEXTO = {
    "01": "Enero", "1": "Enero", "ene": "Enero", "enero": "Enero",
    "02": "Febrero", "2": "Febrero", "feb": "Febrero", "febrero": "Febrero",
    "03": "Marzo", "3": "Marzo", "mar": "Marzo", "marzo": "Marzo",
    "04": "Abril", "4": "Abril", "abr": "Abril", "abril": "Abril",
    "05": "Mayo", "5": "Mayo", "may": "Mayo", "mayo": "Mayo",
    "06": "Junio", "6": "Junio", "jun": "Junio", "junio": "Junio",
    "07": "Julio", "7": "Julio", "jul": "Julio", "julio": "Julio",
    "08": "Agosto", "8": "Agosto", "ago": "Agosto", "agosto": "Agosto",
    "09": "Septiembre", "9": "Septiembre", "sep": "Septiembre", "sept": "Septiembre", "septiembre": "Septiembre",
    "10": "Octubre", "oct": "Octubre", "octubre": "Octubre",
    "11": "Noviembre", "nov": "Noviembre", "noviembre": "Noviembre",
    "12": "Diciembre", "dic": "Diciembre", "diciembre": "Diciembre"
}

st.markdown(f"""
<style>
.stApp {{
    background-color: #f4f9f5;
    color: #000000;
}}
section[data-testid="stSidebar"] {{
    background-color: #e9f3ec;
    border-right: 1px solid #b7e1c1;
}}
h1, h2, h3, h4, p, label, span, div, .stMarkdown {{
    color: #000000;
}}
h1, h2 {{
    color: #14532d !important;
}}

/* Tarjetas de métricas */
div[data-testid="stMetric"] {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 4px solid {VERDE_PRINCIPAL};
    padding: 12px 14px;
    border-radius: 8px;
}}
div[data-testid="stMetric"] label {{
    color: #1f2937 !important;
    font-weight: 600;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: #000000 !important;
    font-weight: 700;
}}

/* Caja del multiselect: visible completa, sin recortes y con 'x' y flechita contrastadas */
[data-testid="stMultiSelect"],
[data-testid="stMultiSelect"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"],
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    background-color: {GRIS_DESPLEGABLE} !important;
    color: #000000 !important;
    border-color: #64748b !important;
    border-radius: 6px !important;
    min-height: 44px !important;
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
}}

[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div:first-child {{
    display: flex !important;
    flex-wrap: wrap !important;
    align-items: center !important;
    gap: 5px !important;
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    padding: 5px 6px !important;
}}

[data-testid="stMultiSelect"] input {{
    color: #000000 !important;
    min-width: 70px !important;
}}

/* Tags seleccionados en verde #30b44e con texto e 'x' en blanco */
[data-testid="stMultiSelect"] [data-baseweb="tag"],
[data-testid="stMultiSelect"] [data-baseweb="tag"]:hover,
[data-testid="stMultiSelect"] [data-baseweb="tag"]:focus,
[data-testid="stMultiSelect"] [data-baseweb="tag"][aria-selected="true"] {{
    background-color: {VERDE_PRINCIPAL} !important;
    background: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border: 1px solid {VERDE_OSCURO} !important;
    border-radius: 6px !important;
    max-width: 100% !important;
    height: auto !important;
    min-height: 28px !important;
    padding: 3px 7px !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    overflow: visible !important;
}}

[data-testid="stMultiSelect"] [data-baseweb="tag"] span,
[data-testid="stMultiSelect"] [data-baseweb="tag"] div {{
    background: transparent !important;
    background-color: transparent !important;
    color: #ffffff !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
    max-width: none !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    line-height: 1.25 !important;
}}

[data-testid="stMultiSelect"] [data-baseweb="tag"] svg {{
    color: #ffffff !important;
    fill: #ffffff !important;
    stroke: #ffffff !important;
    stroke-width: 2.6px !important;
    width: 14px !important;
    height: 14px !important;
    opacity: 1 !important;
    visibility: visible !important;
    flex-shrink: 0 !important;
}}

/* Controles derechos del multiselect ('x' limpiar todo y flechita desplegable) */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div:last-child {{
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding-right: 8px !important;
    padding-left: 4px !important;
    background-color: {GRIS_DESPLEGABLE} !important;
    opacity: 1 !important;
    visibility: visible !important;
    flex-shrink: 0 !important;
}}

[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div:last-child svg {{
    width: 15px !important;
    height: 15px !important;
    color: #0f172a !important;
    fill: #0f172a !important;
    stroke: #0f172a !important;
    stroke-width: 2.6px !important;
    opacity: 1 !important;
    visibility: visible !important;
}}

/* Menú desplegable abierto */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] > div > div,
ul[data-testid="stSelectboxVirtualDropdown"],
ul[role="listbox"],
ul[role="listbox"] > li,
div[role="listbox"],
div[role="listbox"] > div,
[role="option"] {{
    background-color: #ffffff !important;
    color: #000000 !important;
}}
ul[role="listbox"] > li:hover,
[role="option"]:hover,
[aria-selected="true"] {{
    background-color: {GRIS_HOVER} !important;
    color: #000000 !important;
}}
div[data-baseweb="popover"] span,
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] p,
ul[role="listbox"] span,
ul[role="listbox"] div,
[role="option"] span,
[role="option"] div {{
    color: #000000 !important;
}}

/* Botones en verde #30b44e */
.stButton > button,
.stDownloadButton > button {{
    background-color: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}
.stButton > button:hover,
.stDownloadButton > button:hover {{
    background-color: {VERDE_OSCURO} !important;
    color: #ffffff !important;
}}

/* Tarjeta compacta por asesor */
.card-compacta {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 5px solid #1e3a8a;
    border-radius: 4px;
    padding: 12px 14px;
    margin-bottom: 16px;
    color: #000000;
}}
.card-titulo {{
    font-size: 15px;
    font-weight: 800;
    text-align: center;
    color: #0f172a;
    margin-bottom: 3px;
    text-transform: uppercase;
}}
.card-sub {{
    font-size: 11.5px;
    font-weight: 600;
    text-align: center;
    color: #334155;
    margin-bottom: 10px;
    padding-bottom: 7px;
    border-bottom: 1px solid #cbd5e1;
}}
.bloque-verde {{
    background: #eaf7ed;
    border-left: 4px solid {VERDE_PRINCIPAL};
    padding: 7px 9px;
    margin-bottom: 7px;
    font-size: 12px;
    line-height: 1.35;
}}
.bloque-rojo {{
    background: #fef2f2;
    border-left: 4px solid {ROJO_CRITICO};
    padding: 7px 9px;
    margin-bottom: 7px;
    font-size: 12px;
    line-height: 1.35;
}}
.bloque-naranja {{
    background: #fffbeb;
    border-left: 4px solid #eab308;
    padding: 7px 9px;
    margin-bottom: 7px;
    font-size: 12px;
    line-height: 1.35;
}}
.bloque-feedback {{
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    margin-top: 4px;
    font-size: 12px;
    line-height: 1.35;
}}
.tit-verde {{ color: #15803d; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-rojo {{ color: #b91c1c; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-naranja {{ color: #b45309; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-fb {{ color: #0f172a; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}

/* Matriz Mes x Campaña estilo planilla (ajustada al ancho sin scroll lateral) */
.matriz-emp-titulo {{
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 8px;
    margin-bottom: 8px;
    text-transform: uppercase;
}}
.matriz-emp-wrap {{
    width: 100%;
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 6px;
    margin-bottom: 18px;
}}
table.matriz-emp {{
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    font-size: 11.5px;
    color: #000000;
}}
table.matriz-emp th.th-mes {{
    background-color: #ffffff;
    color: #000000;
    font-weight: 800;
    text-align: left;
    padding: 7px 6px;
    border: 1px solid #64748b;
    width: 96px;
    white-space: nowrap;
}}
table.matriz-emp th.th-camp {{
    background-color: #16a34a;
    color: #ffffff;
    font-weight: 700;
    text-align: center;
    padding: 6px 4px;
    border: 1px solid #64748b;
    white-space: normal;
    line-height: 1.15;
    overflow-wrap: break-word;
}}
table.matriz-emp th.th-prom {{
    background-color: #52525b;
    color: #ffffff;
    font-weight: 800;
    text-align: center;
    padding: 6px 5px;
    border: 1px solid #64748b;
    width: 88px;
    white-space: normal;
    line-height: 1.15;
}}
table.matriz-emp td {{
    padding: 6px 4px;
    border: 1px solid #64748b;
    text-align: center;
    vertical-align: middle;
    color: #000000;
    font-weight: 600;
    font-size: 11px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
table.matriz-emp td.td-mes {{
    text-align: left;
    font-weight: 600;
    font-size: 11.5px;
    background-color: #ffffff;
    padding-left: 6px;
}}
table.matriz-emp td.td-prom-fila {{
    background-color: #f4f4f5;
    font-weight: 800;
}}
table.matriz-emp tr.fila-total-camp td {{
    font-weight: 800;
    border-top: 2px solid #334155;
}}
table.matriz-emp tr.fila-total-camp td.td-etq-total {{
    background-color: #9ca3af;
    color: #000000;
    text-align: center;
    white-space: normal;
    line-height: 1.15;
    font-size: 10.5px;
}}
table.matriz-emp tr.fila-total-camp td.td-vacio-final {{
    background-color: #ffffff;
}}

/* Cuadro único consolidado por campaña y período con barra horizontal */
.resumen-per-wrap {{
    width: 100%;
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #64748b;
    border-radius: 4px;
    margin-bottom: 18px;
}}
table.resumen-per {{
    width: max-content;
    min-width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
}}
table.resumen-per th.th-per-grupo {{
    background-color: #bfbfbf;
    color: #000000;
    font-weight: 800;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #64748b;
    font-size: 13px;
    white-space: nowrap;
}}
table.resumen-per th.th-per-camp-hdr {{
    background-color: #2ea043;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 7px 12px;
    border: 1px solid #64748b;
    min-width: 190px;
    white-space: nowrap;
}}
table.resumen-per th.th-per-col {{
    background-color: #2ea043;
    color: #ffffff;
    font-weight: 700;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #64748b;
    min-width: 105px;
    white-space: nowrap;
    line-height: 1.15;
}}
table.resumen-per td.td-per-camp {{
    background-color: #595959;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 6px 12px;
    border: 1px solid #64748b;
    white-space: nowrap;
}}
table.resumen-per td.td-per-q {{
    background-color: #ffffff;
    color: #000000;
    font-weight: 600;
    text-align: center;
    padding: 6px 10px;
    border: 1px solid #64748b;
    white-space: nowrap;
}}
table.resumen-per td.td-per-prom {{
    background-color: #ffffff;
    color: #000000;
    font-weight: 600;
    text-align: center;
    padding: 6px 10px;
    border: 1px solid #64748b;
    white-space: nowrap;
}}
table.resumen-per tr.fila-per-total td {{
    background-color: #2ea043;
    color: #ffffff;
    font-weight: 800;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #64748b;
    white-space: nowrap;
}}
table.resumen-per tr.fila-per-total td.td-per-total-etq {{
    text-align: left;
    padding-left: 12px;
}}

/* Cuadro comparativo con nombre legible y focos completos */
.cuadro-comp-titulo {{
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 8px;
    text-transform: uppercase;
}}
.tabla-comp-wrap {{
    width: 100%;
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    margin-bottom: 14px;
}}
table.tabla-comp {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    color: #000000;
}}
table.tabla-comp th {{
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 9px 10px;
    border: 1px solid #1e293b;
    white-space: nowrap;
}}
table.tabla-comp td {{
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
    line-height: 1.35;
    color: #000000;
}}
table.tabla-comp td.col-asesor {{
    min-width: 210px;
    white-space: nowrap;
    font-weight: 700;
    color: #0f172a;
}}
table.tabla-comp td.col-foco {{
    min-width: 260px;
    white-space: normal;
    overflow-wrap: break-word;
}}
table.tabla-comp tr:nth-child(even) td {{
    background-color: #f8fafc;
}}

/* Deducción final analítica */
.deduccion-box {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 6px solid {VERDE_OSCURO};
    border-radius: 8px;
    padding: 16px 18px;
    margin-top: 12px;
    margin-bottom: 16px;
    color: #000000;
    font-size: 13px;
    line-height: 1.45;
}}
.deduccion-titulo {{
    font-size: 14.5px;
    font-weight: 800;
    color: #14532d;
    margin-bottom: 10px;
    text-transform: uppercase;
}}
.ded-pos {{
    background: #eaf7ed;
    border-left: 4px solid {VERDE_PRINCIPAL};
    padding: 8px 11px;
    border-radius: 4px;
    margin-bottom: 8px;
}}
.ded-alert {{
    background: #fef2f2;
    border-left: 4px solid {ROJO_CRITICO};
    padding: 8px 11px;
    border-radius: 4px;
    margin-bottom: 8px;
}}
.ded-rec {{
    background: #f0fdf4;
    border-left: 4px solid #15803d;
    padding: 8px 11px;
    border-radius: 4px;
}}
.comentario-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid {VERDE_PRINCIPAL};
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
    font-size: 13px;
}}
</style>
""", unsafe_allow_html=True)

st.title("Calidad y Capacitación")
st.caption("Panel de seguimiento de desempeño | Contactel")

# =====================================================
# FUENTE DE DATOS
# =====================================================
URL_MEDICION = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=0&single=true&output=csv"
)

# =====================================================
# PONDERACIONES, CRITERIOS Y CLASIFICACIÓN
# =====================================================
PONDERACIONES = {
    "Genera conexión positiva y de confianza en presentación": (5, 5),
    "Explica motivo de llamada claramente": (5, 5),
    "Explora necesidades reales": (5, 8),
    "Escucha activa": (10, 12),
    "Propuesta adaptada al cliente": (6, 3),
    "Explica beneficios": (3, 5),
    "Usa ejemplos / comparaciones": (3, 5),
    "No realiza monólogo": (5, 2),
    "Avanza hacia el cierre": (8, 10),
    "Identifica objeción real": (5, 5),
    "Maneja objeciones": (10, 20),
    "Realiza cierres parciales": (4, 3),
    "Indica Valor a abonar": (5, 5),
    "Sin connotación de obligatoriedad": (6, 2),
    "Realiza de forma correcta cierres legales": (5, 5),
    "Tono natural y entusiasta": (3, 1),
    "Evita frases robotizadas": (5, 2),
    "Tuteo al cliente/Cortesía": (7, 2)
}

CRITERIOS = [
    "Genera conexión positiva y de confianza en presentación",
    "Explica motivo de llamada claramente",
    "Tipo de preguntas realizadas",
    "Explora necesidades reales",
    "Escucha activa",
    "Propuesta adaptada al cliente",
    "Explica beneficios",
    "Usa ejemplos / comparaciones",
    "No realiza monólogo",
    "Avanza hacia el cierre",
    "Identifica objeción real",
    "Maneja objeciones",
    "Realiza cierres parciales",
    "Indica Valor a abonar",
    "Sin connotación de obligatoriedad",
    "Realiza de forma correcta cierres legales",
    "Tono natural y entusiasta",
    "Evita frases robotizadas",
    "Tuteo al cliente/Cortesía"
]

DIMENSION_CRITERIO = {
    "Genera conexión positiva y de confianza en presentación": "Actitudinal",
    "Explica motivo de llamada claramente": "Comercial",
    "Explora necesidades reales": "Comercial",
    "Escucha activa": "Comercial",
    "Propuesta adaptada al cliente": "Comercial",
    "Explica beneficios": "Comercial",
    "Usa ejemplos / comparaciones": "Comercial",
    "No realiza monólogo": "Comercial",
    "Avanza hacia el cierre": "Comercial",
    "Identifica objeción real": "Comercial",
    "Maneja objeciones": "Comercial",
    "Realiza cierres parciales": "Comercial",
    "Indica Valor a abonar": "Comercial",
    "Sin connotación de obligatoriedad": "Comercial",
    "Realiza de forma correcta cierres legales": "Comercial",
    "Tono natural y entusiasta": "Actitudinal",
    "Evita frases robotizadas": "Actitudinal",
    "Tuteo al cliente/Cortesía": "Actitudinal"
}

FOCO_DESARROLLO_CRITERIO = {
    "Genera conexión positiva y de confianza en presentación": "Cercanía y calidez en la apertura inicial.",
    "Explica motivo de llamada claramente": "Claridad y gancho directo en el motivo de llamada.",
    "Explora necesidades reales": "Sondeo con preguntas abiertas antes de ofertar.",
    "Escucha activa": "Escucha activa sin interrumpir y retomando al cliente.",
    "Propuesta adaptada al cliente": "Adecuar la propuesta a la necesidad detectada.",
    "Explica beneficios": "Traducir atributos en beneficios concretos.",
    "Usa ejemplos / comparaciones": "Uso de ejemplos simples y cotidianos.",
    "No realiza monólogo": "Evitar monólogos y pausar para validar comprensión.",
    "Avanza hacia el cierre": "Conducción firme y ordenada hacia el cierre.",
    "Identifica objeción real": "Detectar la objeción real detrás de la respuesta.",
    "Maneja objeciones": "Seguridad y firmeza ante objeciones y negativas.",
    "Realiza cierres parciales": "Confirmar acuerdos parciales durante la llamada.",
    "Indica Valor a abonar": "Precisión al informar el valor a abonar.",
    "Sin connotación de obligatoriedad": "Evitar tono impositivo u obligatoriedad.",
    "Realiza de forma correcta cierres legales": "Cumplimiento completo de cierres legales.",
    "Tono natural y entusiasta": "Dinamismo, naturalidad y energía vocal.",
    "Evita frases robotizadas": "Hablar con naturalidad evitando lectura rígida.",
    "Tuteo al cliente/Cortesía": "Sostener cortesía y trato acorde al cliente."
}

RECOMENDACIONES_CRITERIO = {
    "Genera conexión positiva y de confianza en presentación":
        "Apertura cálida y cercana en los primeros segundos para generar confianza inicial.",
    "Explica motivo de llamada claramente":
        "Gancho inicial directo y claro para que el cliente entienda desde el inicio el motivo.",
    "Explora necesidades reales":
        "Reforzar preguntas abiertas y de diagnóstico antes de presentar la oferta.",
    "Escucha activa":
        "Evitar interrumpir y retomar palabras clave del cliente.",
    "Propuesta adaptada al cliente":
        "Conectar cada atributo de la propuesta con la necesidad detectada.",
    "Explica beneficios":
        "Traducir características en beneficios concretos para el cliente.",
    "Usa ejemplos / comparaciones":
        "Usar ejemplos cotidianos o comparaciones simples para facilitar la comprensión.",
    "No realiza monólogo":
        "Hacer pausas breves y validar comprensión durante la exposición.",
    "Avanza hacia el cierre":
        "Guiar la conversación con pasos concretos hacia el cierre.",
    "Identifica objeción real":
        "Distinguir entre excusa superficial y objeción de fondo antes de responder.",
    "Maneja objeciones":
        "Practicar empatía, validación, reformulación y cierre ante objeciones.",
    "Realiza cierres parciales":
        "Confirmar acuerdos intermedios durante la llamada.",
    "Indica Valor a abonar":
        "Comunicar con claridad y sin ambigüedades el valor a abonar.",
    "Sin connotación de obligatoriedad":
        "Evitar tono imperativo o sensación de obligación en el cliente.",
    "Realiza de forma correcta cierres legales":
        "Transmitir completos y claros todos los cierres legales obligatorios.",
    "Tono natural y entusiasta":
        "Mantener energía positiva, modulación y naturalidad vocal.",
    "Evita frases robotizadas":
        "Reemplazar frases rígidas por expresiones naturales y conversacionales.",
    "Tuteo al cliente/Cortesía":
        "Sostener trato cordial y coherente con el estilo de la campaña."
}

# =====================================================
# FUNCIONES
# =====================================================
def limpiar_texto_etiqueta(valor):
    return " ".join(str(valor).split()).strip()


def formatear_nombre_recurso(nombre):
    limpio = limpiar_texto_etiqueta(nombre)
    if "," in limpio:
        partes = [p.strip() for p in limpio.split(",", 1)]
        if len(partes) == 2 and partes[1]:
            return f"{partes[0]}, {partes[1]}"
    return limpio


def normalizar_clave(valor):
    return limpiar_texto_etiqueta(valor).lower()


def normalizar_clave_campana(valor):
    texto = normalizar_clave(valor)
    texto = re.sub(r"[\s\-_]+", " ", texto).strip()
    return texto


def parsear_mes_texto(mes_raw):
    texto = normalizar_clave(mes_raw)
    if not texto or texto in ("nan", "nat", "sin mes"):
        return None

    if texto in MAPA_MES_TEXTO:
        return MAPA_MES_TEXTO[texto]

    for clave, nombre_mes in MAPA_MES_TEXTO.items():
        if re.search(rf"(?<![a-z0-9]){re.escape(clave)}(?![a-z0-9])", texto):
            return nombre_mes

    if len(texto) >= 7 and texto[4] == "-":
        parte_mes = texto[5:7]
        if parte_mes in MAPA_MES_TEXTO:
            return MAPA_MES_TEXTO[parte_mes]

    return None


def nombre_mes_desde_valor(mes_raw, fecha_dt):
    mes_por_raw = parsear_mes_texto(mes_raw)
    if mes_por_raw:
        return mes_por_raw

    if pd.notna(fecha_dt):
        return MESES_ES.get(int(fecha_dt.month), "Sin mes")

    return "Sin mes"


def ordenar_meses(lista_meses):
    return sorted(
        [m for m in set(lista_meses) if m and m != "Sin mes"],
        key=lambda m: ORDEN_MESES.get(m, 99)
    )


def fmt_pct(valor):
    if pd.isna(valor):
        return "Sin datos"
    return f"{round(float(valor))}%"


def fmt_pct_dec(valor):
    if pd.isna(valor):
        return "-"
    return f"{float(valor):.2f}%".replace(".", ",")


def color_celda_calidad(valor):
    if pd.isna(valor):
        return "#9ca3af"
    v = float(valor)
    if v < 51.0:
        return "#e6b8af"
    if v < 70.0:
        return "#ffe599"
    return "#b6d7a8"


def convertir_puntaje(valor):
    try:
        texto = str(valor).replace("%", "").replace(",", ".").strip()
        if texto == "":
            return None
        numero = float(texto)
        return numero * 100 if numero <= 1 else numero
    except (ValueError, TypeError):
        return None


def normalizar_tipo(valor):
    texto = str(valor).strip().lower()
    if "no venta" in texto or "no_venta" in texto or "noventa" in texto:
        return "No Venta"
    if "venta" in texto:
        return "Venta"
    return None


def parsear_fecha_segura(serie):
    f1 = pd.to_datetime(serie, dayfirst=True, errors="coerce")
    f2 = pd.to_datetime(serie, dayfirst=False, errors="coerce")
    resultado = f1.fillna(f2)

    faltantes = resultado.isna()
    if faltantes.any():
        nums = pd.to_numeric(serie[faltantes], errors="coerce")
        valid_nums = nums.dropna()
        if not valid_nums.empty:
            fechas_excel = pd.to_datetime(valid_nums, unit="D", origin="1899-12-30", errors="coerce")
            resultado.loc[fechas_excel.index] = fechas_excel

    return resultado


def extraer_anio_seguro(fecha_dt, mes_raw, fecha_raw):
    if pd.notna(fecha_dt):
        return str(int(fecha_dt.year))

    for texto in (str(fecha_raw), str(mes_raw)):
        match_4 = re.search(r"\b(202[4-9])\b", texto)
        if match_4:
            return match_4.group(1)

    for texto in (str(fecha_raw), str(mes_raw)):
        match_2 = re.search(r"(?:^|[/\-])(2[4-9])(?=$|[/\-\s])", texto.strip())
        if match_2:
            return f"20{match_2.group(1)}"

    return "Sin año"


def calcular_puntaje(fila):
    tipo = normalizar_tipo(fila["Tipo de gestión"])
    if tipo is None:
        return None

    indice = 0 if tipo == "Venta" else 1
    obtenido = 0
    posible = 0

    for criterio, pesos in PONDERACIONES.items():
        peso = pesos[indice]
        respuesta = str(fila[criterio]).strip().lower()
        posible += peso

        if respuesta in ("si", "sí", "n/a"):
            obtenido += peso
        elif respuesta == "punto de mejora":
            obtenido += peso / 2

    return (obtenido / posible * 100) if posible else None


@st.cache_data(ttl=300)
def leer_mediciones_crudo_y_procesado():
    bruto = pd.read_csv(
        URL_MEDICION,
        header=None,
        dtype=str,
        keep_default_na=False,
        engine="python"
    )

    n_cols_esperadas = 33
    if bruto.shape[1] < n_cols_esperadas:
        for _ in range(n_cols_esperadas - bruto.shape[1]):
            bruto[bruto.shape[1]] = ""

    datos = bruto.iloc[9:, :n_cols_esperadas].copy()
    datos.columns = (
        ["Fecha", "Mes_raw", "Asesor", "Campaña", "ID",
         "Duración", "Tipo de gestión", "Tipificación"]
        + CRITERIOS
        + ["Puntos a trabajar", "Acción", "Puntaje",
           "Observaciones", "¿Tipifica bien?", "Tipificación correcta"]
    )
    datos = datos.drop(columns=["Acción"])

    for col in datos.columns:
        datos[col] = datos[col].apply(limpiar_texto_etiqueta)

    datos["Fecha_raw"] = datos["Fecha"]

    datos = datos[
        (datos["Asesor"] != "") | (datos["Campaña"] != "")
    ].copy()
    datos["Asesor"] = datos["Asesor"].replace("", "Sin asesor")
    datos["Campaña"] = datos["Campaña"].replace("", "Sin campaña")

    datos["Fecha"] = parsear_fecha_segura(datos["Fecha"])
    datos["Puntaje oficial"] = datos["Puntaje"].apply(convertir_puntaje)
    datos["Puntaje calculado"] = datos.apply(calcular_puntaje, axis=1)
    datos["Puntaje final"] = datos["Puntaje oficial"].fillna(
        datos["Puntaje calculado"]
    )
    datos["Tipo normalizado"] = datos["Tipo de gestión"].apply(normalizar_tipo)

    datos["Mes"] = [
        nombre_mes_desde_valor(m_raw, f_dt)
        for m_raw, f_dt in zip(datos["Mes_raw"], datos["Fecha"])
    ]
    datos["Mes_orden"] = datos["Mes"].map(lambda m: ORDEN_MESES.get(m, 99))

    datos["Año"] = [
        extraer_anio_seguro(f_dt, m_raw, f_raw)
        for f_dt, m_raw, f_raw in zip(datos["Fecha"], datos["Mes_raw"], datos["Fecha_raw"])
    ]
    datos["Campaña_key"] = datos["Campaña"].apply(normalizar_clave_campana)
    datos["Asesor_key"] = datos["Asesor"].apply(normalizar_clave)

    return bruto, datos


def construir_detalle_criterios(datos):
    registros = []
    for _, fila in datos.iterrows():
        tipo = fila["Tipo normalizado"]
        indice = 0 if tipo == "Venta" else 1
        for criterio, pesos in PONDERACIONES.items():
            respuesta = str(fila[criterio]).strip().lower()
            peso = pesos[indice]

            if respuesta not in ["si", "sí", "no", "punto de mejora", "n/a"]:
                continue

            if respuesta == "no":
                descuento, puntos = peso, 0
            elif respuesta == "punto de mejora":
                descuento, puntos = peso / 2, peso / 2
            else:
                descuento, puntos = 0, peso

            registros.append({
                "Fecha": fila["Fecha"],
                "Año": fila["Año"],
                "Mes": fila["Mes"],
                "Mes_orden": fila["Mes_orden"],
                "Asesor": fila["Asesor"],
                "Campaña": fila["Campaña"],
                "Tipo de gestión": tipo if tipo else "Sin tipo",
                "Criterio": criterio,
                "Dimensión": DIMENSION_CRITERIO.get(criterio, "Comercial"),
                "Respuesta": respuesta,
                "Ponderación": peso,
                "Descuento": descuento,
                "Puntos obtenidos": puntos
            })
    return pd.DataFrame(registros)


def estilo_grafico(fig, titulo, eje_x=None, eje_y=None, es_porcentaje_y=False):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color="#000000", size=18)),
        font=dict(color="#000000", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#000000")),
        margin=dict(l=20, r=20, t=60, b=35),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#14532d",
            font=dict(color="#000000", size=12)
        )
    )
    fig.update_xaxes(
        title_text=eje_x,
        color="#000000",
        title_font=dict(color="#000000"),
        tickfont=dict(color="#000000"),
        gridcolor="#d1fae5"
    )
    fig.update_yaxes(
        title_text=eje_y,
        color="#000000",
        title_font=dict(color="#000000"),
        tickfont=dict(color="#000000"),
        gridcolor="#d1fae5",
        ticksuffix="%" if es_porcentaje_y else ""
    )
    return fig


def mostrar_tabla(datos, columnas=None):
    if datos.empty:
        st.info("No hay datos para mostrar con la selección actual.")
    else:
        tabla = datos if columnas is None else datos[columnas]
        st.dataframe(tabla, use_container_width=True, hide_index=True)


def render_matriz_empresa_html(base_emp):
    df_m = base_emp[base_emp["Mes"] != "Sin mes"].copy()
    if df_m.empty:
        st.info("No hay registros con mes válido para construir la matriz.")
        return

    campañas = sorted(df_m["Campaña"].unique())
    periodos_df = (
        df_m[["Año", "Mes", "Mes_orden"]]
        .drop_duplicates()
        .sort_values(["Año", "Mes_orden"])
    )

    headers_html = ['<th class="th-mes">Mes</th>']
    for camp in campañas:
        headers_html.append(f'<th class="th-camp">{camp}</th>')
    headers_html.append('<th class="th-prom">PROMEDIO<br>CALIDAD</th>')

    filas_html = []
    for _, per in periodos_df.iterrows():
        anio_p = per["Año"]
        mes_p = per["Mes"]
        etq_periodo = f"{mes_p.lower()} {anio_p}" if anio_p != "Sin año" else mes_p.lower()

        sub_per = df_m[(df_m["Año"] == anio_p) & (df_m["Mes"] == mes_p)]
        celdas = [f'<td class="td-mes">{etq_periodo}</td>']

        vals_fila = []
        for camp in campañas:
            val_c = sub_per[sub_per["Campaña"] == camp]["Puntaje final"].mean()
            if pd.notna(val_c):
                vals_fila.append(float(val_c))
                bg = color_celda_calidad(val_c)
                celdas.append(f'<td style="background-color:{bg};">{fmt_pct_dec(val_c)}</td>')
            else:
                celdas.append('<td style="background-color:#9ca3af;"></td>')

        prom_fila = (sum(vals_fila) / len(vals_fila)) if vals_fila else None
        prom_txt = fmt_pct_dec(prom_fila) if prom_fila is not None else "-"
        celdas.append(f'<td class="td-prom-fila">{prom_txt}</td>')
        filas_html.append(f"<tr>{''.join(celdas)}</tr>")

    celdas_total = ['<td class="td-etq-total">Promedio<br>Calidad por<br>campaña</td>']
    for camp in campañas:
        val_camp_tot = df_m[df_m["Campaña"] == camp]["Puntaje final"].mean()
        if pd.notna(val_camp_tot):
            bg_c = color_celda_calidad(val_camp_tot)
            celdas_total.append(f'<td style="background-color:{bg_c};">{fmt_pct_dec(val_camp_tot)}</td>')
        else:
            celdas_total.append('<td style="background-color:#9ca3af;">-</td>')
    celdas_total.append('<td class="td-vacio-final"></td>')
    filas_html.append(f'<tr class="fila-total-camp">{"".join(celdas_total)}</tr>')

    st.markdown(
        f'<div class="matriz-emp-wrap"><table class="matriz-emp">'
        f'<thead><tr>{"".join(headers_html)}</tr></thead>'
        f'<tbody>{"".join(filas_html)}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True
    )


def render_cuadros_por_periodo_html(base_emp, camps_sel):
    df_p = base_emp[base_emp["Mes"] != "Sin mes"].copy()
    if df_p.empty:
        st.info("No hay auditorías por período con la selección actual.")
        return

    campañas_mostrar = sorted(camps_sel) if camps_sel else sorted(df_p["Campaña"].unique())
    periodos_df = (
        df_p[["Año", "Mes", "Mes_orden"]]
        .drop_duplicates()
        .sort_values(["Año", "Mes_orden"], ascending=[True, True])
    )

    grupos_hdr = ['<th class="th-per-camp-hdr" rowspan="2">Campaña</th>']
    sub_hdr = []
    totales_q_per = []
    totales_prom_per = []

    for _, per in periodos_df.iterrows():
        anio_p = per["Año"]
        mes_p = per["Mes"]
        etq_per = f"{mes_p.lower()} {anio_p}" if anio_p != "Sin año" else mes_p.lower()

        grupos_hdr.append(f'<th class="th-per-grupo" colspan="2">{etq_per}</th>')
        sub_hdr.append('<th class="th-per-col">Q de auditorias</th>')
        sub_hdr.append('<th class="th-per-col">Puntuación<br>promedio</th>')

        sub_per = df_p[(df_p["Año"] == anio_p) & (df_p["Mes"] == mes_p)]
        q_sum = 0
        proms_c = []
        for camp in campañas_mostrar:
            sc = sub_per[sub_per["Campaña"] == camp]
            q_sum += len(sc)
            if len(sc) > 0 and pd.notna(sc["Puntaje final"].mean()):
                proms_c.append(float(sc["Puntaje final"].mean()))
        totales_q_per.append(q_sum)
        totales_prom_per.append(fmt_pct(sum(proms_c) / len(proms_c)) if proms_c else "-")

    filas_html = []
    for camp in campañas_mostrar:
        celdas = [f'<td class="td-per-camp">{camp}</td>']
        for _, per in periodos_df.iterrows():
            anio_p = per["Año"]
            mes_p = per["Mes"]
            sub_c = df_p[(df_p["Año"] == anio_p) & (df_p["Mes"] == mes_p) & (df_p["Campaña"] == camp)]
            q_c = int(len(sub_c))
            prom_c = sub_c["Puntaje final"].mean() if q_c > 0 else None
            prom_txt = fmt_pct(prom_c) if (prom_c is not None and pd.notna(prom_c)) else ""
            celdas.append(f'<td class="td-per-q">{q_c}</td>')
            celdas.append(f'<td class="td-per-prom">{prom_txt}</td>')
        filas_html.append(f"<tr>{''.join(celdas)}</tr>")

    celdas_tot = ['<td class="td-per-total-etq">Total</td>']
    for q_t, p_t in zip(totales_q_per, totales_prom_per):
        celdas_tot.append(f"<td>{q_t}</td>")
        celdas_tot.append(f"<td>{p_t}</td>")
    filas_html.append(f'<tr class="fila-per-total">{"".join(celdas_tot)}</tr>')

    st.markdown(
        f'<div class="resumen-per-wrap"><table class="resumen-per">'
        f'<thead>'
        f'<tr>{"".join(grupos_hdr)}</tr>'
        f'<tr>{"".join(sub_hdr)}</tr>'
        f'</thead>'
        f'<tbody>{"".join(filas_html)}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True
    )


def resumen_ejes_criterios(df_crit):
    if df_crit.empty:
        return pd.DataFrame(columns=[
            "Criterio", "Dimensión", "Evaluaciones", "% Positivo",
            "% Mejora", "% Crítico", "Descuento", "Estado"
        ])
    res = df_crit.groupby(["Criterio", "Dimensión"], as_index=False).agg(
        Evaluaciones=("Respuesta", "count"),
        Positivos=("Respuesta", lambda x: x.isin(["si", "sí", "n/a"]).sum()),
        Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum()),
        Criticos=("Respuesta", lambda x: (x == "no").sum()),
        Descuento=("Descuento", "sum")
    )
    res["% Positivo_num"] = res["Positivos"] / res["Evaluaciones"] * 100
    res["% Mejora_num"] = res["Mejoras"] / res["Evaluaciones"] * 100
    res["% Crítico_num"] = res["Criticos"] / res["Evaluaciones"] * 100

    res["% Positivo"] = res["% Positivo_num"].apply(fmt_pct)
    res["% Mejora"] = res["% Mejora_num"].apply(fmt_pct)
    res["% Crítico"] = res["% Crítico_num"].apply(fmt_pct)
    res["Descuento"] = res["Descuento"].round(0).astype(int)

    def clasificar(row):
        if row["% Crítico_num"] >= 20 or row["Criticos"] >= 3:
            return "Crítico"
        if row["% Mejora_num"] >= 15 or row["Mejoras"] >= 2:
            return "A mejorar"
        return "Positivo"

    res["Estado"] = res.apply(clasificar, axis=1)
    return res.sort_values(["% Crítico_num", "% Mejora_num", "Descuento"], ascending=[False, False, False])


def filtrar_registros(base_df, anios_sel, meses_sel, camps_sel, ases_sel=None,
                      todas_ases_disp=None):
    out = base_df.copy()
    if anios_sel:
        out = out[out["Año"].isin(anios_sel)]
    if meses_sel:
        out = out[out["Mes"].isin(meses_sel)]

    base_ases = out.copy()
    if camps_sel:
        claves_c = {normalizar_clave_campana(c) for c in camps_sel}
        base_ases = base_ases[base_ases["Campaña_key"].isin(claves_c)]
        out = out[out["Campaña_key"].isin(claves_c)]

    ases_opciones = sorted(base_ases["Asesor"].dropna().unique())
    if not ases_opciones and todas_ases_disp:
        ases_opciones = list(todas_ases_disp)

    if ases_sel is not None and ases_sel:
        claves_a = {normalizar_clave(a) for a in ases_sel}
        out = out[out["Asesor_key"].isin(claves_a)]

    return out, ases_opciones


def preparar_selector_asesor(key_asesor, key_firma, firma_actual, ases_opciones):
    firma_anterior = st.session_state.get(key_firma)
    if key_asesor not in st.session_state or firma_anterior != firma_actual:
        st.session_state[key_asesor] = list(ases_opciones)
        st.session_state[key_firma] = firma_actual


def sintesis_dimension(ejes_df, modo, dimension):
    if ejes_df.empty:
        return "Sin registro suficiente."
    sub = ejes_df[ejes_df["Dimensión"] == dimension]
    if sub.empty:
        return "Sin registro en esta dimensión."

    if modo == "positivo":
        elegidos = sub.sort_values(["% Positivo_num", "Evaluaciones"], ascending=[False, False]).head(2)
    elif modo == "critico":
        elegidos = sub[sub["Criticos"] > 0].sort_values(["% Crítico_num", "Descuento"], ascending=[False, False]).head(2)
        if elegidos.empty:
            return "Sin desvíos críticos registrados."
    else:
        elegidos = sub[sub["Mejoras"] > 0].sort_values(["% Mejora_num", "Descuento"], ascending=[False, False]).head(2)
        if elegidos.empty:
            return "Sin puntos en desarrollo registrados."

    partes = [FOCO_DESARROLLO_CRITERIO.get(r["Criterio"], r["Criterio"]) for _, r in elegidos.iterrows()]
    return "; ".join(partes)


def resumen_feedback_comercial_consolidado(sub_a, ejes_a):
    obs_all = [
        limpiar_texto_etiqueta(o)
        for o in sub_a["Observaciones"]
        if limpiar_texto_etiqueta(o) and limpiar_texto_etiqueta(o).lower() != "nan"
    ]
    pts_all = [
        limpiar_texto_etiqueta(p)
        for p in sub_a["Puntos a trabajar"]
        if limpiar_texto_etiqueta(p) and limpiar_texto_etiqueta(p).lower() != "nan"
    ]
    corpus_texto = " ".join(obs_all + pts_all).lower()

    foco_cierre = []
    if any(k in corpus_texto for k in ["objec", "precio", "valor", "cuota", "caro", "cierre", "oferta", "propuesta"]):
        foco_cierre.append("defender propuesta de valor y cierre")
    if any(k in corpus_texto for k in ["escuch", "interrump", "pregunta", "sondeo", "necesidad", "indag"]):
        foco_cierre.append("profundizar sondeo y escucha activa")
    if any(k in corpus_texto for k in ["tono", "rapido", "rápido", "robot", "guion", "lee", "formal", "natural"]):
        foco_cierre.append("ganar naturalidad y ritmo comercial")

    if not foco_cierre and not ejes_a.empty:
        top_crit = ejes_a[ejes_a["Criticos"] > 0]
        top_mej = ejes_a[ejes_a["Mejoras"] > 0]
        if not top_crit.empty:
            foco_cierre.append(FOCO_DESARROLLO_CRITERIO.get(top_crit.iloc[0]["Criterio"], top_crit.iloc[0]["Criterio"]).rstrip("."))
        elif not top_mej.empty:
            foco_cierre.append(FOCO_DESARROLLO_CRITERIO.get(top_mej.iloc[0]["Criterio"], top_mej.iloc[0]["Criterio"]).rstrip("."))

    fortaleza_criterio = ""
    if not ejes_a.empty:
        mejor_eje = ejes_a.sort_values(["% Positivo_num", "Evaluaciones"], ascending=[False, False]).iloc[0]
        fortaleza_criterio = FOCO_DESARROLLO_CRITERIO.get(mejor_eje["Criterio"], mejor_eje["Criterio"]).rstrip(".")

    prom_txt = fmt_pct(sub_a["Puntaje final"].mean())
    n_aud = len(sub_a)

    if not obs_all and not pts_all and ejes_a.empty:
        return f"Sin observaciones ni evaluaciones registradas en {n_aud} auditoría(s) ({prom_txt})."

    parte_fort = f"Apoyarse en {fortaleza_criterio.lower()}" if fortaleza_criterio else f"Nivel {prom_txt} en {n_aud} aud."
    parte_foco = f"y priorizar {', '.join(foco_cierre[:2]).lower()}" if foco_cierre else "manteniendo consistencia comercial"

    return f"{parte_fort}, {parte_foco} ({n_aud} aud. | {prom_txt})."


def construir_cuadro_comparativo(filtrado_ases, meses_activos):
    filas = []
    meses_ord = ordenar_meses(meses_activos)

    for nom_asesor in sorted(filtrado_ases["Asesor"].unique()):
        sub_a = filtrado_ases[filtrado_ases["Asesor"] == nom_asesor]
        crit_a = construir_detalle_criterios(sub_a)
        ejes_a = resumen_ejes_criterios(crit_a)

        fila = {"Asesor": formatear_nombre_recurso(nom_asesor)}
        proms_mes = []
        for m in meses_ord:
            g_m = sub_a[sub_a["Mes"] == m]["Puntaje final"].mean()
            etq_m = f"Prom. {MESES_CORTO.get(m, m)}"
            fila[etq_m] = fmt_pct(g_m) if pd.notna(g_m) else "-"
            if pd.notna(g_m):
                proms_mes.append((m, float(g_m)))

        prom_tot = sub_a["Puntaje final"].mean()
        fila["Prom. Total"] = fmt_pct(prom_tot)

        if len(proms_mes) >= 2:
            brecha = proms_mes[-1][1] - proms_mes[0][1]
            signo = "+" if brecha > 0 else ""
            estado_b = "Estable" if abs(brecha) < 3 else ("Ajuste" if brecha >= -15 else "Crítico")
            fila["Brecha / Tendencia"] = f"{signo}{brecha:.1f}% ({estado_b})"
        elif len(proms_mes) == 1:
            fila["Brecha / Tendencia"] = "Sin variación (1 mes)"
        else:
            fila["Brecha / Tendencia"] = "Sin datos"

        if not ejes_a.empty:
            focos = [FOCO_DESARROLLO_CRITERIO.get(r["Criterio"], r["Criterio"]) for _, r in ejes_a.head(2).iterrows()]
            fila["Foco principal de desarrollo"] = " | ".join(focos)
        else:
            fila["Foco principal de desarrollo"] = "Mantener desempeño actual."

        filas.append(fila)

    return pd.DataFrame(filas)


def render_tabla_completa_html(df_tabla):
    if df_tabla.empty:
        st.info("No hay datos para mostrar en el cuadro comparativo.")
        return
    headers_html = "".join([f"<th>{col}</th>" for col in df_tabla.columns])
    rows_html = []
    for _, r in df_tabla.iterrows():
        celdas = []
        for col in df_tabla.columns:
            if col == "Asesor":
                celdas.append(f'<td class="col-asesor">{r[col]}</td>')
            elif col == "Foco principal de desarrollo":
                celdas.append(f'<td class="col-foco">{r[col]}</td>')
            else:
                celdas.append(f"<td>{r[col]}</td>")
        rows_html.append(f"<tr>{''.join(celdas)}</tr>")
    st.markdown(
        f'<div class="tabla-comp-wrap"><table class="tabla-comp">'
        f'<thead><tr>{headers_html}</tr></thead>'
        f'<tbody>{"".join(rows_html)}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True
    )


def construir_deduccion_analitica_html(datos, contexto_label):
    if datos.empty:
        return (
            f'<div class="deduccion-box">'
            f'<div class="deduccion-titulo">Deducción final — {contexto_label}</div>'
            f'<div>No hay registros suficientes con los filtros actuales para elaborar una deducción.</div>'
            f'</div>'
        )

    prom_gral = fmt_pct(datos["Puntaje final"].mean())
    total_aud = len(datos)
    n_ases = datos["Asesor"].nunique()
    n_camp = datos["Campaña"].nunique()

    crit_df_all = construir_detalle_criterios(datos)
    ejes = resumen_ejes_criterios(crit_df_all)

    mejores_ejes = ejes.sort_values(["% Positivo_num", "Evaluaciones"], ascending=[False, False]).head(2) if not ejes.empty else pd.DataFrame()
    top_ases = (
        datos.groupby("Asesor", as_index=False)["Puntaje final"]
        .mean()
        .sort_values("Puntaje final", ascending=False)
    )
    mejor_ases_txt = ""
    if not top_ases.empty:
        mejor_ases_txt = f" Destaca <b>{formatear_nombre_recurso(top_ases.iloc[0]['Asesor'])}</b> ({fmt_pct(top_ases.iloc[0]['Puntaje final'])})."

    if not mejores_ejes.empty:
        ejes_pos_txt = " y ".join([f"<b>{r['Criterio']}</b> ({r['% Positivo']})" for _, r in mejores_ejes.iterrows()])
        buenas_energias = (
            f"<b>¡Muy buen impulso!</b> Sobre <b>{total_aud}</b> auditorías ({n_ases} asesor(es) / {n_camp} campaña(s)), "
            f"el promedio general alcanza <b>{prom_gral}</b>, con fuerte tracción positiva en {ejes_pos_txt}.{mejor_ases_txt}"
        )
    else:
        buenas_energias = (
            f"<b>¡Buen avance!</b> Se analizan <b>{total_aud}</b> auditorías con un promedio general de <b>{prom_gral}</b>.{mejor_ases_txt}"
        )

    alertas = []
    top_crit = ejes[ejes["Estado"] == "Crítico"] if not ejes.empty else pd.DataFrame()
    top_mej = ejes[ejes["Estado"] == "A mejorar"] if not ejes.empty else pd.DataFrame()
    if not top_crit.empty:
        alertas.append(f"Criterio crítico principal: <b>{top_crit.iloc[0]['Criterio']}</b> ({top_crit.iloc[0]['% Crítico']} crítico).")
    elif not top_mej.empty:
        alertas.append(f"Aspecto a reforzar: <b>{top_mej.iloc[0]['Criterio']}</b> ({top_mej.iloc[0]['% Mejora']} en mejora).")

    if len(top_ases) >= 2:
        menor_a = top_ases.iloc[-1]
        if float(menor_a["Puntaje final"]) < 70:
            alertas.append(f"Menor promedio del filtro en <b>{formatear_nombre_recurso(menor_a['Asesor'])}</b> ({fmt_pct(menor_a['Puntaje final'])}).")

    res_camp = datos.groupby("Campaña", as_index=False)["Puntaje final"].mean().sort_values("Puntaje final", ascending=False)
    if len(res_camp) >= 2:
        menor_c = res_camp.iloc[-1]
        alertas.append(f"Campaña con menor calidad en selección: <b>{menor_c['Campaña']}</b> ({fmt_pct(menor_c['Puntaje final'])}).")

    if not alertas:
        alertas.append("Sin alertas críticas de puntaje o criterio en los registros filtrados.")

    alerta_html = "Alerta: " + " | ".join(alertas)

    foco_rec = (
        top_crit.iloc[0]["Criterio"] if not top_crit.empty
        else (top_mej.iloc[0]["Criterio"] if not top_mej.empty else None)
    )
    rec_base = RECOMENDACIONES_CRITERIO.get(
        foco_rec,
        "Sostener calibración periódica, compartir buenas prácticas de los perfiles más altos y hacer seguimiento semanal."
    )
    rec_html = f"<b>Recomendación general:</b> {rec_base}"

    return (
        f'<div class="deduccion-box">'
        f'<div class="deduccion-titulo">Deducción final — {contexto_label}</div>'
        f'<div class="ded-pos">{buenas_energias}</div>'
        f'<div class="ded-alert">{alerta_html}</div>'
        f'<div class="ded-rec">{rec_html}</div>'
        f'</div>'
    )


# =====================================================
# CARGA DE DATOS
# =====================================================
try:
    df_crudo, df = leer_mediciones_crudo_y_procesado()
except Exception as error:
    st.error("No se pudieron cargar los datos desde Google Sheets.")
    st.exception(error)
    st.stop()

if df.empty:
    st.warning("Todavía no hay auditorías para mostrar.")
    st.stop()

años_disp = sorted([a for a in df["Año"].dropna().unique() if a != "Sin año"])
if "Sin año" in df["Año"].unique():
    años_disp.append("Sin año")
meses_disp = ordenar_meses(df["Mes"].dropna().unique())
if "Sin mes" in df["Mes"].unique():
    meses_disp.append("Sin mes")
camp_disp = sorted(df["Campaña"].dropna().unique())
ases_disp = sorted(df["Asesor"].dropna().unique())

# =====================================================
# MENÚ LATERAL IZQUIERDO (SOLO LAS 3 VISTAS)
# =====================================================
with st.sidebar:
    st.markdown("## Vistas")
    seccion = st.radio(
        "Seleccionar vista:",
        options=["Vista por asesor", "Vista por empresa", "Detalle por auditoria"],
        index=0,
        key="menu_lateral_vistas",
        label_visibility="collapsed"
    )

# =====================================================
# VISTA 1: VISTA POR ASESOR
# =====================================================
if seccion == "Vista por asesor":
    st.subheader("Vista por asesor")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        a_anios_sel = st.multiselect("Año", options=años_disp, default=años_disp, key="va_anio")
    with f2:
        a_meses_sel = st.multiselect("Mes", options=meses_disp, default=meses_disp, key="va_mes")
    with f3:
        a_camps_sel = st.multiselect("Campaña", options=camp_disp, default=camp_disp, key="va_camp")

    _, ases_opciones_a = filtrar_registros(
        df, a_anios_sel, a_meses_sel, a_camps_sel, ases_sel=None,
        todas_ases_disp=ases_disp
    )
    firma_a = (
        tuple(a_anios_sel or []),
        tuple(a_meses_sel or []),
        tuple(normalizar_clave_campana(c) for c in (a_camps_sel or []))
    )
    preparar_selector_asesor("va_ases", "va_firma_filtro", firma_a, ases_opciones_a)

    with f4:
        a_ases_sel = st.multiselect("Asesor", options=ases_opciones_a, key="va_ases")

    filtrado_ases, _ = filtrar_registros(
        df, a_anios_sel, a_meses_sel, a_camps_sel, ases_sel=a_ases_sel,
        todas_ases_disp=ases_disp
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Auditorías", len(filtrado_ases), delta=f"Total Sheet: {len(df)}")
    k2.metric("Calidad promedio", fmt_pct(filtrado_ases["Puntaje final"].mean()))
    k3.metric("Asesores", filtrado_ases["Asesor"].nunique(), delta=f"Total Sheet: {df['Asesor'].nunique()}")
    k4.metric("Campañas", filtrado_ases["Campaña"].nunique(), delta=f"Total Sheet: {df['Campaña'].nunique()}")

    if filtrado_ases.empty:
        st.warning("No hay auditorías para los filtros seleccionados.")
        st.stop()

    detalle_ases = construir_detalle_criterios(filtrado_ases)
    asesores_a_mostrar = sorted(filtrado_ases["Asesor"].unique())

    for idx_inicio in range(0, len(asesores_a_mostrar), 3):
        grupo = asesores_a_mostrar[idx_inicio:idx_inicio + 3]
        cols = st.columns(len(grupo))

        for col_idx, nom_asesor in enumerate(grupo):
            sub_a = filtrado_ases[filtrado_ases["Asesor"] == nom_asesor].copy()
            crit_a = detalle_ases[detalle_ases["Asesor"] == nom_asesor].copy()
            ejes_a = resumen_ejes_criterios(crit_a)

            prom_total_a = fmt_pct(sub_a["Puntaje final"].mean())
            meses_resumen = []
            for m_val in ordenar_meses(sub_a["Mes"].unique()):
                g_m = sub_a[sub_a["Mes"] == m_val]
                meses_resumen.append(f"{MESES_CORTO.get(m_val, m_val)}: {fmt_pct(g_m['Puntaje final'].mean())}")
            sub_linea = f"Prom. Total: {prom_total_a}" + (f" | {' | '.join(meses_resumen)}" if meses_resumen else "")

            pos_act = sintesis_dimension(ejes_a, "positivo", "Actitudinal")
            pos_com = sintesis_dimension(ejes_a, "positivo", "Comercial")

            crit_act = sintesis_dimension(ejes_a, "critico", "Actitudinal")
            crit_com = sintesis_dimension(ejes_a, "critico", "Comercial")

            des_act = sintesis_dimension(ejes_a, "desarrollo", "Actitudinal")
            des_com = sintesis_dimension(ejes_a, "desarrollo", "Comercial")

            fb_txt = resumen_feedback_comercial_consolidado(sub_a, ejes_a)
            nombre_card = formatear_nombre_recurso(nom_asesor)

            with cols[col_idx]:
                st.markdown(
                    f'<div class="card-compacta">'
                    f'<div class="card-titulo">{nombre_card}</div>'
                    f'<div class="card-sub">{sub_linea}</div>'
                    f'<div class="bloque-verde">'
                    f'<div class="tit-verde">VERDE (Fortalezas)</div>'
                    f'<div>• <b>Actitudinal:</b> {pos_act}</div>'
                    f'<div>• <b>Comercial:</b> {pos_com}</div>'
                    f'</div>'
                    f'<div class="bloque-rojo">'
                    f'<div class="tit-rojo">ROJO (Crítico a Trabajar)</div>'
                    f'<div>• <b>Actitudinal:</b> {crit_act}</div>'
                    f'<div>• <b>Comercial:</b> {crit_com}</div>'
                    f'</div>'
                    f'<div class="bloque-naranja">'
                    f'<div class="tit-naranja">NARANJA (En Desarrollo)</div>'
                    f'<div>• <b>Actitudinal:</b> {des_act}</div>'
                    f'<div>• <b>Comercial:</b> {des_com}</div>'
                    f'</div>'
                    f'<div class="bloque-feedback">'
                    f'<div class="tit-fb">FEEDBACK / OBSERVACIONES:</div>'
                    f'<div>{fb_txt}</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown('<div class="cuadro-comp-titulo">Cuadro comparativo de métricas y focos de desarrollo</div>', unsafe_allow_html=True)
    meses_comp = a_meses_sel if a_meses_sel else meses_disp
    cuadro_comp = construir_cuadro_comparativo(filtrado_ases, meses_comp)
    render_tabla_completa_html(cuadro_comp)

    st.markdown(construir_deduccion_analitica_html(filtrado_ases, "Vista por asesor"), unsafe_allow_html=True)

# =====================================================
# VISTA 2: VISTA POR EMPRESA
# =====================================================
elif seccion == "Vista por empresa":
    st.subheader("Vista por empresa")

    fe1, fe2, fe3 = st.columns(3)
    with fe1:
        e_anios_sel = st.multiselect("Año", options=años_disp, default=años_disp, key="ve_anio")
    with fe2:
        e_meses_sel = st.multiselect("Mes", options=meses_disp, default=meses_disp, key="ve_mes")
    with fe3:
        e_camps_sel = st.multiselect("Campaña", options=camp_disp, default=camp_disp, key="ve_camp")

    base_emp, _ = filtrar_registros(
        df, e_anios_sel, e_meses_sel, e_camps_sel, ases_sel=None,
        todas_ases_disp=ases_disp
    )

    sin_filtros_emp = (
        set(e_anios_sel) == set(años_disp)
        and set(e_meses_sel) == set(meses_disp)
        and set(e_camps_sel) == set(camp_disp)
    )
    total_aud_emp = len(df) if sin_filtros_emp else len(base_emp)

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Calidad empresa", fmt_pct(base_emp["Puntaje final"].mean()))
    e2.metric("Auditorías", total_aud_emp, delta=f"Total Sheet: {len(df)}")
    e3.metric("Campañas", base_emp["Campaña"].nunique(), delta=f"Total Sheet: {df['Campaña'].nunique()}")
    e4.metric("Asesores", base_emp["Asesor"].nunique(), delta=f"Total Sheet: {df['Asesor'].nunique()}")

    if base_emp.empty:
        st.warning("No hay registros a nivel empresa con los filtros seleccionados.")
        st.stop()

    st.markdown('<div class="matriz-emp-titulo">Matriz de calidad por mes y campaña</div>', unsafe_allow_html=True)
    render_matriz_empresa_html(base_emp)

    st.markdown("### Histórico por campaña y mes (Calidad %)")
    hist_emp_camp = base_emp[base_emp["Mes"] != "Sin mes"].groupby(["Año", "Mes", "Mes_orden", "Campaña"], as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values(["Año", "Mes_orden", "Campaña"])

    if not hist_emp_camp.empty:
        hist_emp_camp["Calidad"] = hist_emp_camp["Calidad_num"].apply(fmt_pct)
        fig_ec = px.bar(
            hist_emp_camp,
            x="Mes",
            y="Calidad_num",
            color="Campaña",
            barmode="group",
            custom_data=["Campaña", "Mes", "Calidad", "Auditorías"],
            labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"}
        )
        fig_ec.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Mes: %{customdata[1]}<br>"
                "Calidad: <b>%{customdata[2]}</b><br>"
                "Auditorías: %{customdata[3]}"
                "<extra></extra>"
            )
        )
        st.plotly_chart(
            estilo_grafico(fig_ec, "Campaña y mes — Porcentaje de calidad", "Mes", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )

    st.markdown("### Cuadro de auditorías y puntuación por campaña")
    render_cuadros_por_periodo_html(base_emp, e_camps_sel)

    st.markdown(construir_deduccion_analitica_html(base_emp, "Vista por empresa"), unsafe_allow_html=True)

# =====================================================
# VISTA 3: DETALLE POR AUDITORIA
# =====================================================
else:
    st.subheader("Detalle por auditoria")

    fd1, fd2, fd3, fd4 = st.columns(4)
    with fd1:
        d_anios_sel = st.multiselect("Año", options=años_disp, default=años_disp, key="da_anio")
    with fd2:
        d_meses_sel = st.multiselect("Mes", options=meses_disp, default=meses_disp, key="da_mes")
    with fd3:
        d_camps_sel = st.multiselect("Campaña", options=camp_disp, default=camp_disp, key="da_camp")

    _, ases_opciones_d = filtrar_registros(
        df, d_anios_sel, d_meses_sel, d_camps_sel, ases_sel=None,
        todas_ases_disp=ases_disp
    )
    firma_d = (
        tuple(d_anios_sel or []),
        tuple(d_meses_sel or []),
        tuple(normalizar_clave_campana(c) for c in (d_camps_sel or []))
    )
    preparar_selector_asesor("da_ases", "da_firma_filtro", firma_d, ases_opciones_d)

    with fd4:
        d_ases_sel = st.multiselect("Asesor", options=ases_opciones_d, key="da_ases")

    filtrado_det, _ = filtrar_registros(
        df, d_anios_sel, d_meses_sel, d_camps_sel, ases_sel=d_ases_sel,
        todas_ases_disp=ases_disp
    )

    if filtrado_det.empty:
        st.warning("No hay auditorías con los filtros seleccionados.")
        st.stop()

    columnas_detalle = [
        "Fecha", "Asesor", "Campaña", "Año", "Mes", "ID", "Tipo de gestión",
        "Tipificación", "Puntaje final", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?", "Tipificación correcta"
    ]
    detalle = filtrado_det[columnas_detalle].copy()
    detalle["Fecha_str"] = detalle["Fecha"].dt.strftime("%d/%m/%Y").fillna("Sin fecha")
    detalle["Calidad"] = detalle["Puntaje final"].apply(fmt_pct)
    detalle = detalle.sort_values("Fecha", ascending=False, na_position="last")

    mostrar_tabla(detalle[[
        "Fecha_str", "Asesor", "Campaña", "Año", "Mes", "ID", "Tipo de gestión",
        "Tipificación", "Calidad", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?", "Tipificación correcta"
    ]])

    st.markdown("### Comentarios y observaciones completos")
    con_comentarios = detalle[
        (detalle["Observaciones"] != "") | (detalle["Puntos a trabajar"] != "")
    ]
    if con_comentarios.empty:
        st.info("No hay comentarios u observaciones cargadas en las auditorías filtradas.")
    else:
        for _, fila_d in con_comentarios.iterrows():
            st.markdown(
                f'<div class="comentario-card">'
                f'<b>{formatear_nombre_recurso(fila_d["Asesor"])}</b> — {fila_d["Campaña"]} ({fila_d["Fecha_str"]} | {fila_d["Año"]} - {fila_d["Mes"]} | Calidad: {fila_d["Calidad"]})<br>'
                f'<b>Puntos a trabajar:</b> {fila_d["Puntos a trabajar"] if fila_d["Puntos a trabajar"] else "Sin registro"}<br>'
                f'<b>Observaciones:</b> {fila_d["Observaciones"] if fila_d["Observaciones"] else "Sin registro"}'
                f'</div>',
                unsafe_allow_html=True
            )

    csv = filtrado_det[columnas_detalle].to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button(
        "Descargar auditorías en CSV",
        data=csv,
        file_name="auditorias_calidad_contactel.csv",
        mime="text/csv"
    )

    st.markdown(construir_deduccion_analitica_html(filtrado_det, "Detalle por auditoria"), unsafe_allow_html=True)

# =====================================================
# DIAGNÓSTICO DE LECTURA DEL SHEET (PARA REVISAR CAMPAÑAS)
# =====================================================
with st.expander("Diagnóstico de campañas y fechas en el Sheet"):
    resumen_camp_diag = df.groupby(["Campaña", "Año", "Mes"], as_index=False).agg(
        Filas=("Asesor", "count"),
        Asesores=("Asesor", lambda s: ", ".join(sorted(set(s)))),
        Fechas_raw_muestra=("Fecha_raw", lambda s: ", ".join(sorted({x for x in s if x})[:3])),
        Mes_raw_muestra=("Mes_raw", lambda s: ", ".join(sorted({x for x in s if x})[:3]))
    ).sort_values(["Campaña", "Año", "Mes"])
    st.caption(f"Filas CSV crudas: {len(df_crudo)} | Columnas CSV crudas: {df_crudo.shape[1]} | Registros cargados desde fila 10: {len(df)}")
    st.dataframe(resumen_camp_diag, use_container_width=True, hide_index=True)

    camp_inspeccion = st.selectbox("Inspeccionar filas de una campaña en todo el Sheet:", options=camp_disp, key="diag_camp_sel")
    df_ins = df[df["Campaña_key"] == normalizar_clave_campana(camp_inspeccion)][
        ["Fecha_raw", "Año", "Mes", "Mes_raw", "Asesor", "Campaña", "Puntaje final"]
    ]
    st.dataframe(df_ins, use_container_width=True, hide_index=True)

# =====================================================
# PIE Y ACTUALIZACIÓN
# =====================================================
st.divider()
st.caption("Calidad y Capacitación | Contactel | Actualización automática cada 5 minutos.")
st.caption("La columna AC (Acción) está excluida del análisis y de las vistas.")

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
