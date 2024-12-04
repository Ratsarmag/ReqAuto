from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://ratsa:RingLord24@RATSARMAG\SQLEXPRESS/practice?driver=ODBC+Driver+17+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)