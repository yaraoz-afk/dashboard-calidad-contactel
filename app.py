
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Diagnóstico de estructura",
    layout="wide"
)

URLS = {
    "Medición": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/pub?gid=0&single=true&output=csv",
    "Medición por asesor": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/pub?gid=846850309&single=true&output=csv",
    "Histórico por campaña": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/pub?gid=1211851562&single=true&output=csv",
    "Hoja 2": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/pub?gid=1421200336&single=true&output=csv"
}

@st.cache_data(ttl=300)
def cargar_datos(url):
    return pd.read_csv(
        url,
        header=None,
        dtype=str,
        keep_default_na=False
    )

st.title("CONTACTEL | Estructura de datos")
st.caption("Vista de las primeras filas para identificar encabezados.")

for nombre, url in URLS.items():
    st.divider()
    st.subheader(nombre)

    try:
        df = cargar_datos(url)

        st.write(f"Filas totales: {len(df)}")
        st.write(f"Columnas totales: {len(df.columns)}")

        st.write("**Primeras 6 filas:**")
        st.dataframe(
            df.head(6),
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Error al leer la pestaña: {e}")
