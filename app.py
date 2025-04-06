from flask import Flask, request, render_template, redirect, url_for, jsonify, session, make_response
from models import db, User, Car, RepairRequest, Status, CarMake, CarModel, Role, Notification
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from sqlalchemy import func
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SECRET_KEY'] = '46aed87c7b79f71e5f6c420140b4726eda4af85315ec49aa63959f1403a4703e'
db.init_app(app)


@app.route('/')
def index():
    car_makes = CarMake.query.all()
    user_data = None

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        user_data = {
            'firstName': user.firstName,
            'lastName': user.lastName,
            'patronymic': user.patronymic,
            'phone': user.phone
        }

    return render_template('index.html', car_makes=car_makes, user_data=user_data)


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user.roleID != 1:
        return redirect(url_for('auth'))

    users = User.query.all()
    repair_requests = RepairRequest.query.all()

    return render_template('admin_dashboard.html', users=users)


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


@app.route('/profile_requests')
def profile_requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile_requests.html')


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

    if 'user_id' not in session:
        new_user = User(
            firstName=firstName,
            lastName=lastName,
            phone=phone,
            roleID=4
        )
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.ID
    else:
        user_id = session['user_id']

    new_car = Car(
        carMakeID=carMakeID,
        carModelID=carModelID
    )
    db.session.add(new_car)
    db.session.commit()

    new_repair_request = RepairRequest(
        carID=new_car.ID,
        userID=user_id,
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


@app.route('/api/user-repair-requests', methods=['GET'])
def get_user_repair_requests():
    if 'user_id' not in session:
        return jsonify([]), 403

    user_id = session['user_id']
    repair_requests = RepairRequest.query.filter_by(userID=user_id).all()

    requests_data = []
    for index, request in enumerate(repair_requests, start=1):
        user = User.query.get(request.userID)
        car = Car.query.get(request.carID)
        car_make = CarMake.query.get(car.carMakeID)
        car_model = CarModel.query.get(car.carModelID)
        status = Status.query.get(request.statusID)

        request_data = {
            'number': index,
            'id': request.ID,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'phone': user.phone,
            'carMake': car_make.carMake,
            'carModel': car_model.carModel,
            'defectsDescription': request.defectsDescription,
            'status': status.status,
            'created_at': request.created_at,
            'accepted_at': request.accepted_at,
            'completed_at': request.completed_at
        }
        requests_data.append(request_data)

    return jsonify(requests_data)


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

        user_requests = RepairRequest.query.filter_by(
            userID=repair_request.userID).order_by(RepairRequest.created_at).all()
        request_number = user_requests.index(repair_request) + 1

        notification = Notification(
            userID=repair_request.userID,
            message=f"Ваша заявка под номером #{request_number} была отредактирована оператором сервиса"
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Заявка не найдена'}), 404


@app.route('/api/car-make/<int:car_make_id>', methods=['GET'])
def get_car_make(car_make_id):
    car_make = CarMake.query.get(car_make_id)
    if car_make:
        return jsonify({'carMake': car_make.carMake})
    return jsonify({'status': 'error', 'message': 'Марка автомобиля не найдена'}), 404


@app.route('/api/car-model/<int:car_model_id>', methods=['GET'])
def get_car_model(car_model_id):
    car_model = CarModel.query.get(car_model_id)
    if car_model:
        return jsonify({'carModel': car_model.carModel})
    return jsonify({'status': 'error', 'message': 'Модель автомобиля не найдена'}), 404


@app.route('/api/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    roles_data = [{"ID": role.ID, "roleName": role.roleName} for role in roles]
    return jsonify(roles_data)


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
        repair_request.accepted_at = datetime.utcnow()
        repair_request.mechanicID = mechanic_id
        db.session.commit()
        new_status = Status.query.get(2).status

        user_requests = RepairRequest.query.filter_by(
            userID=repair_request.userID).order_by(RepairRequest.created_at).all()
        request_number = user_requests.index(repair_request) + 1

        notification = Notification(
            userID=repair_request.userID,
            message=f"Ваша заявка под номером #{request_number} принята в работу"
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({'status': 'success', 'new_status': new_status})
    return jsonify({'status': 'error', 'message': 'Заявка не найдена'}), 404


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "User not found"}), 404


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()

    if request.method == 'POST':
        user.firstName = request.form['firstName']
        user.lastName = request.form['lastName']
        user.patronymic = request.form['patronymic']
        user.phone = request.form['phone']
        user.roleID = request.form['roleID']

        if 'username' in request.form and request.form['username']:
            user.username = request.form['username']
        if 'password' in request.form and request.form['password']:
            user.password = generate_password_hash(request.form['password'])

        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_user.html', user=user, roles=roles)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    roles = Role.query.all()

    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        patronymic = request.form['patronymic']
        phone = request.form['phone']
        roleID = request.form['roleID']
        username = request.form['username']
        password = request.form['password']

        new_user = User(
            firstName=firstName,
            lastName=lastName,
            patronymic=patronymic,
            phone=phone,
            roleID=roleID,
            username=username,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('create_user.html', roles=roles)


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    if 'user_id' not in session:
        return jsonify([]), 403

    user_id = session['user_id']
    notifications = Notification.query.filter_by(userID=user_id).all()

    notifications_data = [
        {
            "message": notification.message,
            "created_at": notification.created_at,
            "read": notification.read
        }
        for notification in notifications
    ]

    return jsonify(notifications_data)


@app.route('/api/notifications/mark-all-as-read', methods=['POST'])
def mark_all_as_read():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Пользователь не авторизован"}), 403

    user_id = session['user_id']
    notifications = Notification.query.filter_by(
        userID=user_id, read=False).all()

    for notification in notifications:
        notification.read = True

    db.session.commit()
    return jsonify({"status": "success"})


def calculate_average_completion_time():
    completed_requests = RepairRequest.query.filter(
        RepairRequest.completed_at.isnot(None)).all()

    total_time = timedelta()
    for request in completed_requests:
        if request.created_at and request.completed_at:
            total_time += request.completed_at - request.created_at

    if len(completed_requests) > 0:
        avg_time = total_time / len(completed_requests)
        return avg_time.days
    return 0


def calculate_requests_by_hour():
    requests_by_hour = db.session.query(
        func.strftime('%H', RepairRequest.created_at).label('hour'),
        func.count(RepairRequest.ID).label('count')
    ).group_by(func.strftime('%H', RepairRequest.created_at)).all()

    requests_by_hour_list = [
        {"hour": int(hour), "count": count} for hour, count in requests_by_hour]

    return requests_by_hour_list


@app.route('/admin_statistics')
def admin_statistics():
    if 'user_id' not in session:
        return redirect(url_for('auth'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user.roleID != 1:
        return redirect(url_for('auth'))

    total_users = User.query.count()
    roles = Role.query.all()
    users_by_role = {role.roleName: User.query.filter_by(
        roleID=role.ID).count() for role in roles}

    total_requests = RepairRequest.query.count()
    new_requests = RepairRequest.query.filter_by(statusID=1).count()
    in_progress_requests = RepairRequest.query.filter_by(statusID=2).count()
    completed_requests = RepairRequest.query.filter_by(statusID=3).count()

    avg_completion_time = calculate_average_completion_time()

    requests_by_hour = calculate_requests_by_hour()

    return render_template('admin_statistics.html',
                           total_users=total_users,
                           users_by_role=users_by_role,
                           total_requests=total_requests,
                           new_requests=new_requests,
                           in_progress_requests=in_progress_requests,
                           completed_requests=completed_requests,
                           avg_completion_time=avg_completion_time,
                           requests_by_hour=requests_by_hour)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
