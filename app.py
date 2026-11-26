
import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Calidad y Capacitación | Contactel",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background-color:#F5F8F6;}
h1,h2,h3 {color:#174D3A;}
div[data-testid="stMetric"] {
    background:white;
    border:1px solid #DCE8E1;
    padding:14px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

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

URL_HOJA2 = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=1421200336&single=true&output=csv"
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
# FUNCIONES
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

    # Los registros comienzan en la fila 10.
    # Se toman las columnas A:AG.
    # La columna AC (Acción) se elimina del análisis.

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
# CARGA DE DATOS
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
# FILTROS GENERALES
# =====================================================

st.subheader("Filtros generales")

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
# INDICADORES PRINCIPALES
# =====================================================

st.divider()
st.subheader("Indicadores generales")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Auditorías", len(filtrado))

promedio = filtrado["Puntaje final"].mean()

k2.metric(
    "Calidad promedio",
    f"{promedio:.1f}%" if pd.notna(promedio) else "Sin datos"
)

k3.metric("Asesores", filtrado["Asesor"].nunique())
k4.metric("Campañas", filtrado["Campaña"].nunique())


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
        evolucion = (
            evolucion.groupby("Fecha")["Puntaje final"]
            .mean()
            .reset_index()
            .set_index("Fecha")
        )

        st.line_chart(evolucion)

    st.subheader("Resultados por asesor")

    tabla = filtrado.groupby("Asesor").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index()

    tabla["Calidad"] = tabla["Calidad"].round(1)
    tabla = tabla.sort_values("Calidad", ascending=False)

    st.bar_chart(tabla.set_index("Asesor")["Calidad"])

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Resultados por tipo de gestión")

    por_tipo = filtrado.groupby("Tipo normalizado").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad=("Puntaje final", "mean")
    ).reset_index()

    por_tipo["Calidad"] = por_tipo["Calidad"].round(1)

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

    # Indicadores individuales

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

    # 1. Descuentos por criterio

    st.markdown("### 1. Descuentos por criterio")

    if not criterios_individual.empty:

        descuentos = criterios_individual.groupby("Criterio").agg(
            Descuento=("Descuento", "sum"),
            Evaluaciones=("Respuesta", "count"),
            Incumplimientos=("Respuesta", lambda x: (x == "no").sum()),
            Mejoras=("Respuesta", lambda x: (x == "punto de mejora").sum())
        ).reset_index()

        descuentos = descuentos.sort_values(
            "Descuento",
            ascending=False
        )

        st.bar_chart(
            descuentos.set_index("Criterio")["Descuento"]
        )

        st.dataframe(
            descuentos,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No hay criterios evaluados para este asesor.")

    st.divider()

    # 2. Reincidencias

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
            "Se consideran reincidencias los criterios que vuelven a aparecer "
            "como NO o Punto de mejora en distintas auditorías."
        )

    st.divider()

    # 3. Fortalezas individuales

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

    # 4. Evolución mensual de calidad

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

        st.line_chart(
            evolucion_mensual.set_index("Mes")["Calidad"]
        )

        st.dataframe(
            evolucion_mensual,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # 5. Evolución de cada criterio

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

            st.line_chart(tabla_evolucion)

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

            st.line_chart(
                evolucion_un_criterio.set_index("Mes")["% obtenido"]
            )

            st.dataframe(
                evolucion_un_criterio,
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # 6. Historial de auditorías

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

    st.bar_chart(
        campañas_resumen.set_index("Campaña")["Calidad"]
    )

    st.dataframe(
        campañas_resumen,
        use_container_width=True,
        hide_index=True
    )

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

        st.line_chart(evolucion_campañas)


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

        st.markdown("**Criterios con mayor descuento acumulado**")

        mayores_descuentos = resumen.sort_values(
            "Descuento",
            ascending=False
        )

        st.bar_chart(
            mayores_descuentos.set_index("Criterio")["Descuento"]
        )

        st.dataframe(
            resumen.round(1),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "El análisis de cumplimiento considera SI y N/A como respuestas "
            "que obtienen la ponderación completa. Los N/A se identifican "
            "por separado para no confundirlos con criterios efectivamente evaluados."
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
# ACTUALIZACIÓN
# =====================================================

st.divider()

st.caption(
    "Calidad y Capacitación | Contactel | "
    "Actualización automática de datos cada 5 minutos."
)

st.caption(
    "La columna AC (Acción) está excluida del análisis."
)

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
