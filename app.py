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

/* Tags seleccionados dentro del multiselect */
span[data-baseweb="tag"] {{
    background-color: {VERDE_PRINCIPAL} !important;
    color: #ffffff !important;
    border-radius: 6px !important;
}}
span[data-baseweb="tag"] span,
span[data-baseweb="tag"] svg {{
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

/* Bloques de estado: crítico (rojo), a trabajar (naranja), positivo (verde) */
.estado-critico {{
    background: #fef2f2;
    border-left: 5px solid {ROJO_CRITICO};
    border-top: 1px solid #fecaca;
    border-right: 1px solid #fecaca;
    border-bottom: 1px solid #fecaca;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #000000;
}}
.estado-trabajar {{
    background: #fff7ed;
    border-left: 5px solid {NARANJA_TRABAJAR};
    border-top: 1px solid #fed7aa;
    border-right: 1px solid #fed7aa;
    border-bottom: 1px solid #fed7aa;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #000000;
}}
.estado-positivo {{
    background: {VERDE_SUAVE};
    border-left: 5px solid {VERDE_PRINCIPAL};
    border-top: 1px solid #bbf7d0;
    border-right: 1px solid #bbf7d0;
    border-bottom: 1px solid #bbf7d0;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #000000;
}}
.badge-critico {{
    color: {ROJO_CRITICO};
    font-weight: 700;
}}
.badge-trabajar {{
    color: {NARANJA_TRABAJAR};
    font-weight: 700;
}}
.badge-positivo {{
    color: {VERDE_PRINCIPAL};
    font-weight: 700;
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

    datos["Año"] = datos["Fecha"].dt.year

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


def estilo_grafico(fig, titulo, eje_x=None, eje_y=None, es_porcentaje_y=False, color_map=None):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color="#000000", size=19)),
        font=dict(color="#000000", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#000000")),
        margin=dict(l=20, r=20, t=65, b=35),
        hoverlabel=dict(font=dict(color="#000000"))
    )
    if color_map:
        fig.update_traces(marker=dict(color=[color_map.get(v, VERDE_PRINCIPAL) for v in fig.data[0].y]) if fig.data and fig.data[0].orientation == "h" else None)
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


def colorear_estado_df(df_mostrar):
    def estilo_fila(fila):
        estilos = [""] * len(fila)
        for idx, col in enumerate(fila.index):
            val = str(fila[col]).lower()
            if "crític" in col.lower() or "incumpl" in col.lower() or "no" == val:
                estilos[idx] = f"color: {ROJO_CRITICO}; font-weight: 700;"
            elif "trabajar" in col.lower() or "mejora" in col.lower():
                estilos[idx] = f"color: {NARANJA_TRABAJAR}; font-weight: 700;"
            elif "positiv" in col.lower() or "cumpl" in col.lower() or "fortaleza" in col.lower():
                estilos[idx] = f"color: {VERDE_PRINCIPAL}; font-weight: 700;"
        return estilos

    return df_mostrar.style.apply(estilo_fila, axis=1)


def mostrar_tabla(datos, columnas=None, colorear=False):
    if datos.empty:
        st.info("No hay datos para mostrar con la selección actual.")
    else:
        tabla = datos if columnas is None else datos[columnas]
        if colorear:
            st.dataframe(colorear_estado_df(tabla), use_container_width=True, hide_index=True)
        else:
            st.dataframe(tabla, use_container_width=True, hide_index=True)


def promedio_anual(datos):
    return datos["Puntaje final"].mean()


def resumen_por_dimension(df_criterios):
    if df_criterios.empty:
        return pd.DataFrame(columns=[
            "Criterio", "Dimensión", "Descuento", "Evaluaciones",
            "Incumplimientos", "Mejoras", "% crítico"
        ])
    res = df_criterios.groupby(["Criterio", "Dimensión"], as_index=False).agg(
        Descuento=("Descuento", "sum"),
        Evaluaciones=("Respuesta", "count"),
        Incumplimientos=("Respuesta", lambda x: (x == "no").sum()),
        Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum())
    )
    res["% crítico"] = (
        ((res["Incumplimientos"] + res["Mejoras"]) / res["Evaluaciones"] * 100)
        .round(0).astype(int).astype(str) + "%"
    )
    res["Descuento"] = res["Descuento"].round(0).astype(int)
    return res.sort_values(["Descuento", "Incumplimientos"], ascending=[False, False])


# =====================================================
# CARGA
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

df_con_fecha = df.dropna(subset=["Fecha"]).copy()

# =====================================================
# FILTROS GENERALES (CAMPAÑAS, ASESORES, PERÍODO Y MESES)
# =====================================================
st.subheader("Filtros generales")

f1, f2 = st.columns(2)

with f1:
    opciones_campaña = sorted(df["Campaña"].dropna().unique())
    campañas = st.multiselect(
        "Campaña", opciones_campaña, default=opciones_campaña,
        key="filtro_campanias"
    )

with f2:
    base_asesores = df[df["Campaña"].isin(campañas)] if campañas else df
    opciones_asesor = sorted(base_asesores["Asesor"].dropna().unique())
    asesores = st.multiselect(
        "Asesor", opciones_asesor, default=opciones_asesor,
        key="filtro_asesores"
    )

p1, p2 = st.columns([1.2, 1.8])

if not df_con_fecha.empty:
    fecha_min = df_con_fecha["Fecha"].min().date()
    fecha_max = df_con_fecha["Fecha"].max().date()
else:
    fecha_min = fecha_max = pd.Timestamp.today().date()

with p1:
    periodo = st.date_input(
        "Período (seleccioná fecha inicio y fecha fin)",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
        format="DD/MM/YYYY",
        key="filtro_rango_fechas"
    )

with p2:
    meses_disponibles = sorted(
        m for m in df["Mes"].dropna().unique() if m and m != "Sin mes"
    )
    meses_seleccionados = st.multiselect(
        "Meses (podés elegir uno o varios, ej. agosto y septiembre para comparar)",
        options=meses_disponibles,
        default=[],
        key="filtro_meses"
    )

if isinstance(periodo, tuple) and len(periodo) == 2:
    fecha_inicio, fecha_fin = periodo
elif isinstance(periodo, tuple) and len(periodo) == 1:
    fecha_inicio = fecha_fin = periodo[0]
else:
    fecha_inicio, fecha_fin = fecha_min, fecha_max

filtrado = df.copy()
if campañas:
    filtrado = filtrado[filtrado["Campaña"].isin(campañas)]
if asesores:
    filtrado = filtrado[filtrado["Asesor"].isin(asesores)]

if not df_con_fecha.empty:
    misma_rango_total = (fecha_inicio == fecha_min) and (fecha_fin == fecha_max)
    if not misma_rango_total or meses_seleccionados:
        filtrado = filtrado[
            filtrado["Fecha"].isna() | filtrado["Fecha"].dt.date.between(fecha_inicio, fecha_fin)
        ]

if meses_seleccionados:
    filtrado = filtrado[filtrado["Mes"].isin(meses_seleccionados)]

if filtrado.empty:
    st.warning("No hay registros con los filtros seleccionados.")
    st.stop()

detalle_filtrado = construir_detalle_criterios(filtrado)

# =====================================================
# INDICADORES GENERALES
# =====================================================
st.divider()
st.subheader("Indicadores generales")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Auditorías filtradas", len(filtrado))
k2.metric("Total en Sheet", len(df))
promedio = filtrado["Puntaje final"].mean()
k3.metric("Calidad promedio", fmt_pct(promedio))
k4.metric("Asesores", filtrado["Asesor"].nunique())
k5.metric("Campañas", filtrado["Campaña"].nunique())

# =====================================================
# COMPARATIVO AUTOMÁTICO CUANDO SE ELIGEN 2 O MÁS MESES
# =====================================================
if len(meses_seleccionados) >= 2:
    st.divider()
    st.subheader(f"Comparativo de meses seleccionados: {', '.join(sorted(meses_seleccionados))}")

    comp_mes = filtrado.groupby("Mes", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values("Mes")
    comp_mes["Calidad"] = comp_mes["Calidad_num"].apply(fmt_pct)

    fig_comp = px.bar(
        comp_mes, x="Mes", y="Calidad_num", text="Calidad",
        labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"},
        color_discrete_sequence=[VERDE_PRINCIPAL]
    )
    fig_comp.update_traces(textposition="outside")
    st.plotly_chart(
        estilo_grafico(fig_comp, "Comparativa de calidad por mes", "Mes", "Calidad", es_porcentaje_y=True),
        use_container_width=True
    )
    mostrar_tabla(comp_mes[["Mes", "Auditorías", "Calidad"]])

    comp_camp_mes = filtrado.groupby(["Mes", "Campaña"], as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values(["Campaña", "Mes"])
    comp_camp_mes["Calidad"] = comp_camp_mes["Calidad_num"].apply(fmt_pct)

    if not comp_camp_mes.empty:
        fig_cm = px.bar(
            comp_camp_mes, x="Campaña", y="Calidad_num", color="Mes",
            barmode="group", text="Calidad",
            labels={"Campaña": "Campaña", "Calidad_num": "Calidad (%)"}
        )
        fig_cm.update_traces(textposition="outside")
        st.plotly_chart(
            estilo_grafico(fig_cm, "Comparativa por campaña entre meses", "Campaña", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )
        mostrar_tabla(comp_camp_mes[["Campaña", "Mes", "Auditorías", "Calidad"]])

# =====================================================
# PESTAÑAS
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Resumen y evolución",
    "Análisis por asesor",
    "Por campaña",
    "Histórico empresa",
    "Histórico por asesor",
    "Criterios y auditorías",
    "Análisis y recomendaciones"
])

# =====================================================
# 1. RESUMEN Y EVOLUCIÓN
# =====================================================
with tab1:
    st.subheader("Evolución de calidad por campaña y por asesor")

    e1, e2 = st.columns(2)
    with e1:
        camp_evol = st.multiselect(
            "Campañas a graficar",
            options=sorted(filtrado["Campaña"].unique()),
            default=sorted(filtrado["Campaña"].unique()),
            key="evol_camp_sel"
        )
    with e2:
        ases_evol = st.multiselect(
            "Asesores a graficar",
            options=sorted(filtrado["Asesor"].unique()),
            default=sorted(filtrado["Asesor"].unique())[:6],
            key="evol_ases_sel"
        )

    base_evol = filtrado[
        filtrado["Campaña"].isin(camp_evol) &
        filtrado["Asesor"].isin(ases_evol) &
        (filtrado["Mes"] != "Sin mes")
    ].copy()

    g1, g2 = st.columns(2)

    with g1:
        evol_camp = base_evol.groupby(["Mes", "Campaña"], as_index=False).agg(
            Auditorías=("Puntaje final", "count"),
            Calidad_num=("Puntaje final", "mean")
        ).sort_values(["Mes", "Campaña"])
        if not evol_camp.empty:
            fig = px.line(
                evol_camp, x="Mes", y="Calidad_num", color="Campaña", markers=True,
                labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"}
            )
            st.plotly_chart(
                estilo_grafico(fig, "Evolución mensual por campaña", "Mes", "Calidad", es_porcentaje_y=True),
                use_container_width=True
            )

    with g2:
        evol_ases = base_evol.groupby(["Mes", "Asesor"], as_index=False).agg(
            Auditorías=("Puntaje final", "count"),
            Calidad_num=("Puntaje final", "mean")
        ).sort_values(["Mes", "Asesor"])
        if not evol_ases.empty:
            fig = px.line(
                evol_ases, x="Mes", y="Calidad_num", color="Asesor", markers=True,
                labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"}
            )
            st.plotly_chart(
                estilo_grafico(fig, "Evolución mensual por asesor", "Mes", "Calidad", es_porcentaje_y=True),
                use_container_width=True
            )

    st.subheader("Resultados por asesor")
    tabla_asesores = filtrado.groupby("Asesor", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values("Calidad_num", ascending=False)
    tabla_asesores["Calidad"] = tabla_asesores["Calidad_num"].apply(fmt_pct)

    fig = px.bar(
        tabla_asesores, x="Asesor", y="Calidad_num",
        labels={"Calidad_num": "Calidad (%)", "Asesor": "Asesor"},
        text="Calidad",
        color_discrete_sequence=[VERDE_PRINCIPAL]
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(
        estilo_grafico(fig, "Calidad promedio por asesor", "Asesor", "Calidad", es_porcentaje_y=True),
        use_container_width=True
    )
    mostrar_tabla(tabla_asesores[["Asesor", "Auditorías", "Calidad"]])

    st.subheader("Resultados por tipo de gestión")
    por_tipo = filtrado.assign(
        Tipo=filtrado["Tipo normalizado"].fillna("Sin clasificar")
    ).groupby("Tipo", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    )
    por_tipo["Calidad"] = por_tipo["Calidad_num"].apply(fmt_pct)
    mostrar_tabla(por_tipo[["Tipo", "Auditorías", "Calidad"]])

# =====================================================
# 2. ANÁLISIS POR ASESOR
# =====================================================
with tab2:
    st.subheader("Análisis individual del asesor")
    asesor = st.selectbox(
        "Seleccionar asesor",
        sorted(filtrado["Asesor"].unique()),
        key="asesor_analisis"
    )

    individual = filtrado[filtrado["Asesor"] == asesor].copy()
    criterios_individual = detalle_filtrado[
        detalle_filtrado["Asesor"] == asesor
    ].copy()

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Auditorías", len(individual))
    a2.metric("Puntuación de calidad", fmt_pct(individual["Puntaje final"].mean()))
    a3.metric("Puntos descontados", f"{criterios_individual['Descuento'].sum():.0f}")
    a4.metric("Incumplimientos", int((criterios_individual["Respuesta"] == "no").sum()))

    st.markdown("#### Aspectos críticos: Comerciales vs. Actitudinales")
    res_dim = resumen_por_dimension(criterios_individual)

    c_com, c_act = st.columns(2)
    with c_com:
        st.markdown(f'<span class="badge-critico">Aspectos críticos comerciales</span>', unsafe_allow_html=True)
        top_com = res_dim[res_dim["Dimensión"] == "Comercial"].head(5)
        mostrar_tabla(top_com[[
            "Criterio", "Descuento", "Incumplimientos", "Mejoras", "% crítico"
        ]], colorear=True)

    with c_act:
        st.markdown(f'<span class="badge-critico">Aspectos críticos actitudinales</span>', unsafe_allow_html=True)
        top_act = res_dim[res_dim["Dimensión"] == "Actitudinal"].head(5)
        mostrar_tabla(top_act[[
            "Criterio", "Descuento", "Incumplimientos", "Mejoras", "% crítico"
        ]], colorear=True)

    st.markdown(f'<span class="badge-trabajar">Aspectos a trabajar reportados en auditoría</span>', unsafe_allow_html=True)
    puntos_trabajar = individual[
        individual["Puntos a trabajar"].str.strip() != ""
    ][["Fecha", "Campaña", "Puntaje final", "Puntos a trabajar", "Observaciones"]].copy()
    if not puntos_trabajar.empty:
        puntos_trabajar["Calidad"] = puntos_trabajar["Puntaje final"].apply(fmt_pct)
        puntos_trabajar["Fecha_str"] = puntos_trabajar["Fecha"].dt.strftime("%d/%m/%Y").fillna("Sin fecha")
        puntos_trabajar = puntos_trabajar.sort_values("Fecha", ascending=False, na_position="last")
        mostrar_tabla(puntos_trabajar[["Fecha_str", "Campaña", "Calidad", "Puntos a trabajar", "Observaciones"]])
    else:
        mostrar_tabla(pd.DataFrame())

    st.markdown("#### Descuentos por criterio")
    if not criterios_individual.empty:
        descuentos = criterios_individual.groupby(["Criterio", "Dimensión"], as_index=False).agg(
            Descuento=("Descuento", "sum"),
            Evaluaciones=("Respuesta", "count"),
            Incumplimientos=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum())
        ).sort_values("Descuento", ascending=False)
        descuentos["Descuento"] = descuentos["Descuento"].round(0).astype(int)

        fig = px.bar(
            descuentos, x="Descuento", y="Criterio", color="Dimensión", orientation="h",
            labels={"Descuento": "Puntos descontados", "Criterio": "Criterio"},
            color_discrete_map={"Comercial": ROJO_CRITICO, "Actitudinal": NARANJA_TRABAJAR}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Puntos descontados por criterio", "Puntos", "Criterio"),
            use_container_width=True
        )
        mostrar_tabla(descuentos, colorear=True)

        st.markdown(f'<span class="badge-trabajar">Reincidencias (a trabajar)</span>', unsafe_allow_html=True)
        reinc = criterios_individual[
            criterios_individual["Respuesta"].isin(["no", "punto de mejora"])
        ].groupby(["Criterio", "Dimensión", "Respuesta"]).size().unstack(fill_value=0).reset_index()

        if "no" not in reinc.columns:
            reinc["no"] = 0
        if "punto de mejora" not in reinc.columns:
            reinc["punto de mejora"] = 0
        reinc["Total de apariciones"] = reinc["no"] + reinc["punto de mejora"]
        reinc = reinc.rename(columns={
            "no": "Incumplimientos",
            "punto de mejora": "Puntos de mejora"
        }).sort_values("Total de apariciones", ascending=False)
        mostrar_tabla(reinc, colorear=True)

        st.markdown(f'<span class="badge-positivo">Fortalezas individuales (aspectos positivos)</span>', unsafe_allow_html=True)
        fortalezas = criterios_individual.groupby(["Criterio", "Dimensión"], as_index=False).agg(
            Evaluaciones=("Respuesta", "count"),
            Cumplimientos=("Respuesta", lambda x: x.isin(["si", "sí"]).sum()),
            N_A=("Respuesta", lambda x: (x == "n/a").sum())
        )
        fortalezas["% respuestas positivas"] = (
            ((fortalezas["Cumplimientos"] + fortalezas["N_A"]) / fortalezas["Evaluaciones"] * 100)
            .round(0).astype(int).astype(str) + "%"
        )
        mostrar_tabla(fortalezas, colorear=True)

    st.markdown("#### Evolución mensual del asesor")
    mensual = individual[individual["Mes"] != "Sin mes"].groupby("Mes", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values("Mes")
    if not mensual.empty:
        mensual["Calidad"] = mensual["Calidad_num"].apply(fmt_pct)
        fig = px.line(
            mensual, x="Mes", y="Calidad_num", markers=True,
            labels={"Mes": "Mes", "Calidad_num": "Calidad (%)"},
            color_discrete_sequence=[VERDE_PRINCIPAL]
        )
        st.plotly_chart(
            estilo_grafico(fig, "Evolución mensual", "Mes", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )
        mostrar_tabla(mensual[["Mes", "Auditorías", "Calidad"]])

    st.markdown("#### Historial de auditorías")
    cols_hist = [
        "Fecha", "Campaña", "ID", "Tipo de gestión", "Tipificación",
        "Puntaje final", "Puntos a trabajar", "Observaciones"
    ]
    historial = individual[cols_hist].copy()
    historial["Fecha_str"] = historial["Fecha"].dt.strftime("%d/%m/%Y").fillna("Sin fecha")
    historial["Calidad"] = historial["Puntaje final"].apply(fmt_pct)
    historial = historial.sort_values("Fecha", ascending=False, na_position="last")
    mostrar_tabla(historial[["Fecha_str", "Campaña", "ID", "Tipo de gestión", "Tipificación", "Calidad", "Puntos a trabajar", "Observaciones"]])

# =====================================================
# 3. POR CAMPAÑA
# =====================================================
with tab3:
    st.subheader("Desempeño por campaña")
    resumen_camp = filtrado.groupby("Campaña", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Asesores=("Asesor", "nunique"),
        Calidad_num=("Puntaje final", "mean")
    ).sort_values("Calidad_num", ascending=False)
    resumen_camp["Calidad"] = resumen_camp["Calidad_num"].apply(fmt_pct)

    fig = px.bar(
        resumen_camp, x="Campaña", y="Calidad_num", text="Calidad",
        labels={"Calidad_num": "Calidad (%)", "Campaña": "Campaña"},
        color_discrete_sequence=[VERDE_PRINCIPAL]
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(
        estilo_grafico(fig, "Calidad promedio por campaña", "Campaña", "Calidad", es_porcentaje_y=True),
        use_container_width=True
    )
    mostrar_tabla(resumen_camp[["Campaña", "Auditorías", "Asesores", "Calidad"]])

    st.subheader("Evolución mensual por campaña")
    base_camp = filtrado[filtrado["Mes"] != "Sin mes"].copy()
    if not base_camp.empty:
        mensual_camp = base_camp.groupby(["Mes", "Campaña"], as_index=False).agg(
            Auditorías=("Puntaje final", "count"),
            Calidad_num=("Puntaje final", "mean")
        ).sort_values(["Mes", "Campaña"])
        mensual_camp["Calidad"] = mensual_camp["Calidad_num"].apply(fmt_pct)

        fig = px.line(
            mensual_camp, x="Mes", y="Calidad_num", color="Campaña",
            markers=True, labels={"Calidad_num": "Calidad (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Evolución mensual por campaña", "Mes", "Calidad", es_porcentaje_y=True),
            use_container_width=True
        )
        mostrar_tabla(mensual_camp[["Mes", "Campaña", "Auditorías", "Calidad"]])

# =====================================================
# 4. HISTÓRICO GENERAL DE EMPRESA
# =====================================================
with tab4:
    st.subheader("Histórico general de Calidad | Empresa")

    if not df_con_fecha.empty:
        años = sorted(df_con_fecha["Año"].dropna().astype(int).unique())
        año_actual_datos = int(df_con_fecha["Año"].max())
        año_sel_empresa = st.selectbox(
            "Año a consultar", años,
            index=años.index(año_actual_datos),
            key="año_historico_empresa"
        )
        empresa_anual = df_con_fecha[df_con_fecha["Año"] == año_sel_empresa].copy()
    else:
        año_sel_empresa = "Todos"
