import pickle

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gravedad de accidentes - Bucaramanga", page_icon="🚦")

# Etiquetas amigables para la interfaz (si una variable no está aquí, se muestra su nombre)
ETIQUETAS = {
    "Mes": "Mes",
    "Dia": "Día de la semana",
    "Hora": "Hora del día (0-23)",
    "Jornada": "Jornada",
    "Barrio": "Barrio",
    "Propietario": "Propietario del vehículo",
    "Automovil": "Número de automóviles involucrados",
    "Moto": "Número de motos involucradas",
}


@st.cache_resource
def cargar_modelo(ruta="modelo-class-accidentes.pkl"):
    with open(ruta, "rb") as f:
        return pickle.load(f)


artefactos = cargar_modelo()
modelo = artefactos["modelo"]
labelencoder = artefactos["labelencoder"]
variables = artefactos["variables"]      # columnas (dummies) con las que se entrenó el modelo
info = artefactos["info"]                # variables de entrada, rangos y categorías

st.title("🚦 Predicción de la gravedad de un accidente de tránsito")
st.write(
    "Comuna Centro de Bucaramanga. Ingresa las características del accidente y el modelo "
    f"(**{info.get('nombre_modelo', 'modelo')}**) estimará si terminará **con víctimas** o **solo con daños**."
)

# ---------------- Captura de datos
entradas = {}
for col in info["columnas_entrada"]:
    etiqueta = ETIQUETAS.get(col, col)
    if col in info["numericas"]:
        minimo, maximo = info["numericas"][col]
        if minimo < maximo:
            entradas[col] = st.slider(etiqueta, min_value=minimo, max_value=maximo,
                                      value=minimo, step=1)
        else:
            entradas[col] = st.number_input(etiqueta, value=minimo)
    else:
        entradas[col] = st.selectbox(etiqueta, info["categoricas"][col])

# ---------------- Preparación + predicción
if st.button("Predecir gravedad"):
    datos = pd.DataFrame([entradas])

    # Se fijan las categorías del entrenamiento para que el dummy de una sola fila sea correcto
    for col, categorias in info["categoricas"].items():
        datos[col] = pd.Categorical(datos[col], categories=categorias)
    preparada = pd.get_dummies(datos, columns=list(info["categoricas"]), dtype=int)

    # Se dejan exactamente las columnas del entrenamiento (la categoría de referencia queda fuera)
    preparada = preparada.reindex(columns=variables, fill_value=0)

    prediccion = labelencoder.inverse_transform(modelo.predict(preparada))[0]
    probabilidades = modelo.predict_proba(preparada)[0]

    if prediccion == "Con víctimas":
        st.error(f"Resultado: **{prediccion}**")
    else:
        st.success(f"Resultado: **{prediccion}**")

    tabla = pd.DataFrame({"Clase": labelencoder.classes_, "Probabilidad": probabilidades}).set_index("Clase")
    st.bar_chart(tabla)
    st.dataframe(tabla.style.format("{:.1%}"))

metricas = info.get("metricas_cv")
if metricas:
    st.warning(
        f"Desempeño del modelo en validación cruzada: F1 macro ≈ {metricas['f1_macro']:.2f}, "
        f"exactitud ≈ {metricas['accuracy']:.2f}. Es una herramienta de apoyo, no reemplaza el criterio experto."
    )
