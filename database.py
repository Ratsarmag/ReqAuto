from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, CarMake, CarModel, Car, User, Role, Status, RepairRequest

#db = SQLAlchemy()

#def init_app(app):
 #   app.config[
  #      'SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://ratsa:RingLord24@RATSARMAG\SQLEXPRESS/practice?driver=ODBC+Driver+17+for+SQL+Server'
   # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #db.init_app(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print('Создана база данных requests')