from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)


class Notification(db.Model):
    __tablename__ = 'Notification'
    ID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.ID'), nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)


class Chat(db.Model):
    __tablename__ = 'ChatSupport'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    operator_id = db.Column(db.Integer, nullable=True)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey(
        'RepairRequest.ID'), nullable=True)
    mechanicID = db.Column(db.Integer, db.ForeignKey('User.ID'), nullable=True)
    description = db.Column(db.Text, nullable=False)
    diagnostics = db.Column(db.Text, nullable=True)
    materials = db.Column(db.Text, nullable=False)
    tools_used = db.Column(db.Text, nullable=True)
    complexity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    recommendations = db.Column(db.Text, nullable=True)
    before_photos = db.Column(db.Text, nullable=True)
    after_photos = db.Column(db.Text, nullable=True)
    mechanic_comments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
