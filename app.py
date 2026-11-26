import streamlit as st
import pandas as pd
import re
from datetime import date

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Calidad y Capacitación | Contactel",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #F5F8F6;
    }
    h1, h2, h3 {
        color: #174D3A;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #DCE8E1;
        padding: 15px;
        border-radius: 10px;
    }
    div[data-testid="stMetric"] label {
        color: #527263;
    }
    .titulo {
        color: #174D3A;
        font-size: 30px;
        font-weight: 700;
    }
    .subtitulo {
        color: #668276;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUENTES DE GOOGLE SHEETS
# =========================================================

URL_MEDICION = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=0&single=true&output=csv"
)

URL_MEDICION_ASESOR = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=846850309&single=true&output=csv"
)

URL_HISTORICO_CAMPANIA = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=1211851562&single=true&output=csv"
)

URL_HOJA2 = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/"
    "pub?gid=1421200336&single=true&output=csv"
)


# =========================================================
# CRITERIOS Y PONDERACIONES
# =========================================================

CRITERIOS = {
    "I": "Genera conexión positiva y de confianza en presentación",
    "J": "Explica motivo de llamada claramente",
    "K": "Tipo de preguntas realizadas",
    "L": "Explora necesidades reales",
    "M": "Escucha activa",
    "N": "Propuesta adaptada al cliente",
    "O": "Explica beneficios",
    "P": "Usa ejemplos / comparaciones",
    "Q": "No realiza monólogo",
    "R": "Avanza hacia el cierre",
    "S": "Identifica objeción real",
    "T": "Maneja objeciones",
    "U": "Realiza cierres parciales",
    "V": "Indica Valor a abonar",
    "W": "Sin connotación de obligatoriedad",
    "X": "Realiza de forma correcta cierres legales",
    "Y": "Tono natural y entusiasta",
    "Z": "Evita frases robotizadas",
    "AA": "Tuteo al cliente/Cortesía"
}

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

COLUMNAS = [
    "Fecha", "Mes", "Asesor", "Campaña", "ID",
    "Duración", "Tipo de gestión", "Tipificación"
]

COLUMNAS += list(CRITERIOS.values())

COLUMNAS += [
    "Puntos a trabajar",
    "Puntaje",
    "Observaciones",
    "¿Tipifica bien?",
    "Tipificación correcta"
]

COLUMNAS_CRITERIOS = list(CRITERIOS.values())


# =========================================================
# LECTURA DE DATOS
# =========================================================

@st.cache_data(ttl=300)
def leer_csv(url):
    return pd.read_csv(
        url,
        header=None,
        dtype=str,
        keep_default_na=False
    )


@st.cache_data(ttl=300)
def cargar_mediciones():
    bruto = leer_csv(URL_MEDICION)

    # Los registros comienzan en la fila 10.
    # La columna AC (Acción) se excluye.
    datos = bruto.iloc[9:, :33].copy()

    datos = datos.reindex(columns=range(33))
    datos.columns = [
        "Fecha", "Mes", "Asesor", "Campaña", "ID",
        "Duración", "Tipo de gestión", "Tipificación"
    ] + COLUMNAS_CRITERIOS + [
        "Puntos a trabajar",
        "AC_EXCLUIDA",
        "Puntaje",
        "Observaciones",
        "¿Tipifica bien?",
        "Tipificación correcta"
    ]

    datos = datos.drop(columns=["AC_EXCLUIDA"])

    for columna in datos.columns:
        datos[columna] = datos[columna].astype(str).str.strip()

    datos = datos[
        (datos["Asesor"] != "") &
        (datos["Campaña"] != "")
    ].copy()

    datos["Fecha"] = pd.to_datetime(
        datos["Fecha"],
        dayfirst=True,
        errors="coerce"
    )

    datos["Puntaje oficial"] = datos["Puntaje"].apply(convertir_puntaje)

    datos["Puntaje calculado"] = datos.apply(
        calcular_puntaje,
        axis=1
    )

    datos["Puntaje final"] = datos["Puntaje oficial"].fillna(
        datos["Puntaje calculado"]
    )

    return datos


def convertir_puntaje(valor):
    if valor is None:
        return None

    texto = str(valor).strip().replace("%", "").replace(",", ".")

    try:
        numero = float(texto)
        if numero <= 1:
            numero = numero * 100
        return numero
    except:
        return None


def tipo_gestion_normalizado(valor):
    texto = str(valor).strip().lower()

    if "no venta" in texto:
        return "No Venta"

    if "venta" in texto:
        return "Venta"

    return None


def calcular_puntaje(fila):
    tipo = tipo_gestion_normalizado(fila["Tipo de gestión"])

    if tipo is None:
        return None

    columna_ponderacion = 0 if tipo == "Venta" else 1

    total_obtenido = 0
    total_posible = 0

    for criterio in COLUMNAS_CRITERIOS:

        if criterio not in PONDERACIONES:
            continue

        ponderacion = PONDERACIONES[criterio][columna_ponderacion]
        respuesta = str(fila[criterio]).strip().lower()

        total_posible += ponderacion

        if respuesta == "si":
            total_obtenido += ponderacion

        elif respuesta == "punto de mejora":
            total_obtenido += ponderacion / 2

        elif respuesta == "n/a":
            total_obtenido += ponderacion

    if total_posible == 0:
        return None

    return (total_obtenido / total_posible) * 100


# =========================================================
# TIPIFICACIONES POR CAMPAÑA
# =========================================================

@st.cache_data(ttl=300)
def cargar_tipificaciones():
    bruto = leer_csv(URL_HOJA2)

    if bruto.shape[1] <= 10:
        return {}

    auxiliar = bruto.iloc[:, [9, 10]].copy()
    auxiliar.columns = ["Campaña", "Tipificación"]

    auxiliar["Campaña"] = auxiliar["Campaña"].astype(str).str.strip()
    auxiliar["Tipificación"] = auxiliar["Tipificación"].astype(str).str.strip()

    auxiliar = auxiliar[
        (auxiliar["Campaña"] != "") &
        (auxiliar["Tipificación"] != "")
    ]

    resultado = {}

    for campaña, grupo in auxiliar.groupby("Campaña"):
        resultado[campaña] = sorted(
            grupo["Tipificación"].unique().tolist()
        )

    return resultado


# =========================================================
# ANÁLISIS DE CRITERIOS
# =========================================================

def preparar_criterios(datos):
    registros = []

    for _, fila in datos.iterrows():

        tipo = tipo_gestion_normalizado(fila["Tipo de gestión"])

        if tipo is None:
            continue

        for criterio in COLUMNAS_CRITERIOS:

            if criterio not in PONDERACIONES:
                continue

            respuesta = str(fila[criterio]).strip().lower()

            registros.append({
                "Fecha": fila["Fecha"],
                "Asesor": fila["Asesor"],
                "Campaña": fila["Campaña"],
                "Tipo de gestión": tipo,
                "Criterio": criterio,
                "Respuesta": respuesta
            })

    return pd.DataFrame(registros)


def resumen_criterios(datos):
    if datos.empty:
        return pd.DataFrame()

    evaluados = datos[
        datos["Respuesta"].isin(["si", "no", "punto de mejora"])
    ]

    if evaluados.empty:
        return pd.DataFrame()

    resumen = evaluados.groupby("Criterio").agg(
        Evaluaciones=("Respuesta", "count"),
        Cumplimientos=("Respuesta", lambda x: (x == "si").sum()),
        Incumplimientos=("Respuesta", lambda x: (x == "no").sum()),
        Puntos_de_mejora=("Respuesta", lambda x: (x == "punto de mejora").sum())
    ).reset_index()

    resumen["% Cumplimiento"] = (
        resumen["Cumplimientos"] / resumen["Evaluaciones"] * 100
    )

    resumen["% Incumplimiento"] = (
        resumen["Incumplimientos"] / resumen["Evaluaciones"] * 100
    )

    return resumen.sort_values("% Cumplimiento")


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    '<div class="titulo">Calidad y Capacitación</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Panel de seguimiento de desempeño | Contactel</div>',
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# CARGA PRINCIPAL
# =========================================================

try:
    df = cargar_mediciones()
    mapa_tipificaciones = cargar_tipificaciones()

except Exception as error:
    st.error("No se pudieron cargar los datos de Google Sheets.")
    st.code(str(error))
    st.stop()


if df.empty:
    st.warning("Todavía no hay registros disponibles para mostrar.")
    st.stop()


# =========================================================
# FILTROS
# =========================================================

st.subheader("Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    campañas_disponibles = sorted(df["Campaña"].dropna().unique().tolist())

    campañas = st.multiselect(
        "Campaña",
        campañas_disponibles,
        default=campañas_disponibles
    )

with col2:
    if campañas:
        asesores_disponibles = sorted(
            df[df["Campaña"].isin(campañas)]["Asesor"].dropna().unique().tolist()
        )
    else:
        asesores_disponibles = sorted(df["Asesor"].dropna().unique().tolist())

    asesores = st.multiselect(
        "Asesor",
        asesores_disponibles,
        default=asesores_disponibles
    )

with col3:
    if campañas:
        tipificaciones_disponibles = sorted(set(
            tip
            for campaña in campañas
            for tip in mapa_tipificaciones.get(campaña, [])
        ))
    else:
        tipificaciones_disponibles = sorted(
            df["Tipificación"].dropna().unique().tolist()
        )

    # Se incluyen también las tipificaciones realmente registradas.
    tipificaciones_disponibles = sorted(set(
        tipificaciones_disponibles +
        df[df["Campaña"].isin(campañas)]["Tipificación"].dropna().unique().tolist()
    ))

    tipificaciones = st.multiselect(
        "Tipificación",
        tipificaciones_disponibles,
        default=tipificaciones_disponibles
    )


# Filtro de fechas
fechas_validas = df["Fecha"].dropna()

if not fechas_validas.empty:
    fecha_min = fechas_validas.min().date()
    fecha_max = fechas_validas.max().date()

    rango_fechas = st.date_input(
        "Período de análisis",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
        format="DD/MM/YYYY"
    )
else:
    rango_fechas = None


# =========================================================
# APLICAR FILTROS
# =========================================================

filtrado = df.copy()

if campañas:
    filtrado = filtrado[filtrado["Campaña"].isin(campañas)]
else:
    filtrado = filtrado.iloc[0:0]

if asesores:
    filtrado = filtrado[filtrado["Asesor"].isin(asesores)]
else:
    filtrado = filtrado.iloc[0:0]

if tipificaciones:
    filtrado = filtrado[filtrado["Tipificación"].isin(tipificaciones)]
else:
    filtrado = filtrado.iloc[0:0]

if rango_fechas and len(rango_fechas) == 2:
    inicio, fin = rango_fechas

    filtrado = filtrado[
        filtrado["Fecha"].dt.date.between(inicio, fin)
    ]


if filtrado.empty:
    st.warning("No hay registros que coincidan con los filtros seleccionados.")
    st.stop()


criterios_filtrados = preparar_criterios(filtrado)


# =========================================================
# INDICADORES GENERALES
# =========================================================

st.divider()
st.subheader("Indicadores generales")

total_auditorias = len(filtrado)

promedio = filtrado["Puntaje final"].mean()

cantidad_asesores = filtrado["Asesor"].nunique()

cantidad_campañas = filtrado["Campaña"].nunique()

ventas = (
    filtrado["Tipo de gestión"].apply(tipo_gestion_normalizado) == "Venta"
).sum()

no_ventas = (
    filtrado["Tipo de gestión"].apply(tipo_gestion_normalizado) == "No Venta"
).sum()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Auditorías", f"{total_auditorias:,}".replace(",", "."))
k2.metric("Calidad promedio", f"{promedio:.1f}%" if pd.notna(promedio) else "Sin datos")
k3.metric("Asesores", cantidad_asesores)
k4.metric("Campañas", cantidad_campañas)
k5.metric("Ventas / No ventas", f"{ventas} / {no_ventas}")


# =========================================================
# PESTAÑAS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen",
    "Por asesor",
    "Por campaña",
    "Criterios de calidad",
    "Detalle de auditorías"
])


# =========================================================
# TAB 1: RESUMEN
# =========================================================

with tab1:

    st.subheader("Evolución general")

    evolucion = (
        filtrado.dropna(subset=["Fecha"])
        .groupby("Fecha")["Puntaje final"]
        .mean()
        .reset_index()
        .sort_values("Fecha")
        .set_index("Fecha")
    )

    if not evolucion.empty:
        st.line_chart(evolucion, y="Puntaje final")
    else:
        st.info("No hay fechas válidas para construir la evolución.")

    st.subheader("Resultados por tipo de gestión")

    por_tipo = filtrado.copy()
    por_tipo["Tipo normalizado"] = por_tipo["Tipo de gestión"].apply(
        tipo_gestion_normalizado
    )

    tabla_tipo = por_tipo.groupby("Tipo normalizado").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_promedio=("Puntaje final", "mean")
    ).reset_index()

    tabla_tipo = tabla_tipo.rename(columns={
        "Tipo normalizado": "Tipo de gestión",
        "Calidad_promedio": "Calidad promedio"
    })

    tabla_tipo["Calidad promedio"] = tabla_tipo["Calidad promedio"].round(1)

    st.dataframe(tabla_tipo, use_container_width=True, hide_index=True)

    st.subheader("Resultados por mes")

    mensual = filtrado.dropna(subset=["Fecha"]).copy()

    if not mensual.empty:
        mensual["Mes"] = mensual["Fecha"].dt.to_period("M").astype(str)

        tabla_mensual = mensual.groupby("Mes").agg(
            Auditorías=("Puntaje final", "count"),
            Calidad_promedio=("Puntaje final", "mean")
        ).reset_index()

        tabla_mensual["Calidad_promedio"] = tabla_mensual[
            "Calidad_promedio"
        ].round(1)

        tabla_mensual = tabla_mensual.rename(columns={
            "Calidad_promedio": "Calidad promedio"
        })

        st.bar_chart(
            tabla_mensual.set_index("Mes")["Calidad promedio"]
        )

        st.dataframe(
            tabla_mensual,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# TAB 2: POR ASESOR
# =========================================================

with tab2:

    st.subheader("Desempeño por asesor")

    por_asesor = filtrado.groupby("Asesor").agg(
        Auditorías=("Puntaje final", "count"),
        Calidad_promedio=("Puntaje final", "mean")
    ).reset_index()

    por_asesor["Calidad_promedio"] = por_asesor[
        "Calidad_promedio"
    ].round(1)

    por_asesor = por_asesor.sort_values(
        "Calidad_promedio",
        ascending=False
    )

    por_asesor = por_asesor.rename(columns={
        "Calidad_promedio": "Calidad promedio"
    })

    st.bar_chart(
        por_asesor.set_index("Asesor")["Calidad promedio"]
    )

    st.dataframe(
        por_asesor,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Evolución individual")

    asesor_elegido = st.selectbox(
        "Seleccionar asesor para ver su evolución",
        sorted(filtrado["Asesor"].unique())
    )

    evolucion_asesor = filtrado[
        filtrado["Asesor"] == asesor_elegido
    ].dropna(subset=["Fecha"])

    evolucion_asesor = (
        evolucion_asesor.groupby("Fecha")["Puntaje final"]
        .mean()
        .reset_index()
        .sort_values("Fecha")
        .set_index("Fecha")
    )

    if not evolucion_asesor.empty:
        st.line_chart(evolucion_asesor, y="Puntaje final")


# =========================================================
# TAB 3: POR CAMPAÑA
# =========================================================

with tab3:

    st.subheader("Desempeño por campaña")

    por_campaña = filtrado.groupby("Campaña").agg(
        Auditorías=("Puntaje final", "count"),
        Asesores=("Asesor", "nunique"),
        Calidad_promedio=("Puntaje final", "mean")
    ).reset_index()

    por_campaña["Calidad_promedio"] = por_campaña[
        "Calidad_promedio"
    ].round(1)

    por_campaña = por_campaña.rename(columns={
        "Calidad_promedio": "Calidad promedio"
    })

    st.bar_chart(
        por_campaña.set_index("Campaña")["Calidad promedio"]
    )

    st.dataframe(
        por_campaña,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Evolución histórica por campaña")

    evolucion_campaña = filtrado.dropna(subset=["Fecha"]).copy()

    if not evolucion_campaña.empty:
        evolucion_campaña["Mes"] = (
            evolucion_campaña["Fecha"].dt.to_period("M").astype(str)
        )

        tabla_evolucion = evolucion_campaña.pivot_table(
            index="Mes",
            columns="Campaña",
            values="Puntaje final",
            aggfunc="mean"
        )

        st.line_chart(tabla_evolucion)


# =========================================================
# TAB 4: CRITERIOS DE CALIDAD
# =========================================================

with tab4:

    st.subheader("Análisis de criterios")

    resumen = resumen_criterios(criterios_filtrados)

    if resumen.empty:
        st.info("No hay respuestas de criterios disponibles.")
    else:

        st.markdown("**Cumplimiento por criterio**")

        st.bar_chart(
            resumen.set_index("Criterio")["% Cumplimiento"]
        )

        st.markdown("**Detalle de resultados**")

        tabla_criterios = resumen[[
            "Criterio",
            "Evaluaciones",
            "Cumplimientos",
            "Incumplimientos",
            "Puntos_de_mejora",
            "% Cumplimiento",
            "% Incumplimiento"
        ]].copy()

        tabla_criterios = tabla_criterios.rename(columns={
            "Puntos_de_mejora": "Puntos de mejora",
            "% Cumplimiento": "% Cumplimiento",
            "% Incumplimiento": "% Incumplimiento"
        })

        tabla_criterios["% Cumplimiento"] = tabla_criterios[
            "% Cumplimiento"
        ].round(1)

        tabla_criterios["% Incumplimiento"] = tabla_criterios[
            "% Incumplimiento"
        ].round(1)

        st.dataframe(
            tabla_criterios,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Fortalezas**")
            fortalezas = resumen.sort_values(
                "% Cumplimiento",
                ascending=False
            ).head(5)

            st.dataframe(
                fortalezas[["Criterio", "% Cumplimiento"]],
                use_container_width=True,
                hide_index=True
            )

        with col_b:
            st.markdown("**Puntos críticos**")
            criticos = resumen.sort_values(
                "% Incumplimiento",
                ascending=False
            ).head(5)

            st.dataframe(
                criticos[["Criterio", "% Incumplimiento"]],
                use_container_width=True,
                hide_index=True
            )

        st.subheader("Puntos de mejora")

        mejoras = resumen.sort_values(
            "Puntos_de_mejora",
            ascending=False
        ).head(10)

        st.dataframe(
            mejoras[["Criterio", "Puntos_de_mejora", "Evaluaciones"]],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Los porcentajes de criterios se calculan sobre respuestas "
            "SI, NO y Punto de mejora. Los N/A se excluyen de este análisis "
            "cualitativo, aunque en la ponderación oficial aportan el puntaje completo."
        )


# =========================================================
# TAB 5: DETALLE
# =========================================================

with tab5:

    st.subheader("Detalle de auditorías")

    columnas_mostrar = [
        "Fecha",
        "Asesor",
        "Campaña",
        "ID",
        "Tipo de gestión",
        "Tipificación",
        "Puntaje final",
        "Puntos a trabajar",
        "Observaciones",
        "¿Tipifica bien?",
        "Tipificación correcta"
    ]

    detalle = filtrado[columnas_mostrar].copy()

    detalle["Fecha"] = detalle["Fecha"].dt.strftime("%d/%m/%Y")
    detalle["Puntaje final"] = detalle["Puntaje final"].round(1)

    st.dataframe(
        detalle.sort_values(
            "Fecha",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    csv = filtrado[columnas_mostrar].to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    st.download_button(
        "Descargar detalle en CSV",
        data=csv,
        file_name="detalle_calidad_contactel.csv",
        mime="text/csv"
    )


# =========================================================
# PIE
# =========================================================

st.divider()

st.caption(
    "Calidad y Capacitación | Contactel | "
    "Los datos se actualizan automáticamente cada 5 minutos."
)

st.caption(
    "La medición oficial utiliza la ponderación correspondiente "
    "a Venta o No Venta. La columna AC (Acción) no se utiliza."
)

if st.button("Actualizar datos ahora"):
    st.cache_data.clear()
    st.rerun()
