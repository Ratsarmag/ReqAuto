from flask import Flask, request, render_template, redirect, url_for, jsonify
from models import db, User, Car, RepairRequest, Status, CarMake, CarModel
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://ratsa:RingLord24@RATSARMAG\SQLEXPRESS/practice?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    car_makes = CarMake.query.all()
    return render_template('index.html', car_makes=car_makes)


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/clients_requests')
def clients_requests():
    return render_template('clients_requests.html')


@app.route('/auth-submit', methods=['POST'])
def auth_submit():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({"status": "error", "message": "Неправильный логин или пароль"})

    if user.roleID == 1:
        return jsonify({"status": "success", "redirect": url_for('admin_dashboard')})
    elif user.roleID == 2:
        return jsonify({"status": "success", "redirect": url_for('clients_requests')})
    elif user.roleID == 3:
        return jsonify({"status": "success", "redirect": url_for('mechanic_dashboard')})
    elif user.roleID == 4:
        return jsonify({"status": "success", "redirect": url_for('client_dashboard')})

    return jsonify({"status": "error", "message": "Unknown error"})


@app.route('/get_models/<int:car_make_id>')
def get_models(car_make_id):
    car_models = CarModel.query.filter_by(carMakeID=car_make_id).all()
    return jsonify([{'ID': model.ID, 'carModel': model.carModel} for model in car_models])


@app.route('/submit', methods=['POST'])
def submit():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phone = request.form['phone']
    carMakeID = request.form['carMake']
    carModelID = request.form['carModel']
    defectsDescription = request.form['defectsDescription']

    new_user = User(
        firstName=firstName,
        lastName=lastName,
        phone=phone
    )
    db.session.add(new_user)
    db.session.commit()

    new_car = Car(
        carMakeID=carMakeID,
        carModelID=carModelID
    )
    db.session.add(new_car)
    db.session.commit()

    default_status = Status.query.filter_by(ID=1).first()
    if not default_status:
        default_status = Status(status="Новая заявка")
        db.session.add(default_status)
        db.session.commit()

    new_repair_request = RepairRequest(
        carID=new_car.ID,
        userID=new_user.ID,
        defectsDescription=defectsDescription,
        statusID=default_status.ID
    )
    db.session.add(new_repair_request)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
