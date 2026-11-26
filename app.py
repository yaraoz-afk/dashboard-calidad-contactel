import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.set_page_config(
    page_title="Calidad y Capacitación | Contactel",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background-color:#F5F8F6;}
h1, h2, h3, h4, p, label, span, div {color:#17211C;}
div[data-testid="stMetric"] {
    background:white; border:1px solid #DCE8E1;
    padding:14px; border-radius:10px;
}
div[data-testid="stMetric"] label {color:#26332C !important;}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color:#111111 !important;
}
.insight-box {
    background:white;
    border-left:4px solid #1F6F50;
    border-top:1px solid #DCE8E1;
    border-right:1px solid #DCE8E1;
    border-bottom:1px solid #DCE8E1;
    padding:14px 16px;
    border-radius:8px;
    margin-bottom:10px;
}
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
def convertir_puntaje(valor):
    try:
        numero = float(str(valor).replace("%", "").replace(",", ".").strip())
        return numero * 100 if numero <= 1 else numero
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

        if respuesta in ("si", "sí", "n/a"):
            obtenido += peso
        elif respuesta == "punto de mejora":
            obtenido += peso / 2

    return (obtenido / posible * 100) if posible else None


@st.cache_data(ttl=300)
def leer_mediciones():
    bruto = pd.read_csv(
        URL_MEDICION, header=None, dtype=str, keep_default_na=False
    )

    # Los registros comienzan en la fila 10.
    # Se leen A:AG y se excluye por completo AC (Acción).
    datos = bruto.iloc[9:, :33].copy()
    datos.columns = (
        ["Fecha", "Mes", "Asesor", "Campaña", "ID",
         "Duración", "Tipo de gestión", "Tipificación"]
        + CRITERIOS
        + ["Puntos a trabajar", "Acción", "Puntaje",
           "Observaciones", "¿Tipifica bien?", "Tipificación correcta"]
    )
    datos = datos.drop(columns=["Acción"])

    for col in datos.columns:
        datos[col] = datos[col].astype(str).str.strip()

    datos = datos[
        (datos["Asesor"] != "") &
        (datos["Campaña"] != "")
    ].copy()

    datos["Fecha"] = pd.to_datetime(
        datos["Fecha"], dayfirst=True, errors="coerce"
    )
    datos["Puntaje oficial"] = datos["Puntaje"].apply(convertir_puntaje)
    datos["Puntaje calculado"] = datos.apply(calcular_puntaje, axis=1)
    datos["Puntaje final"] = datos["Puntaje oficial"].fillna(
        datos["Puntaje calculado"]
    )
    datos["Tipo normalizado"] = datos["Tipo de gestión"].apply(normalizar_tipo)
    datos["Mes"] = datos["Fecha"].dt.to_period("M").astype(str)
    datos["Año"] = datos["Fecha"].dt.year

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
                "Tipo de gestión": tipo,
                "Criterio": criterio,
                "Dimensión": DIMENSION_CRITERIO.get(criterio, "Comercial"),
                "Respuesta": respuesta,
                "Ponderación": peso,
                "Descuento": descuento,
                "Puntos obtenidos": puntos
            })
    return pd.DataFrame(registros)


def estilo_grafico(fig, titulo, eje_x=None, eje_y=None):
    fig.update_layout(
        title=dict(text=titulo, font=dict(color="#000000", size=19)),
        font=dict(color="#000000", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#000000")),
        margin=dict(l=20, r=20, t=65, b=35),
        hoverlabel=dict(font=dict(color="#000000"))
    )
    fig.update_xaxes(
        title_text=eje_x,
        color="#000000",
        title_font=dict(color="#000000"),
        tickfont=dict(color="#000000"),
        gridcolor="#E2E8E4"
    )
    fig.update_yaxes(
        title_text=eje_y,
        color="#000000",
        title_font=dict(color="#000000"),
        tickfont=dict(color="#000000"),
        gridcolor="#E2E8E4"
    )
    return fig


def mostrar_tabla(datos, columnas=None):
    if datos.empty:
        st.info("No hay datos para mostrar con la selección actual.")
    else:
        st.dataframe(
            datos if columnas is None else datos[columnas],
            use_container_width=True,
            hide_index=True
        )


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
        (res["Incumplimientos"] + res["Mejoras"]) / res["Evaluaciones"] * 100
    ).round(1)
    res["Descuento"] = res["Descuento"].round(1)
    return res.sort_values(["Descuento", "% crítico"], ascending=[False, False])


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
if df_con_fecha.empty:
    st.warning("No se encontraron fechas válidas en las auditorías.")
    st.stop()

# =====================================================
# FILTROS GENERALES
# =====================================================
st.subheader("Filtros generales")

f1, f2, f3 = st.columns(3)

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

with f3:
    base_tipos = df[df["Campaña"].isin(campañas)] if campañas else df
    opciones_tipificacion = sorted(
        x for x in base_tipos["Tipificación"].dropna().unique() if x
    )
    tipificaciones = st.multiselect(
        "Tipificación", opciones_tipificacion,
        default=opciones_tipificacion, key="filtro_tipificaciones"
    )

p1, p2 = st.columns([1.2, 1.8])

fecha_min = df_con_fecha["Fecha"].min().date()
fecha_max = df_con_fecha["Fecha"].max().date()

with p1:
    periodo = st.date_input(
        "Período (rango de fechas)",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
        format="DD/MM/YYYY",
        key="filtro_rango_fechas"
    )

with p2:
    meses_disponibles = sorted(
        m for m in df_con_fecha["Mes"].dropna().unique() if m and m != "NaT"
    )
    meses_seleccionados = st.multiselect(
        "Elegir meses específicos (opcional — vacío usa todo el rango de fechas)",
        options=meses_disponibles,
        default=[],
        key="filtro_meses",
        help="Si seleccionás uno o varios meses, se filtran esos meses dentro del rango de fechas elegido."
    )

if isinstance(periodo, tuple) and len(periodo) == 2:
    fecha_inicio, fecha_fin = periodo
elif isinstance(periodo, tuple) and len(periodo) == 1:
    fecha_inicio = fecha_fin = periodo[0]
else:
    fecha_inicio, fecha_fin = fecha_min, fecha_max

filtrado = df[
    df["Campaña"].isin(campañas) &
    df["Asesor"].isin(asesores) &
    df["Tipificación"].isin(tipificaciones)
].copy()

filtrado = filtrado[
    filtrado["Fecha"].dt.date.between(fecha_inicio, fecha_fin)
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

k1, k2, k3, k4 = st.columns(4)
k1.metric("Auditorías", len(filtrado))
promedio = filtrado["Puntaje final"].mean()
k2.metric("Calidad promedio", f"{promedio:.1f}%" if pd.notna(promedio) else "Sin datos")
k3.metric("Asesores", filtrado["Asesor"].nunique())
k4.metric("Campañas", filtrado["Campaña"].nunique())

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
            default=sorted(filtrado["Asesor"].unique())[:5],
            key="evol_ases_sel"
        )

    base_evol = filtrado[
        filtrado["Campaña"].isin(camp_evol) &
        filtrado["Asesor"].isin(ases_evol)
    ].dropna(subset=["Fecha"]).copy()

    g1, g2 = st.columns(2)

    with g1:
        evol_camp = base_evol.groupby(["Mes", "Campaña"], as_index=False).agg(
            Auditorías=("Puntaje final", "count"),
            Calidad=("Puntaje final", "mean")
        ).sort_values(["Mes", "Campaña"])
        if not evol_camp.empty:
            fig = px.line(
                evol_camp, x="Mes", y="Calidad", color="Campaña", markers=True,
                labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
            )
            st.plotly_chart(
                estilo_grafico(fig, "Evolución mensual por campaña", "Mes", "Calidad (%)"),
                use_container_width=True
            )

    with g2:
        evol_ases = base_evol.groupby(["Mes", "Asesor"], as_index=False).agg(
            Auditorías=("Puntaje final", "count"),
            Calidad=("Puntaje final", "mean")
        ).sort_values(["Mes", "Asesor"])
        if not evol_ases.empty:
            fig = px.line(
                evol_ases, x="Mes", y="Calidad", color="Asesor", markers=True,
                labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
            )
            st.plotly_chart(
                estilo_grafico(fig, "Evolución mensual por asesor", "Mes", "Calidad (%)"),
                use_container_width=True
            )

    st.subheader("Resultados por asesor")
    tabla_asesores = filtrado.groupby("Asesor").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index().sort_values("Calidad", ascending=False)
    tabla_asesores["Calidad"] = tabla_asesores["Calidad"].round(1)

    fig = px.bar(
        tabla_asesores, x="Asesor", y="Calidad",
        labels={"Calidad": "Calidad promedio (%)", "Asesor": "Asesor"},
        text="Calidad"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(
        estilo_grafico(fig, "Calidad promedio por asesor", "Asesor", "Calidad (%)"),
        use_container_width=True
    )
    mostrar_tabla(tabla_asesores)

    st.subheader("Resultados por tipo de gestión")
    por_tipo = filtrado.groupby("Tipo normalizado").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index()
    por_tipo["Calidad"] = por_tipo["Calidad"].round(1)
    mostrar_tabla(por_tipo)

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
    prom_ind = individual["Puntaje final"].mean()
    a2.metric("Puntuación de calidad", f"{prom_ind:.1f}%" if pd.notna(prom_ind) else "Sin datos")
    a3.metric("Puntos descontados", f"{criterios_individual['Descuento'].sum():.1f}")
    a4.metric("Incumplimientos", int((criterios_individual["Respuesta"] == "no").sum()))

    st.markdown("#### Aspectos críticos: Comerciales vs. Actitudinales")
    res_dim = resumen_por_dimension(criterios_individual)

    c_com, c_act = st.columns(2)
    with c_com:
        st.markdown("**Aspectos críticos comerciales**")
        top_com = res_dim[res_dim["Dimensión"] == "Comercial"].head(5)
        mostrar_tabla(top_com[[
            "Criterio", "Descuento", "Incumplimientos", "Mejoras", "% crítico"
        ]])

    with c_act:
        st.markdown("**Aspectos críticos actitudinales**")
        top_act = res_dim[res_dim["Dimensión"] == "Actitudinal"].head(5)
        mostrar_tabla(top_act[[
            "Criterio", "Descuento", "Incumplimientos", "Mejoras", "% crítico"
        ]])

    st.markdown("#### Aspectos a trabajar reportados en auditoría")
    puntos_trabajar = individual[
        individual["Puntos a trabajar"].str.strip() != ""
    ][["Fecha", "Campaña", "Puntaje final", "Puntos a trabajar", "Observaciones"]].copy()
    if not puntos_trabajar.empty:
        puntos_trabajar["Fecha"] = puntos_trabajar["Fecha"].dt.strftime("%d/%m/%Y")
        puntos_trabajar["Puntaje final"] = puntos_trabajar["Puntaje final"].round(1)
        puntos_trabajar = puntos_trabajar.sort_values("Fecha", ascending=False)
    mostrar_tabla(puntos_trabajar)

    st.markdown("#### Descuentos por criterio")
    if not criterios_individual.empty:
        descuentos = criterios_individual.groupby(["Criterio", "Dimensión"]).agg(
            Descuento=("Descuento", "sum"),
            Evaluaciones=("Respuesta", "count"),
            Incumplimientos=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum())
        ).reset_index().sort_values("Descuento", ascending=False)
        descuentos["Descuento"] = descuentos["Descuento"].round(1)

        fig = px.bar(
            descuentos, x="Descuento", y="Criterio", color="Dimensión", orientation="h",
            labels={"Descuento": "Puntos descontados", "Criterio": "Criterio"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Puntos descontados por criterio", "Puntos", "Criterio"),
            use_container_width=True
        )
        mostrar_tabla(descuentos)

        st.markdown("#### Reincidencias")
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
        mostrar_tabla(reinc)

        st.markdown("#### Fortalezas individuales")
        fortalezas = criterios_individual.groupby(["Criterio", "Dimensión"]).agg(
            Evaluaciones=("Respuesta", "count"),
            Cumplimientos=("Respuesta", lambda x: x.isin(["si", "sí"]).sum()),
            N_A=("Respuesta", lambda x: (x == "n/a").sum())
        ).reset_index()
        fortalezas["% respuestas positivas"] = (
            (fortalezas["Cumplimientos"] + fortalezas["N_A"]) /
            fortalezas["Evaluaciones"] * 100
        ).round(1)
        fortalezas = fortalezas.sort_values("% respuestas positivas", ascending=False)
        mostrar_tabla(fortalezas)

    st.markdown("#### Evolución mensual del asesor")
    mensual = individual.dropna(subset=["Fecha"]).groupby("Mes").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index().sort_values("Mes")
    if not mensual.empty:
        fig = px.line(
            mensual, x="Mes", y="Calidad", markers=True,
            labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Evolución mensual", "Mes", "Calidad (%)"),
            use_container_width=True
        )
        mensual["Calidad"] = mensual["Calidad"].round(1)
        mostrar_tabla(mensual)

    st.markdown("#### Historial de auditorías")
    cols_hist = [
        "Fecha", "Campaña", "ID", "Tipo de gestión", "Tipificación",
        "Puntaje final", "Puntos a trabajar", "Observaciones"
    ]
    historial = individual[cols_hist].copy()
    historial["Fecha"] = historial["Fecha"].dt.strftime("%d/%m/%Y")
    historial["Puntaje final"] = historial["Puntaje final"].round(1)
    mostrar_tabla(historial.sort_values("Fecha", ascending=False))

# =====================================================
# 3. POR CAMPAÑA
# =====================================================
with tab3:
    st.subheader("Desempeño por campaña")
    resumen_camp = filtrado.groupby("Campaña").agg(
        Auditorías=("Puntaje final", "count"),
        Asesores=("Asesor", "nunique"),
        Calidad=("Puntaje final", "mean")
    ).reset_index().sort_values("Calidad", ascending=False)
    resumen_camp["Calidad"] = resumen_camp["Calidad"].round(1)

    fig = px.bar(
        resumen_camp, x="Campaña", y="Calidad", text="Calidad",
        labels={"Calidad": "Calidad promedio (%)", "Campaña": "Campaña"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(
        estilo_grafico(fig, "Calidad promedio por campaña", "Campaña", "Calidad (%)"),
        use_container_width=True
    )
    mostrar_tabla(resumen_camp)

    st.subheader("Evolución mensual por campaña")
    base_camp = filtrado.dropna(subset=["Fecha"]).copy()
    if not base_camp.empty:
        mensual_camp = base_camp.groupby(["Mes", "Campaña"], as_index=False).agg(
            Auditorías=("Puntaje final", "count"),
            Calidad=("Puntaje final", "mean")
        )
        fig = px.line(
            mensual_camp, x="Mes", y="Calidad", color="Campaña",
            markers=True, labels={"Calidad": "Calidad promedio (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Evolución mensual por campaña", "Mes", "Calidad (%)"),
            use_container_width=True
        )
        mensual_camp["Calidad"] = mensual_camp["Calidad"].round(1)
        mostrar_tabla(mensual_camp.sort_values(["Mes", "Campaña"]))

# =====================================================
# 4. HISTÓRICO GENERAL DE EMPRESA
# =====================================================
with tab4:
    st.subheader("Histórico general de Calidad | Empresa")

    años = sorted(df_con_fecha["Año"].dropna().astype(int).unique())
    año_actual_datos = int(df_con_fecha["Año"].max())
    año_sel_empresa = st.selectbox(
        "Año a consultar", años,
        index=años.index(año_actual_datos),
        key="año_historico_empresa"
    )

    empresa_anual = df_con_fecha[df_con_fecha["Año"] == año_sel_empresa].copy()

    m1, m2, m3 = st.columns(3)
    puntaje_anual = promedio_anual(empresa_anual)
    m1.metric(
        f"Puntuación total empresa {año_sel_empresa}",
        f"{puntaje_anual:.1f}%" if pd.notna(puntaje_anual) else "Sin datos"
    )
    m2.metric("Auditorías del año", len(empresa_anual))
    m3.metric("Campañas del año", empresa_anual["Campaña"].nunique())

    st.markdown("#### Evolución mensual de la empresa")
    empresa_mensual = empresa_anual.groupby("Mes", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values("Mes")

    if not empresa_mensual.empty:
        fig = px.line(
            empresa_mensual, x="Mes", y="Calidad", markers=True,
            labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Promedio mensual de calidad | Empresa", "Mes", "Calidad (%)"),
            use_container_width=True
        )
        tabla_mensual_empresa = empresa_mensual.copy()
        tabla_mensual_empresa["Calidad"] = tabla_mensual_empresa["Calidad"].round(1)
        mostrar_tabla(tabla_mensual_empresa)

    st.markdown("#### Desglose mensual por campaña")
    empresa_mes_camp = empresa_anual.groupby(["Mes", "Campaña"], as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values(["Mes", "Campaña"])

    if not empresa_mes_camp.empty:
        fig = px.line(
            empresa_mes_camp, x="Mes", y="Calidad", color="Campaña",
            markers=True, labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Calidad mensual por campaña | Empresa", "Mes", "Calidad (%)"),
            use_container_width=True
        )
        tabla_mes_camp = empresa_mes_camp.copy()
        tabla_mes_camp["Calidad"] = tabla_mes_camp["Calidad"].round(1)
        mostrar_tabla(tabla_mes_camp)

    st.markdown("#### Promedio anual por campaña")
    empresa_por_camp = empresa_anual.groupby("Campaña", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Asesores=("Asesor", "nunique"),
        Calidad=("Puntaje final", "mean")
    ).sort_values("Calidad", ascending=False)
    empresa_por_camp["Calidad"] = empresa_por_camp["Calidad"].round(1)
    mostrar_tabla(empresa_por_camp)

# =====================================================
# 5. HISTÓRICO POR ASESOR Y CAMPAÑA
# =====================================================
with tab5:
    st.subheader("Histórico mensual por asesor y campaña")
    asesores_historico = sorted(df_con_fecha["Asesor"].dropna().unique())
    asesor_historico = st.selectbox(
        "Seleccionar asesor", asesores_historico,
        key="asesor_historico"
    )

    años_asesor = sorted(
        df_con_fecha[df_con_fecha["Asesor"] == asesor_historico]["Año"]
        .dropna().astype(int).unique()
    )
    año_sel_asesor = st.selectbox(
        "Año",
        options=años_asesor,
        index=max(0, len(años_asesor) - 1),
        key="año_historico_asesor"
    )

    base_asesor_hist = df_con_fecha[
        (df_con_fecha["Asesor"] == asesor_historico) &
        (df_con_fecha["Año"] == año_sel_asesor)
    ].copy()

    b1, b2, b3 = st.columns(3)
    b1.metric("Auditorías", len(base_asesor_hist))
    prom_asesor_anual = base_asesor_hist["Puntaje final"].mean()
    b2.metric(
        "Promedio anual del asesor",
        f"{prom_asesor_anual:.1f}%" if pd.notna(prom_asesor_anual) else "Sin datos"
    )
    b3.metric("Campañas", base_asesor_hist["Campaña"].nunique())

    st.markdown("#### Evolución mensual: una línea por campaña")
    asesor_mes_camp = base_asesor_hist.groupby(
        ["Mes", "Campaña"], as_index=False
    ).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values(["Mes", "Campaña"])

    if not asesor_mes_camp.empty:
        fig = px.line(
            asesor_mes_camp, x="Mes", y="Calidad", color="Campaña",
            markers=True, labels={"Mes": "Mes", "Calidad": "Calidad promedio (%)"}
        )
        st.plotly_chart(
            estilo_grafico(
                fig, f"Evolución mensual por campaña | {asesor_historico}",
                "Mes", "Calidad (%)"
            ),
            use_container_width=True
        )

        tabla_asesor_mes = asesor_mes_camp.copy()
        tabla_asesor_mes["Calidad"] = tabla_asesor_mes["Calidad"].round(1)
        mostrar_tabla(tabla_asesor_mes)

    st.markdown("#### Promedio anual por campaña del asesor")
    asesor_por_camp = base_asesor_hist.groupby("Campaña", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values("Calidad", ascending=False)
    asesor_por_camp["Calidad"] = asesor_por_camp["Calidad"].round(1)
    mostrar_tabla(asesor_por_camp)

# =====================================================
# 6. CRITERIOS Y DETALLE DE AUDITORÍAS
# =====================================================
with tab6:
    st.subheader("Análisis general de criterios")
    if not detalle_filtrado.empty:
        resumen_criterios = detalle_filtrado.groupby(["Criterio", "Dimensión"]).agg(
            Evaluaciones=("Respuesta", "count"),
            SI=("Respuesta", lambda x: x.isin(["si", "sí"]).sum()),
            NO=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum()),
            NA=("Respuesta", lambda x: (x == "n/a").sum()),
            Descuento=("Descuento", "sum")
        ).reset_index()

        resumen_criterios["% cumplimiento"] = (
            (resumen_criterios["SI"] + resumen_criterios["NA"]) /
            resumen_criterios["Evaluaciones"] * 100
        )
        resumen_criterios["% incumplimiento"] = (
            resumen_criterios["NO"] /
            resumen_criterios["Evaluaciones"] * 100
        )

        mayores = resumen_criterios.sort_values("Descuento", ascending=False)
        fig = px.bar(
            mayores, x="Descuento", y="Criterio", color="Dimensión", orientation="h",
            labels={"Descuento": "Puntos descontados", "Criterio": "Criterio"}
        )
        st.plotly_chart(
            estilo_grafico(fig, "Criterios con mayor descuento", "Puntos", "Criterio"),
            use_container_width=True
        )
        tabla_criterios = resumen_criterios.round(1)
        mostrar_tabla(tabla_criterios)

    st.divider()
    st.subheader("Detalle de auditorías")
    columnas_detalle = [
        "Fecha", "Asesor", "Campaña", "ID", "Tipo de gestión",
        "Tipificación", "Puntaje final", "Puntos a trabajar",
        "Observaciones", "¿Tipifica bien?", "Tipificación correcta"
    ]
    detalle = filtrado[columnas_detalle].copy()
    detalle["Fecha"] = detalle["Fecha"].dt.strftime("%d/%m/%Y")
    detalle["Puntaje final"] = detalle["Puntaje final"].round(1)
    mostrar_tabla(detalle.sort_values("Fecha", ascending=False))

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
# 7. ANÁLISIS RÁPIDO Y RECOMENDACIONES
# =====================================================
with tab7:
    st.subheader("Diagnóstico rápido y recomendaciones accionables")
    st.caption("Calculado automáticamente sobre los registros filtrados actualmente.")

    res_global_dim = resumen_por_dimension(detalle_filtrado)
    ranking_asesores = filtrado.groupby("Asesor", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values("Calidad", ascending=True)

    ranking_campanas = filtrado.groupby("Campaña", as_index=False).agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).sort_values("Calidad", ascending=True)

    hallazgos = []

    if not ranking_asesores.empty:
        peor_asesor = ranking_asesores.iloc[0]
        mejor_asesor = ranking_asesores.iloc[-1]
        hallazgos.append(
            f"**Asesores:** Mayor oportunidad de mejora en **{peor_asesor['Asesor']}** "
            f"({peor_asesor['Calidad']:.1f}% en {int(peor_asesor['Auditorías'])} auditorías); "
            f"referente del período: **{mejor_asesor['Asesor']}** ({mejor_asesor['Calidad']:.1f}%)."
        )

    if not ranking_campanas.empty:
        peor_camp = ranking_campanas.iloc[0]
        hallazgos.append(
            f"**Campañas:** **{peor_camp['Campaña']}** registra el menor promedio del filtro "
            f"({peor_camp['Calidad']:.1f}%)."
        )

    top_com_global = res_global_dim[res_global_dim["Dimensión"] == "Comercial"]
    if not top_com_global.empty:
        c_crit = top_com_global.iloc[0]
        rec_c = RECOMENDACIONES_CRITERIO.get(c_crit["Criterio"], "Reforzar práctica guiada en coaching.")
        hallazgos.append(
            f"**Aspecto comercial más crítico:** **{c_crit['Criterio']}** "
            f"({c_crit['Descuento']:.1f} pts descontados / {c_crit['% crítico']:.1f}% crítico). "
            f"*Recomendación:* {rec_c}"
        )

    top_act_global = res_global_dim[res_global_dim["Dimensión"] == "Actitudinal"]
    if not top_act_global.empty:
        a_crit = top_act_global.iloc[0]
        rec_a = RECOMENDACIONES_CRITERIO.get(a_crit["Criterio"], "Trabajar tono y cercanía en llamada.")
        hallazgos.append(
            f"**Aspecto actitudinal más crítico:** **{a_crit['Criterio']}** "
            f"({a_crit['Descuento']:.1f} pts descontados / {a_crit['% crítico']:.1f}% crítico). "
            f"*Recomendación:* {rec_a}"
        )

    if "¿Tipifica bien?" in filtrado.columns:
        mal_tip = filtrado[filtrado["¿Tipifica bien?"].str.lower().isin(["no", "incorrecto"])]
        if not mal_tip.empty:
            pct_tip = len(mal_tip) / len(filtrado) * 100
            hallazgos.append(
                f"**Tipificación:** {len(mal_tip)} auditorías ({pct_tip:.1f}%) presentan error de tipificación. "
                f"*Recomendación:* revisar catálogo de motivos y validar cierre de gestión en calibraciones."
            )

    for h in hallazgos:
        st.markdown(f'<div class="insight-box">{h}</div>', unsafe_allow_html=True)

    st.markdown("#### Plan de acción sugerido por criterio crítico")
    if not res_global_dim.empty:
        plan = res_global_dim.head(6).copy()
        plan["Acción recomendada"] = plan["Criterio"].map(
            lambda c: RECOMENDACIONES_CRITERIO.get(c, "Realizar coaching 1 a 1.")
        )
        mostrar_tabla(plan[[
            "Dimensión", "Criterio", "Descuento", "% crítico", "Acción recomendada"
        ]])

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
