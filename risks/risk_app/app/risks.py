"""Module to handle risk operations"""
from flask import Flask, jsonify, request, make_response
import memorystore
import uuid
import cloudstorage
import json
import redis

app = Flask(__name__)
redis_client=redis.StrictRedis(host="redis", port=6379,decode_responses=True)

@app.route('/risk/<risk_id>', methods=['GET', 'POST'])
def get_risk(risk_id: uuid.UUID):
    if request.method == 'GET':
        #Recuperar el dato desde Redis
        data = redis_client.get(str(risk_id))
        if data:
            #Si el dato existe, deserializarlo y devolverlo
            return json.loads(data)
        else:
            #Si no existe, devuelve un error 404
            return None
    
    if request.method == 'POST':
        #Procesar una solicitud POST para agregar un riesgo
        data = request.get_json()
        data['risk_id'] = str(risk_id)
        #Guardar el riesgo en Redis con un tiempo de expiración de 10 segundos
        redis_client.setex(str(risk_id),10, json.dumps(data))
        create_product(
            data['city_id'],
            data['city_name'],
            data['risk'],
            data['level'])
        return jsonify({ "status": "ok"}), 201


def add_risk(risk_id: uuid.UUID, **risk_description):
    """
    Almacenar el riesgo en Redis con una expiración de 10 segundos.
    """
    #Convertir el risk_id a string y guardar los datos en Redis
    redis_client.setex(str(risk_id), 10, json.dumps(risk_description))
    #Devolver el riesgo
    return {"city_id": str(risk_id), **risk_description}
