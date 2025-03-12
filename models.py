# from database import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CarMake(db.Model):
    __tablename__ = 'CarMake'
    ID = db.Column(db.Integer, primary_key=True)
    carMake = db.Column(db.String(50), unique=True)


class CarModel(db.Model):
    __tablename__ = 'CarModel'
    ID = db.Column(db.Integer, primary_key=True)
    carMakeID = db.Column(db.Integer, db.ForeignKey('CarMake.ID'))
    carModel = db.Column(db.String(50))


class Car(db.Model):
    __tablename__ = 'Car'
    ID = db.Column(db.Integer, primary_key=True)
    carMakeID = db.Column(db.Integer, db.ForeignKey('CarMake.ID'))
    carModelID = db.Column(db.Integer, db.ForeignKey('CarModel.ID'))


class User(db.Model):
    __tablename__ = 'User'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    patronymic = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    dateBirth = db.Column(db.Date, nullable=True)
    roleID = db.Column(db.Integer, db.ForeignKey('Role.ID'))
    photo = db.Column(db.String(256), nullable=True)


class Role(db.Model):
    __tablename__ = 'Role'
    ID = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(50))


class Status(db.Model):
    __tablename__ = 'Status'
    ID = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))


class RepairRequest(db.Model):
    __tablename__ = 'RepairRequest'
    ID = db.Column(db.Integer, primary_key=True)
    carID = db.Column(db.Integer, db.ForeignKey('Car.ID'))
    userID = db.Column(db.Integer, db.ForeignKey('User.ID'))
    defectsDescription = db.Column(db.String)
    statusID = db.Column(db.Integer, db.ForeignKey('Status.ID'))
    mechanicID = db.Column(db.Integer, db.ForeignKey('User.ID'), nullable=True)
