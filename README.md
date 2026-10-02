# Minería de datos en Python - Accidentes de tránsito en Bucaramanga (Comuna Centro, 2017)
 
**Práctica 3 - Analítica de Datos 2026 · Universidad Pontificia Bolivariana**
 
**Grupo de trabajo** 
 
- Santiago Maya Horta 
- Santiago Posso Acevedo
- Andres Felipe Nunez Hernandez
- 
Modelo de clasificación que predice si un accidente de tránsito en la Comuna Centro de Bucaramanga termina **con víctimas** (heridos o muertos) o **solo con daños materiales**, y su despliegue en una interfaz gráfica con Streamlit.
 
**Aplicación desplegada:** https://despliegue-accidentes-bucaramanga-tyeafamwxu26vsiyjqegrs.streamlit.app
 
**Datos:** accidentes de tránsito publicados por la Secretaría de Tránsito de Bucaramanga en [datos.gov.co](https://www.datos.gov.co) (39.193 registros, 2012-2023), filtrados a la Comuna 15 - Centro en 2017: **406 registros**.
 
## Resumen del proyecto
 
| Etapa | Qué se hizo |
|---|---|
| Calidad de datos | Integración, eliminación de variables irrelevantes y redundantes, revisión de atípicos y nulos (sin nulos ni errores lógicos), correlaciones |
| Variable objetivo | `Gravedad` agrupada en `Con víctimas` (heridos + muertos) y `Solo daños`. La clase `Con muertos` solo tenía 2 registros, por lo que se unió a heridos; así las clases quedan balanceadas (203 y 203), no se necesita SMOTE y no se usan datos sintéticos |
| Selección de factores | De 8 variables candidatas se conservaron 3 (`Moto`, `Automovil`, `Barrio`) con pruebas de asociación (Chi-cuadrado, Mann-Whitney), información mutua e importancia de Random Forest |
| Modelos | Árbol, Random Forest, XGBoost, KNN, Red Neuronal y SVM con validación cruzada estratificada de 10 pliegues y revisión de overfitting / underfitting |
| Optimización | `GridSearchCV` (F1 macro, 10 pliegues) a los seis modelos; se eligió el Random Forest por su F1 y porque no necesita normalizar las variables |
| Despliegue | Interfaz en Streamlit que carga el modelo y predice la gravedad a partir de los datos del accidente |
 
## Resultados
 
F1 macro en test (promedio de 10 pliegues), con la configuración inicial de cada modelo y después del `GridSearchCV`:
 
| Modelo | F1 macro inicial | Diferencia train − test | F1 macro con GridSearch |
|---|---|---|---|
| Red Neuronal | 0.754 | 0.001 | 0.754 |
| **Random Forest** | 0.751 | 0.004 | **0.754** |
| XGBoost | 0.749 | 0.006 | 0.749 |
| Árbol de decisión | 0.746 | 0.001 | 0.746 |
| SVM | 0.738 | 0.017 | 0.751 |
| KNN | 0.701 | 0.015 | 0.718 |
 
Ningún modelo presenta overfitting (diferencias menores a 0.05). El modelo final es el **Random Forest**, que empata en F1 con la Red Neuronal pero no necesita normalizar y entrega la importancia de las variables; con las predicciones de la validación cruzada obtiene **exactitud de 0.756** (recall de 0.83 para `Con víctimas` y de 0.68 para `Solo daños`). Hay empate técnico entre casi todos los modelos: con solo tres variables, el desempeño está limitado por la información disponible y no por el algoritmo.
 
## Contenido del repositorio
 
| Archivo | Descripción |
|---|---|
| `Modelos_Bucaramanga_Practica_Mineria_De_Datos.ipynb` | Preparación de datos, selección de factores, validación cruzada de los 6 modelos, revisión de overfitting / underfitting, `GridSearchCV` de los 6 modelos, selección del modelo final y guardado |
| `Despliegue_Bucaramanga_Mineria_De_Datos.ipynb` | Carga del modelo, preparación de datos nuevos, creación de la interfaz y pantallazo del despliegue |
| `app.py` | Interfaz gráfica en Streamlit (es el notebook de despliegue descargado como `.py`) |
| `modelo-class-accidentes.pkl` | Modelo entrenado (se genera al ejecutar el notebook de modelos) |
| `accidentes_bucaramanga_completo.csv` | Datos originales |
| `requirements.txt` | Dependencias de la aplicación (versiones iguales a las del entrenamiento) |
| `Proyecto_accidentes_bucaramanga.xlsx` | Resumen del proyecto con el formato del archivo compartido en Teams |
 
 
 
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
* El modelo tiende a dar falsas alarmas: clasifica como "con víctimas" cerca de 1 de cada 3 accidentes que solo dejaron daños.
* Es una herramienta de apoyo para analizar patrones, no para decidir casos individuales.

