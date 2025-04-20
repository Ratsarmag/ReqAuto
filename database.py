from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import db, CarMake, CarModel, Car, User, Role, Status, RepairRequest, Notification, Chat, Report

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

        car_makes = ['Toyota', 'Ford', 'BMW', 'Audi',
                     'Honda', 'Chevrolet', 'Nissan', 'Volkswagen']
        for make in car_makes:
            car_make = CarMake(carMake=make)
            db.session.add(car_make)
        db.session.commit()

        car_models = [
            ('Corolla', 1), ('Focus', 2), ('X5', 3), ('A4', 4),
            ('Civic', 5), ('Malibu', 6), ('Altima', 7), ('Golf', 8),
            ('Camry', 1), ('Mustang', 2), ('3 Series', 3), ('Q5', 4),
            ('Accord', 5), ('Impala', 6), ('Maxima', 7), ('Passat', 8),
            ('RAV4', 1), ('F-150', 2), ('X3', 3), ('A6', 4),
            ('CR-V', 5), ('Equinox', 6), ('Rogue', 7), ('Tiguan', 8)
        ]
        for model, make_id in car_models:
            car_model = CarModel(carModel=model, carMakeID=make_id)
            db.session.add(car_model)
        db.session.commit()

        users = [
            ('admin', 'Admin123', 'Алексей', 'Петров',
             'Сергеевич', '123456789', datetime(1990, 1, 1), 1),
            ('operator', 'Oper123', 'Мария', 'Иванова',
             'Алексеевна', '987654321', datetime(1985, 5, 5), 2),
            ('mechanic1', 'Mech123', 'Дмитрий', 'Смирнов',
             'Игоревич', '111222333', datetime(1980, 8, 8), 3),
            ('mechanic2', 'Mech456', 'Ольга', 'Кузнецова',
             'Викторовна', '444555666', datetime(1975, 12, 12), 3),
            ('client1', 'Client123', 'Екатерина', 'Новикова',
             'Петровна', '777888999', datetime(1995, 3, 3), 4),
            ('client2', 'Client456', 'Андрей', 'Морозов',
             'Иванов', '222333444', datetime(2000, 7, 7), 4),
            ('client3', 'Client789', 'Анна', 'Соколова',
             'Алексеевна', '333444555', datetime(1988, 11, 11), 4),
            ('client4', 'Client012', 'Сергей', 'Лебедев',
             'Владимирович', '444555666', datetime(1992, 9, 9), 4),
            ('client5', 'Client345', 'Ирина', 'Захарова',
             'Сергеевна', '555666777', datetime(1998, 4, 4), 4)
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
            (1, 5, 'Шум в двигателе при запуске, возможно проблема с подшипниками.', 1),
            (2, 6, 'Тормоза стали менее эффективными, требуется замена колодок.', 1),
            (3, 7, 'Проблемы с переключением передач, возможна неисправность трансмиссии.', 2),
            (4, 8, 'Электрическая система дает сбои, необходима диагностика.', 2),
            (5, 9, 'Подвеска издает стуки при движении по неровной дороге.', 3),
            (6, 5, 'Требуется замена изношенных шин на всех колесах.', 3),
            (7, 6, 'Необходима замена масла и фильтров в двигателе.', 1),
            (8, 7, 'Аккумулятор быстро разряжается, требуется замена.', 1),
            (9, 8, 'Кондиционер не охлаждает салон, необходима проверка.', 2),
            (10, 9, 'Выхлопная система издает громкий звук, возможна пробоина.', 2)
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
