# MasLectura

## Descripción del proyecto

+Lectura es un sitio web enfocado en la busqueda de nuevas lecturas. Permitiendo al usuario obtener recomendaciones mediante Inteligencia Artificial, utilizando Singular Value Decomposition (SVD) y Árboles de Decisiones con XGBoost; Además de ofrecer funcionalidades base de un sitio web que se basa en recomendar y obtener recomendaciones de contenido literario, tales como:

+ Creación y gestión de una cuenta propia.
+ Creación, gestión y uso de listas por defecto o personalizadas.
+ Obtener recomendaciones en base a gustos.
+ Comentar acerca de libros.
+ Calificar libros.
+ Buscar libros con una extensa cantidad de filtros y métodos de filtrado.
+ Agregar y editar obras literarias.
+ Administrar contenido en caso que tenga permisos.

## Requerimientos

### Consideraciones

Antes de comenzar, el proyecto corre en base a Python para backend, por lo que es necesario instalar librerías para ello. Asegurese de tener **Python 3.13.2**.

___

Debe cargar el dump en MySQL. Puede hacerlo directamente desde MySQL Workbench, abriendo el dump como script y ejecutandolo directamente.

___

Dentro de `/backend`, debe tener un .env que permita conectarlo a la base de datos. Este tiene la siguiente estructura:

```env
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=
PORT=
JWT_SECRET_KEY=""
SALT_ROUNDS=10
MAIL_USERNAME=""
MAIL_PASSWORD=""
```

_Tanto `MAIL_USERNAME` como `MAIL_PASSWORD` son algo complejos de hacer funcionar, debido a que debe agregar una clave de API para inicio de sesión a su cuenta de Google, lo cual es poco seguro y además requiere que su cuenta de Google tenga 2FA activado. Sin embargo, este solo se utiliza para la recuperación de contraseña. En caso el formato, si lo desea, es el siguiente: `MAIL_USERNAME="correo@example.com"`, `MAIL_PASSWORD="XXXX XXXX XXXX XXXX"`_

___

Debe también tener Node instalado, asegurese de tener la version **Node v20.16.0**.

___

Se considera buena práctica el uso de un entorno virtual para evitar errores entre las librerías instaladas globalmente. Esto fue utilizado durante el proyecto.

Los pasos se encuentran a continuación:

+ Se comienza por la creación del entorno virtual, utilizando el comando `python -m venv .venv`.
+ Después, se debe activar el entorno virtual, mediante la ejecución de `.\.venv\Scripts\activate`. Esto permite que todas las dependencias se instalen solo dentro de este proyecto, y no globalmente. Evitando así conflictos con dependencias instaladas globalmente, como fue mencionado anteriormente.
+ Instalar las dependencias utilizando `pip install -r requirements.txt`. _Es importante considerar que debes dentro de la carpeta /backend para esto._

___

Además debe instalar las dependencias de frontend, de la siguiente forma:

+ Ingrese a frontend `cd frontend`
+ Instale las dependencias mediante `npm install`

___

**Recuerde poner la URL correcta de su backend en los siguientes archivos:**

+ `api.ts`, línea 4. En `/frontend/src/api/api.ts`
+ `BookView.vue`, línea 154. En `/frontend/src/views/BookView.vue`

El formato es `http://(url):(port)`, por ejemplo: `http://127.0.0.1:3306/api`.

___

### Dependencias

Para funcionar con normalidad, el proyecto requiere las siguientes bibliotecas de python:

+ bcrypt==4.3.0
+ blinker==1.9.0
+ click==8.1.8
+ colorama==0.4.6
+ contourpy==1.3.2
+ cycler==0.12.1
+ dotenv==0.9.9
+ et_xmlfile==2.0.0
+ Flask==3.1.0
+ flask-cors==5.0.1
+ Flask-Mail==0.10.0
+ Flask-MySQLdb==2.0.0
+ fonttools==4.58.1
+ itsdangerous==2.2.0
+ Jinja2==3.1.6
+ joblib==1.5.0
+ kiwisolver==1.4.8
+ MarkupSafe==3.0.2
+ matplotlib==3.10.3
+ mysqlclient==2.2.7
+ numpy==2.2.5
+ openpyxl==3.1.5
+ packaging==25.0
+ pandas==2.2.3
+ pillow==11.2.1
+ PyJWT==2.10.1
+ pyparsing==3.2.3
+ python-dateutil==2.9.0.post0
+ python-dotenv==1.1.0
+ pytz==2025.2
+ scikit-learn==1.6.1
+ scipy==1.15.3
+ six==1.17.0
+ threadpoolctl==3.6.0
+ tzdata==2025.2
+ Werkzeug==3.1.3
+ xgboost==3.0.0

_Estas dependencias fueron generadas utilizando `pip freeze > requirements.txt`, puede que algunas librerias estén de más, o fueron descargadas como dependencias extras de una librería._

### Datos de entrenamiento

Además, es fundamental para el entrenamiento tener el .csv de los datos de amazon para un entrenamiento eficiente, estos pueden ser descargados desde [aquí](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews).

Luego de descargarlos, debe crear un directorio dentro de `/backend/ai`, con nombre "**training**", para posteriormente arrastrar ambos CSV's dentro del .zip descargado.

_En el caso que quiera entrenar con los mismos datos del sistema, debe ir a `/backend/ai/train.py` y **editar** la línea 17, y pasarle **False** como parámetro._

```py
15 | df = getCombinedRatingsDF(
16 |    use_local=True,
17 |    use_amazon=False
18 | )
```

## Uso

### Iniciar web

Para comenzar a utilizar la web, primero debe iniciar tanto frontend como backend, a continuación se encuentran los pasos para cada uno.

___

#### Backend

Para iniciar el backend, debe ingresar los siguientes comandos en la terminal:

+ `cd backend`
+ `.\.venv\Scripts\activate`
+ `python app.py`

___

#### Frontend

Para iniciar el frontend, debe ingresar los siguientes comandos en la terminal:

+ `cd frontend`
+ `npm run dev`
+ (Opcional) Puede servir el frontend dentro de su red utilizando `npx vite build` y luego `serve -s dist`.

___

### Entrenar el modelo

Para entrenar el modelo, es necesario ingresar a `/backend` y luego ejecutar el siguiente comando:

```sh
python -m ai.train
```

Los resultados de entrenamiento se guardarán dentro de `/backend/model` para ser utilizados por el sistema.

___

**Felicidades! Ya puede utilizar +Lectura. No es necesario crearse una cuenta para navegar, pero para obtener recomendaciones en base a sus gustos, debe crearse una cuenta, calificar más de 4 libros y posteriormente entrenar el modelo para que este le entregue recomendaciones.**
