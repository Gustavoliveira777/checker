from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

beneficiary_classroom = db.Table('beneficiary_classroom',
    db.Column('beneficiary_id', db.Integer, db.ForeignKey('beneficiary.id')),
    db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id'))
)

class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    beneficiaries = db.relationship('Beneficiary', secondary=beneficiary_classroom, backref=db.backref('classroom', lazy='dynamic'))

class Beneficiary(db.Model):
    __tablename__ = 'beneficiary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.Text)
    documentNumber = db.Column(db.String(12))
    active = db.Column(db.Boolean)
    classrooms = db.relationship('Classroom', secondary=beneficiary_classroom, backref=db.backref('beneficiary', lazy='dynamic'))