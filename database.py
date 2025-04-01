from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import db, CarMake, CarModel, Car, User, Role, Status, RepairRequest, Notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SECRET_KEY'] = '46aed87c7b79f71e5f6c420140b4726eda4af85315ec49aa63959f1403a4703e'
db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()

        roles = ['Администратор', 'Оператор', 'Механик', 'Клиент']
        for role_name in roles:
            role = Role(roleName=role_name)
            db.session.add(role)
        db.session.commit()

        statuses = ['Новая заявка', 'В работе', 'Завершена']
        for status_name in statuses:
            status = Status(status=status_name)
            db.session.add(status)
        db.session.commit()

        car_makes = ['Toyota', 'Ford', 'BMW', 'Audi']
        for make in car_makes:
            car_make = CarMake(carMake=make)
            db.session.add(car_make)
        db.session.commit()

        car_models = [
            ('Corolla', 1), ('Focus', 2), ('X5', 3), ('A4', 4),
            ('Camry', 1), ('Mustang', 2), ('3 Series', 3), ('Q5', 4),
            ('RAV4', 1), ('F-150', 2)
        ]
        for model, make_id in car_models:
            car_model = CarModel(carModel=model, carMakeID=make_id)
            db.session.add(car_model)
        db.session.commit()

        users = [
            ('admin', 'Admin123', 'Иван', 'Иванов',
             'Иванович', '123456789', datetime(1990, 1, 1), 1),
            ('operator', 'Oper123', 'Петр', 'Петров',
             'Петрович', '987654321', datetime(1985, 5, 5), 2),
            ('mechanic1', 'Mech123', 'Сергей', 'Сергеев',
             'Сергеевич', '111222333', datetime(1980, 8, 8), 3),
            ('mechanic2', 'Mech456', 'Алексей', 'Алексеев',
             'Алексеевич', '444555666', datetime(1975, 12, 12), 3),
            ('client1', 'Client123', 'Анна', 'Аннова',
             'Анновна', '777888999', datetime(1995, 3, 3), 4),
            ('client2', 'Client456', 'Мария', 'Марина',
             'Мариновна', '222333444', datetime(2000, 7, 7), 4)
        ]
        for user_data in users:
            hashed_password = generate_password_hash(
                user_data[1], method='pbkdf2:sha256')
            user = User(
                username=user_data[0],
                password=hashed_password,
                firstName=user_data[2],
                lastName=user_data[3],
                patronymic=user_data[4],
                phone=user_data[5],
                dateBirth=user_data[6],
                roleID=user_data[7]
            )
            db.session.add(user)
        db.session.commit()

        cars = [
            (1, 1), (2, 2), (3, 3), (4, 4),
            (1, 5), (2, 6), (3, 7), (4, 8),
            (1, 9), (2, 10)
        ]
        for make_id, model_id in cars:
            car = Car(carMakeID=make_id, carModelID=model_id)
            db.session.add(car)
        db.session.commit()

        repair_requests = [
            (1, 5, 'Шум в двигателе', 1),
            (2, 6, 'Проблема с тормозами', 1),
            (3, 5, 'Проблема с трансмиссией', 2),
            (4, 6, 'Электрическая неисправность', 2),
            (5, 5, 'Ремонт подвески', 3),
            (6, 6, 'Замена шин', 3),
            (7, 5, 'Замена масла', 1),
            (8, 6, 'Замена аккумулятора', 1),
            (9, 5, 'Обслуживание кондиционера', 2),
            (10, 6, 'Ремонт выхлопной системы', 2)
        ]
        for car_id, user_id, description, status_id in repair_requests:
            request = RepairRequest(
                carID=car_id,
                userID=user_id,
                defectsDescription=description,
                statusID=status_id
            )
            db.session.add(request)
        db.session.commit()


if __name__ == '__main__':
    init_db()
