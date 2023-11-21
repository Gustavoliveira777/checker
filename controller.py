from flask import Flask, request, jsonify
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from config import config_const
import io
import base64
from core import reconhecimentoImagemEstatica
from model import Beneficiary
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
    if 'classroomId' not in received:
        receivedValidations['error'].append('"classroomId" not found in the body')
    if len(receivedValidations['error']) > 0:
        return jsonify(receivedValidations), 400

    newBeneficiary = Beneficiary.Beneficiary(name=received['name'],image=received['checkImage'],documentNumber=received['cpf'],classroomId=received['classroomId'])

    db.session.add(newBeneficiary)
    db.session.commit()

    return jsonify({'message':'Beneficiário criado com sucesso'}), 201

@app.route('/classroom/verify', methods=['POST'])
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
    response = reconhecimentoImagemEstatica.roomValidate(imageRoomPIL=image)

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
