from flask import Flask, request, jsonify
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from config import config_const
import io
import base64
from core import reconhecimentoImagemEstatica
from model import DataModels
import jsonpickle
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config_const.POSTGRESQL_CONNECTION_URL
db = SQLAlchemy(app)
@app.route('/beneficiary', methods=['POST'])
def beneficiaryInclusion():
    received = request.get_json()
    receivedValidations = {'error':[]}
    if 'name' not in received:
        receivedValidations['error'].append('"name" not found in the body')
    if 'cpf' not in received:
        receivedValidations['error'].append('"cpf" not found in the body')
    if 'checkImage' not in received:
        receivedValidations['error'].append('"checkImage" not found in the body')
    if len(receivedValidations['error']) > 0:
        return jsonify(receivedValidations), 400

    newBeneficiary = DataModels.Beneficiary(name=received['name'],image=received['checkImage'],documentNumber=received['cpf'],active=True)

    db.session.add(newBeneficiary)
    db.session.commit()
    beneficiario = db.session.query(DataModels.Beneficiary).filter_by(documentNumber= received["cpf"]).first()
    beneficiarioObj = {"id":beneficiario.id,"name":beneficiario.name,"documentNumber":beneficiario.documentNumber,"active":beneficiario.active}

    return jsonify(beneficiarioObj), 201

@app.route('/classroom/presence_list', methods=['POST'])
def verifyPresence():
    received = request.get_json()
    receivedValidations = {'error':[]}
    if 'image' not in received:
        receivedValidations['error'].append('"image" not found in the body')
    if 'classId' not in received:
        receivedValidations['error'].append('"classId" not found in the body')
    if len(receivedValidations['error']) > 0:
        return jsonify(receivedValidations), 400
    
    roomImageBytes = base64.b64decode(received['image'])
    image = Image.open(io.BytesIO(roomImageBytes))
    response = reconhecimentoImagemEstatica.roomValidate(image,received['classId'],db)

    return jsonify(response), 200


@app.route('/classroom', methods=['POST'])
def createClassroom():
    received = request.get_json()
    receivedValidations = {'error':[]}
    if 'name' not in received:
        receivedValidations['error'].append('"image" not found in the body')
    if len(receivedValidations['error']) > 0:
        return jsonify(receivedValidations), 400
    
    newClassroom = DataModels.Classroom(name=received['name'])
    db.session.add(newClassroom)
    db.session.commit()
    
    return jsonify({'message':'Classe criada com sucesso'}), 201


@app.route('/beneficiary/<beneficiary_id>/classroom', methods=['PUT'])
def includeClassroom(beneficiary_id):
    received = request.get_json()
    receivedValidations = {'error':[]}
    if 'classId' not in received:
        receivedValidations['error'].append('"classId" not found in the body')
    if len(receivedValidations['error']) > 0:
        return jsonify(receivedValidations), 400
    beneficiary = db.session.query(DataModels.Beneficiary).get(beneficiary_id)
    classroom = db.session.query(DataModels.Classroom).get(int(received['classId']))
    beneficiary.classrooms.append(classroom)
    db.session.commit()

    return jsonify({'message':'Classe adicionada com sucesso'}), 200

@app.route('/beneficiary/<beneficiary_id>/classroom/<classroom_id>', methods=['DELETE'])
def removeClassroom(beneficiary_id,classroom_id):
    received = request.get_json()
    receivedValidations = {'error':[]}
    if 'classId' not in received:
        receivedValidations['error'].append('"image" not found in the body')
    if len(receivedValidations['error']) > 0:
        return jsonify(receivedValidations), 400
    
    beneficiary = DataModels.Beneficiary.query(id=beneficiary_id).first()
    beneficiary.classrooms.append(received['classId'])
    db.session.commit()

    return jsonify({'message':'Classe adicionada com sucesso'}), 200


if __name__ == '__main__':
    app.run(debug=True)
