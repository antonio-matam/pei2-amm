[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/vMX1Gv3E)
###### tags: `ASO-GIT`
# ASO-GIT PEI2 2023-2024

Este repositorio se utilizará como enunciado y como entregable para esta segunda prueba de evaluación continua PEI2. Los trabajos a realizar por parte del estudiante se han dividido en niveles. Cada nivel requiere la realización de una serie de tareas y genera a su vez una serie de entregables. Para facilitar la corrección de las tareas se ha añadido, al final de este documento, una sección con ese nombre [entregables](#entregables). En esa sección se enumeran los entregables mínimos para superar cada nivel, y en dicha sección el estudiante puede incluir todo aquello que estime que puede contribuir a asegurar su calificación.

## Datos del estudiante:

La primera actividad a realizar será rellenar los siguientes campos con tu nombre, apellidos y dirección de email.

- Nombre y apellidos: Antonio Mata Marco
- email: antonio.matam@edu.uah.es
- URL perfil público de Google Skillboost: 

A continuación debes marcar la casilla que viene a continuación. Este documento está redactado utilizando el lenguaje de marcado Markdown, por lo tanto, las casillas de verificación se representan mediante la apertura y cierre de los corchetes, separados a su vez por un espacio en blanco, "[ ]". Para marcar una casilla debes sustituir ese espacio en blanco con una X mayúscula, así "[X]".

- [X] Al modificar este archivo con mi nombre y con mi email, me comprometo a cumplir con el siguiente código de honor:

    - Tus respuestas a tareas, cuestionarios y exámenes deben ser tu propio trabajo (excepto para las tareas que permiten explícitamente la colaboración). Esto incluye en particular resultados obtenidos mediante el uso de inteligencias artificiales y otros generadores automáticos de código.
    - No puedes compartir tus soluciones de tareas, cuestionarios o exámenes con otra persona a menos que el instructor lo permita explícitamente. Esto incluye cualquier cosa escrita por ti, como también cualquier solución oficial proporcionada por el personal del curso.

## `Nivel 1 `Crear una aplicación web `pei2-author` flask dockerizada y publicarla en `docker-hub` 

Crear una aplicación web flask. Esta aplicación expondrá un endpoint `GET /author` que devolverá la siguiente información (ejemplo):

```json=
{
    "author": "Óscar García",
    "email": "oscar.gpoblacion@uah.es"
}
```

El nombre del autor y su email deben obtenerse a través de dos variables de entorno: `AUTHOR_NAME` y `AUTHOR_EMAIL`. Si no se proporcionan dichas variables de entorno, la ejecución debe fallar elevando la excepción correspondiente.

A partir de esta aplicación hay que generar una imagen docker de la misma y publicarla en docker-hub. La imagen debe generarse a partir de `python:latest` y debe escuchar sus peticiones en el puerto `PORT`.

Realice los cambios oportunos en la carpeta `author`de este repositorio para la creación de la imagen, realice las pruebas necesarias, publique la imagen en docker-hub y finalmente suba los cambios realizados al repositorio de git-hub.

Consulte la sección [entregables](#entregables) de este documento. 

## `Nivel 2` Publicar la aplicación `pei2` en Cloud Run. 

Vamos a utilizar el servicio Cloud Run de Google Cloud Platform para publicar la aplicación web que acabamos de construir. 

En este nivel el valor de las variables de entorno `AUTHOR_NAME` y `AUTHOR_EMAIL` deben ser las del propio estudiante.

Es recomendable, pero no obligatorio, configurar el servicio de despliegue continuo para facilitar las labores de desarrollo.

Consulte la sección [entregables](#entregables) de este documento. 

## `Nivel 3` API de gestión de riesgos persistidos en Redis. 

En este apartado vamos a añadir a nuestra aplicación web una serie de endpoints para poder crear y persistir alertas de riesgos asociados a una localidad de España.

Para declarar un riesgo en una localidad utilizaremos el endpoint `[POST] /risk/<city_id>`, indicando en el cuerpo (body) de la petición la siguiente información:
```json=
{
    "city_name": "Alcalá de Henares"
    "risk": "Severe snowfall",
    "level": 6
}
```

El campo `risk` es un campo de texto libre que tendrá una longitud máxima de 80 caracteres. El campo `level` es un número entero mayor que cero.

Para hacer la petición POST se puede usar `curl` de la siguiente forma:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"city_name": "Alcalá de Henares" "risk": "Severe snowfall", "level": 6}" \
  http://hostname/risk/d67deae4-c143-4849-a08f-1f98f966f3fb
```

La respuesta de este endpoint debe contener la información indicada en el cuerpo de la petición más el identificador de la ciudad, por ejemplo:
```json
{
    "city_id": "d67deae4-c143-4849-a08f-1f98f966f3fb",
    "city": "Madrid",
    "risk": "Severe hail",
    "level": 8
}
```

Para obtener el riesgo declarado de una ciudad concreta se puede utilizar el endpoint `GET /risk/<city_id>`. La respuesta será similar a la siguiente:
```json
{
    "city_id": "550e8400-e29b-41d4-a716-446655440000",
    "city_name": "Alcalá de Henares",
    "risk": "Severe snowfall",
    "level": 6
{
```

El equivalente con `curl` sería similar al siguiente:
```bash
curl --header "Content-Type: application/json" \
  --request GET \
  http://hostname/risk/d67deae4-c143-4849-a08f-1f98f966f3fb
```

Cuando se crea un nuevo riesgo, el API deberá persistir dicho riesgo en una base de datos in-memory, en este caso Redis. Esta persistencia estará limitada a 10 segundos. Pasado ese tiempo Redis, se eliminará el riesgo de forma automática.

Cuando se consulta un riesgo se buscará en la base de datos in-memory y, de encontrarse allí, se retornará como resultado de la llamada.

Para las labores de desarrollo local debe crear un entorno de ejecución utilizando `docker-compose`. En dicho entorno se harán las pruebas oportunas de creación y consulta de riesgos. En la carpeta `risks` encontrará un esqueleto del código, **incompleto y con posibles errores**, que deberá ir completando progresivamente.

Cuando haya terminado esta parte consulte la sección [entregables](#entregables) de este documento. 


## `Nivel 4` Gestión de alertas en CloudRun y Memorystore. 

Una vez completadas las pruebas en el entorno local, realizar las labores necesarias para publicar este servicio en Cloud Run, utilizando como base de datos in-memory Google Memorystore.

Consulte la sección [entregables](#entregables) de este documento. 

## `Nivel 5` Gestión de alertas persistidas en Google Cloud Storage. 

Al servicio diseñado en el nivel 4 vamos a añadir una capa de persistencia más fiable utilizando Google Cloud Storage. Ahora, cuando se crea un nuevo riesgo, además de añadirlo a la base de datos in-memory, vamos a crear un objeto dentro de un bucket en el que almacenaremos el contenido del riesgo.

Además, cuando se consulte un riesgo a través del endpoint correspondiente, si el identificador no se encontrara en la base de datos in-memory, se procederá buscar el objeto cuyo nombre coincida con el identificador de riesgo en GCS. Si se localizara dicho objeto se cargará de nuevo en la base de datos in-memory y se devolverá como resultado de la llamada. En caso contrario se devolverá un objeto vacío.

Para esta tarea deberá por lo tanto crear un bucket en su proyecto de GCP y, corregir, completar y ajustar el codigo proporcionado para lograr la funcionalidad requerida. En la carpeta `risk_app` encontrará el módulo `cloudstorage` que contiene el código necesario para este fin.

Realice los cambios necesarios en primer lugar para que la aplicación funcione correctamente en local (en la máquina de operaciones) y opcionalmente despliegue la aplicación en Google Cloud Run.

## `Nivel 6` Aplicación de alertas basadas en riesgos. 

Se desea ahora poder activar una serie de alarmas cuando se registren riesgos cuyo nivel (`level`) sea mayor al indicado en la variable de entorno ALERT\_THRESHOLD.

Para desacoplar esta funcionalidad del API de registro de riesgos, se utilizará una arquitectura basada en eventos. Se configurará Google Cloud Storage para que publique un evento en un topic de Google Pub/Sub. La aplicación que vamos a desarrollar y que denominaremos `alert_app` se suscribirá a dicho topic y quedará a la espera de que aparezcan eventos de creación de objetos. Cuando aparezcan estos eventos se mostrarán por el registro de logs de la aplicación y con esto se dará por concluido este nivel 6. 

Es muy importante resaltar que no está permitido modificar la aplicación `risk_app` para incluir ninguna de las funcionalidades descritas, tanto en este nivel 6 como en los sucesivos.

Comenzaremos por crear un topic en Google Pub/Sub utilizando la consola. Para este ejemplo utilizaré el nombre `risks`, dentro del proyecto de Google Cloud denominado `aso-git`. También necesitaré el nombre del bucket para activar su servicio de mensajería, así es que para facilitar el trabajo crearemos las siguientes variables de entorno en una shell. No olvide modificar estos datos con los correspondientes a su entorno de trabajo. También es importante recordar que estas operaciones requieren permisos que no tienen la máquina de operaciones y su service account asociada. Es necesario por lo tanto ejecutar dichas órdenes desde un entorno autenticado con una cuenta de servicio con los permisos adecuados, por ejemplo usando la Cloud Shell o `gcloud` desde una máquina local configurada adecuadamente.

```bash!
export BUCKET_NAME=gs://ogp-pei2-2023-24-risk
export TOPIC_NAME=projects/aso-git/topics/risks
```

Si lo desea, también puede crear el topic utilizando `gcloud` haciendo:

```bash!
gcloud pubsub topics create $TOPIC_NAME
```

A continuación activamos las notificaciones del bucket donde almacenamos los riesgos con:

```bash!
gcloud storage buckets notifications create $BUCKET_NAME --topic=$TOPIC_NAME
```

Y por último creamos una suscripción con la que recibir los mensajes correspondientes:

```bash!
gcloud pubsub subscriptions create new_risk --topic=$TOPIC_NAME
```

Si desea comprobar el trabajo realizado hasta este punto, puede crear un nuevo riesgo y, acto seguido, consultar las notificaciones enviadas a la suscripción haciendo
```bash
gcloud pubsub subscriptions pull new_risk --auto-ack
```

Analice el código facilitado en la aplicación `alert_app` y realice los cambios oportunos para poner en marcha la aplicación y que esta reciba los eventos correspondientes cuando se cree un nuevo riesgo.


## `Nivel 7` Aplicación de alertas con publicación en una BBDD postgres  


En este nivel completaremos la funcionalidad desarrollada en el apartado anterior. Cuando se detecte la publicación de un riesgo con un nivel (`level`) superior al establecido en la variable de entorno `ALERT_THRESHOLD`, se publicará el evento en la tabla `alerts` de una base de datos de tipo Postgres denominada `alerts`.

Para la creación de la tabla de la base de datos, consulte el archivo `alert.ddl.sql`.

Complete, ajuste y corrija el código proporcionado en la aplicación `alert_app` para lograr este objetivo.

# Entregables <a name="entregables"></a>

## `Nivel 1` Servicio de Autor  💰1

### Comprobaciones previas
- [X] He realizado las pruebas oportunas y he verificado que todo funciona según lo especificado en el enunciado.
- [X] He añadido (`commit`) todos los cambios a mi repositorio, los he subido a git-hub (`push`), y he verificado en la web de `git-hub` que los cambios se han reflejado correctamente.
### Entrega
- [X] URL de la imagen construida en docker-hub: https://hub.docker.com/layers/ilias3d1/pei2/latest/images/sha256-7c2cbd1be7ce69b916bfcca67ca9d37e30de1ab4b06a2501656da081b7658dda?context=repo
- [] He añadido (`commit`) todos los cambios a mi repositorio, los he subido a git-hub (`push`), y he verificado en la web de `git-hub` que los cambios se han reflejado correctamente.
### Prueba
- Crear un contenedor a partir de la imagen generada y publicada.
- Verificar que La llamada `curl localhost:PORT/author` devuelve el JSON esperado

## `Nivel 2` Servicio de Autor corriendo el Cloud Run  💰1.5

### Comprobaciones previas
- [X] He configurado Cloud Run para ejecutar en él la aplicación WEB construida en el apartado anterior.
- [X] He realizado las pruebas oportunas y he verificado que todo funciona según lo especificado en el enunciado.
### Entrega
- [X] URL del servicio en Cloud Run: https://cuestion2-coudbfqksa-uc.a.run.app
- [X] He añadido (`commit`) todos los cambios a mi repositorio, los he subido a git-hub (`push`), y he verificado en la web de 
  `git-hub` que los cambios se han reflejado correctamente.
### Prueba
- La llamada `curl URL_DEL_SERVICIO/author` devuelve el JSON esperado

## `Nivel 3` Gestión de alertas persistidas en Redis. 💰1.5
### Comprobaciones previas
- [X] He configurado docker-compose para ejecutar en local la aplicación WEB con sus nuevos endpoints.
- [X] He hecho los ajustes necesarios en el código para asegurar que funciona según lo especificado.
### Entrega
- [X] He añadido (`commit`) todos los cambios a mi repositorio, los he subido a git-hub (`push`), y he verificado en la web de
  `git-hub` que los cambios se han reflejado correctamente.
```
 --- A realizar por el estudiante ---
```
### Prueba
- La llamada POST `URL_DEL_SERVICIO/risk` devuelve el JSON esperado.
- La llamada GET `URL_DEL_SERVICIO/risk` devuelve el JSON esperado.
- Tras 10 segundos, la llamada GET anterior devuelve un valor vacío.

## `Nivel 4` Gestión de alertas en Cloud Run persistidas en Memory Store. 💰1.5
### Comprobaciones previas
- [ ] He completado los pasos del apartado anterior.
- [ ] He configurado Cloud Run para ejecutar en él la aplicación WEB con sus nuevos endpoints.
- [ ] He configurado la integración con Cloud Memory Storage
- [ ] He realizado las pruebas oportunas y he verificado que todo funciona según lo especificado en el enunciado.
### Entrega
- Como esta entrega implica aprovisionar recursos costosos en GCP, avise al
  profesor del laboratorio para que valide su práctica en el mismo momento en el
  que esté disponible.
- [ ] URL del servicio publicado en Cloud Run: `_____ pegar aquí ______`

### Prueba
- La llamada POST `URL_DEL_SERVICIO/risk` devuelve el JSON esperado.
- La llamada GET `URL_DEL_SERVICIO/risk` devuelve el JSON esperado.
- Tras 10 segundos, la llamada GET anterior devuelve un valor vacío.

## `Nivel 5` Gestión de alertas en Cloud Run, persistidas en Cloud Storage. 💰1.5
### Comprobaciones previas
- [ ] He completado los ajustes y correcciones del código necesarias para cumplir con la especificación dada.
- [ ] He creado el bucket correspondiente en google cloud storage.
- [ ] He ejecutado la aplicación utilizando `docker-compose` y he hecho las pruebas oportunas allí.
### Prueba
- Como esta entrega implica aprovisionar recursos costosos en GCP, avise al
  profesor del laboratorio para que valide su práctica en el mismo momento en el
  que esté disponible.
- La llamada POST `URL_DEL_SERVICIO/risk` devuelve el JSON esperado.
- La llamada GET `URL_DEL_SERVICIO/risk` devuelve el JSON esperado, que ahora incluye la clave `"cache": True`
- Tras 10 segundos, la llamada GET anterior devuelve el JSON esperado, pero ahora la clave muestra `"cache": False`
- Otra llamada adicional a GET `URL_DEL_SERVICIO/risk` devuelve el JSON esperado con la clave `"cache": True` de nuevo.

## `Nivel 6` Aplicación de alarmas basada en eventos. 💰1.5
### Comprobaciones previas
- [ ] He completado los ajustes y correcciones del código necesarias para cumplir con la especificación dada.
- [ ] He activado la generación de eventos, he creado el topic correspondiente y he verificado que llegan los mensajes a dicho topic.
- [ ] He ejecutado la aplicación utilizando `docker-compose` y he hecho las pruebas oportunas allí.
### Prueba
- La llamada POST `URL_DEL_SERVICIO/risk` devuelve el JSON esperado.
- La creación del objeto del riesgo en GCS dispara un evento que es recibido por la aplicación y mostrado por pantalla.
### Entrega
- [ ] Los ajustes en el código se han entregado (`commit + push`) y están visibles en la consola web de github

## `Nivel 7` Aplicación de alertas con publicación en una BBDD postgres 💰1.5

- [ ] He realizado las modificaciones oportunas en el repositorio para proporcionar la funcionalidad requerida.
- [ ] He añadido (`commit`) todos los cambios a mi repositorio, los he subido a git-hub (`push`), y he verificado en la web de `git-hub` que los cambios se han reflejado correctamente.
- [ ] He ejecutado la aplicación utilizando `docker-compose` y he hecho las pruebas oportunas allí.
### Prueba
- Se publica un nuevo riesgo de nivel superior al marcado como umbral. 
- Se comprueba que aparece una nueva entrada en la tabla de la base de datos
### Entrega
- [ ] Los ajustes en el código se han entregado (`commit + push`) y están visibles en la consola web de github
- [ ] Escriba a continuación las órdenes que ha ejecutado para comprobar que se crean las entradas correspondientes en la tabla de la base de datos.
```
# Completar por el estudiante
```



