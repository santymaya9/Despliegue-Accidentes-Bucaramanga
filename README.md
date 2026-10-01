# Minería de datos en Python - Accidentes de tránsito en Bucaramanga (Comuna Centro, 2017)

**Práctica 3 - Analítica de Datos 2026 · Universidad Pontificia Bolivariana**

Modelo de clasificación que predice si un accidente de tránsito en la Comuna Centro de Bucaramanga termina **con víctimas** (heridos o muertos) o **solo con daños materiales**, y su despliegue en una interfaz gráfica con Streamlit.

**Aplicación desplegada:** https://despliegue-accidentes-bucaramanga-tyeafamwxu26vsiyjqegrs.streamlit.app

**Datos:** accidentes de tránsito publicados por la Secretaría de Tránsito de Bucaramanga en [datos.gov.co](https://www.datos.gov.co) (39.193 registros, 2012-2023), filtrados a la Comuna 15 - Centro en 2017: **406 registros**.

## Resumen del proyecto

| Etapa | Qué se hizo |
|---|---|
| Calidad de datos | Integración, eliminación de variables irrelevantes y redundantes, revisión de atípicos y nulos (sin nulos ni errores lógicos), correlaciones |
| Variable objetivo | `Gravedad` agrupada en `Con víctimas` (heridos + muertos) y `Solo daños`. La clase `Con muertos` solo tenía 2 registros, por lo que se unió a heridos; así las clases quedan balanceadas (203 y 203) y no se necesita SMOTE |
| Selección de factores | De 8 variables candidatas se conservaron 3 (`Moto`, `Automovil`, `Barrio`) con pruebas de asociación (Chi-cuadrado, Mann-Whitney), información mutua e importancia de Random Forest |
| Modelos | Árbol, Random Forest, XGBoost, KNN, Red Neuronal y SVM con validación cruzada estratificada de 10 pliegues y revisión de overfitting / underfitting |
| Optimización | `GridSearchCV` (64 combinaciones) sobre el mejor modelo, la Red Neuronal |
| Despliegue | Interfaz en Streamlit que carga el modelo y predice la gravedad a partir de los datos del accidente |

## Resultados

F1 macro en test (promedio de 10 pliegues):

| Modelo | F1 macro | Diferencia train − test |
|---|---|---|
| Red Neuronal | 0.751 | 0.004 |
| Random Forest | 0.746 | 0.008 |
| SVM | 0.739 | 0.010 |
| XGBoost | 0.739 | 0.014 |
| Árbol de decisión | 0.739 | 0.010 |
| KNN | 0.713 | 0.011 |

Ningún modelo presenta overfitting (diferencias menores a 0.05). El mejor modelo, la Red Neuronal con `GridSearchCV`, obtiene **F1 macro de 0.754 y exactitud de 0.756**. Hay empate técnico entre casi todos los modelos: con solo tres variables, el desempeño está limitado por la información disponible y no por el algoritmo.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `Modelos_Bucaramanga_Practica_Mineria_De_Datos.ipynb` | Preparación de datos, selección de factores, validación cruzada de los 6 modelos, revisión de overfitting / underfitting, `GridSearchCV` del mejor modelo y guardado |
| `Despliegue_Bucaramanga_Mineria_De_Datos.ipynb` | Carga del modelo, preparación de datos nuevos, creación de la interfaz y pantallazo del despliegue |
| `app.py` | Interfaz gráfica en Streamlit |
| `modelo-class-accidentes.pkl` | Modelo entrenado (se genera al ejecutar el notebook de modelos) |
| `accidentes_bucaramanga_completo.csv` | Datos originales |
| `requirements.txt` | Dependencias de la aplicación (versiones iguales a las del entrenamiento) |
| `.streamlit/config.toml` | Tema visual de la interfaz |
| `pantallazo_despliegue.png` | Pantallazo de la interfaz funcionando |

![Pantallazo del despliegue]
<img width="1917" height="1032" alt="image" src="https://github.com/user-attachments/assets/5d87b098-90d0-491d-ac35-7c6d3819ba38" />


## Cómo ejecutarlo

**Ver la aplicación:** abrir el enlace de la aplicación desplegada.

**Ejecutar la interfaz en un computador:**

```
pip install -r requirements.txt
streamlit run app.py
```

**Volver a entrenar el modelo:** instalar las librerías del notebook y ejecutar todas las celdas de `Modelos_Bucaramanga_Practica_Mineria_De_Datos.ipynb` con el CSV en la misma carpeta. Esto genera `modelo-class-accidentes.pkl`.

```
pip install pandas numpy matplotlib seaborn scipy scikit-learn xgboost openpyxl ydata-profiling
```

El modelo se entrenó con `pandas==2.2.3`, `numpy==2.1.3`, `scikit-learn==1.6.1` y `xgboost==3.4.1`; usar esas versiones para cargar el `.pkl` sin problemas.

## Limitaciones

* Son 406 accidentes de una sola comuna y un solo año; el modelo no debe usarse para otras zonas o épocas.
* Solo usa 8 variables candidatas (3 seleccionadas); las columnas de peatones y otros tipos de vehículo se dejaron fuera.
* Es una herramienta de apoyo para analizar patrones, no para decidir casos individuales.

## Integrantes

- Santiago Maya Horta ([@santymaya9](https://github.com/santymaya9))
- (nombre del integrante 2)
- (nombre del integrante 3)
