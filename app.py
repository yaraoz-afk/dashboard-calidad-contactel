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
VERDE_SUAVE = "#eaf7ed"
GRIS_DESPLEGABLE = "#e5e7eb"
GRIS_HOVER = "#d1d5db"
ROJO_CRITICO = "#dc2626"
NARANJA_TRABAJAR = "#ea580c"

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

ORDEN_MESES = {nombre: num for num, nombre in MESES_ES.items()}

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
    border: 1px solid #b7e1c1;
    border-top: 4px solid {VERDE_PRINCIPAL};
    padding: 12px 14px;
    border-radius: 10px;
}}
div[data-testid="stMetric"] label {{
    color: #1f2937 !important;
    font-weight: 600;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: #000000 !important;
    font-weight: 700;
}}

/* Desplegables en gris con texto negro */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {{
    background-color: {GRIS_DESPLEGABLE} !important;
    color: #000000 !important;
    border: 1px solid #9ca3af !important;
    border-radius: 8px !important;
}}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="input"] input {{
    color: #000000 !important;
}}
div[data-baseweb="select"] svg {{
    fill: #000000 !important;
    color: #000000 !important;
}}

/* Etiquetas seleccionadas (tags) en verde #30b44e con texto blanco */
[data-baseweb="tag"],
[data-baseweb="tag"] > div,
[data-baseweb="tag"] > span,
span[data-baseweb="tag"],
div[data-baseweb="select"] [data-baseweb="tag"],
div[data-testid="stMultiSelect"] [data-baseweb="tag"],
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background-color: {VERDE_PRINCIPAL} !important;
    background: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border: 1px solid {VERDE_OSCURO} !important;
    border-radius: 6px !important;
}}
[data-baseweb="tag"] *,
[data-baseweb="tag"] span,
[data-baseweb="tag"] div,
[data-baseweb="tag"] svg,
[data-baseweb="tag"] path,
div[data-testid="stMultiSelect"] [data-baseweb="tag"] * {{
    background-color: transparent !important;
    color: #ffffff !important;
    fill: #ffffff !important;
    stroke: #ffffff !important;
}}

/* Menú desplegable flotante en gris */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
ul[role="listbox"] li,
div[data-baseweb="popover"] div[role="option"] {{
    background-color: {GRIS_DESPLEGABLE} !important;
    color: #000000 !important;
}}
ul[role="listbox"] li:hover,
div[data-baseweb="popover"] div[role="option"]:hover,
li[aria-selected="true"] {{
    background-color: {GRIS_HOVER} !important;
    color: #000000 !important;
}}
ul[role="listbox"] * {{
    color: #000000 !important;
}}

/* Botones en verde #30b44e */
.stButton > button,
.stDownloadButton > button {{
    background-color: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}}
.stButton > button:hover,
.stDownloadButton > button:hover {{
    background-color: {VERDE_OSCURO} !important;
    color: #ffffff !important;
}}

/* Tarjeta compacta por asesor / campaña */
.card-asesor {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top: 5px solid #1e3a8a;
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 16px;
    color: #000000;
}}
.card-asesor-titulo {{
    font-size: 16px;
    font-weight: 800;
    text-align: center;
    color: #0f172a;
    margin-bottom: 4px;
}}
.card-asesor-sub {{
    font-size: 12px;
    font-weight: 600;
    text-align: center;
    color: #334155;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
}}
.sec-verde {{
    background: #ecfdf5;
    border-left: 4px solid {VERDE_PRINCIPAL};
    padding: 8px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-size: 12.5px;
}}
.sec-rojo {{
    background: #fef2f2;
    border-left: 4px solid {ROJO_CRITICO};
    padding: 8px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-size: 12.5px;
}}
.sec-naranja {{
    background: #fff7ed;
    border-left: 4px solid {NARANJA_TRABAJAR};
    padding: 8px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-size: 12.5px;
}}
.sec-neutro {{
    background: #f8fafc;
    border-left: 4px solid #334155;
    padding: 8px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-size: 12.5px;
}}
.deduccion-box {{
    background: #ffffff;
    border: 1px solid #86efac;
    border-left: 6px solid {VERDE_OSCURO};
    border-radius: 10px;
    padding: 16px 18px;
    margin-top: 12px;
    margin-bottom: 16px;
    color: #000000;
    font-size: 13.5px;
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
.t-verde {{ color: #15803d; font-weight: 700; }}
.t-rojo {{ color: #b91c1c; font-weight: 700; }}
.t-naranja {{ color: #c2410c; font-weight: 700; }}
.t-neutro {{ color: #1e293b; font-weight: 700; }}
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


def normalizar_clave(valor):
    return limpiar_texto_etiqueta(valor).lower()


def nombre_mes_desde_valor(mes_raw, fecha_dt):
    if pd.notna(fecha_dt):
        return MESES_ES.get(int(fecha_dt.month), "Sin mes")

    texto = normalizar_clave(mes_raw)
    if not texto or texto in ("nan", "nat", "sin mes"):
        return "Sin mes"

    mapa_texto = {
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
    if texto in mapa_texto:
        return mapa_texto[texto]

    if len(texto) >= 7 and texto[4] == "-":
        parte_mes = texto[5:7]
        if parte_mes in mapa_texto:
            return mapa_texto[parte_mes]

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
def leer_mediciones():
    bruto = pd.read_csv(
        URL_MEDICION,
        header=None,
        dtype=str,
        keep_default_na=False,
        engine="python"
    )

    if bruto.shape[1] < 33:
        for _ in range(33 - bruto.shape[1]):
            bruto[bruto.shape[1]] = ""

    datos = bruto.iloc[9:, :33].copy()
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

    datos["Año"] = datos["Fecha"].dt.year.astype("Int64").astype(str).replace("<NA>", "Sin año")
    datos["Campaña_key"] = datos["Campaña"].apply(normalizar_clave)
    datos["Asesor_key"] = datos["Asesor"].apply(normalizar_clave)

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
        title=dict(text=titulo, font=dict(color="#000000", size=18)),
        font=dict(color="#000000", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#000000")),
        margin=dict(l=20, r=20, t=60, b=35),
        hoverlabel=dict(font=dict(color="#000000"))
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


def aplicar_filtros(base_df, anios_sel, meses_sel, camps_sel, ases_sel=None,
                    todos_anios=True, todos_meses=True, todas_camps=True, todos_ases=True):
    out = base_df.copy()
    if anios_sel and not todos_anios:
        out = out[out["Año"].isin(anios_sel)]
    if meses_sel and not todos_meses:
        out = out[out["Mes"].isin(meses_sel)]
    if camps_sel and not todas_camps:
        claves_c = {normalizar_clave(c) for c in camps_sel}
        out = out[out["Campaña_key"].isin(claves_c)]
    if ases_sel is not None and ases_sel and not todos_ases:
        claves_a = {normalizar_clave(a) for a in ases_sel}
        out = out[out["Asesor_key"].isin(claves_a)]
    return out


def construir_deduccion_final(datos, contexto_label):
    if datos.empty:
        return "No hay registros suficientes con los filtros actuales para elaborar una deducción."

    prom_gral = fmt_pct(datos["Puntaje final"].mean())
    total_aud = len(datos)
    crit_df_all = construir_detalle_criterios(datos)
    ejes = resumen_ejes_criterios(crit_df_all)

    top_crit = ejes[ejes["Estado"] == "Crítico"] if not ejes.empty else pd.DataFrame()
    top_mej = ejes[ejes["Estado"] == "A mejorar"] if not ejes.empty else pd.DataFrame()

    if not top_crit.empty:
        foco_crit = f"El mayor foco crítico es <b>{top_crit.iloc[0]['Criterio']}</b> ({top_crit.iloc[0]['Dimensión']})."
        accion_sug = RECOMENDACIONES_CRITERIO.get(top_crit.iloc[0]["Criterio"], "Reforzar capacitación focalizada.")
    elif not top_mej.empty:
        foco_crit = f"El principal aspecto a mejorar es <b>{top_mej.iloc[0]['Criterio']}</b> ({top_mej.iloc[0]['Dimensión']})."
        accion_sug = RECOMENDACIONES_CRITERIO.get(top_mej.iloc[0]["Criterio"], "Sostener coaching y monitoreo.")
    else:
        foco_crit = "No se detectan desvíos críticos ni puntos de mejora relevantes en el período filtrado."
        accion_sug = "Mantener el estándar actual de calidad y calibración."

    res_camp = datos.groupby("Campaña", as_index=False)["Puntaje final"].mean().sort_values("Puntaje final", ascending=False)
    if not res_camp.empty:
        mejor_c = f"{res_camp.iloc[0]['Campaña']} ({fmt_pct(res_camp.iloc[0]['Puntaje final'])})"
        menor_c = f"{res_camp.iloc[-1]['Campaña']} ({fmt_pct(res_camp.iloc[-1]['Puntaje final'])})"
        texto_camp = f"Campaña con mayor calidad: <b>{mejor_c}</b>; campaña con menor promedio: <b>{menor_c}</b>."
    else:
        texto_camp = ""

    return (
        f"<b>Deducción final ({contexto_label}):</b> Sobre <b>{total_aud}</b> auditorías analizadas, "
        f"la calidad promedio es <b>{prom_gral}</b>. {texto_camp} {foco_crit} "
        f"<b>Acción recomendada:</b> {accion_sug}"
    )


# =====================================================
# CARGA DE DATOS
# =====================================================
try:
    df = leer_mediciones()
except Exception as error:
    st.error("No se pudieron cargar los datos desde Google Sheets.")
    st.exception(error)
    st.stop()

if df.empty:
    st.warning("Todavía no hay auditorías para mostrar.")
    st.stop()

años_disp = sorted([a for a in df["Año"].dropna().unique() if a != "Sin año"])
meses_disp = ordenar_meses(df["Mes"].dropna().unique())
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
# VISTA 1: VISTA POR ASESOR (FILTROS EN PÁGINA PRINCIPAL)
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

    todos_a_camps_pre = (set(a_camps_sel) == set(camp_disp)) if camp_disp else True
    if a_camps_sel and not todos_a_camps_pre:
        claves_c_pre = {normalizar_clave(c) for c in a_camps_sel}
        ases_disp_va = sorted(df[df["Campaña_key"].isin(claves_c_pre)]["Asesor"].dropna().unique())
        if not ases_disp_va:
            ases_disp_va = ases_disp
    else:
        ases_disp_va = ases_disp

    with f4:
        a_ases_sel = st.multiselect("Asesor", options=ases_disp_va, default=ases_disp_va, key="va_ases")

    todos_a_anios = (set(a_anios_sel) == set(años_disp)) if años_disp else True
    todos_a_meses = (set(a_meses_sel) == set(meses_disp)) if meses_disp else True
    todos_a_camps = (set(a_camps_sel) == set(camp_disp)) if camp_disp else True
    todos_a_ases = (set(a_ases_sel) == set(ases_disp_va)) if ases_disp_va else True

    filtrado_ases = aplicar_filtros(
        df, a_anios_sel, a_meses_sel, a_camps_sel, a_ases_sel,
        todos_a_anios, todos_a_meses, todos_a_camps, todos_a_ases
    )

    if filtrado_ases.empty and a_camps_sel and not todos_a_camps:
        claves_c = {normalizar_clave(c) for c in a_camps_sel}
        filtrado_ases = df[df["Campaña_key"].isin(claves_c)].copy()
        if a_ases_sel and not todos_a_ases:
            claves_a = {normalizar_clave(a) for a in a_ases_sel}
            filtrado_ases = filtrado_ases[filtrado_ases["Asesor_key"].isin(claves_a)]

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
                meses_resumen.append(f"{m_val}: {fmt_pct(g_m['Puntaje final'].mean())}")
            sub_linea = f"Prom. Total: {prom_total_a}" + (f" | {' | '.join(meses_resumen)}" if meses_resumen else "")

            tot_eval = len(crit_a)
            pct_pos = fmt_pct(crit_a["Respuesta"].isin(["si", "sí", "n/a"]).sum() / tot_eval * 100) if tot_eval else "Sin datos"
            pct_mej = fmt_pct((crit_a["Respuesta"] == "punto de mejora").sum() / tot_eval * 100) if tot_eval else "Sin datos"
            pct_crit = fmt_pct((crit_a["Respuesta"] == "no").sum() / tot_eval * 100) if tot_eval else "Sin datos"

            crit_df = ejes_a[ejes_a["% Crítico_num"] > 0] if not ejes_a.empty else pd.DataFrame()
            des_df = ejes_a[ejes_a["% Mejora_num"] > 0] if not ejes_a.empty else pd.DataFrame()
            pos_df = ejes_a.sort_values("% Positivo_num", ascending=False) if not ejes_a.empty else pd.DataFrame()

            txt_pos = "<br>".join([f"• {r['Criterio']}" for _, r in pos_df.iterrows()]) if not pos_df.empty else "• Sin puntos positivos."
            txt_crit = "<br>".join([f"• {r['Criterio']}" for _, r in crit_df.iterrows()]) if not crit_df.empty else "• Sin puntos críticos."
            txt_des = "<br>".join([f"• {r['Criterio']}" for _, r in des_df.iterrows()]) if not des_df.empty else "• Sin puntos a mejorar."

            rec_asesor = (
                RECOMENDACIONES_CRITERIO.get(crit_df.iloc[0]["Criterio"], "Sostener práctica guiada.")
                if not crit_df.empty
                else (RECOMENDACIONES_CRITERIO.get(des_df.iloc[0]["Criterio"], "Reforzar consistencia.") if not des_df.empty else "Mantener desempeño actual.")
            )

            camp_hist = (
                sub_a.groupby("Campaña", as_index=False).agg(
                    Calidad=("Puntaje final", "mean"),
                    Auds=("Puntaje final", "count")
                )
                .sort_values("Auds", ascending=False)
                .assign(txt=lambda d: d["Campaña"] + " (" + d["Calidad"].apply(fmt_pct) + ")")["txt"]
                .tolist()
            )
            txt_camp = ", ".join(camp_hist) if camp_hist else "Sin campañas"

            with cols[col_idx]:
                st.markdown(
                    f'<div class="card-asesor">'
                    f'<div class="card-asesor-titulo">{nom_asesor}</div>'
                    f'<div class="card-asesor-sub">{sub_linea} | Auds: {len(sub_a)}</div>'
                    f'<div style="font-size:12px; margin-bottom:8px;">'
                    f'<b>Aspectos:</b> <span class="t-verde">Pos {pct_pos}</span> · '
                    f'<span class="t-naranja">Mej {pct_mej}</span> · '
                    f'<span class="t-rojo">Crit {pct_crit}</span>'
                    f'</div>'
                    f'<div class="sec-verde"><div class="t-verde">PUNTOS POSITIVOS</div>{txt_pos}</div>'
                    f'<div class="sec-rojo"><div class="t-rojo">PUNTOS CRÍTICOS</div>{txt_crit}</div>'
                    f'<div class="sec-naranja"><div class="t-naranja">PUNTOS A MEJORAR</div>{txt_des}</div>'
                    f'<div style="font-size:12px; margin-bottom:6px;"><b>Campañas en filtro:</b> {txt_camp}</div>'
                    f'<div style="font-size:12px;"><b>Recomendación:</b> {rec_asesor}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown(f'<div class="deduccion-box">{construir_deduccion_final(filtrado_ases, "Vista por asesor")}</div>', unsafe_allow_html=True)

# =====================================================
# VISTA 2: VISTA POR EMPRESA (FILTROS AÑO, MES, CAMPAÑA EN PÁGINA PRINCIPAL)
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

    todos_e_anios = (set(e_anios_sel) == set(años_disp)) if años_disp else True
    todos_e_meses = (set(e_meses_sel) == set(meses_disp)) if meses_disp else True
    todos_e_camps = (set(e_camps_sel) == set(camp_disp)) if camp_disp else True

    base_emp = aplicar_filtros(
        df, e_anios_sel, e_meses_sel, e_camps_sel, ases_sel=None,
        todos_anios=todos_e_anios, todos_meses=todos_e_meses, todas_camps=todos_e_camps
    )

    sin_filtros_emp = todos_e_anios and todos_e_meses and todos_e_camps
    total_aud_emp = len(df) if sin_filtros_emp else len(base_emp)

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Calidad empresa", fmt_pct(base_emp["Puntaje final"].mean()))
    e2.metric("Auditorías", total_aud_emp, delta=f"Total Sheet: {len(df)}")
    e3.metric("Campañas", base_emp["Campaña"].nunique(), delta=f"Total Sheet: {df['Campaña'].nunique()}")
    e4.metric("Asesores", base_emp["Asesor"].nunique(), delta=f"Total Sheet: {df['Asesor'].nunique()}")

    if base_emp.empty:
        st.warning("No hay registros a nivel empresa con los filtros seleccionados.")
        st.stop()

    st.markdown("### Histórico por campaña y mes (Calidad %)")
    hist_emp_camp = base_emp[base_emp["Mes"] != "Sin mes"].groupby(["Año", "Mes", "Mes_orden", "Campaña"], as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values(["Año", "Mes_orden", "Campaña"])

    if not hist_emp_camp.empty:
        hist_emp_camp["Calidad"] = hist_emp_camp["Calidad_num"].apply(fmt_pct)
        fig_ec = px.line(
            hist_emp_camp, x="Mes", y="Calidad_num", color="Campaña", markers=True,
            labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig_ec, "Campaña y mes — Porcentaje de calidad", "Mes", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )

    st.markdown("### Cuadro de auditorías por año y mes")
    cuadro_emp = base_emp[base_emp["Mes"] != "Sin mes"].groupby(["Año", "Mes", "Mes_orden"], as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values(["Año", "Mes_orden"])
    if not cuadro_emp.empty:
        cuadro_emp["Calidad"] = cuadro_emp["Calidad_num"].apply(fmt_pct)
        mostrar_tabla(cuadro_emp[["Año", "Mes", "Auditorías", "Calidad"]])
    else:
        mostrar_tabla(pd.DataFrame(columns=["Año", "Mes", "Auditorías", "Calidad"]))

    st.markdown("### Tarjetas por campaña")
    crit_emp = construir_detalle_criterios(base_emp)
    campañas_emp = sorted(base_emp["Campaña"].unique())

    for i_c in range(0, len(campañas_emp), 3):
        grupo_c = campañas_emp[i_c:i_c + 3]
        cols_c = st.columns(len(grupo_c))
        for idx_c, nom_c in enumerate(grupo_c):
            sub_c = base_emp[base_emp["Campaña"] == nom_c]
            ejes_c = resumen_ejes_criterios(crit_emp[crit_emp["Campaña"] == nom_c])

            prom_camp_sel = fmt_pct(sub_c["Puntaje final"].mean())
            crit_c = ejes_c[ejes_c["Estado"] == "Crítico"] if not ejes_c.empty else pd.DataFrame()
            mej_c = ejes_c[ejes_c["Estado"] == "A mejorar"] if not ejes_c.empty else pd.DataFrame()
            pos_c = ejes_c[ejes_c["Estado"] == "Positivo"] if not ejes_c.empty else pd.DataFrame()

            b_pos = "<br>".join([f"• {r['Criterio']}" for _, r in pos_c.iterrows()]) if not pos_c.empty else "• Sin puntos positivos."
            b_mej = "<br>".join([f"• {r['Criterio']}" for _, r in mej_c.iterrows()]) if not mej_c.empty else "• Sin puntos a mejorar."
            b_crit = "<br>".join([f"• {r['Criterio']}" for _, r in crit_c.iterrows()]) if not crit_c.empty else "• Sin puntos críticos."

            ejes_lista = []
            if not crit_c.empty:
                ejes_lista.append(f"Crítico: {crit_c.iloc[0]['Criterio']} ({crit_c.iloc[0]['Dimensión']})")
            if not mej_c.empty:
                ejes_lista.append(f"A mejorar: {mej_c.iloc[0]['Criterio']} ({mej_c.iloc[0]['Dimensión']})")
            if not pos_c.empty:
                ejes_lista.append(f"Positivo: {pos_c.iloc[0]['Criterio']} ({pos_c.iloc[0]['Dimensión']})")
            b_ejes = "<br>".join([f"• {e}" for e in ejes_lista]) if ejes_lista else "• Sin ejes definidos."

            foco_rec = (
                crit_c.iloc[0]["Criterio"] if not crit_c.empty
                else (mej_c.iloc[0]["Criterio"] if not mej_c.empty else (pos_c.iloc[0]["Criterio"] if not pos_c.empty else None))
            )
            rec_camp = RECOMENDACIONES_CRITERIO.get(foco_rec, "Mantener seguimiento continuo y coaching de calidad.") if foco_rec else "Mantener seguimiento continuo."

            with cols_c[idx_c]:
                st.markdown(
                    f'<div class="card-asesor">'
                    f'<div class="card-asesor-titulo">{nom_c}</div>'
                    f'<div class="card-asesor-sub">Promedio selección: {prom_camp_sel} | Auditorías: {len(sub_c)}</div>'
                    f'<div class="sec-verde"><div class="t-verde">PUNTOS POSITIVOS</div>{b_pos}</div>'
                    f'<div class="sec-naranja"><div class="t-naranja">PUNTOS A MEJORAR</div>{b_mej}</div>'
                    f'<div class="sec-rojo"><div class="t-rojo">PUNTOS CRÍTICOS</div>{b_crit}</div>'
                    f'<div class="sec-neutro"><div class="t-neutro">EJES DE TRABAJO</div>{b_ejes}</div>'
                    f'<div style="font-size:12px;"><b>Recomendaciones:</b> {rec_camp}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown(f'<div class="deduccion-box">{construir_deduccion_final(base_emp, "Vista por empresa")}</div>', unsafe_allow_html=True)

# =====================================================
# VISTA 3: DETALLE POR AUDITORIA (FILTROS EN PÁGINA PRINCIPAL)
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
    with fd4:
        d_ases_sel = st.multiselect("Asesor", options=ases_disp, default=ases_disp, key="da_ases")

    todos_d_anios = (set(d_anios_sel) == set(años_disp)) if años_disp else True
    todos_d_meses = (set(d_meses_sel) == set(meses_disp)) if meses_disp else True
    todos_d_camps = (set(d_camps_sel) == set(camp_disp)) if camp_disp else True
    todos_d_ases = (set(d_ases_sel) == set(ases_disp)) if ases_disp else True

    filtrado_det = aplicar_filtros(
        df, d_anios_sel, d_meses_sel, d_camps_sel, d_ases_sel,
        todos_d_anios, todos_d_meses, todos_d_camps, todos_d_ases
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
                f'<b>{fila_d["Asesor"]}</b> — {fila_d["Campaña"]} ({fila_d["Fecha_str"]} | {fila_d["Año"]} - {fila_d["Mes"]} | Calidad: {fila_d["Calidad"]})<br>'
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

    st.markdown(f'<div class="deduccion-box">{construir_deduccion_final(filtrado_det, "Detalle por auditoria")}</div>', unsafe_allow_html=True)

# =====================================================
# PIE Y ACTUALIZACIÓN
# =====================================================
st.divider()
st.caption("Calidad y Capacitación | Contactel | Actualización automática cada 5 minutos.")
st.caption("La columna AC (Acción) está excluida del análisis y de las vistas.")

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
