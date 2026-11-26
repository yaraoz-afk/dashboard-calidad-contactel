
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Calidad y Capacitación | Contactel",
    page_icon="📊",
    layout="wide"
)

# Paleta visual
VERDE = "#176B46"
VERDE_MEDIO = "#238653"
VERDE_CLARO = "#DCEFE3"
VERDE_OSCURO = "#174D3A"
NARANJA = "#E58A36"
ROJO = "#C94C4C"
GRIS = "#64776C"
FONDO = "#F3F6F4"
BORDE = "#DCE8E1"

st.markdown("""
<style>
.stApp {
    background-color: #F3F6F4;
    color: #263B32;
}

html, body, [class*="css"] {
    color: #263B32 !important;
}

h1, h2, h3, h4, p, label {
    color: #263B32;
}

h1 {
    color: #174D3A !important;
    font-weight: 800;
    letter-spacing: -0.5px;
}

h2, h3 {
    color: #246348 !important;
    font-weight: 700;
}

h4 {
    color: #176B46 !important;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DCE8E1;
    border-radius: 13px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(25, 65, 45, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #60766A !important;
    font-size: 14px;
}

div[data-testid="stMetricValue"] {
    color: #174D3A !important;
    font-size: 30px;
    font-weight: 800;
}

button[data-baseweb="tab"] {
    color: #486456 !important;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #176B46 !important;
    border-bottom: 3px solid #238653;
}

div[data-baseweb="select"] {
    background-color: white;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

hr {
    border-color: #DCE8E1;
}

.stButton button, .stDownloadButton button {
    background-color: #176B46;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 8px 18px;
}

.stButton button:hover, .stDownloadButton button:hover {
    background-color: #104D32;
    color: white !important;
}

div[data-testid="stCaptionContainer"] p {
    color: #64776C !important;
}

div[data-testid="stMarkdownContainer"] p {
    color: #263B32;
}

</style>
""", unsafe_allow_html=True)

st.title("Calidad y Capacitación")
st.caption("Panel ejecutivo de seguimiento de desempeño | Contactel")

# =====================================================
# FUENTES DE DATOS
# =====================================================

URL_MEDICION = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=0&single=true&output=csv"
)

# =====================================================
# PONDERACIONES
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

CRITERIOS_PONDERADOS = list(PONDERACIONES.keys())

# =====================================================
# FUNCIONES DE DISEÑO DE GRÁFICOS
# =====================================================

def formato_grafico(fig, altura=390):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=12,
            color="#263B32"
        ),
        margin=dict(l=15, r=25, t=55, b=25),
        height=altura,
        hoverlabel=dict(
            bgcolor="#174D3A",
            font_color="white",
            font_size=12
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E8EFEB",
            zeroline=False,
            title_font=dict(color="#486456")
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(color="#486456")
        ),
        title=dict(
            font=dict(
                size=17,
                color="#174D3A"
            ),
            x=0.02,
            xanchor="left"
        )
    )
    return fig


def grafico_barras(
    datos,
    x,
    y,
    titulo,
    horizontal=False,
    color=VERDE_MEDIO,
    formato_texto=".1f",
    sufijo=""
):
    if horizontal:
        fig = px.bar(
            datos,
            x=x,
            y=y,
            orientation="h",
            text=x,
            title=titulo
        )

        fig.update_traces(
            marker_color=color,
            texttemplate="%{text:" + formato_texto + "}" + sufijo,
            textposition="outside",
            cliponaxis=False
        )

    else:
        fig = px.bar(
            datos,
            x=x,
            y=y,
            text=y,
            title=titulo
        )

        fig.update_traces(
            marker_color=color,
            texttemplate="%{text:" + formato_texto + "}" + sufijo,
            textposition="outside",
            cliponaxis=False
        )

    return formato_grafico(fig)


def grafico_lineas(datos, x, y, titulo, color=VERDE_MEDIO):
    fig = px.line(
        datos,
        x=x,
        y=y,
        markers=True,
        title=titulo
    )

    fig.update_traces(
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color)
    )

    return formato_grafico(fig)


# =====================================================
# FUNCIONES DE DATOS
# =====================================================

def convertir_puntaje(valor):
    try:
        numero = float(
            str(valor).replace("%", "").replace(",", ".").strip()
        )
        if numero <= 1:
            numero *= 100
        return numero
    except (ValueError, TypeError):
        return None


def normalizar_tipo(valor):
    texto = str(valor).strip().lower()

    if "no venta" in texto:
        return "No Venta"

    if "venta" in texto:
        return "Venta"

    return None


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

        if respuesta in ["si", "n/a"]:
            obtenido += peso

        elif respuesta == "punto de mejora":
            obtenido += peso / 2

    if posible == 0:
        return None

    return obtenido / posible * 100


@st.cache_data(ttl=300)
def leer_mediciones():
    bruto = pd.read_csv(
        URL_MEDICION,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    datos = bruto.iloc[9:, :33].copy()

    datos.columns = [
        "Fecha", "Mes", "Asesor", "Campaña", "ID",
        "Duración", "Tipo de gestión", "Tipificación"
    ] + CRITERIOS + [
        "Puntos a trabajar",
        "Acción",
        "Puntaje",
        "Observaciones",
        "¿Tipifica bien?",
        "Tipificación correcta"
    ]

    # Se excluye la columna AC: Acción
    datos = datos.drop(columns=["Acción"])

    for col in datos.columns:
        datos[col] = datos[col].astype(str).str.strip()

    datos = datos[
        (datos["Asesor"] != "") &
        (datos["Campaña"] != "")
    ].copy()

    datos["Fecha"] = pd.to_datetime(
        datos["Fecha"],
        dayfirst=True,
        errors="coerce"
    )

    datos["Puntaje oficial"] = datos["Puntaje"].apply(
        convertir_puntaje
    )

    datos["Puntaje calculado"] = datos.apply(
        calcular_puntaje,
        axis=1
    )

    datos["Puntaje final"] = datos["Puntaje oficial"].fillna(
        datos["Puntaje calculado"]
    )

    datos["Tipo normalizado"] = datos["Tipo de gestión"].apply(
        normalizar_tipo
    )

    return datos


def construir_detalle_criterios(datos):
    registros = []

    for _, fila in datos.iterrows():
        tipo = fila["Tipo normalizado"]

        if tipo is None:
            continue

        indice = 0 if tipo == "Venta" else 1

        for criterio, pesos in PONDERACIONES.items():
            respuesta = str(fila[criterio]).strip().lower()
            peso = pesos[indice]

            if respuesta not in ["si", "no", "punto de mejora", "n/a"]:
                continue

            if respuesta == "no":
                descuento = peso
                puntos_obtenidos = 0

            elif respuesta == "punto de mejora":
                descuento = peso / 2
                puntos_obtenidos = peso / 2

            else:
                descuento = 0
                puntos_obtenidos = peso

            registros.append({
                "Fecha": fila["Fecha"],
                "Mes": (
                    fila["Fecha"].strftime("%Y-%m")
                    if pd.notna(fila["Fecha"]) else ""
                ),
                "Asesor": fila["Asesor"],
                "Campaña": fila["Campaña"],
                "Tipo de gestión": tipo,
                "Criterio": criterio,
                "Respuesta": respuesta,
                "Ponderación": peso,
                "Descuento": descuento,
                "Puntos obtenidos": puntos_obtenidos
            })

    return pd.DataFrame(registros)


# =====================================================
# CARGA DE INFORMACIÓN
# =====================================================

try:
    df = leer_mediciones()
    detalle_criterios = construir_detalle_criterios(df)

except Exception as error:
    st.error("No se pudieron cargar los datos.")
    st.exception(error)
    st.stop()

if df.empty:
    st.warning("No hay auditorías para mostrar.")
    st.stop()


# =====================================================
# FILTROS
# =====================================================

st.markdown("### Filtros de consulta")

c1, c2, c3 = st.columns(3)

with c1:
    opciones_campaña = sorted(df["Campaña"].unique())

    campañas = st.multiselect(
        "Campaña",
        opciones_campaña,
        default=opciones_campaña
    )

with c2:
    base_asesores = df[df["Campaña"].isin(campañas)]
    opciones_asesor = sorted(base_asesores["Asesor"].unique())

    asesores = st.multiselect(
        "Asesor",
        opciones_asesor,
        default=opciones_asesor
    )

with c3:
    base_tipos = df[df["Campaña"].isin(campañas)]

    opciones_tipificacion = sorted(
        base_tipos["Tipificación"].dropna().unique()
    )

    tipificaciones = st.multiselect(
        "Tipificación",
        opciones_tipificacion,
        default=opciones_tipificacion
    )

fechas = df["Fecha"].dropna()

if not fechas.empty:
    periodo = st.date_input(
        "Período",
        value=(fechas.min().date(), fechas.max().date()),
        min_value=fechas.min().date(),
        max_value=fechas.max().date(),
        format="DD/MM/YYYY"
    )

    if isinstance(periodo, (tuple, list)):
        fecha_inicio = periodo[0]
        fecha_fin = periodo[-1]
    else:
        fecha_inicio = periodo
        fecha_fin = periodo
else:
    fecha_inicio, fecha_fin = None, None


filtrado = df[
    df["Campaña"].isin(campañas) &
    df["Asesor"].isin(asesores) &
    df["Tipificación"].isin(tipificaciones)
].copy()

if fecha_inicio and fecha_fin:
    filtrado = filtrado[
        filtrado["Fecha"].dt.date.between(
            fecha_inicio,
            fecha_fin
        )
    ]

if filtrado.empty:
    st.warning("No hay registros con los filtros seleccionados.")
    st.stop()

detalle_filtrado = construir_detalle_criterios(filtrado)


# =====================================================
# INDICADORES GENERALES
# =====================================================

st.divider()
st.markdown("### Indicadores generales")

k1, k2, k3, k4 = st.columns(4)

promedio = filtrado["Puntaje final"].mean()

k1.metric("Auditorías", len(filtrado))

k2.metric(
    "Calidad promedio",
    f"{promedio:.1f}%" if pd.notna(promedio) else "Sin datos"
)

k3.metric("Asesores", filtrado["Asesor"].nunique())
k4.metric("Campañas", filtrado["Campaña"].nunique())

st.divider()


# =====================================================
# PESTAÑAS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen",
    "Análisis individual",
    "Por campaña",
    "Criterios generales",
    "Detalle de auditorías"
])


# =====================================================
# 1. RESUMEN
# =====================================================

with tab1:

    st.subheader("Evolución de calidad")

    evolucion = filtrado.dropna(subset=["Fecha"]).copy()

    if not evolucion.empty:

        evolucion["Mes"] = evolucion["Fecha"].dt.to_period("M").astype(str)

        evolucion_mensual = evolucion.groupby("Mes").agg(
            Calidad=("Puntaje final", "mean"),
            Auditorías=("Puntaje final", "count")
        ).reset_index()

        evolucion_mensual["Calidad"] = evolucion_mensual["Calidad"].round(1)

        fig = grafico_lineas(
            evolucion_mensual,
            "Mes",
            "Calidad",
            "Evolución mensual de calidad"
        )

        fig.update_yaxes(title="Calidad (%)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Desempeño por asesor")

    tabla = filtrado.groupby("Asesor").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index()

    tabla["Calidad"] = tabla["Calidad"].round(1)
    tabla = tabla.sort_values("Calidad", ascending=True)

    fig = grafico_barras(
        tabla,
        "Calidad",
        "Asesor",
        "Calidad promedio por asesor",
        horizontal=True,
        color=VERDE_MEDIO,
        sufijo="%"
    )

    fig.update_xaxes(title="Calidad (%)")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        tabla.sort_values("Calidad", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("Resultados por tipo de gestión")

    por_tipo = filtrado.groupby("Tipo normalizado").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index()

    por_tipo["Calidad"] = por_tipo["Calidad"].round(1)

    fig = px.bar(
        por_tipo,
        x="Tipo normalizado",
        y="Calidad",
        text="Calidad",
        title="Calidad promedio por tipo de gestión"
    )

    fig.update_traces(
        marker_color=[VERDE_MEDIO, NARANJA][:len(por_tipo)],
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_yaxes(title="Calidad (%)")
    fig.update_xaxes(title="")
    st.plotly_chart(formato_grafico(fig), use_container_width=True)

    st.dataframe(
        por_tipo,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 2. ANÁLISIS INDIVIDUAL
# =====================================================

with tab2:

    st.subheader("Análisis individual del asesor")

    asesor = st.selectbox(
        "Seleccionar asesor",
        sorted(filtrado["Asesor"].unique()),
        key="asesor_individual"
    )

    individual = filtrado[
        filtrado["Asesor"] == asesor
    ].copy()

    criterios_individual = detalle_filtrado[
        detalle_filtrado["Asesor"] == asesor
    ].copy()

    a1, a2, a3, a4 = st.columns(4)

    promedio_individual = individual["Puntaje final"].mean()

    a1.metric("Auditorías", len(individual))

    a2.metric(
        "Calidad promedio",
        f"{promedio_individual:.1f}%"
        if pd.notna(promedio_individual) else "Sin datos"
    )

    a3.metric(
        "Puntos descontados",
        f"{criterios_individual['Descuento'].sum():.1f}"
    )

    a4.metric(
        "Incumplimientos",
        int((criterios_individual["Respuesta"] == "no").sum())
    )

    st.divider()

    # DESCUENTOS

    st.markdown("### 1. Descuentos por criterio")

    if not criterios_individual.empty:

        descuentos = criterios_individual.groupby("Criterio").agg(
            Descuento=("Descuento", "sum"),
            Evaluaciones=("Respuesta", "count"),
            Incumplimientos=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum())
        ).reset_index()

        descuentos = descuentos.sort_values("Descuento", ascending=True)

        fig = grafico_barras(
            descuentos,
            "Descuento",
            "Criterio",
            "Puntos descontados por criterio",
            horizontal=True,
            color=NARANJA
        )

        fig.update_xaxes(title="Puntos descontados")
        fig.update_yaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            descuentos.sort_values("Descuento", ascending=False),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No hay criterios evaluados para este asesor.")

    st.divider()

    # REINCIDENCIAS

    st.markdown("### 2. Reincidencias")

    if not criterios_individual.empty:

        reincidencias = criterios_individual[
            criterios_individual["Respuesta"].isin(
                ["no", "punto de mejora"]
            )
        ].groupby(["Criterio", "Respuesta"]).size().unstack(
            fill_value=0
        ).reset_index()

        if "no" not in reincidencias.columns:
            reincidencias["no"] = 0

        if "punto de mejora" not in reincidencias.columns:
            reincidencias["punto de mejora"] = 0

        reincidencias["Total de apariciones"] = (
            reincidencias["no"] +
            reincidencias["punto de mejora"]
        )

        reincidencias = reincidencias.sort_values(
            "Total de apariciones",
            ascending=False
        )

        reincidencias = reincidencias.rename(columns={
            "no": "Incumplimientos",
            "punto de mejora": "Puntos de mejora"
        })

        st.dataframe(
            reincidencias,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Se contabilizan las apariciones de cada criterio como NO "
            "o Punto de mejora en las auditorías."
        )

    st.divider()

    # FORTALEZAS

    st.markdown("### 3. Fortalezas individuales")

    if not criterios_individual.empty:

        fortalezas = criterios_individual.groupby("Criterio").agg(
            Evaluaciones=("Respuesta", "count"),
            Cumplimientos=("Respuesta", lambda x: (x == "si").sum()),
            N_A=("Respuesta", lambda x: (x == "n/a").sum())
        ).reset_index()

        fortalezas["% Respuestas positivas"] = (
            (fortalezas["Cumplimientos"] + fortalezas["N_A"]) /
            fortalezas["Evaluaciones"] * 100
        )

        fortalezas = fortalezas.sort_values(
            "% Respuestas positivas",
            ascending=False
        )

        st.dataframe(
            fortalezas.round(1),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # EVOLUCIÓN MENSUAL

    st.markdown("### 4. Evolución mensual de calidad")

    mensual = individual.dropna(subset=["Fecha"]).copy()

    if not mensual.empty:

        mensual["Mes"] = mensual["Fecha"].dt.to_period("M").astype(str)

        evolucion_mensual = mensual.groupby("Mes").agg(
            Auditorías=("Puntaje final", "count"),
            Calidad=("Puntaje final", "mean")
        ).reset_index()

        evolucion_mensual["Calidad"] = (
            evolucion_mensual["Calidad"].round(1)
        )

        fig = grafico_lineas(
            evolucion_mensual,
            "Mes",
            "Calidad",
            "Evolución mensual del asesor"
        )

        fig.update_yaxes(title="Calidad (%)")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            evolucion_mensual,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # EVOLUCIÓN POR CRITERIO

    st.markdown("### 5. Evolución de cada criterio")

    if not criterios_individual.empty:

        evolucion_criterios = criterios_individual[
            criterios_individual["Mes"] != ""
        ].copy()

        evolucion_criterios["% obtenido"] = (
            evolucion_criterios["Puntos obtenidos"] /
            evolucion_criterios["Ponderación"] * 100
        )

        tabla_evolucion = evolucion_criterios.pivot_table(
            index="Mes",
            columns="Criterio",
            values="% obtenido",
            aggfunc="mean"
        )

        if not tabla_evolucion.empty:

            fig = px.line(
                tabla_evolucion.reset_index(),
                x="Mes",
                y=tabla_evolucion.columns.tolist(),
                markers=True,
                title="Evolución de criterios"
            )

            fig.update_layout(
                legend_title="Criterios",
                height=480
            )

            st.plotly_chart(
                formato_grafico(fig, altura=480),
                use_container_width=True
            )

            criterio_elegido = st.selectbox(
                "Ver evolución de un criterio específico",
                CRITERIOS_PONDERADOS,
                key="criterio_evolucion"
            )

            detalle_criterio = evolucion_criterios[
                evolucion_criterios["Criterio"] == criterio_elegido
            ]

            evolucion_un_criterio = detalle_criterio.groupby("Mes").agg(
                porcentaje_obtenido=("% obtenido", "mean"),
                Evaluaciones=("Respuesta", "count")
            ).reset_index()

            evolucion_un_criterio = evolucion_un_criterio.rename(
                columns={"porcentaje_obtenido": "% obtenido"}
            )

            evolucion_un_criterio["% obtenido"] = (
                evolucion_un_criterio["% obtenido"].round(1)
            )

            fig = grafico_lineas(
                evolucion_un_criterio,
                "Mes",
                "% obtenido",
                "Evolución del criterio seleccionado"
            )

            fig.update_yaxes(
                title="% de ponderación obtenida",
                range=[0, 105]
            )

            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                evolucion_un_criterio,
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # HISTORIAL

    st.markdown("### 6. Historial de auditorías")

    columnas_historial = [
        "Fecha", "Campaña", "ID", "Tipo de gestión",
        "Tipificación", "Puntaje final",
        "Puntos a trabajar", "Observaciones"
    ]

    historial = individual[columnas_historial].copy()

    historial["Fecha"] = historial["Fecha"].dt.strftime("%d/%m/%Y")
    historial["Puntaje final"] = historial["Puntaje final"].round(1)

    st.dataframe(
        historial.sort_values("Fecha", ascending=False),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 3. POR CAMPAÑA
# =====================================================

with tab3:

    st.subheader("Desempeño por campaña")

    campañas_resumen = filtrado.groupby("Campaña").agg(
        Auditorías=("Puntaje final", "count"),
        Asesores=("Asesor", "nunique"),
        Calidad=("Puntaje final", "mean")
    ).reset_index()

    campañas_resumen["Calidad"] = (
        campañas_resumen["Calidad"].round(1)
    )

    campañas_resumen = campañas_resumen.sort_values(
        "Calidad",
        ascending=True
    )

    fig = grafico_barras(
        campañas_resumen,
        "Calidad",
        "Campaña",
        "Calidad promedio por campaña",
        horizontal=True,
        color=VERDE_MEDIO,
        sufijo="%"
    )

    fig.update_xaxes(title="Calidad (%)")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        campañas_resumen.sort_values("Calidad", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Evolución mensual por campaña")

    base = filtrado.dropna(subset=["Fecha"]).copy()

    if not base.empty:

        base["Mes"] = base["Fecha"].dt.to_period("M").astype(str)

        evolucion_campañas = base.pivot_table(
            index="Mes",
            columns="Campaña",
            values="Puntaje final",
            aggfunc="mean"
        )

        fig = px.line(
            evolucion_campañas.reset_index(),
            x="Mes",
            y=evolucion_campañas.columns.tolist(),
            markers=True,
            title="Evolución de calidad por campaña"
        )

        fig.update_layout(
            legend_title="Campañas",
            height=440
        )

        st.plotly_chart(
            formato_grafico(fig, altura=440),
            use_container_width=True
        )


# =====================================================
# 4. CRITERIOS GENERALES
# =====================================================

with tab4:

    st.subheader("Análisis general de criterios")

    if not detalle_filtrado.empty:

        resumen = detalle_filtrado.groupby("Criterio").agg(
            Evaluaciones=("Respuesta", "count"),
            SI=("Respuesta", lambda x: (x == "si").sum()),
            NO=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum()),
            NA=("Respuesta", lambda x: (x == "n/a").sum()),
            Descuento=("Descuento", "sum")
        ).reset_index()

        resumen["% cumplimiento"] = (
            (resumen["SI"] + resumen["NA"]) /
            resumen["Evaluaciones"] * 100
        )

        resumen["% incumplimiento"] = (
            resumen["NO"] /
            resumen["Evaluaciones"] * 100
        )

        st.markdown("#### Criterios con mayor descuento acumulado")

        mayores_descuentos = resumen.sort_values(
            "Descuento",
            ascending=True
        )

        fig = grafico_barras(
            mayores_descuentos,
            "Descuento",
            "Criterio",
            "Descuentos acumulados por criterio",
            horizontal=True,
            color=NARANJA
        )

        fig.update_xaxes(title="Puntos descontados")
        fig.update_yaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.markdown("#### Porcentaje de incumplimientos")

        incumplimientos = resumen.sort_values(
            "% incumplimiento",
            ascending=True
        )

        fig = grafico_barras(
            incumplimientos,
            "% incumplimiento",
            "Criterio",
            "Incumplimientos por criterio",
            horizontal=True,
            color=ROJO,
            sufijo="%"
        )

        fig.update_xaxes(
            title="% de respuestas NO",
            range=[0, 100]
        )

        fig.update_yaxes(title="")
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.markdown("#### Tabla de resultados por criterio")

        st.dataframe(
            resumen.round(1).sort_values(
                "Descuento",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Los N/A reciben la ponderación completa según la fórmula "
            "de evaluación. Se muestran por separado de los cumplimientos."
        )


# =====================================================
# 5. DETALLE DE AUDITORÍAS
# =====================================================

with tab5:

    st.subheader("Detalle de auditorías")

    columnas = [
        "Fecha", "Asesor", "Campaña", "ID",
        "Tipo de gestión", "Tipificación",
        "Puntaje final", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?",
        "Tipificación correcta"
    ]

    detalle = filtrado[columnas].copy()

    detalle["Fecha"] = detalle["Fecha"].dt.strftime("%d/%m/%Y")
    detalle["Puntaje final"] = detalle["Puntaje final"].round(1)

    st.dataframe(
        detalle.sort_values("Fecha", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    csv = filtrado[columnas].to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    st.download_button(
        "Descargar auditorías en CSV",
        data=csv,
        file_name="auditorias_calidad_contactel.csv",
        mime="text/csv"
    )


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.divider()

st.caption(
    "Calidad y Capacitación | Contactel | "
    "Actualización automática de datos cada 5 minutos."
)

st.caption("La columna AC (Acción) está excluida del análisis.")

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
