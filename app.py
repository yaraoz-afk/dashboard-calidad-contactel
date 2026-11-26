
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Encabezados - Contactel",
    layout="wide"
)

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5Y5jNYGiX9tk0RgKMb3alZ4DLM2YjYXkk5zjbFjy0kvFFKc-BVB--KpXEwPJHhzgFTtfd6uqFKj-t/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(
        URL,
        header=None,
        dtype=str,
        keep_default_na=False
    )

st.title("CONTACTEL | Encabezados de medición")
st.write("Identificación de las columnas de la hoja Medición.")

try:
    df = cargar_datos()

    columnas = []

    for i in range(len(df.columns)):
        letra = ""
        n = i + 1

        while n:
            n, resto = divmod(n - 1, 26)
            letra = chr(65 + resto) + letra

        fila1 = df.iloc[0, i].strip()
        fila2 = df.iloc[1, i].strip()

        columnas.append(
            f"Columna {letra} | Fila 1: {fila1 or '[vacío]'} | Fila 2: {fila2 or '[vacío]'}"
        )

    resultado = "\n".join(columnas)

    st.success("Encabezados identificados correctamente.")
    st.caption("Podés seleccionar y copiar el texto de abajo.")
    st.code(resultado, language="text")

except Exception as e:
    st.error(f"No se pudo leer la información: {e}")
