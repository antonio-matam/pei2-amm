"""Module to handle risk operations"""
import memorystore
import uuid
import cloudstorage
import json

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

    # Niveles 3,4: Consulta en la base de datos in-memory haciendo uso del módulo `memorystore`

    # Nivel 5: consultar la base de datos in-memory y, si el elemento no se encontrara allí, buscarlo en
    # GCP storage haciendo uso del módulo `cloudstorage`. Si se encontrara allí añadirlo a la base de datos in-memory
    # para que haga las veces de caché. Dependiendo de si el riesgo se encontrara o no en la base de datos in-memory
    # (cache) añada a la respuesta una clave que refleje este hecho haciendo
    # `return {"cache": False, **risk_description}` si el dato no estaba en cache, y
    # return {"cache": True, **risk_description} en caso contrario.

    return None




def add_risk(risk_id: uuid.UUID, **risk_description):
    risk= None

    # Niveles 3 y 4
    # Almacenar el riesgo en la base de datos in-memory haciendo `risk = memorystore.save_risk ....`

    # Nivel 5
    # Almacenar el riesgo en cloud storage haciendo `cloudstorage.upload_blob(...)`

    return risk
