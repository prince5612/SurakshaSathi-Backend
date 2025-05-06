from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import get_db 

def pay_life_insurance_premium(data):
    data = request.get_json()

    required_fields = ['email', 'age', 'gender', 'income', 'occupation_risk', 'dependents', 'predicted_premium']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    email = data["email"]

    db = get_db()
    payments = db["life_insurance_payments"]

    payment_record = {
        "user_email": email,
        "age": data["age"],
        "gender": data["gender"],
        "income": data["income"],
        "occupation_risk": data["occupation_risk"],
        "dependents": data["dependents"],
        "predicted_premium": data["predicted_premium"],
        "payment_date": datetime.utcnow()
    }

    result = payments.insert_one(payment_record)

    return jsonify({"message": "Payment successful", "payment_id": str(result.inserted_id)}), 201

def get_life_details(data):
    """
    Fetch stored life insurance details and last payment for the current user.
    Request JSON: { "email": "user@example.com" }
    Response JSON: { details: {...}, last_payment: { amount, date } }
    """
    
    email = data.get('email') 

    db = get_db()
    details_col = db['user_life_insurance_detail']
    payments_col = db['life_insurance_payments']

    # fetch user details
    details = details_col.find_one({'user_email': email}, {'_id': 0})

    # fetch last payment
    last_pay = payments_col.find_one(
        {'user_email': email},
        sort=[('payment_date', -1)],
        projection={'_id': 0, 'predicted_premium': 1, 'payment_date': 1}
    )

    result = {'details': details}
    if last_pay:
        result['last_payment'] = {
            'amount': last_pay['predicted_premium'],
            'date': last_pay['payment_date'].isoformat()
        }
    return jsonify(result), 200



def create_life_details(data):
    """
    Create new life insurance detail record for user.
    Request JSON: { email, age, gender, income, occupation_risk, dependents }
    """

    required = ['email', 'age', 'gender', 'income', 'occupation_risk', 'dependents']
    if not all(field in data for field in required):
        return jsonify({ 'message': 'Missing required fields' }), 400

    email = data['email']
    db = get_db()
    details_col = db['user_life_insurance_detail']

    # prevent duplicate
    if details_col.find_one({'user_email': email}):
        return jsonify({ 'message': 'Details already exist, use update endpoint' }), 409

    record = {
        'user_email': email,
        'age': data['age'],
        'gender': data['gender'],
        'income': data['income'],
        'occupation_risk': data['occupation_risk'],
        'dependents': data['dependents'],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    details_col.insert_one(record)
    return jsonify({ 'message': 'Details created successfully' }), 201



def update_life_details(data):
    """
    Update existing life insurance detail record for user.
    Request JSON: { email, age, gender, income, occupation_risk, dependents }
    """
   
    required = ['email', 'age', 'gender', 'income', 'occupation_risk', 'dependents']
    if not all(field in data for field in required):
        return jsonify({ 'message': 'Missing required fields' }), 400

    email = data['email']
    db = get_db()
    details_col = db['user_life_insurance_detail']

    update_result = details_col.update_one(
        { 'user_email': email },
        { '$set': {
            'age': data['age'],
            'gender': data['gender'],
            'income': data['income'],
            'occupation_risk': data['occupation_risk'],
            'dependents': data['dependents'],
            'updated_at': datetime.utcnow()
        }}
    )

    if update_result.matched_count == 0:
        return jsonify({ 'message': 'No existing details found' }), 404

    return jsonify({ 'message': 'Details updated successfully' }), 200


def pay_flood_insurance_premium(data):
    data = request.get_json()

    required_fields = ['email', 'rain_mm','has_alert' , 'near_water', 'predicted_premium']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
    
    email = data["email"]

    db = get_db()
    payments = db["flood_insurance_payments"]

    payment_record = {
        "user_email": email,
        "city" : data["city"],
        "rain_mm": data["rain_mm"],
        "has_alert": data["has_alert"],
        "near_water": data["near_water"],
        "predicted_premium": data["predicted_premium"],
        "payment_date": datetime.utcnow()
    }

    result = payments.insert_one(payment_record)

    return jsonify({"message": "Payment successful", "payment_id": str(result.inserted_id)}), 201

def get_last_flood_payment(data):
    
    email = data.get('email') 
    db = get_db()
    payments = db['flood_insurance_payments']
    last = payments.find_one(
        {'user_email': email},
        sort=[('payment_date', -1)],
        projection={'_id': 0, 'predicted_premium': 1, 'payment_date': 1}
    )

    if last:
        return jsonify({'last_payment': {
            'amount': last['predicted_premium'],
            'date': last['payment_date'].isoformat()
        }}), 200

    return jsonify({'last_payment': None}), 200

def get_travel_details(data):
    """
    Fetch stored life insurance details and last payment for the current user.
    Request JSON: { "email": "user@example.com" }
    Response JSON: { details: {...}, last_payment: { amount, date } }
    """
    
    email = data.get('email') 

    db = get_db()
    payments_col = db['travel_insurance_payments']

    # fetch user details
    details = payments_col.find_one({'user_email': email}, {'_id': 0})

    # fetch last payment
    last_pay = payments_col.find_one(
        {'user_email': email},
        sort=[('payment_date', -1)],
        projection={'_id': 0, 'predicted_premium': 1, 'payment_date': 1}
    )

    result = {'details': details}
    if last_pay:
        result['last_payment'] = {
            'amount': last_pay['predicted_premium'],
            'date': last_pay['payment_date'].isoformat()
        }
    return jsonify(result), 200

def pay_travel_insurance_premium(data):
    data = request.get_json()
     
    required_fields = ['email', 'start_date','end_date' , 'transport_mode', 'city','state','duration_days','aqi','crime_index','rainfall_mm','weather_risk','predicted_premium']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
    
    email = data["email"]

    db = get_db()
    payments = db["travel_insurance_payments"]

    payment_record = {
        "user_email": email,
        "city" : data["city"],
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "transport_mode": data["transport_mode"],
        "state": data["state"],
        "duration_days":data["duration_days"] ,
        "aqi":data["aqi"],
        "crime_index":data["crime_index"],
        "rainfall_mm":data["rainfall_mm"],
        "weather_risk":data["weather_risk"],
        "predicted_premium":data["predicted_premium"],
        "payment_date":  datetime.utcnow(),
    }

    result = payments.insert_one(payment_record)

    return jsonify({"message": "Payment successful", "payment_id": str(result.inserted_id)}), 201








def get_car_details(data):
    """
    Return saved car insurance details and last payment for the user.
    Request JSON: { "email": ... }
    Response JSON: { details: {...} or null, last_payment: { amount, date } or null }
    """
    
    email = data.get('email') 

    db = get_db()
    details_col = db['user_car_insurance_detail']
    payments_col = db['car_insurance_payments']

    # fetch user-saved details
    details = details_col.find_one({'user_email': email}, {'_id': 0})

    # fetch last payment
    last = payments_col.find_one(
        {'user_email': email},
        sort=[('payment_date', -1)],
        projection={'_id': 0, 'predicted_premium': 1, 'payment_date': 1}
    )

    result = {'details': details}
    if last:
        result['last_payment'] = {
            'amount': last['predicted_premium'],
            'date': last['payment_date'].isoformat()
        }
    else:
        result['last_payment'] = None

    return jsonify(result), 200



def create_car_details(data):
    """
    Save new car insurance detail record.
    Request JSON: { email, manufacturer_date, car_price_lakhs, city, user_age }
    """
    
    required = ['email', 'manufacturer_date', 'car_price_lakhs', 'city', 'user_age']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400

    email = data['email']
    db = get_db()
    details_col = db['user_car_insurance_detail']

    # avoid duplicate
    if details_col.find_one({'user_email': email}):
        return jsonify({'message': 'Details already exist; use update'}), 409

    record = {
        'user_email': email,
        'manufacturer_date': data['manufacturer_date'],
        'car_price_lakhs': data['car_price_lakhs'],
        'city': data['city'],
        'user_age': data['user_age'],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    details_col.insert_one(record)
    return jsonify({'message': 'Details created'}), 201



def update_car_details(data):
    """
    Update existing car insurance details.
    Request JSON: { email, manufacturer_date, car_price_lakhs, city, user_age }
    """
    required = ['email', 'manufacturer_date', 'car_price_lakhs', 'city', 'user_age']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400

    email = data['email']
    db = get_db()
    details_col = db['user_car_insurance_detail']

    res = details_col.update_one(
        {'user_email': email},
        {'$set': {
            'manufacturer_date': data['manufacturer_date'],
            'car_price_lakhs': data['car_price_lakhs'],
            'city': data['city'],
            'user_age': data['user_age'],
            'updated_at': datetime.utcnow()
        }}
    )
    if res.matched_count == 0:
        return jsonify({'message': 'No existing details found'}), 404

    return jsonify({'message': 'Details updated'}), 200



# def calculate_car_premium(data):
#     """
#     Compute a premium based on car details.
#     Request JSON: { manufacturer_date, car_price_lakhs, city, user_age }
#     Response JSON: { predicted_premium: float }
#     """
    
#     try:
#         price = float(data.get('car_price_lakhs', 0))
#         age = int(data.get('user_age', 0))
#     except (TypeError, ValueError):
#         return jsonify({'error': 'Invalid numeric values'}), 400

#     premium=

#     return jsonify({'predicted_premium': premium}), 200



def pay_car_premium(data):
    """
    Record a premium payment.
    Request JSON: { email, manufacturer_date, car_price_lakhs, city, user_age, predicted_premium }
    """
    
    required = ['email', 'predicted_premium']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400

    email = data['email']
    db = get_db()
    payments_col = db['car_insurance_payments']

    payment_record = {
        'user_email': email,
        'manufacturer_date': data.get('manufacturer_date'),
        'car_price_lakhs': data.get('car_price_lakhs'),
        'city': data.get('city'),
        'user_age': data.get('user_age'),
        'predicted_premium': data['predicted_premium'],
        'payment_date': datetime.utcnow()
    }
    payments_col.insert_one(payment_record)

    return jsonify({'message': 'Payment recorded'}), 201



def pay_health_insurance_premium(data):
    """
    Store a payment record for health insurance.
    Expected JSON: { email, age, gender, bmi, daily_steps, sleep_hours, pre_existing_condition, smoking, alcohol_consumption, predicted_premium }
    """
    data = request.get_json()

    required_fields = ['email', 'age', 'gender', 'bmi', 'daily_steps', 'sleep_hours',
                       'pre_existing_condition', 'smoking', 'alcohol_consumption', 'predicted_premium']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    email = data["email"]

    db = get_db()
    payments = db["health_insurance_payments"]

    payment_record = {
        "user_email": email,
        "age": data["age"],
        "gender": data["gender"],
        "bmi": data["bmi"],
        "daily_steps": data["daily_steps"],
        "sleep_hours": data["sleep_hours"],
        "pre_existing_condition": data["pre_existing_condition"],
        "smoking": data["smoking"],
        "alcohol_consumption": data["alcohol_consumption"],
        "predicted_premium": data["predicted_premium"],
        "payment_date": datetime.utcnow()
    }

    result = payments.insert_one(payment_record)

    return jsonify({"message": "Payment successful", "payment_id": str(result.inserted_id)}), 201


def get_health_details(data):
    """
    Fetch stored health insurance details and last payment for the current user.
    Request JSON: { "email": "user@example.com" }
    Response JSON: { details: {...}, last_payment: { amount, date } }
    """
    email = data.get('email')
    db = get_db()
    details_col = db['user_health_insurance_detail']
    payments_col = db['health_insurance_payments']

    details = details_col.find_one({'user_email': email}, {'_id': 0})

    last_pay = payments_col.find_one(
        {'user_email': email},
        sort=[('payment_date', -1)],
        projection={'_id': 0, 'predicted_premium': 1, 'payment_date': 1}
    )

    result = {'details': details}
    if last_pay:
        result['last_payment'] = {
            'amount': last_pay['predicted_premium'],
            'date': last_pay['payment_date'].isoformat()
        }
    return jsonify(result), 200


def create_health_details(data):
    """
    Create new health insurance detail record for user.
    Request JSON: { email, age, gender, bmi, daily_steps, sleep_hours, pre_existing_condition, smoking, alcohol_consumption }
    """
    required = ['email', 'age', 'gender', 'bmi', 'daily_steps', 'sleep_hours',
                'pre_existing_condition', 'smoking', 'alcohol_consumption']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400

    email = data['email']
    db = get_db()
    details_col = db['user_health_insurance_detail']

    if details_col.find_one({'user_email': email}):
        return jsonify({'message': 'Details already exist, use update endpoint'}), 409

    record = {
        'user_email': email,
        'age': data['age'],
        'gender': data['gender'],
        'bmi': data['bmi'],
        'daily_steps': data['daily_steps'],
        'sleep_hours': data['sleep_hours'],
        'pre_existing_condition': data['pre_existing_condition'],
        'smoking': data['smoking'],
        'alcohol_consumption': data['alcohol_consumption'],
        'city' : data['city'],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    details_col.insert_one(record)
    return jsonify({'message': 'Details created successfully'}), 201


def update_health_details(data):
    """
    Update existing health insurance detail record for user.
    Request JSON: { email, age, gender, bmi, daily_steps, sleep_hours, pre_existing_condition, smoking, alcohol_consumption }
    """
    required = ['email', 'age', 'gender', 'bmi', 'daily_steps', 'sleep_hours',
                'pre_existing_condition', 'smoking', 'alcohol_consumption']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400

    email = data['email']
    db = get_db()
    details_col = db['user_health_insurance_detail']

    update_result = details_col.update_one(
        {'user_email': email},
        {'$set': {
            'age': data['age'],
            'gender': data['gender'],
            'bmi': data['bmi'],
            'daily_steps': data['daily_steps'],
            'sleep_hours': data['sleep_hours'],
            'pre_existing_condition': data['pre_existing_condition'],
            'smoking': data['smoking'],
            'alcohol_consumption': data['alcohol_consumption'],
            'city' : data['city'],
            'updated_at': datetime.utcnow()
        }}
    )

    if update_result.matched_count == 0:
        return jsonify({'message': 'No existing details found'}), 404

    return jsonify({'message': 'Details updated successfully'}), 200