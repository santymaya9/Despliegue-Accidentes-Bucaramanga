# Minería de datos en Python - Accidentes de tránsito en Bucaramanga (Comuna Centro, 2017)

**Práctica 3 - Analítica de Datos 2026**

Modelo de clasificación que predice si un accidente de tránsito termina **con víctimas** (heridos o muertos) o **solo con daños**, con despliegue en una interfaz gráfica (Streamlit).

**Datos:** accidentes de tránsito de Bucaramanga publicados en datos.gov.co (Secretaría de Tránsito), filtrados a la Comuna 15 - Centro, año 2017.

## Contenido

| Archivo | Descripción |
|---|---|
| `Modelos_Bucaramanga_Practica3.ipynb` | Preparación de datos, selección de factores, validación cruzada (árbol, random forest, XGBoost, KNN, red neuronal, SVM), revisión de overfitting/underfitting, GridSearchCV del mejor modelo y guardado |
| `Despliegue_Bucaramanga_Practica3.ipynb` | Carga del modelo, preparación de datos nuevos y creación de la interfaz |
| `app.py` | Interfaz gráfica en Streamlit |
| `modelo-class-accidentes.pkl` | Modelo entrenado (se genera al ejecutar el notebook de modelos) |
| `accidentes_bucaramanga_completo.csv` | Datos originales |
| `pantallazo_despliegue.png` | Pantallazo de la interfaz funcionando |

## Cómo ejecutarlo

```
pip install -r requirements.txt
# 1. Ejecutar todas las celdas de Modelos_Bucaramanga_Practica3.ipynb (genera el .pkl)
# 2. Lanzar la interfaz
streamlit run app.py
```

## Integrantes

- (nombres del equipo)
