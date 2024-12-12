from flask import jsonify, Flask, request, make_response
import uuid
import os

from risks import get_risk, add_risk

app = Flask(__name__)


@app.route('/risk/<risk_id>', methods=['POST'])
def create_risk(risk_id: uuid.UUID):
    """This endpoint creates a new risk associated with a city"""
    try:
        assert risk_id, "missing risk_id parameter"
        body = request.json
        assert "risk" in body, "missing risk parameter"
        assert len(body["risk"]) <= 80, "risk must be less than 80 characters"
        assert "level" in body, "missing level parameter"
        assert isinstance(body["level"], int), "level must be an integer"
        assert "city_name" in body, "missing city_name parameter"
        assert len(body["city_name"]) <= 180, "city_name must be less than 180 characters"
    except AssertionError as e:
        return make_response(jsonify({"error": str(e)}), 400)

    response = add_risk(risk_id=risk_id, **body)

    return make_response(jsonify(response), 201)


@app.route('/risk/<risk_id>', methods=['GET'])
def retrieve_risk(risk_id):
    response = get_risk(risk_id)
    if response: #Si se encuentra el riesgo
        return jsonify(response), 200
    else:  #Si no se encuentra el riesgo
        return jsonify({"error": "Risk not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ["PORT"]))
