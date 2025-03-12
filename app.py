from flask import Flask, request, render_template, redirect, url_for, jsonify, session, make_response
from models import db, User, Car, RepairRequest, Status, CarMake, CarModel, Role
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SECRET_KEY'] = '46aed87c7b79f71e5f6c420140b4726eda4af85315ec49aa63959f1403a4703e'
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
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user.roleID != 2:
        return redirect(url_for('auth'))

    response = make_response(render_template('clients_requests.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    response = make_response(render_template('profile.html', user=user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.firstName = request.form['firstName']
        user.lastName = request.form['lastName']
        user.patronymic = request.form['patronymic']
        user.phone = request.form['phone']
        user.dateBirth = datetime.strptime(
            request.form['dateBirth'], '%Y-%m-%d')

        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                photo_path = f"static/uploads/{secure_filename(photo.filename)}"
                photo.save(photo_path)
                user.photo = photo_path

        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    response = make_response(redirect(url_for('auth')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/check-session', methods=['POST'])
def check_session():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        role = Role.query.get(user.roleID).roleName
        return jsonify({"authenticated": True, "role": role})
    return jsonify({"authenticated": False}), 401


@app.route('/auth-submit', methods=['POST'])
def auth_submit():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"status": "error", "message": "Неправильный логин или пароль"})

    session['user_id'] = user.ID

    if user.roleID == 1:
        return jsonify({"status": "success", "redirect": url_for('admin_dashboard')})
    elif user.roleID == 2:
        return jsonify({"status": "success", "redirect": url_for('clients_requests')})
    elif user.roleID == 3:
        return jsonify({"status": "success", "redirect": url_for('mechanic_dashboard')})
    elif user.roleID == 4:
        return jsonify({"status": "success", "redirect": url_for('profile')})

    return jsonify({"status": "error", "message": "Ошибка авторизации"})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstName = request.form['firstName'].strip()
        lastName = request.form['lastName'].strip()
        patronymic = request.form['patronymic'].strip()
        phone = request.form['phone'].strip()
        dateBirth = datetime.strptime(request.form['dateBirth'], '%Y-%m-%d')
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256')

        default_photo_path = url_for(
            'static', filename='uploads/no_image-600x315_0.jpg')

        new_user = User(
            firstName=firstName,
            lastName=lastName,
            patronymic=patronymic,
            phone=phone,
            dateBirth=dateBirth,
            username=username,
            password=hashed_password,
            roleID=4,
            photo=default_photo_path
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth'))

    return render_template('register.html')


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

    new_repair_request = RepairRequest(
        carID=new_car.ID,
        userID=new_user.ID,
        defectsDescription=defectsDescription,
        statusID=1
    )
    db.session.add(new_repair_request)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/api/repair-requests', methods=['GET'])
def get_repair_requests():
    repair_requests = RepairRequest.query.all()
    requests_data = []
    for request in repair_requests:
        user = User.query.get(request.userID)
        car = Car.query.get(request.carID)
        car_make = CarMake.query.get(car.carMakeID)
        car_model = CarModel.query.get(car.carModelID)
        status = Status.query.get(request.statusID)
        requests_data.append({
            'id': request.ID,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'phone': user.phone,
            'carMake': car_make.carMake,
            'carModel': car_model.carModel,
            'defectsDescription': request.defectsDescription,
            'status': status.status,
            'isAccepted': request.statusID == 2 or request.statusID == 3

        })
    return jsonify(requests_data)


@app.route('/api/repair-requests/<int:request_id>', methods=['GET'])
def get_repair_request(request_id):
    repair_request = RepairRequest.query.get(request_id)
    if repair_request:
        user = User.query.get(repair_request.userID)
        car = Car.query.get(repair_request.carID)
        car_make = CarMake.query.get(car.carMakeID)
        car_model = CarModel.query.get(car.carModelID)
        return jsonify({
            'id': repair_request.ID,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'phone': user.phone,
            'carMakeID': car_make.ID,
            'carModelID': car_model.ID,
            'defectsDescription': repair_request.defectsDescription
        })
    return jsonify({'status': 'error', 'message': 'Заявка не найдена'}), 404


@app.route('/api/repair-requests/<int:request_id>/edit', methods=['POST'])
def edit_request(request_id):
    repair_request = RepairRequest.query.get(request_id)
    if repair_request:
        user = User.query.get(repair_request.userID)
        car = Car.query.get(repair_request.carID)

        user.firstName = request.form['firstName']
        user.lastName = request.form['lastName']
        user.phone = request.form['phone']

        car_make = CarMake.query.filter_by(
            carMake=request.form['carMake']).first()
        car_model = CarModel.query.filter_by(
            carModel=request.form['carModel'], carMakeID=car_make.ID).first()

        if not car_make:
            car_make = CarMake(carMake=request.form['carMake'])
            db.session.add(car_make)
            db.session.commit()

        if not car_model:
            car_model = CarModel(
                carModel=request.form['carModel'], carMakeID=car_make.ID)
            db.session.add(car_model)
            db.session.commit()

        car.carMakeID = car_make.ID
        car.carModelID = car_model.ID
        repair_request.defectsDescription = request.form['defectsDescription']

        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Request not found'}), 404


@app.route('/api/car-make/<int:car_make_id>', methods=['GET'])
def get_car_make(car_make_id):
    car_make = CarMake.query.get(car_make_id)
    if car_make:
        return jsonify({'carMake': car_make.carMake})
    return jsonify({'status': 'error', 'message': 'Car make not found'}), 404


@app.route('/api/car-model/<int:car_model_id>', methods=['GET'])
def get_car_model(car_model_id):
    car_model = CarModel.query.get(car_model_id)
    if car_model:
        return jsonify({'carModel': car_model.carModel})
    return jsonify({'status': 'error', 'message': 'Car model not found'}), 404


@app.route('/api/mechanics', methods=['GET'])
def get_mechanics():
    all_mechanics = User.query.filter_by(roleID=3).all()
    active_requests = RepairRequest.query.filter_by(statusID=2).all()
    busy_mechanic_ids = [
        request.mechanicID for request in active_requests if request.mechanicID is not None]
    available_mechanics = [
        mechanic for mechanic in all_mechanics if mechanic.ID not in busy_mechanic_ids]
    mechanics_data = [{'ID': mechanic.ID, 'firstName': mechanic.firstName,
                       'lastName': mechanic.lastName} for mechanic in available_mechanics]
    return jsonify(mechanics_data)


@app.route('/api/repair-requests/<int:request_id>/accept', methods=['POST'])
def accept_request(request_id):
    repair_request = RepairRequest.query.get(request_id)
    if repair_request:
        mechanic_id = request.form['mechanicId']
        repair_request.statusID = 2
        repair_request.mechanicID = mechanic_id
        db.session.commit()
        new_status = Status.query.get(2).status
        return jsonify({'status': 'success', 'new_status': new_status})
    return jsonify({'status': 'error', 'message': 'Request not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
