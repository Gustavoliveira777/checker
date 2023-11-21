from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    beneficiaries = db.relationship('Beneficiary', backref='classroom', lazy=True)  

class Beneficiary(db.Model):
    __tablename__ = 'beneficiary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.Text)
    documentNumber = db.Column(db.String(12))
    classroomId = db.Column(db.Integer, db.ForeignKey('classroom.id'))