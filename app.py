import base64
import hmac
from pathlib import Path
import re
import streamlit as st
import streamlit.components.v1 as components
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

VERDE_PRINCIPAL = "#2e8b57"
VERDE_OSCURO = "#1f5c3b"
GRIS_DESPLEGABLE = "#f1f5f9"
GRIS_HOVER = "#e6f2ec"
ROJO_CRITICO = "#b91c1c"

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
    background-color: #f6f8f7;
    color: #0f172a;
}}
section[data-testid="stSidebar"] {{
    background-color: #eef2f0;
    border-right: 1px solid #cbd5e1;
}}
h1, h2, h3, h4, p, label, span, div, .stMarkdown {{
    color: #0f172a;
}}
h1, h2 {{
    color: #1e293b !important;
}}

/* Caja de acceso por contraseña */
.login-card {{
    max-width: 420px;
    margin: 48px auto 16px auto;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 4px solid {VERDE_PRINCIPAL};
    border-radius: 8px;
    padding: 24px 22px;
    color: #0f172a;
}}
.login-titulo {{
    font-size: 18px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 6px;
}}
.login-sub {{
    font-size: 13px;
    color: #475569;
    margin-bottom: 14px;
}}
div[data-testid="stForm"] {{
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 18px 20px !important;
}}
div[data-testid="stTextInput"] input {{
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border: 1px solid #94a3b8 !important;
    border-radius: 6px !important;
}}
div[data-testid="stTextInput"] input::placeholder {{
    color: #64748b !important;
    opacity: 1 !important;
}}

/* Títulos y textos dentro del modal (dialog) en blanco puro */
div[data-testid="stDialog"],
div[data-testid="stDialog"] > div,
div[data-testid="stDialog"] > div > div,
div[role="dialog"],
div[role="dialog"] > div,
div[role="dialog"] > div > div {{
    color: #ffffff !important;
}}

div[data-testid="stDialog"] h1,
div[data-testid="stDialog"] h2,
div[data-testid="stDialog"] h3,
div[data-testid="stDialog"] h4,
div[data-testid="stDialog"] [data-testid="stHeading"],
div[data-testid="stDialog"] [data-testid="stHeading"] *,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h1,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h3,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] h4,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] span,
div[data-testid="stDialog"] [data-testid="stCaptionContainer"],
div[data-testid="stDialog"] [data-testid="stCaptionContainer"] *,
div[role="dialog"] h1,
div[role="dialog"] h2,
div[role="dialog"] h3,
div[role="dialog"] h4,
div[role="dialog"] [data-testid="stHeading"],
div[role="dialog"] [data-testid="stHeading"] *,
div[role="dialog"] [data-testid="stMarkdownContainer"] h1,
div[role="dialog"] [data-testid="stMarkdownContainer"] h2,
div[role="dialog"] [data-testid="stMarkdownContainer"] h3,
div[role="dialog"] [data-testid="stMarkdownContainer"] h4,
div[role="dialog"] [data-testid="stMarkdownContainer"] p,
div[role="dialog"] [data-testid="stMarkdownContainer"] span,
div[role="dialog"] [data-testid="stCaptionContainer"],
div[role="dialog"] [data-testid="stCaptionContainer"] * {{
    color: #ffffff !important;
}}

/* Asegurar que el contenido interno de las tablas blancas del modal siga legible en oscuro */
div[data-testid="stDialog"] .enc-modal-wrap,
div[data-testid="stDialog"] .enc-modal-wrap *,
div[role="dialog"] .enc-modal-wrap,
div[role="dialog"] .enc-modal-wrap * {{
    color: #0f172a !important;
}}

/* Tabla legible y completa dentro del modal de encuentros con barra de scroll visible */
.enc-modal-wrap {{
    width: 100%;
    max-height: 360px;
    overflow: scroll !important;
    scrollbar-width: auto !important;
    scrollbar-color: #64748b #e2e8f0 !important;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    margin: 6px 0 12px 0;
}}
.enc-modal-wrap::-webkit-scrollbar {{
    width: 12px;
    height: 12px;
}}
.enc-modal-wrap::-webkit-scrollbar-track {{
    background: #e2e8f0;
    border-radius: 6px;
}}
.enc-modal-wrap::-webkit-scrollbar-thumb {{
    background: #64748b;
    border-radius: 6px;
    border: 2px solid #e2e8f0;
}}
table.enc-modal-tbl {{
    width: max-content;
    min-width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    color: #0f172a;
}}
table.enc-modal-tbl th {{
    position: sticky;
    top: 0;
    z-index: 2;
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.enc-modal-tbl td {{
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
    line-height: 1.4;
    color: #0f172a;
    white-space: normal;
    word-break: break-word;
}}
table.enc-modal-tbl td.col-fb-full {{
    min-width: 360px;
    max-width: 680px;
}}
table.enc-modal-tbl tr:nth-child(even) td {{
    background-color: #f8fafc;
}}

/* Logo dentro del menú de vistas (sidebar) */
.sidebar-brand-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
    padding: 8px 10px;
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
}}
.sidebar-brand-logo {{
    max-height: 54px;
    max-width: 100%;
    width: auto;
    object-fit: contain;
    display: block;
}}

/* Tarjetas de métricas */
div[data-testid="stMetric"] {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 3px solid {VERDE_PRINCIPAL};
    padding: 12px 14px;
    border-radius: 8px;
}}
div[data-testid="stMetric"] label {{
    color: #334155 !important;
    font-weight: 600;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: #0f172a !important;
    font-weight: 700;
}}

/* Caja del multiselect: visible completa, sin recortes y con 'x' y flechita contrastadas */
[data-testid="stMultiSelect"],
[data-testid="stMultiSelect"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"],
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    background-color: {GRIS_DESPLEGABLE} !important;
    color: #0f172a !important;
    border-color: #94a3b8 !important;
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
    color: #0f172a !important;
    min-width: 70px !important;
}}

/* Tags seleccionados */
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

/* Controles derechos del multiselect */
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
    color: #0f172a !important;
}}
ul[role="listbox"] > li:hover,
[role="option"]:hover,
[aria-selected="true"] {{
    background-color: {GRIS_HOVER} !important;
    color: #0f172a !important;
}}
div[data-baseweb="popover"] span,
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] p,
ul[role="listbox"] span,
ul[role="listbox"] div,
[role="option"] span,
[role="option"] div {{
    color: #0f172a !important;
}}

/* Botones generales y de formularios */
.stButton > button,
.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] > button,
button[kind="formSubmit"] {{
    background-color: {VERDE_PRINCIPAL} !important;
    background: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border: 1px solid {VERDE_OSCURO} !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}}
.stButton > button *,
.stDownloadButton > button *,
div[data-testid="stFormSubmitButton"] > button *,
button[kind="formSubmit"] * {{
    color: #ffffff !important;
    fill: #ffffff !important;
}}
.stButton > button:hover,
.stDownloadButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover,
button[kind="formSubmit"]:hover {{
    background-color: {VERDE_OSCURO} !important;
    background: {VERDE_OSCURO} !important;
    color: #ffffff !important;
}}

/* Botón compacto "Ver auditoria" / "ver detalle" dentro de cada tarjeta */
.btn-ver-aud-wrap .stButton > button {{
    min-height: 26px !important;
    height: 26px !important;
    padding: 2px 10px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    border-radius: 5px !important;
    line-height: 1.1 !important;
    margin-top: 6px !important;
}}

/* Tarjeta compacta por asesor / campaña */
.card-compacta {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 4px solid #475569;
    border-radius: 6px;
    padding: 12px 14px 10px 14px;
    margin-bottom: 12px;
    color: #0f172a;
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
    color: #475569;
    margin-bottom: 10px;
    padding-bottom: 7px;
    border-bottom: 1px solid #e2e8f0;
}}
.enc-contadores {{
    display: flex;
    justify-content: space-around;
    gap: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 6px;
    margin-bottom: 10px;
}}
.enc-cnt-item {{
    text-align: center;
    flex: 1;
}}
.enc-cnt-num {{
    font-size: 17px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
}}
.enc-cnt-lbl {{
    font-size: 11px;
    font-weight: 600;
    color: #475569;
    margin-top: 2px;
}}
.bloque-verde {{
    background: #f0fdf4;
    border-left: 3px solid {VERDE_PRINCIPAL};
    padding: 7px 9px;
    margin-bottom: 7px;
    font-size: 12px;
    line-height: 1.35;
}}
.bloque-rojo {{
    background: #fef2f2;
    border-left: 3px solid {ROJO_CRITICO};
    padding: 7px 9px;
    margin-bottom: 7px;
    font-size: 12px;
    line-height: 1.35;
}}
.bloque-naranja {{
    background: #fffbeb;
    border-left: 3px solid #d97706;
    padding: 7px 9px;
    margin-bottom: 7px;
    font-size: 12px;
    line-height: 1.35;
}}
.bloque-azul {{
    background: #eff6ff;
    border-left: 3px solid #2563eb;
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
.tit-verde {{ color: #166534; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-rojo {{ color: #991b1b; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-naranja {{ color: #92400e; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-azul {{ color: #1e40af; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}
.tit-fb {{ color: #1e293b; font-weight: 800; font-size: 11.5px; margin-bottom: 2px; }}

/* Matriz Mes x Campaña */
.matriz-emp-titulo {{
    font-size: 15px;
    font-weight: 800;
    color: #1e293b;
    margin-top: 8px;
    margin-bottom: 8px;
    text-transform: uppercase;
}}
.matriz-emp-wrap {{
    width: 100%;
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    margin-bottom: 18px;
}}
table.matriz-emp {{
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    font-size: 11.5px;
    color: #0f172a;
}}
table.matriz-emp th.th-mes {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 800;
    text-align: left;
    padding: 7px 6px;
    border: 1px solid #cbd5e1;
    width: 96px;
    white-space: nowrap;
}}
table.matriz-emp th.th-camp {{
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
    text-align: center;
    padding: 6px 4px;
    border: 1px solid #cbd5e1;
    white-space: normal;
    line-height: 1.15;
    overflow-wrap: break-word;
}}
table.matriz-emp th.th-prom {{
    background-color: #cbd5e1;
    color: #0f172a;
    font-weight: 800;
    text-align: center;
    padding: 6px 5px;
    border: 1px solid #94a3b8;
    width: 88px;
    white-space: normal;
    line-height: 1.15;
}}
table.matriz-emp td {{
    padding: 6px 4px;
    border: 1px solid #cbd5e1;
    text-align: center;
    vertical-align: middle;
    color: #0f172a;
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
    background-color: #f8fafc;
    font-weight: 800;
}}
table.matriz-emp tr.fila-total-camp td {{
    font-weight: 800;
    border-top: 2px solid #94a3b8;
}}
table.matriz-emp tr.fila-total-camp td.td-etq-total {{
    background-color: #e2e8f0;
    color: #0f172a;
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
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    margin-bottom: 18px;
}}
table.resumen-per {{
    width: max-content;
    min-width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
}}
table.resumen-per th.th-per-grupo {{
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 800;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    font-size: 13px;
    white-space: nowrap;
}}
table.resumen-per th.th-per-camp-hdr {{
    background-color: #cbd5e1;
    color: #0f172a;
    font-weight: 800;
    text-align: left;
    padding: 7px 12px;
    border: 1px solid #cbd5e1;
    min-width: 190px;
    white-space: nowrap;
}}
table.resumen-per th.th-per-col {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    min-width: 105px;
    white-space: nowrap;
    line-height: 1.15;
}}
table.resumen-per td.td-per-camp {{
    background-color: #f8fafc;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 6px 12px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.resumen-per td.td-per-q {{
    background-color: #ffffff;
    color: #0f172a;
    font-weight: 600;
    text-align: center;
    padding: 6px 10px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.resumen-per td.td-per-sin-aud {{
    background-color: #e2e8f0;
    color: #475569;
    font-weight: 600;
    text-align: center;
    padding: 6px 10px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.resumen-per td.td-per-prom {{
    background-color: #ffffff;
    color: #0f172a;
    font-weight: 600;
    text-align: center;
    padding: 6px 10px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.resumen-per tr.fila-per-total td {{
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 800;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.resumen-per tr.fila-per-total td.td-per-total-etq {{
    text-align: left;
    padding-left: 12px;
}}

/* Cuadro comparativo */
.cuadro-comp-titulo {{
    font-size: 15px;
    font-weight: 800;
    color: #1e293b;
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
    color: #0f172a;
}}
table.tabla-comp th {{
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 9px 10px;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
}}
table.tabla-comp td {{
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
    line-height: 1.35;
    color: #0f172a;
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

/* Tabla Detalle por auditoria: títulos fijos arriba + Asesor fijo a la izquierda + scroll visible */
.det-aud-wrap {{
    width: 100%;
    height: 62vh;
    min-height: 340px;
    max-height: 620px;
    overflow: scroll !important;
    scrollbar-width: auto !important;
    scrollbar-color: #64748b #e2e8f0 !important;
    background: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 6px;
    margin: 8px 0;
}}
.det-aud-wrap::-webkit-scrollbar {{
    width: 14px;
    height: 14px;
}}
.det-aud-wrap::-webkit-scrollbar-track {{
    background: #e2e8f0;
    border-radius: 6px;
}}
.det-aud-wrap::-webkit-scrollbar-thumb {{
    background: #64748b;
    border-radius: 6px;
    border: 2px solid #e2e8f0;
}}
.det-aud-wrap::-webkit-scrollbar-thumb:hover {{
    background: #475569;
}}
.det-aud-wrap::-webkit-scrollbar-corner {{
    background: #e2e8f0;
}}

table.det-aud {{
    width: max-content;
    min-width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 11.5px;
    color: #0f172a;
}}
table.det-aud th {{
    position: sticky;
    top: 0;
    z-index: 2;
    border-right: 1px solid #cbd5e1;
    border-bottom: 2px solid #94a3b8;
    border-top: 1px solid #cbd5e1;
}}
table.det-aud th.th-meta {{
    background-color: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
    text-align: center;
    padding: 8px 8px;
    white-space: nowrap;
}}
table.det-aud th.th-item {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: center;
    padding: 7px 6px;
    max-width: 130px;
    min-width: 84px;
    white-space: normal;
    line-height: 1.15;
}}
table.det-aud th.th-bloque {{
    background-color: #cbd5e1;
    color: #0f172a;
    font-weight: 800;
    text-align: center;
    padding: 7px 6px;
    min-width: 88px;
    white-space: normal;
    line-height: 1.15;
}}
table.det-aud th.th-asesor-fijo {{
    position: sticky;
    top: 0;
    left: 0;
    z-index: 4;
    background-color: #cbd5e1;
    color: #0f172a;
    font-weight: 800;
    text-align: left;
    padding: 8px 10px;
    min-width: 180px;
    white-space: nowrap;
    border-right: 2px solid #94a3b8;
    border-bottom: 2px solid #94a3b8;
}}
table.det-aud td.td-asesor-fijo {{
    position: sticky;
    left: 0;
    z-index: 1;
    background-color: #f8fafc;
    color: #0f172a;
    padding: 6px 10px;
    border-right: 2px solid #94a3b8;
    border-bottom: 1px solid #cbd5e1;
    vertical-align: top;
    font-weight: 700;
    white-space: nowrap;
}}
table.det-aud td.td-meta {{
    background-color: #ffffff;
    color: #0f172a;
    padding: 6px 8px;
    border-right: 1px solid #cbd5e1;
    border-bottom: 1px solid #cbd5e1;
    vertical-align: top;
    font-weight: 600;
    white-space: nowrap;
}}
table.det-aud td.td-tipificacion {{
    background-color: #ffffff;
    color: #0f172a;
    padding: 6px 8px;
    border-right: 1px solid #cbd5e1;
    border-bottom: 1px solid #cbd5e1;
    vertical-align: top;
    font-weight: 600;
    min-width: 135px;
    max-width: 210px;
    white-space: normal;
    line-height: 1.25;
}}
table.det-aud td.td-puntos-trabajar {{
    background-color: #ffffff;
    color: #0f172a;
    padding: 5px 7px;
    border-right: 1px solid #cbd5e1;
    border-bottom: 1px solid #cbd5e1;
    vertical-align: top;
    min-width: 120px;
    max-width: 175px;
    font-size: 11px;
    white-space: normal;
    line-height: 1.25;
}}
table.det-aud td.td-observaciones {{
    background-color: #ffffff;
    color: #0f172a;
    padding: 6px 8px;
    border-right: 1px solid #cbd5e1;
    border-bottom: 1px solid #cbd5e1;
    vertical-align: top;
    min-width: 220px;
    max-width: 320px;
    white-space: normal;
    line-height: 1.3;
}}
table.det-aud td.td-pct {{
    text-align: center;
    vertical-align: middle;
    padding: 6px 6px;
    border-right: 1px solid #cbd5e1;
    border-bottom: 1px solid #cbd5e1;
    font-weight: 700;
    color: #0f172a;
    white-space: nowrap;
}}
table.det-aud td.td-bloque {{
    background-color: #f1f5f9;
    text-align: center;
    vertical-align: middle;
    padding: 6px 6px;
    border-right: 1px solid #cbd5e1;
    border-bottom: 1px solid #cbd5e1;
    font-weight: 800;
    color: #0f172a;
    white-space: nowrap;
}}

/* Deducción final analítica */
.deduccion-box {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid {VERDE_PRINCIPAL};
    border-radius: 8px;
    padding: 16px 18px;
    margin-top: 12px;
    margin-bottom: 16px;
    color: #0f172a;
    font-size: 13px;
    line-height: 1.45;
}}
.deduccion-titulo {{
    font-size: 14.5px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 10px;
    text-transform: uppercase;
}}
.ded-pos {{
    background: #f0fdf4;
    border-left: 3px solid {VERDE_PRINCIPAL};
    padding: 8px 11px;
    border-radius: 4px;
    margin-bottom: 8px;
}}
.ded-alert {{
    background: #fef2f2;
    border-left: 3px solid {ROJO_CRITICO};
    padding: 8px 11px;
    border-radius: 4px;
    margin-bottom: 8px;
}}
.ded-rec {{
    background: #f8fafc;
    border-left: 3px solid #64748b;
    padding: 8px 11px;
    border-radius: 4px;
}}
</style>
""", unsafe_allow_html=True)


def obtener_clave_secreta():
    try:
        val = st.secrets.get("APP_PASSWORD", "")
    except Exception:
        val = ""
    return str(val).strip()


def exigir_clave_acceso():
    if st.session_state.get("acceso_autorizado") is True:
        return

    clave_esperada = obtener_clave_secreta()

    st.markdown(
        '<div class="login-card">'
        '<div class="login-titulo">Acceso restringido — Calidad y Capacitación</div>'
        '<div class="login-sub">Ingresá la clave de acceso para ver el panel.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    _, col_c, _ = st.columns([1, 1.3, 1])
    with col_c:
        if not clave_esperada:
            st.error(
                "Falta configurar `APP_PASSWORD` en Secrets (Manage app → Settings → Secrets)."
            )
            st.stop()

        with st.form("form_clave_acceso", clear_on_submit=False):
            clave_ingresada = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Escribí la contraseña"
            )
            entrar = st.form_submit_button("Ingresar", use_container_width=True)

        if entrar:
            if hmac.compare_digest(clave_ingresada.strip(), clave_esperada):
                st.session_state["acceso_autorizado"] = True
                st.session_state["asesor_popup_activo"] = None
                st.session_state["encuentro_popup_activo"] = None
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Revisá e intentá de nuevo.")

    st.stop()


exigir_clave_acceso()


def render_logo_contactel_sidebar():
    """Muestra el archivo real del logo subido al repositorio dentro del menú de vistas."""
    base_dir = Path(__file__).resolve().parent
    candidatos = [
        base_dir / "LOGO Contactel-01 (2).png",
        base_dir / "logo_contactel.png",
        base_dir / "LOGO Contactel-01.png",
        base_dir / "assets" / "LOGO Contactel-01 (2).png",
        base_dir / "assets" / "logo_contactel.png",
        base_dir / "assets" / "LOGO Contactel-01.png",
    ]
    for ruta in candidatos:
        if ruta.exists() and ruta.is_file():
            try:
                raw = ruta.read_bytes()
                b64 = base64.b64encode(raw).decode("ascii")
                st.markdown(
                    f'<div class="sidebar-brand-wrap">'
                    f'<img src="data:image/png;base64,{b64}" alt="Logo Contactel" class="sidebar-brand-logo"/>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                return
            except OSError:
                break


st.title("Calidad y Capacitación")
st.caption("Panel de seguimiento de desempeño | Contactel")

# =====================================================
# FUENTES DE DATOS
# =====================================================
URL_MEDICION = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=0&single=true&output=csv"
)

URL_TALLERES = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTg4uPACuLnySzZdV_KYogF5OeurPQmztxquAyWoyl6TVNwCKAGkKdGfe7FA8Mmlw612I3u8h9nbzkk/"
    "pub?gid=1026009010&single=true&output=csv"
)

URL_DEVOLUCIONES = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTg4uPACuLnySzZdV_KYogF5OeurPQmztxquAyWoyl6TVNwCKAGkKdGfe7FA8Mmlw612I3u8h9nbzkk/"
    "pub?gid=14680736&single=true&output=csv"
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

ESTRUCTURA_BLOQUES_PDF = [
    (
        "APERTURA",
        [
            "Genera conexión positiva y de confianza en presentación",
            "Explica motivo de llamada claramente"
        ]
    ),
    (
        "SONDEO",
        [
            "Explora necesidades reales",
            "Escucha activa"
        ]
    ),
    (
        "ARGUMENTACIÓN/PROPUESTA",
        [
            "Propuesta adaptada al cliente",
            "Explica beneficios",
            "Usa ejemplos / comparaciones",
            "No realiza monólogo",
            "Avanza hacia el cierre"
        ]
    ),
    (
        "MANEJO DE OBJECIONES",
        [
            "Identifica objeción real",
            "Maneja objeciones"
        ]
    ),
    (
        "ESTRUCTURA",
        [
            "Realiza cierres parciales",
            "Indica Valor a abonar",
            "Sin connotación de obligatoriedad",
            "Realiza de forma correcta cierres legales"
        ]
    ),
    (
        "LENGUAJE Y TONO",
        [
            "Tono natural y entusiasta",
            "Evita frases robotizadas",
            "Tuteo al cliente/Cortesía"
        ]
    )
]

DIMENSION_CRITERIO = {criterio: "Comercial" for criterio in PONDERACIONES}

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


def contar_talleres_unicos(df_t):
    """Si varios talleres ocurren el mismo día y tienen el mismo nombre, cuentan como 1."""
    if df_t is None or df_t.empty:
        return 0
    claves_unicas = set()
    for _, r in df_t.iterrows():
        f_dt = r.get("Fecha", pd.NaT)
        if pd.notna(f_dt):
            dia_key = f_dt.strftime("%Y-%m-%d")
        else:
            dia_key = normalizar_clave(r.get("Fecha_raw", "")) or "sin_fecha"

        nombre_t = (
            limpiar_texto_etiqueta(r.get("Tipo de refuerzo/taller", ""))
            or limpiar_texto_etiqueta(r.get("Tipo_encuentro", ""))
            or "taller / refuerzo"
        )
        taller_key = normalizar_clave(nombre_t)
        claves_unicas.add((dia_key, taller_key))
    return len(claves_unicas)


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
        return "#e2e8f0"
    v = float(valor)
    if v < 51.0:
        return "#fecaca"
    if v < 70.0:
        return "#fef3c7"
    return "#dcfce7"


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


def extraer_anio_seguro(fecha_dt, mes_raw, fecha_raw, anio_col_raw=""):
    if anio_col_raw:
        m_col = re.search(r"\b(202[4-9])\b", str(anio_col_raw))
        if m_col:
            return m_col.group(1)

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


def pct_item_en_fila(fila, criterio):
    resp = str(fila.get(criterio, "")).strip().lower()
    if resp in ("si", "sí", "n/a"):
        return 100.0
    if resp == "punto de mejora":
        return 50.0
    if resp == "no":
        return 0.0
    return None


def pct_bloque_en_fila(fila, criterios_bloque):
    tipo = normalizar_tipo(fila["Tipo de gestión"])
    indice = 0 if tipo == "Venta" else 1
    obtenido = 0.0
    posible = 0.0

    for crit in criterios_bloque:
        pesos = PONDERACIONES.get(crit)
        if not pesos:
            continue
        peso = pesos[indice]
        resp = str(fila.get(crit, "")).strip().lower()
        if resp not in ("si", "sí", "no", "punto de mejora", "n/a"):
            continue
        posible += peso
        if resp in ("si", "sí", "n/a"):
            obtenido += peso
        elif resp == "punto de mejora":
            obtenido += peso / 2.0

    if posible <= 0:
        vals = [pct_item_en_fila(fila, c) for c in criterios_bloque]
        vals_num = [v for v in vals if v is not None]
        return (sum(vals_num) / len(vals_num)) if vals_num else None

    return (obtenido / posible) * 100.0


@st.cache_data(ttl=120, show_spinner=False)
def construir_df_detalle_items_cached(filtrado_det):
    columnas_fijas = [
        "Asesor", "Fecha", "Campaña", "ID", "Tipificación", "Puntaje",
        "Puntos a trabajar", "Observaciones"
    ]
    registros = []
    ordenado = filtrado_det.sort_values("Fecha", ascending=False, na_position="last")

    for _, fila in ordenado.iterrows():
        fecha_str = fila["Fecha"].strftime("%d/%m/%Y") if pd.notna(fila["Fecha"]) else (fila["Fecha_raw"] or "Sin fecha")
        row_dict = {
            "Asesor": formatear_nombre_recurso(fila["Asesor"]),
            "Fecha": fecha_str,
            "Campaña": fila["Campaña"],
            "ID": fila["ID"] if fila["ID"] else "-",
            "Tipificación": fila["Tipificación"] if fila["Tipificación"] else "-",
            "Puntaje": fmt_pct_dec(fila["Puntaje final"]) if pd.notna(fila["Puntaje final"]) else "-",
            "Puntos a trabajar": fila["Puntos a trabajar"] if fila["Puntos a trabajar"] else "-",
            "Observaciones": fila["Observaciones"] if fila["Observaciones"] else "-"
        }

        for nombre_bloque, crits_bloque in ESTRUCTURA_BLOQUES_PDF:
            for crit in crits_bloque:
                val_p = pct_item_en_fila(fila, crit)
                row_dict[crit] = f"{round(val_p)}%" if val_p is not None else "-"
            val_b = pct_bloque_en_fila(fila, crits_bloque)
            row_dict[nombre_bloque] = f"{round(val_b)}%" if val_b is not None else "-"

        registros.append(row_dict)

    cols_ordenadas = list(columnas_fijas)
    for nombre_bloque, crits_bloque in ESTRUCTURA_BLOQUES_PDF:
        cols_ordenadas.extend(crits_bloque)
        cols_ordenadas.append(nombre_bloque)

    return pd.DataFrame(registros, columns=cols_ordenadas)


def construir_df_detalle_items(filtrado_det):
    return construir_df_detalle_items_cached(filtrado_det)


def render_controles_scroll_contenedor(box_id, uid):
    components.html(
        f"""
        <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px; padding:4px 0; font-family:sans-serif; font-size:12px; color:#334155;">
            <span style="font-weight:700;">Desplazar cuadro:</span>
            <button type="button" onclick="mover_{uid}('left', 360)" style="background:#ffffff; color:#0f172a; border:1px solid #94a3b8; border-radius:5px; padding:4px 10px; font-weight:600; cursor:pointer;">← Izquierda</button>
            <button type="button" onclick="mover_{uid}('right', 360)" style="background:#ffffff; color:#0f172a; border:1px solid #94a3b8; border-radius:5px; padding:4px 10px; font-weight:600; cursor:pointer;">→ Derecha</button>
            <button type="button" onclick="mover_{uid}('up', 220)" style="background:#ffffff; color:#0f172a; border:1px solid #94a3b8; border-radius:5px; padding:4px 10px; font-weight:600; cursor:pointer;">↑ Arriba</button>
            <button type="button" onclick="mover_{uid}('down', 220)" style="background:#ffffff; color:#0f172a; border:1px solid #94a3b8; border-radius:5px; padding:4px 10px; font-weight:600; cursor:pointer;">↓ Abajo</button>
            <button type="button" onclick="mover_{uid}('reset', 0)" style="background:#f1f5f9; color:#0f172a; border:1px solid #94a3b8; border-radius:5px; padding:4px 10px; font-weight:600; cursor:pointer;">Inicio</button>
        </div>
        <script>
        function mover_{uid}(dir, px) {{
            const doc = window.parent.document;
            const box = doc.getElementById("{box_id}");
            if (!box) return;
            if (dir === 'left') box.scrollLeft -= px;
            if (dir === 'right') box.scrollLeft += px;
            if (dir === 'up') box.scrollTop -= px;
            if (dir === 'down') box.scrollTop += px;
            if (dir === 'reset') {{ box.scrollLeft = 0; box.scrollTop = 0; }}
        }}
        </script>
        """,
        height=38
    )


def render_controles_scroll_auditoria():
    render_controles_scroll_contenedor("det_aud_scroll_box", "aud")


def render_detalle_auditoria_pdf_html(df_det_items):
    if df_det_items.empty:
        st.info("No hay auditorías para mostrar con los filtros seleccionados.")
        return

    meta_cols = ["Fecha", "Campaña", "ID", "Tipificación", "Puntaje", "Puntos a trabajar", "Observaciones"]
    nombres_bloques = {b for b, _ in ESTRUCTURA_BLOQUES_PDF}

    th_html = ['<th class="th-asesor-fijo">Asesor</th>']
    for col in df_det_items.columns:
        if col == "Asesor":
            continue
        if col in meta_cols:
            th_html.append(f'<th class="th-meta">{col}</th>')
        elif col in nombres_bloques:
            th_html.append(f'<th class="th-bloque">{col}</th>')
        else:
            th_html.append(f'<th class="th-item">{col}</th>')

    filas_html = []
    for _, r in df_det_items.iterrows():
        celdas = [f'<td class="td-asesor-fijo">{r["Asesor"]}</td>']
        for col in df_det_items.columns:
            if col == "Asesor":
                continue
            val = str(r[col])
            if col == "Tipificación":
                celdas.append(f'<td class="td-tipificacion">{val}</td>')
            elif col == "Puntos a trabajar":
                celdas.append(f'<td class="td-puntos-trabajar">{val}</td>')
            elif col == "Observaciones":
                celdas.append(f'<td class="td-observaciones">{val}</td>')
            elif col in meta_cols:
                celdas.append(f'<td class="td-meta">{val}</td>')
            elif col in nombres_bloques:
                celdas.append(f'<td class="td-bloque">{val}</td>')
            else:
                if val == "100%":
                    bg = "#dcfce7"
                elif val == "50%":
                    bg = "#fef9c3"
                elif val == "0%":
                    bg = "#fee2e2"
                else:
                    bg = "#f8fafc"
                celdas.append(f'<td class="td-pct" style="background-color:{bg};">{val}</td>')
        filas_html.append(f"<tr>{''.join(celdas)}</tr>")

    render_controles_scroll_auditoria()

    st.markdown(
        f'<div id="det_aud_scroll_box" class="det-aud-wrap"><table class="det-aud">'
        f'<thead><tr>{"".join(th_html)}</tr></thead>'
        f'<tbody>{"".join(filas_html)}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True
    )

    render_controles_scroll_auditoria()


def mostrar_contenido_popup_auditorias(df_recurso, nombre_recurso):
    prom_r = fmt_pct(df_recurso["Puntaje final"].mean()) if not df_recurso.empty else "Sin datos"
    st.caption(
        f"Recurso: **{nombre_recurso}** | Auditorías en filtro: **{len(df_recurso)}** | Promedio: **{prom_r}**"
    )
    if df_recurso.empty:
        st.info("No hay auditorías para este recurso con los filtros actuales.")
    else:
        df_det_r = construir_df_detalle_items(df_recurso)
        render_detalle_auditoria_pdf_html(df_det_r)
        csv_r = df_det_r.to_csv(index=False, sep=";", encoding="utf-8-sig")
        st.download_button(
            "Descargar auditorías de este recurso (CSV)",
            data=csv_r,
            file_name=f"auditorias_{normalizar_clave(nombre_recurso).replace(' ', '_')}.csv",
            mime="text/csv",
            key="dl_popup_asesor"
        )

    if st.button("Cerrar ventana", key="btn_cerrar_popup_asesor"):
        st.session_state["asesor_popup_activo"] = None
        st.rerun()


if hasattr(st, "dialog"):
    @st.dialog("Detalle de auditorías por recurso", width="large")
    def popup_auditorias_asesor(df_recurso, nombre_recurso):
        mostrar_contenido_popup_auditorias(df_recurso, nombre_recurso)
else:
    def popup_auditorias_asesor(df_recurso, nombre_recurso):
        with st.container(border=True):
            st.markdown("### Detalle de auditorías por recurso")
            mostrar_contenido_popup_auditorias(df_recurso, nombre_recurso)


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


@st.cache_data(ttl=300)
def leer_talleres():
    raw = pd.read_csv(
        URL_TALLERES,
        header=None,
        dtype=str,
        keep_default_na=False,
        engine="python"
    )
    if raw.shape[1] < 7:
        for _ in range(7 - raw.shape[1]):
            raw[raw.shape[1]] = ""

    datos = raw.iloc[2:, :7].copy()
    datos.columns = [
        "Asesor", "Fecha_raw", "Mes_raw", "Campaña",
        "Tipo de refuerzo/taller", "Feedback", "Año_raw"
    ]

    for col in datos.columns:
        datos[col] = datos[col].apply(limpiar_texto_etiqueta)

    datos = datos[
        (datos["Asesor"] != "")
        | (datos["Campaña"] != "")
        | (datos["Tipo de refuerzo/taller"] != "")
        | (datos["Feedback"] != "")
    ].copy()
    datos["Asesor"] = datos["Asesor"].replace("", "Sin asesor")
    datos["Campaña"] = datos["Campaña"].replace("", "Sin campaña")

    datos["Fecha"] = parsear_fecha_segura(datos["Fecha_raw"])
    datos["Mes"] = [
        nombre_mes_desde_valor(m_raw, f_dt)
        for m_raw, f_dt in zip(datos["Mes_raw"], datos["Fecha"])
    ]
    datos["Mes_orden"] = datos["Mes"].map(lambda m: ORDEN_MESES.get(m, 99))
    datos["Año"] = [
        extraer_anio_seguro(f_dt, m_raw, f_raw, a_raw)
        for f_dt, m_raw, f_raw, a_raw in zip(
            datos["Fecha"], datos["Mes_raw"], datos["Fecha_raw"], datos["Año_raw"]
        )
    ]
    datos["Campaña_key"] = datos["Campaña"].apply(normalizar_clave_campana)
    datos["Asesor_key"] = datos["Asesor"].apply(normalizar_clave)
    datos["Tipo_encuentro"] = datos["Tipo de refuerzo/taller"].replace("", "Taller / Refuerzo")
    datos["Archivo"] = ""
    datos["Origen"] = "Taller"
    return datos


@st.cache_data(ttl=300)
def leer_devoluciones():
    raw = pd.read_csv(
        URL_DEVOLUCIONES,
        header=None,
        dtype=str,
        keep_default_na=False,
        engine="python"
    )
    if raw.shape[1] < 8:
        for _ in range(8 - raw.shape[1]):
            raw[raw.shape[1]] = ""

    datos = raw.iloc[1:, :8].copy()
    datos.columns = [
        "Asesor", "Fecha_raw", "Mes_raw", "Campaña",
        "Tipo de encuentro", "Archivo", "Feedback", "Año_raw"
    ]

    for col in datos.columns:
        datos[col] = datos[col].apply(limpiar_texto_etiqueta)

    datos = datos[
        (datos["Asesor"] != "")
        | (datos["Campaña"] != "")
        | (datos["Tipo de encuentro"] != "")
        | (datos["Feedback"] != "")
        | (datos["Archivo"] != "")
    ].copy()
    datos["Asesor"] = datos["Asesor"].replace("", "Sin asesor")
    datos["Campaña"] = datos["Campaña"].replace("", "Sin campaña")

    datos["Fecha"] = parsear_fecha_segura(datos["Fecha_raw"])
    datos["Mes"] = [
        nombre_mes_desde_valor(m_raw, f_dt)
        for m_raw, f_dt in zip(datos["Mes_raw"], datos["Fecha"])
    ]
    datos["Mes_orden"] = datos["Mes"].map(lambda m: ORDEN_MESES.get(m, 99))
    datos["Año"] = [
        extraer_anio_seguro(f_dt, m_raw, f_raw, a_raw)
        for f_dt, m_raw, f_raw, a_raw in zip(
            datos["Fecha"], datos["Mes_raw"], datos["Fecha_raw"], datos["Año_raw"]
        )
    ]
    datos["Campaña_key"] = datos["Campaña"].apply(normalizar_clave_campana)
    datos["Asesor_key"] = datos["Asesor"].apply(normalizar_clave)
    datos["Tipo_encuentro"] = datos["Tipo de encuentro"].replace("", "Devolución")
    datos["Origen"] = "Devolución"
    return datos


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
        title=dict(text=titulo, font=dict(color="#0f172a", size=18)),
        font=dict(color="#0f172a", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#0f172a")),
        margin=dict(l=20, r=20, t=60, b=35),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#64748b",
            font=dict(color="#0f172a", size=12)
        )
    )
    fig.update_xaxes(
        title_text=eje_x,
        color="#0f172a",
        title_font=dict(color="#0f172a"),
        tickfont=dict(color="#0f172a"),
        gridcolor="#e2e8f0"
    )
    fig.update_yaxes(
        title_text=eje_y,
        color="#0f172a",
        title_font=dict(color="#0f172a"),
        tickfont=dict(color="#0f172a"),
        gridcolor="#e2e8f0",
        ticksuffix="%" if es_porcentaje_y else ""
    )
    return fig


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
                celdas.append('<td style="background-color:#e2e8f0;"></td>')

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
            celdas_total.append('<td style="background-color:#e2e8f0;">-</td>')
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
            if q_c > 0:
                prom_c = sub_c["Puntaje final"].mean()
                prom_txt = fmt_pct(prom_c) if pd.notna(prom_c) else ""
                celdas.append(f'<td class="td-per-q">{q_c}</td>')
                celdas.append(f'<td class="td-per-prom">{prom_txt}</td>')
            else:
                celdas.append('<td class="td-per-sin-aud"></td>')
                celdas.append('<td class="td-per-prom"></td>')
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


def sintesis_comercial(ejes_df, modo):
    if ejes_df.empty:
        return "Sin registro suficiente."

    if modo == "positivo":
        elegidos = ejes_df.sort_values(["% Positivo_num", "Evaluaciones"], ascending=[False, False]).head(2)
        if elegidos.empty:
            return "Sin fortalezas registradas."
    elif modo == "critico":
        elegidos = ejes_df[ejes_df["Criticos"] > 0].sort_values(["% Crítico_num", "Descuento"], ascending=[False, False]).head(2)
        if elegidos.empty:
            return "Sin desvíos críticos registrados."
    else:
        elegidos = ejes_df[ejes_df["Mejoras"] > 0].sort_values(["% Mejora_num", "Descuento"], ascending=[False, False]).head(2)
        if elegidos.empty:
            return "Sin puntos de mejora registrados."

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


def analizar_feedback_encuentros(df_t_a, df_d_a):
    """Genera deducciones separadas en lo comercial y en lo actitudinal a partir de feedbacks y tipos."""
    partes_fb = []
    if not df_t_a.empty:
        for _, r in df_t_a.iterrows():
            fb = limpiar_texto_etiqueta(r.get("Feedback", ""))
            tp = limpiar_texto_etiqueta(r.get("Tipo_encuentro", ""))
            if fb:
                partes_fb.append(f"{tp}: {fb}" if tp else fb)
    if not df_d_a.empty:
        for _, r in df_d_a.iterrows():
            fb = limpiar_texto_etiqueta(r.get("Feedback", ""))
            tp = limpiar_texto_etiqueta(r.get("Tipo_encuentro", ""))
            if fb:
                partes_fb.append(f"{tp}: {fb}" if tp else fb)

    if not partes_fb:
        return (
            "Sin comentarios de feedback cargados en el período seleccionado para evaluar técnica comercial.",
            "Sin registros suficientes en feedback para valorar actitud, apertura o adherencia."
        )

    texto_full = " | ".join(partes_fb)
    low = texto_full.lower()

    ejes_com = []
    if any(k in low for k in ["objec", "rechaz", "no le interesa", "caro", "precio", "cuota", "descuento"]):
        ejes_com.append("manejo de objeciones y defensa de valor")
    if any(k in low for k in ["cierre", "cerrar", "oferta", "propuesta", "beneficio", "cobertura", "plan"]):
        ejes_com.append("argumentación de la propuesta y avance al cierre")
    if any(k in low for k in ["sondeo", "pregunta", "necesidad", "indag", "escuch", "interrump"]):
        ejes_com.append("sondeo inicial y escucha activa")
    if any(k in low for k in ["legal", "valor a abonar", "obligator", "informar", "dato", "tipific"]):
        ejes_com.append("precisión en la información y cierre formal")

    rescate_com = partes_fb[-1]
    if len(rescate_com) > 150:
        rescate_com = rescate_com[:147].rstrip() + "..."

    if ejes_com:
        ded_comercial = (
            f"Foco en <b>{', '.join(ejes_com[:2])}</b>. "
            f"Último registro: <i>“{rescate_com}”</i>."
        )
    else:
        ded_comercial = (
            f"Seguimiento técnico sobre los encuentros registrados. "
            f"Último registro: <i>“{rescate_com}”</i>."
        )

    senales_pos = [
        "predisp", "receptiv", "actitud", "comprom", "particip", "buena onda",
        "atent", "proactiv", "mejora", "avanza", "motiv", "interés", "interes", "colabor"
    ]
    senales_alerta = [
        "a la defensiva", "defensiv", "desgano", "desgan", "poca participación", "poca participacion",
        "no participa", "rígid", "rigid", "apático", "apatic", "dispers", "monóton", "monoton",
        "cuesta", "resist", "duda", "nervios", "insegur"
    ]

    tiene_pos = any(k in low for k in senales_pos)
    tiene_alert = any(k in low for k in senales_alerta)

    if tiene_pos and not tiene_alert:
        ded_actitudinal = (
            "Actitud <b>receptiva y participativa</b> en los espacios de capacitación/devolución, "
            "mostrando disposición para tomar los lineamientos y aplicarlos."
        )
    elif tiene_alert and not tiene_pos:
        ded_actitudinal = (
            "Se perciben señales de <b>tensión, rigidez o cautela</b> en el intercambio; "
            "conviene acompañar con devoluciones cercanas, claras y orientadas a la práctica."
        )
    elif tiene_pos and tiene_alert:
        ded_actitudinal = (
            "Actitud con <b>matices según el momento</b>: muestra apertura en ciertos tramos, "
            "pero requiere mayor soltura y confianza sostenida frente a los desvíos."
        )
    else:
        ded_actitudinal = (
            "Sin marcas explícitas de actitud en el texto del feedback; se sugiere observar "
            "apertura al intercambio, nivel de participación y receptividad en el próximo encuentro."
        )

    return ded_comercial, ded_actitudinal


def render_tabla_encuentros_completa(df_sub, columnas_cfg, box_id, uid):
    """Renderiza una tabla HTML con barra de navegación y feedback completo sin truncar."""
    ths = "".join([f"<th>{etq}</th>" for _, etq in columnas_cfg])
    trs = []
    for _, r in df_sub.iterrows():
        tds = []
        for campo, etq in columnas_cfg:
            val = limpiar_texto_etiqueta(r.get(campo, "")) or "-"
            clase = ' class="col-fb-full"' if campo == "Feedback" else ""
            tds.append(f"<td{clase}>{val}</td>")
        trs.append(f"<tr>{''.join(tds)}</tr>")

    render_controles_scroll_contenedor(box_id, uid)
    st.markdown(
        f'<div id="{box_id}" class="enc-modal-wrap"><table class="enc-modal-tbl">'
        f'<thead><tr>{ths}</tr></thead>'
        f'<tbody>{"".join(trs)}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True
    )
    render_controles_scroll_contenedor(box_id, f"{uid}_bot")


def mostrar_contenido_popup_encuentros(df_t_a, df_d_a, nombre_recurso):
    q_t_unicos = contar_talleres_unicos(df_t_a)
    st.caption(
        f"Recurso: **{nombre_recurso}** | Talleres: **{q_t_unicos}** | Devoluciones: **{len(df_d_a)}**"
    )

    st.markdown("### Talleres / Refuerzos")
    if df_t_a.empty:
        st.info("No hay talleres registrados para este asesor con los filtros actuales.")
    else:
        t_ord = df_t_a.sort_values("Fecha", ascending=False, na_position="last").copy()
        t_ord["Fecha_fmt"] = [
            f_dt.strftime("%d/%m/%Y") if pd.notna(f_dt) else (f_raw or "-")
            for f_dt, f_raw in zip(t_ord["Fecha"], t_ord["Fecha_raw"])
        ]
        render_tabla_encuentros_completa(
            t_ord,
            [
                ("Fecha_fmt", "Fecha"),
                ("Campaña", "Campaña"),
                ("Tipo de refuerzo/taller", "Tipo de taller"),
                ("Feedback", "Feedback"),
            ],
            box_id="enc_talleres_scroll_box",
            uid="enc_t"
        )

    st.markdown("### Devoluciones")
    if df_d_a.empty:
        st.info("No hay devoluciones registradas para este asesor con los filtros actuales.")
    else:
        d_ord = df_d_a.sort_values("Fecha", ascending=False, na_position="last").copy()
        d_ord["Fecha_fmt"] = [
            f_dt.strftime("%d/%m/%Y") if pd.notna(f_dt) else (f_raw or "-")
            for f_dt, f_raw in zip(d_ord["Fecha"], d_ord["Fecha_raw"])
        ]
        render_tabla_encuentros_completa(
            d_ord,
            [
                ("Fecha_fmt", "Fecha"),
                ("Campaña", "Campaña"),
                ("Tipo de encuentro", "Tipo de encuentro"),
                ("Archivo", "Archivo"),
                ("Feedback", "Feedback"),
            ],
            box_id="enc_devoluciones_scroll_box",
            uid="enc_d"
        )

    if st.button("Cerrar ventana", key="btn_cerrar_popup_encuentros"):
        st.session_state["encuentro_popup_activo"] = None
        st.rerun()


if hasattr(st, "dialog"):
    @st.dialog("Detalle de encuentros por asesor", width="large")
    def popup_encuentros_asesor(df_t_a, df_d_a, nombre_recurso):
        mostrar_contenido_popup_encuentros(df_t_a, df_d_a, nombre_recurso)
else:
    def popup_encuentros_asesor(df_t_a, df_d_a, nombre_recurso):
        with st.container(border=True):
            st.markdown("### Detalle de encuentros por asesor")
            mostrar_contenido_popup_encuentros(df_t_a, df_d_a, nombre_recurso)


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


def construir_deduccion_encuentros_html(df_t_f, df_d_f):
    n_t = contar_talleres_unicos(df_t_f)
    n_d = len(df_d_f)
    total_enc = n_t + n_d
    if total_enc == 0:
        return (
            '<div class="deduccion-box">'
            '<div class="deduccion-titulo">Deducción final — Encuentros</div>'
            '<div>No hay talleres ni devoluciones con los filtros seleccionados.</div>'
            '</div>'
        )

    ases_unicos = {
        normalizar_clave(a)
        for a in list(df_t_f["Asesor"]) + list(df_d_f["Asesor"])
        if limpiar_texto_etiqueta(a)
    }
    fb_todos = [
        limpiar_texto_etiqueta(x)
        for x in list(df_t_f.get("Feedback", [])) + list(df_d_f.get("Feedback", []))
        if limpiar_texto_etiqueta(x)
    ]

    pos_html = (
        f"Se registran <b>{total_enc}</b> encuentros en el filtro "
        f"(<b>{n_t}</b> talleres/refuerzos y <b>{n_d}</b> devoluciones) alcanzando a "
        f"<b>{len(ases_unicos)}</b> asesor(es), con <b>{len(fb_todos)}</b> feedback(s) cargados."
    )

    low_all = " ".join(fb_todos).lower()
    alertas = []
    if n_d > n_t * 2 and n_d >= 3:
        alertas.append("El volumen de devoluciones supera ampliamente al de talleres; conviene revisar si hay desvíos recurrentes en piso.")
    if any(k in low_all for k in ["objec", "cierre", "sondeo", "escuch", "beneficio"]):
        alertas.append("En los feedbacks aparece recurrencia en aspectos comerciales (sondeo, escucha, objeciones o cierre).")
    if any(k in low_all for k in ["defensiv", "desgano", "rígid", "rigid", "duda", "nervios"]):
        alertas.append("Existen menciones actitudinales a cuidar en el seguimiento individual.")
    if not alertas:
        alertas.append("Sin alertas críticas de volumen o tono en los feedbacks del filtro actual.")

    rec_html = (
        "<b>Recomendación general:</b> Cruzar los hallazgos de talleres y devoluciones con los puntajes de auditoría "
        "para priorizar refuerzos focalizados y verificar su impacto en las siguientes llamadas."
    )

    return (
        '<div class="deduccion-box">'
        '<div class="deduccion-titulo">Deducción final — Encuentros</div>'
        f'<div class="ded-pos">{pos_html}</div>'
        f'<div class="ded-alert">Alerta: {" | ".join(alertas)}</div>'
        f'<div class="ded-rec">{rec_html}</div>'
        '</div>'
    )


# =====================================================
# CARGA DE DATOS
# =====================================================
try:
    _, df = leer_mediciones_crudo_y_procesado()
    df_talleres = leer_talleres()
    df_devoluciones = leer_devoluciones()
except Exception as error:
    st.error("No se pudieron cargar los datos desde Google Sheets.")
    st.exception(error)
    st.stop()

if df.empty and df_talleres.empty and df_devoluciones.empty:
    st.warning("Todavía no hay información para mostrar.")
    st.stop()

base_filtros = df if not df.empty else pd.concat([df_talleres, df_devoluciones], ignore_index=True)

años_disp = sorted([a for a in base_filtros["Año"].dropna().unique() if a != "Sin año"])
if "Sin año" in base_filtros["Año"].unique():
    años_disp.append("Sin año")
meses_disp = ordenar_meses(base_filtros["Mes"].dropna().unique())
if "Sin mes" in base_filtros["Mes"].unique():
    meses_disp.append("Sin mes")
camp_disp = sorted(base_filtros["Campaña"].dropna().unique())
ases_disp = sorted(base_filtros["Asesor"].dropna().unique())

# =====================================================
# MENÚ LATERAL IZQUIERDO (CON LOGO EN EL MENÚ DE VISTAS)
# =====================================================
with st.sidebar:
    render_logo_contactel_sidebar()
    st.markdown("## Vistas")
    seccion = st.radio(
        "Seleccionar vista:",
        options=[
            "Vista por asesor",
            "Detalle por auditoria",
            "Vista por empresa",
            "Encuentros"
        ],
        index=0,
        key="menu_lateral_vistas",
        label_visibility="collapsed"
    )
    st.divider()
    if st.button("Cerrar sesión", key="btn_cerrar_sesion_sidebar"):
        st.session_state["acceso_autorizado"] = False
        st.session_state["asesor_popup_activo"] = None
        st.session_state["encuentro_popup_activo"] = None
        st.rerun()

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

            fortalezas_txt = sintesis_comercial(ejes_a, "positivo")
            mejoras_txt = sintesis_comercial(ejes_a, "desarrollo")
            criticos_txt = sintesis_comercial(ejes_a, "critico")

            fb_txt = resumen_feedback_comercial_consolidado(sub_a, ejes_a)
            nombre_card = formatear_nombre_recurso(nom_asesor)

            with cols[col_idx]:
                st.markdown(
                    f'<div class="card-compacta">'
                    f'<div class="card-titulo">{nombre_card}</div>'
                    f'<div class="card-sub">{sub_linea}</div>'
                    f'<div class="bloque-verde">'
                    f'<div class="tit-verde">Fortalezas</div>'
                    f'<div>{fortalezas_txt}</div>'
                    f'</div>'
                    f'<div class="bloque-naranja">'
                    f'<div class="tit-naranja">Puntos de mejora</div>'
                    f'<div>{mejoras_txt}</div>'
                    f'</div>'
                    f'<div class="bloque-rojo">'
                    f'<div class="tit-rojo">Críticos</div>'
                    f'<div>{criticos_txt}</div>'
                    f'</div>'
                    f'<div class="bloque-feedback">'
                    f'<div class="tit-fb">FEEDBACK / OBSERVACIONES:</div>'
                    f'<div>{fb_txt}</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                _, col_btn_c, _ = st.columns([2, 2.2, 2])
                with col_btn_c:
                    st.markdown('<div class="btn-ver-aud-wrap">', unsafe_allow_html=True)
                    if st.button("Ver auditoria", key=f"btn_ver_aud_{idx_inicio}_{col_idx}", use_container_width=True):
                        st.session_state["asesor_popup_activo"] = nom_asesor
                    st.markdown('</div>', unsafe_allow_html=True)

    asesor_popup = st.session_state.get("asesor_popup_activo")
    if asesor_popup and asesor_popup in asesores_a_mostrar:
        df_pop = filtrado_ases[filtrado_ases["Asesor"] == asesor_popup].copy()
        popup_auditorias_asesor(df_pop, formatear_nombre_recurso(asesor_popup))

    st.markdown('<div class="cuadro-comp-titulo">Cuadro comparativo de métricas y focos de desarrollo</div>', unsafe_allow_html=True)
    meses_comp = a_meses_sel if a_meses_sel else meses_disp
    cuadro_comp = construir_cuadro_comparativo(filtrado_ases, meses_comp)
    render_tabla_completa_html(cuadro_comp)

    st.markdown(construir_deduccion_analitica_html(filtrado_ases, "Vista por asesor"), unsafe_allow_html=True)

# =====================================================
# VISTA 2: DETALLE POR AUDITORIA
# =====================================================
elif seccion == "Detalle por auditoria":
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

    df_det_items = construir_df_detalle_items(filtrado_det)
    render_detalle_auditoria_pdf_html(df_det_items)

    csv = df_det_items.to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button(
        "Descargar detalle por auditoría en CSV",
        data=csv,
        file_name="detalle_por_auditoria_contactel.csv",
        mime="text/csv"
    )

    st.markdown(construir_deduccion_analitica_html(filtrado_det, "Detalle por auditoria"), unsafe_allow_html=True)

# =====================================================
# VISTA 3: VISTA POR EMPRESA
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
# VISTA 4: ENCUENTROS (TALLERES + DEVOLUCIONES)
# =====================================================
else:
    st.subheader("Encuentros")

    enc_años = sorted(
        list(set(años_disp) | set(df_talleres["Año"].dropna().unique()) | set(df_devoluciones["Año"].dropna().unique()))
    )
    if "Sin año" in enc_años:
        enc_años.remove("Sin año")
        enc_años.append("Sin año")

    enc_meses = ordenar_meses(
        list(meses_disp) + list(df_talleres["Mes"].dropna().unique()) + list(df_devoluciones["Mes"].dropna().unique())
    )
    if "Sin mes" in list(df_talleres["Mes"].unique()) + list(df_devoluciones["Mes"].unique()):
        enc_meses.append("Sin mes")

    enc_camps = sorted(
        list(set(camp_disp) | set(df_talleres["Campaña"].dropna().unique()) | set(df_devoluciones["Campaña"].dropna().unique()))
    )
    enc_ases_disp = sorted(
        list(set(ases_disp) | set(df_talleres["Asesor"].dropna().unique()) | set(df_devoluciones["Asesor"].dropna().unique()))
    )

    fe_1, fe_2, fe_3, fe_4 = st.columns(4)
    with fe_1:
        en_anios_sel = st.multiselect("Año", options=enc_años, default=enc_años, key="en_anio")
    with fe_2:
        en_meses_sel = st.multiselect("Mes", options=enc_meses, default=enc_meses, key="en_mes")
    with fe_3:
        en_camps_sel = st.multiselect("Campaña", options=enc_camps, default=enc_camps, key="en_camp")

    _, ases_op_t = filtrar_registros(
        df_talleres, en_anios_sel, en_meses_sel, en_camps_sel, ases_sel=None,
        todas_ases_disp=enc_ases_disp
    )
    _, ases_op_d = filtrar_registros(
        df_devoluciones, en_anios_sel, en_meses_sel, en_camps_sel, ases_sel=None,
        todas_ases_disp=enc_ases_disp
    )
    ases_opciones_en = sorted(set(ases_op_t) | set(ases_op_d))
    if not ases_opciones_en:
        ases_opciones_en = list(enc_ases_disp)

    firma_en = (
        tuple(en_anios_sel or []),
        tuple(en_meses_sel or []),
        tuple(normalizar_clave_campana(c) for c in (en_camps_sel or []))
    )
    preparar_selector_asesor("en_ases", "en_firma_filtro", firma_en, ases_opciones_en)

    with fe_4:
        en_ases_sel = st.multiselect("Asesor", options=ases_opciones_en, key="en_ases")

    filt_t, _ = filtrar_registros(
        df_talleres, en_anios_sel, en_meses_sel, en_camps_sel, ases_sel=en_ases_sel,
        todas_ases_disp=enc_ases_disp
    )
    filt_d, _ = filtrar_registros(
        df_devoluciones, en_anios_sel, en_meses_sel, en_camps_sel, ases_sel=en_ases_sel,
        todas_ases_disp=enc_ases_disp
    )

    q_t_filt = contar_talleres_unicos(filt_t)
    q_t_sheet = contar_talleres_unicos(df_talleres)
    q_d_filt = len(filt_d)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Talleres", q_t_filt, delta=f"Total Sheet: {q_t_sheet}")
    m2.metric("Devoluciones", q_d_filt, delta=f"Total Sheet: {len(df_devoluciones)}")
    m3.metric("Total encuentros", q_t_filt + q_d_filt)
    ases_en_filtro = sorted(set(filt_t["Asesor"].unique()) | set(filt_d["Asesor"].unique()))
    m4.metric("Asesores con encuentros", len(ases_en_filtro))

    if not ases_en_filtro and filt_t.empty and filt_d.empty:
        st.warning("No hay talleres ni devoluciones para los filtros seleccionados.")
        st.markdown(construir_deduccion_encuentros_html(filt_t, filt_d), unsafe_allow_html=True)
        st.stop()

    filtro_asesor_acotado = bool(en_ases_sel) and (set(en_ases_sel) != set(ases_opciones_en))

    modo_card = st.radio(
        "Mostrar tarjetas por:",
        options=["Campaña", "Asesor"],
        index=1 if filtro_asesor_acotado else 0,
        horizontal=True,
        key="en_modo_tarjeta"
    )

    if modo_card == "Campaña":
        camps_en_filtro = sorted(set(filt_t["Campaña"].unique()) | set(filt_d["Campaña"].unique()))
        for idx_inicio in range(0, len(camps_en_filtro), 3):
            grupo = camps_en_filtro[idx_inicio:idx_inicio + 3]
            cols = st.columns(len(grupo))

            for col_idx, nom_camp in enumerate(grupo):
                clave_c = normalizar_clave_campana(nom_camp)
                sub_t_c = filt_t[filt_t["Campaña_key"] == clave_c].copy()
                sub_d_c = filt_d[filt_d["Campaña_key"] == clave_c].copy()

                q_ases = len(set(sub_t_c["Asesor_key"]) | set(sub_d_c["Asesor_key"]))
                q_t_c = contar_talleres_unicos(sub_t_c)
                q_d_c = len(sub_d_c)
                ded_com_c, ded_act_c = analizar_feedback_encuentros(sub_t_c, sub_d_c)

                with cols[col_idx]:
                    st.markdown(
                        f'<div class="card-compacta">'
                        f'<div class="card-titulo">{nom_camp}</div>'
                        f'<div class="card-sub">Asesores: <b>{q_ases}</b></div>'
                        f'<div class="enc-contadores">'
                        f'<div class="enc-cnt-item"><div class="enc-cnt-num">{q_t_c}</div><div class="enc-cnt-lbl">Talleres</div></div>'
                        f'<div class="enc-cnt-item"><div class="enc-cnt-num">{q_d_c}</div><div class="enc-cnt-lbl">Devoluciones</div></div>'
                        f'<div class="enc-cnt-item"><div class="enc-cnt-num">{q_t_c + q_d_c}</div><div class="enc-cnt-lbl">Total</div></div>'
                        f'</div>'
                        f'<div class="bloque-azul">'
                        f'<div class="tit-azul">Análisis comercial</div>'
                        f'<div>{ded_com_c}</div>'
                        f'</div>'
                        f'<div class="bloque-verde">'
                        f'<div class="tit-verde">Análisis actitudinal</div>'
                        f'<div>{ded_act_c}</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
    else:
        for idx_inicio in range(0, len(ases_en_filtro), 3):
            grupo = ases_en_filtro[idx_inicio:idx_inicio + 3]
            cols = st.columns(len(grupo))

            for col_idx, nom_asesor in enumerate(grupo):
                clave_a = normalizar_clave(nom_asesor)
                sub_t = filt_t[filt_t["Asesor_key"] == clave_a].copy()
                sub_d = filt_d[filt_d["Asesor_key"] == clave_a].copy()

                q_t = contar_talleres_unicos(sub_t)
                q_d = len(sub_d)
                ded_com, ded_act = analizar_feedback_encuentros(sub_t, sub_d)

                camps_a = sorted(set(sub_t["Campaña"].unique()) | set(sub_d["Campaña"].unique()))
                sub_camp = " | ".join(camps_a) if camps_a else "Sin campaña"

                with cols[col_idx]:
                    st.markdown(
                        f'<div class="card-compacta">'
                        f'<div class="card-titulo">{formatear_nombre_recurso(nom_asesor)}</div>'
                        f'<div class="card-sub">{sub_camp}</div>'
                        f'<div class="enc-contadores">'
                        f'<div class="enc-cnt-item"><div class="enc-cnt-num">{q_t}</div><div class="enc-cnt-lbl">Talleres</div></div>'
                        f'<div class="enc-cnt-item"><div class="enc-cnt-num">{q_d}</div><div class="enc-cnt-lbl">Devoluciones</div></div>'
                        f'<div class="enc-cnt-item"><div class="enc-cnt-num">{q_t + q_d}</div><div class="enc-cnt-lbl">Total</div></div>'
                        f'</div>'
                        f'<div class="bloque-azul">'
                        f'<div class="tit-azul">Análisis comercial</div>'
                        f'<div>{ded_com}</div>'
                        f'</div>'
                        f'<div class="bloque-verde">'
                        f'<div class="tit-verde">Análisis actitudinal</div>'
                        f'<div>{ded_act}</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    _, col_btn_c, _ = st.columns([2, 2.2, 2])
                    with col_btn_c:
                        st.markdown('<div class="btn-ver-aud-wrap">', unsafe_allow_html=True)
                        if st.button("ver detalle", key=f"btn_ver_enc_{idx_inicio}_{col_idx}", use_container_width=True):
                            st.session_state["encuentro_popup_activo"] = nom_asesor
                        st.markdown('</div>', unsafe_allow_html=True)

        enc_popup = st.session_state.get("encuentro_popup_activo")
        if enc_popup and enc_popup in ases_en_filtro:
            clave_pop = normalizar_clave(enc_popup)
            popup_encuentros_asesor(
                filt_t[filt_t["Asesor_key"] == clave_pop].copy(),
                filt_d[filt_d["Asesor_key"] == clave_pop].copy(),
                formatear_nombre_recurso(enc_popup)
            )

    st.markdown(construir_deduccion_encuentros_html(filt_t, filt_d), unsafe_allow_html=True)

# =====================================================
# PIE Y ACTUALIZACIÓN
# =====================================================
st.divider()
st.caption("Calidad y Capacitación | Contactel | Actualización automática cada 5 minutos.")
st.caption("La columna AC (Acción) está excluida del análisis y de las vistas.")

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
