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

st.markdown(f"""
<style>
.stApp {{
    background-color: #f4f9f5;
    color: #000000;
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
    padding: 14px;
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

/* Desplegables (Selectbox, Multiselect, DateInput) en gris con texto negro */
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

/* Tags seleccionados dentro del multiselect en verde #30b44e */
[data-baseweb="tag"],
[data-baseweb="tag"] > div,
span[data-baseweb="tag"],
div[data-baseweb="select"] [data-baseweb="tag"],
div[data-testid="stMultiSelect"] [data-baseweb="tag"] {{
    background-color: {VERDE_PRINCIPAL} !important;
    background: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border: 1px solid {VERDE_OSCURO} !important;
    border-radius: 6px !important;
}}
[data-baseweb="tag"] span,
[data-baseweb="tag"] svg,
[data-baseweb="tag"] *,
div[data-testid="stMultiSelect"] [data-baseweb="tag"] * {{
    color: #ffffff !important;
    fill: #ffffff !important;
}}

/* Menú desplegable flotante (popover / listbox) en gris y opciones en negro */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
ul[role="listbox"] li,
div[role="option"] {{
    background-color: {GRIS_DESPLEGABLE} !important;
    color: #000000 !important;
}}
ul[role="listbox"] li:hover,
div[role="option"]:hover,
li[aria-selected="true"] {{
    background-color: {GRIS_HOVER} !important;
    color: #000000 !important;
}}
ul[role="listbox"] * {{
    color: #000000 !important;
}}

/* Pestañas en verde #30b44e */
button[data-baseweb="tab"] {{
    color: #1f2937 !important;
    font-weight: 600;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {VERDE_PRINCIPAL} !important;
    border-bottom-color: {VERDE_PRINCIPAL} !important;
}}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background-color: {VERDE_PRINCIPAL} !important;
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

/* Tarjetas de asesor y bloques semánticos */
.asesor-card {{
    background: #ffffff;
    border: 1px solid #b7e1c1;
    border-left: 6px solid {VERDE_PRINCIPAL};
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 16px;
}}
.box-critico {{
    background: #fef2f2;
    border-left: 5px solid {ROJO_CRITICO};
    border-top: 1px solid #fecaca;
    border-right: 1px solid #fecaca;
    border-bottom: 1px solid #fecaca;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    color: #000000;
}}
.box-mejora {{
    background: #fff7ed;
    border-left: 5px solid {NARANJA_TRABAJAR};
    border-top: 1px solid #fed7aa;
    border-right: 1px solid #fed7aa;
    border-bottom: 1px solid #fed7aa;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    color: #000000;
}}
.box-positivo {{
    background: {VERDE_SUAVE};
    border-left: 5px solid {VERDE_PRINCIPAL};
    border-top: 1px solid #bbf7d0;
    border-right: 1px solid #bbf7d0;
    border-bottom: 1px solid #bbf7d0;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    color: #000000;
}}
.txt-critico {{ color: {ROJO_CRITICO}; font-weight: 700; }}
.txt-mejora {{ color: {NARANJA_TRABAJAR}; font-weight: 700; }}
.txt-positivo {{ color: {VERDE_PRINCIPAL}; font-weight: 700; }}
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
        "Trabajar una apertura cálida y cercana en los primeros segundos para generar confianza inicial.",
    "Explica motivo de llamada claramente":
        "Practicar un gancho inicial directo y claro para que el cliente entienda desde el inicio el motivo de la llamada.",
    "Explora necesidades reales":
        "Reforzar preguntas abiertas y de diagnóstico antes de presentar la oferta.",
    "Escucha activa":
        "Evitar interrumpir y retomar palabras clave del cliente para demostrar atención real.",
    "Propuesta adaptada al cliente":
        "Conectar cada característica de la propuesta con la necesidad puntual detectada.",
    "Explica beneficios":
        "Traducir atributos técnicos en beneficios concretos y relevantes para el cliente.",
    "Usa ejemplos / comparaciones":
        "Apoyarse en ejemplos cotidianos o comparaciones simples para facilitar la comprensión.",
    "No realiza monólogo":
        "Hacer pausas breves y chequear comprensión con el cliente en lugar de exponer de corrido.",
    "Avanza hacia el cierre":
        "Guiar la conversación con pasos concretos hacia la decisión final sin dilatar.",
    "Identifica objeción real":
        "Distinguir entre excusas superficiales y la objeción de fondo antes de responder.",
    "Maneja objeciones":
        "Aplicar roleplays de manejo de objeciones (empatía, validación, reformulación y cierre).",
    "Realiza cierres parciales":
        "Confirmar acuerdos intermedios durante la llamada para construir el cierre final.",
    "Indica Valor a abonar":
        "Comunicar con claridad y sin ambigüedades el monto a abonar y condiciones asociadas.",
    "Sin connotación de obligatoriedad":
        "Revisar el lenguaje para evitar tono imperativo o sensación de obligación en el cliente.",
    "Realiza de forma correcta cierres legales":
        "Asegurar que se transmitan completos y claros todos los requisitos y cierres legales obligatorios.",
    "Tono natural y entusiasta":
        "Entrenar modulación, energía positiva y naturalidad vocal durante toda la gestión.",
    "Evita frases robotizadas":
        "Reemplazar muletillas o guiones rígidos por expresiones naturales y conversacionales.",
    "Tuteo al cliente/Cortesía":
        "Mantener trato respetuoso, cordial y coherente con el estilo de comunicación de la campaña."
}

# =====================================================
# FUNCIONES
# =====================================================
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
        datos[col] = datos[col].astype(str).str.strip()

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

    mes_fecha = datos["Fecha"].dt.to_period("M").astype(str)
    mes_raw = datos["Mes_raw"].where(datos["Mes_raw"].str.match(r"^\d{4}-\d{2}$"), "")
    datos["Mes"] = mes_fecha.where(datos["Fecha"].notna(), mes_raw)
    datos.loc[datos["Mes"].isin(["", "NaT"]), "Mes"] = "Sin mes"

    datos["Año"] = datos["Fecha"].dt.year.astype("Int64").astype(str).replace("<NA>", "Sin año")

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


def colorear_df(df_mostrar):
    def estilo_fila(fila):
        estilos = [""] * len(fila)
        for idx, col in enumerate(fila.index):
            c_low = col.lower()
            if "crític" in c_low or "incumpl" in c_low:
                estilos[idx] = f"color: {ROJO_CRITICO}; font-weight: 700;"
            elif "mejora" in c_low or "trabajar" in c_low:
                estilos[idx] = f"color: {NARANJA_TRABAJAR}; font-weight: 700;"
            elif "positiv" in c_low or "cumpl" in c_low:
                estilos[idx] = f"color: {VERDE_PRINCIPAL}; font-weight: 700;"
        return estilos
    return df_mostrar.style.apply(estilo_fila, axis=1)


def mostrar_tabla(datos, columnas=None, colorear=False):
    if datos.empty:
        st.info("No hay datos para mostrar con la selección actual.")
    else:
        tabla = datos if columnas is None else datos[columnas]
        if colorear:
            st.dataframe(colorear_df(tabla), use_container_width=True, hide_index=True)
        else:
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
            return "A trabajar / Mejora"
        return "Positivo"

    res["Estado"] = res.apply(clasificar, axis=1)
    return res.sort_values(["% Crítico_num", "% Mejora_num", "Descuento"], ascending=[False, False, False])


# =====================================================
# CARGA DE DATOS
# =====================================================
try:
    df = leer_mediciones()
    detalle_criterios = construir_detalle_criterios(df)
except Exception as error:
    st.error("No se pudieron cargar los datos desde Google Sheets.")
    st.exception(error)
    st.stop()

if df.empty:
    st.warning("Todavía no hay auditorías para mostrar.")
    st.stop()

# =====================================================
# FILTROS INICIALES: AÑO, MES, CAMPAÑA Y ASESOR
# =====================================================
st.subheader("Filtros principales")

f1, f2, f3, f4 = st.columns(4)

with f1:
    años_disp = sorted([a for a in df["Año"].dropna().unique() if a != "Sin año"])
    años_sel = st.multiselect(
        "Año", options=años_disp, default=años_disp, key="filtro_anio"
    )

base_mes = df[df["Año"].isin(años_sel)] if años_sel else df
with f2:
    meses_disp = sorted([m for m in base_mes["Mes"].dropna().unique() if m != "Sin mes"])
    meses_sel = st.multiselect(
        "Mes", options=meses_disp, default=meses_disp, key="filtro_mes"
    )

base_camp = base_mes[base_mes["Mes"].isin(meses_sel)] if meses_sel else base_mes
with f3:
    camp_disp = sorted(base_camp["Campaña"].dropna().unique())
    camp_sel = st.multiselect(
        "Campaña", options=camp_disp, default=camp_disp, key="filtro_camp"
    )

base_ases = base_camp[base_camp["Campaña"].isin(camp_sel)] if camp_sel else base_camp
with f4:
    ases_disp = sorted(base_ases["Asesor"].dropna().unique())
    ases_sel = st.multiselect(
        "Asesor", options=ases_disp, default=ases_disp, key="filtro_ases"
    )

filtrado = df.copy()
if años_sel:
    filtrado = filtrado[filtrado["Año"].isin(años_sel)]
if meses_sel:
    filtrado = filtrado[filtrado["Mes"].isin(meses_sel)]
if camp_sel:
    filtrado = filtrado[filtrado["Campaña"].isin(camp_sel)]
if ases_sel:
    filtrado = filtrado[filtrado["Asesor"].isin(ases_sel)]

if filtrado.empty:
    st.warning("No hay registros con los filtros seleccionados.")
    st.stop()

detalle_filtrado = construir_detalle_criterios(filtrado)

# =====================================================
# INDICADORES GENERALES
# =====================================================
st.divider()
st.subheader("Indicadores generales")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Auditorías filtradas", len(filtrado))
k2.metric("Calidad promedio", fmt_pct(filtrado["Puntaje final"].mean()))
k3.metric("Asesores", filtrado["Asesor"].nunique())
k4.metric("Campañas", filtrado["Campaña"].nunique())

# =====================================================
# VISTAS PRINCIPALES
# =====================================================
tab_asesor, tab_campana, tab_empresa, tab_detalle = st.tabs([
    "Vista por asesor",
    "Vista por campaña",
    "Vista por empresa",
    "Detalle de auditorías"
])

# =====================================================
# 1. VISTA DETALLADA POR ASESOR
# =====================================================
with tab_asesor:
    st.subheader("Detalle por asesor seleccionado")
    asesores_a_mostrar = sorted(filtrado["Asesor"].unique())

    for nom_asesor in asesores_a_mostrar:
        sub_a = filtrado[filtrado["Asesor"] == nom_asesor].copy()
        crit_a = detalle_filtrado[detalle_filtrado["Asesor"] == nom_asesor].copy()
        ejes_a = resumen_ejes_criterios(crit_a)

        total_eval = len(crit_a)
        pct_pos_global = (crit_a["Respuesta"].isin(["si", "sí", "n/a"]).sum() / total_eval * 100) if total_eval else None
        pct_mej_global = ((crit_a["Respuesta"] == "punto de mejora").sum() / total_eval * 100) if total_eval else None
        pct_crit_global = ((crit_a["Respuesta"] == "no").sum() / total_eval * 100) if total_eval else None

        with st.container():
            st.markdown(f'<div class="asesor-card"><h3>{nom_asesor}</h3></div>', unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Calidad promedio", fmt_pct(sub_a["Puntaje final"].mean()))
            m2.metric("Aspectos positivos (%)", fmt_pct(pct_pos_global))
            m3.metric("Puntos de mejora (%)", fmt_pct(pct_mej_global))
            m4.metric("Puntos críticos (%)", fmt_pct(pct_crit_global))

            # Calidad por meses seleccionados
            st.markdown("**Calidad por meses seleccionados**")
            cal_mes_a = sub_a[sub_a["Mes"] != "Sin mes"].groupby("Mes", as_index=False).agg(
                Auditorías=("Puntaje final", "count"),
                Calidad_num=("Puntaje final", "mean")
            ).sort_values("Mes")
            if not cal_mes_a.empty:
                cal_mes_a["Calidad"] = cal_mes_a["Calidad_num"].apply(fmt_pct)
                mostrar_tabla(cal_mes_a[["Mes", "Auditorías", "Calidad"]])

            # Puntos críticos, de mejora, a trabajar y positivos
            st.markdown("**Diagnóstico de aspectos del asesor**")
            col_c, col_m, col_t, col_p = st.columns(4)

            criticos_df = ejes_a[ejes_a["% Crítico_num"] > 0] if not ejes_a.empty else pd.DataFrame()
            mejoras_df = ejes_a[ejes_a["% Mejora_num"] > 0] if not ejes_a.empty else pd.DataFrame()
            trabajar_df = sub_a[sub_a["Puntos a trabajar"].str.strip() != ""][["Fecha", "Campaña", "Puntos a trabajar"]].copy()
            positivos_df = ejes_a.sort_values("% Positivo_num", ascending=False).head(5) if not ejes_a.empty else pd.DataFrame()

            with col_c:
                st.markdown('<div class="box-critico"><span class="txt-critico">Puntos críticos</span></div>', unsafe_allow_html=True)
                if not criticos_df.empty:
                    for _, r in criticos_df.head(5).iterrows():
                        st.markdown(f"- **{r['Criterio']}** ({r['% Crítico']})")
                else:
                    st.caption("Sin puntos críticos en el filtro.")

            with col_m:
                st.markdown('<div class="box-mejora"><span class="txt-mejora">Puntos de mejora</span></div>', unsafe_allow_html=True)
                if not mejoras_df.empty:
                    for _, r in mejoras_df.head(5).iterrows():
                        st.markdown(f"- **{r['Criterio']}** ({r['% Mejora']})")
                else:
                    st.caption("Sin puntos de mejora en el filtro.")

            with col_t:
                st.markdown('<div class="box-mejora"><span class="txt-mejora">Puntos a trabajar</span></div>', unsafe_allow_html=True)
                if not trabajar_df.empty:
                    for _, r in trabajar_df.head(5).iterrows():
                        f_txt = r["Fecha"].strftime("%d/%m/%Y") if pd.notna(r["Fecha"]) else "Sin fecha"
                        st.markdown(f"- [{f_txt}] {r['Puntos a trabajar']}")
                else:
                    st.caption("Sin observaciones a trabajar registradas.")

            with col_p:
                st.markdown('<div class="box-positivo"><span class="txt-positivo">Puntos positivos</span></div>', unsafe_allow_html=True)
                if not positivos_df.empty:
                    for _, r in positivos_df.iterrows():
                        st.markdown(f"- **{r['Criterio']}** ({r['% Positivo']})")
                else:
                    st.caption("Sin datos positivos en el filtro.")

            # Histórico de campañas de esos asesores
            st.markdown("**Histórico de campañas del asesor**")
            hist_camp_a = sub_a.groupby(["Campaña", "Mes"], as_index=False).agg(
                Auditorías=("Puntaje final", "count"),
                Calidad_num=("Puntaje final", "mean")
            ).sort_values(["Campaña", "Mes"])
            if not hist_camp_a.empty:
                hist_camp_a["Calidad"] = hist_camp_a["Calidad_num"].apply(fmt_pct)
                fig_hc = px.line(
                    hist_camp_a, x="Mes", y="Calidad_num", color="Campaña", markers=True,
                    labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"}
                )
                st.plotly_chart(
                    estilo_grafico(fig_hc, f"Histórico por campaña | {nom_asesor}", "Mes", "Calidad", es_porcentaje_y=True),
                    use_container_width=True
                )
                mostrar_tabla(hist_camp_a[["Campaña", "Mes", "Auditorías", "Calidad"]])

            # Análisis y recomendaciones del asesor
            st.markdown("**Análisis y recomendaciones para el asesor**")
            if not ejes_a.empty:
                top_foco = ejes_a.iloc[0]
                rec_texto = RECOMENDACIONES_CRITERIO.get(
                    top_foco["Criterio"], "Reforzar práctica y seguimiento en coaching."
                )
                clase_box = "box-critico" if top_foco["Estado"] == "Crítico" else ("box-mejora" if top_foco["Estado"] == "A trabajar / Mejora" else "box-positivo")
                st.markdown(
                    f'<div class="{clase_box}">'
                    f'<b>Foco prioritario ({top_foco["Estado"]}):</b> {top_foco["Criterio"]} ({top_foco["Dimensión"]}) — '
                    f'Crítico: {top_foco["% Crítico"]} | Mejora: {top_foco["% Mejora"]} | Positivo: {top_foco["% Positivo"]}.<br>'
                    f'<b>Recomendación:</b> {rec_texto}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.divider()

# =====================================================
# 2. VISTA DETALLADA POR CAMPAÑA
# =====================================================
with tab_campana:
    st.subheader("Detalle por campaña")

    res_camp = filtrado.groupby("Campaña", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Asesores=("Asesor", "nunique"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values("Calidad_num", ascending=False)
    res_camp["Calidad"] = res_camp["Calidad_num"].apply(fmt_pct)

    fig_c = px.bar(
        res_camp, x="Campaña", y="Calidad_num", text="Calidad",
        labels={"Campaña": "Campaña", "Calidad_num": "Calidad (%)"},
        color_discrete_sequence=[VERDE_PRINCIPAL]
    )
    fig_c.update_traces(textposition="outside")
    st.plotly_chart(
        estilo_grafico(fig_c, "Calidad promedio por campaña", "Campaña", "Calidad", es_porcentaje_y=True),
        use_container_width=True
    )
    mostrar_tabla(res_camp[["Campaña", "Auditorías", "Asesores", "Calidad"]])

    st.markdown("### Ejes de trabajo por campaña (Críticos, Mejoras y Positivos)")
    for nom_camp in sorted(filtrado["Campaña"].unique()):
        crit_c = detalle_filtrado[detalle_filtrado["Campaña"] == nom_camp]
        ejes_c = resumen_ejes_criterios(crit_c)
        prom_c = filtrado[filtrado["Campaña"] == nom_camp]["Puntaje final"].mean()

        st.markdown(f"#### {nom_camp} — Calidad: {fmt_pct(prom_c)}")
        c1, c2, c3 = st.columns(3)

        crit_list = ejes_c[ejes_c["Estado"] == "Crítico"] if not ejes_c.empty else pd.DataFrame()
        mej_list = ejes_c[ejes_c["Estado"] == "A trabajar / Mejora"] if not ejes_c.empty else pd.DataFrame()
        pos_list = ejes_c[ejes_c["Estado"] == "Positivo"] if not ejes_c.empty else pd.DataFrame()

        with c1:
            st.markdown('<div class="box-critico"><span class="txt-critico">Puntos críticos</span></div>', unsafe_allow_html=True)
            if not crit_list.empty:
                for _, r in crit_list.iterrows():
                    st.markdown(f"- **{r['Criterio']}** ({r['% Crítico']})")
            else:
                st.caption("Sin criterios críticos.")

        with c2:
            st.markdown('<div class="box-mejora"><span class="txt-mejora">Puntos de mejora</span></div>', unsafe_allow_html=True)
            if not mej_list.empty:
                for _, r in mej_list.iterrows():
                    st.markdown(f"- **{r['Criterio']}** ({r['% Mejora']})")
            else:
                st.caption("Sin criterios en mejora.")

        with c3:
            st.markdown('<div class="box-positivo"><span class="txt-positivo">Puntos positivos</span></div>', unsafe_allow_html=True)
            if not pos_list.empty:
                for _, r in pos_list.head(6).iterrows():
                    st.markdown(f"- **{r['Criterio']}** ({r['% Positivo']})")
            else:
                st.caption("Sin criterios positivos destacados.")

        mostrar_tabla(ejes_c[[
            "Criterio", "Dimensión", "% Positivo", "% Mejora", "% Crítico", "Estado"
        ]], colorear=True)

# =====================================================
# 3. VISTA DETALLADA POR EMPRESA
# =====================================================
with tab_empresa:
    st.subheader("Detalle a nivel empresa")

    meses_emp_disp = sorted([m for m in df["Mes"].dropna().unique() if m != "Sin mes"])
    meses_emp_sel = st.multiselect(
        "Filtrar meses para histórico de calidad y campaña (Empresa)",
        options=meses_emp_disp,
        default=meses_emp_disp,
        key="filtro_meses_empresa"
    )

    base_emp = df.copy()
    if meses_emp_sel:
        base_emp = base_emp[base_emp["Mes"].isin(meses_emp_sel)]

    e1, e2, e3 = st.columns(3)
    e1.metric("Calidad empresa", fmt_pct(base_emp["Puntaje final"].mean()))
    e2.metric("Auditorías", len(base_emp))
    e3.metric("Campañas", base_emp["Campaña"].nunique())

    st.markdown("### Histórico de puntuaciones de calidad por mes (Empresa)")
    hist_emp_mes = base_emp[base_emp["Mes"] != "Sin mes"].groupby("Mes", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values("Mes")
    if not hist_emp_mes.empty:
        hist_emp_mes["Calidad"] = hist_emp_mes["Calidad_num"].apply(fmt_pct)
        fig_em = px.line(
            hist_emp_mes, x="Mes", y="Calidad_num", markers=True,
            labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"},
            color_discrete_sequence=[VERDE_PRINCIPAL]
        )
        st.plotly_chart(
            estilo_grafico(fig_em, "Histórico mensual de calidad | Empresa", "Mes", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )
        mostrar_tabla(hist_emp_mes[["Mes", "Auditorías", "Calidad"]])

    st.markdown("### Histórico de puntuaciones por campaña y mes (Empresa)")
    hist_emp_camp = base_emp[base_emp["Mes"] != "Sin mes"].groupby(["Mes", "Campaña"], as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values(["Mes", "Campaña"])
    if not hist_emp_camp.empty:
        hist_emp_camp["Calidad"] = hist_emp_camp["Calidad_num"].apply(fmt_pct)
        fig_ec = px.line(
            hist_emp_camp, x="Mes", y="Calidad_num", color="Campaña", markers=True,
            labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig_ec, "Histórico por campaña y mes | Empresa", "Mes", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )
        mostrar_tabla(hist_emp_camp[["Mes", "Campaña", "Auditorías", "Calidad"]])

    st.markdown("### Ejes generales de la empresa")
    crit_emp = construir_detalle_criterios(base_emp)
    ejes_emp = resumen_ejes_criterios(crit_emp)
    mostrar_tabla(ejes_emp[[
        "Criterio", "Dimensión", "% Positivo", "% Mejora", "% Crítico", "Estado"
    ]], colorear=True)

# =====================================================
# 4. DETALLE DE AUDITORÍAS
# =====================================================
with tab_detalle:
    st.subheader("Detalle de auditorías filtradas")
    columnas_detalle = [
        "Fecha", "Asesor", "Campaña", "ID", "Tipo de gestión",
        "Tipificación", "Puntaje final", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?", "Tipificación correcta"
    ]
    detalle = filtrado[columnas_detalle].copy()
    detalle["Fecha_str"] = detalle["Fecha"].dt.strftime("%d/%m/%Y").fillna("Sin fecha")
    detalle["Calidad"] = detalle["Puntaje final"].apply(fmt_pct)
    detalle = detalle.sort_values("Fecha", ascending=False, na_position="last")
    mostrar_tabla(detalle[[
        "Fecha_str", "Asesor", "Campaña", "ID", "Tipo de gestión",
        "Tipificación", "Calidad", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?", "Tipificación correcta"
    ]])

    csv = filtrado[columnas_detalle].to_csv(
        index=False, sep=";", encoding="utf-8-sig"
    )
    st.download_button(
        "Descargar auditorías en CSV",
        data=csv,
        file_name="auditorias_calidad_contactel.csv",
        mime="text/csv"
    )

# =====================================================
# PIE Y ACTUALIZACIÓN
# =====================================================
st.divider()
st.caption(
    "Calidad y Capacitación | Contactel | "
    "Actualización automática de datos cada 5 minutos."
)
st.caption("La columna AC (Acción) está excluida del análisis y de las vistas.")

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
