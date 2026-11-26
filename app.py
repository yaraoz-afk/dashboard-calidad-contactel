
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Diagnóstico - Calidad Contactel",
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
    return pd.read_csv(url, sep=None, engine="python")

st.title("CONTACTEL | Diagnóstico de datos")
st.caption("Verificación de las cuatro fuentes antes de construir el panel.")

for nombre, url in URLS.items():
    st.subheader(nombre)

    try:
        df = cargar_datos(url)
        st.success(f"Conexión correcta: {len(df)} registros y {len(df.columns)} columnas.")

        st.write("**Encabezados detectados:**")
        st.code("\n".join(str(c) for c in df.columns))

        st.write("**Tipos de datos:**")
        st.code(df.dtypes.to_string())

    except Exception as e:
        st.error(f"No se pudo leer esta pestaña: {e}")

st.info("Diagnóstico finalizado. No se muestran los registros ni los datos personales.")
