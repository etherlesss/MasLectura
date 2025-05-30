# Instrucciones de trabajo Py + Flask

## Como trabajar con Py y Flask

Se comienza por la creacion del entorno virtual, utilizando el comando `python -m venv .venv`.

Despues, se debe activar el entorno virtual, mediante la ejecución de `.\.venv\Scripts\activate`. Esto permite que todas las dependencias se instalen solo dentro de este proyecto, y no globalmente.

Para salir de .venv, se debe escribir el comando `deactivate`.

## Correr backend

`python app.py`

## Entrenar modelo

Debido al peso del dataset de entrenamiento, es necesario descargar el [https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews](dataset) desde kaggle. Crear dentro de `/ai` una carpeta llamada _training_ e insertar ambos CSV dentro de esa carpeta.

Para obtener nuevas recomendaciones (por ejemplo, después de crear un usuario y calificar varios libros), podemos volver a entrenar el modelo ejecutando el comando `python -m ai.train` desde la carpeta `/backend`.
