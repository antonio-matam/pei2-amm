"""Module to handle risk operations"""
import memorystore
import uuid
import cloudstorage
import json
import redis

#Configuración de Redis
#redis_client=redis.StrictRedis(jost='redis', port=6379, decode_responses=True)

@app.route('/product', methods=['GET', 'POST'])
def get_risk(risk_id: uuid.UUID):
    if request.method == 'GET':
        response = get_products()
        return jsonify(response)
    
    if request.method == 'POST':
        data = request.get_json()
        data['risk_id'] = data['risk_id'] if 'risk_id' in data else None
        create_product(
            data['city_id'],
            data['city_name'],
            data['risk'],
            data['level'])
        return jsonify({ "status": "ok"})

    """
    Esta función devuelve el riesgo asociado a un identificador.

    En los niveles 3 y 4 la consulta se realiza en la base de datos in-memory, ya sera Redis o GCP Memory Storage

    :param risk_id: Identificador del riesgo a consultar
    :return:
    {
        "city": "Alcalá de Henares",
        "risk": "Severe snowfall",
        "level": 6
    }
    """
    """
    Recuperar un riesgo desde Redis.
    :param risk_id: Identificador único del riesgo.
    :return: El riesgo almacenado o un mensaje de error si no lo encuentra.
    """

    # Niveles 3,4: Consulta en la base de datos in-memory haciendo uso del módulo `memorystore`
    # Obtener el riesgo desde Redis
    risk_data=redis.client.get(str(risk_id))
    if not risk_data:
        return {"message": "Risk not found"}, 404

    # Nivel 5: consultar la base de datos in-memory y, si el elemento no se encontrara allí, buscarlo en
    # GCP storage haciendo uso del módulo `cloudstorage`. Si se encontrara allí añadirlo a la base de datos in-memory
    # para que haga las veces de caché. Dependiendo de si el riesgo se encontrara o no en la base de datos in-memory
    # (cache) añada a la respuesta una clave que refleje este hecho haciendo
    # `return {"cache": False, **risk_description}` si el dato no estaba en cache, y
    # return {"cache": True, **risk_description} en caso contrario.

    #Convertir de JSON a diccionario y devolverlo
    return json.loads(risk_data)




def add_risk(risk_id: uuid.UUID, **risk_description):
    # Niveles 3 y 4
    # Almacenar el riesgo en la base de datos in-memory haciendo `risk = memorystore.save_risk ....`
    """
    Almacenar el riesgo en Redis con una expiración de 10 segundos.
    :param risk_id: Identificador único del riesgo
    :param risk_description: Descripción completa del riesgo.
    :return: El riesgo almacenado.
    """
    #Convertir el riesgo a JSON y almacenarlo en Redis con expiración
    redis_client.setex(str(risk_id),10,json.dumps(risk_description))
    return risk_description

    # Nivel 5
    # Almacenar el riesgo en cloud storage haciendo `cloudstorage.upload_blob(...)`
