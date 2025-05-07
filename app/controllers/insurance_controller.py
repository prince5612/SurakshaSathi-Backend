from flask import request, jsonify ,current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import get_db 
import os
from werkzeug.utils import secure_filename
import cloudinary.uploader

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



def sum_user_premiums(email,col):
    db = get_db()
    pipeline = [
        { "$match": { "user_email": email } },
        { "$group": {
            "_id": None,
            "total_premium": { "$sum": "$predicted_premium" }
        }},
        { "$project": { "_id": 0, "total_premium": 1 } }
    ]

    agg_result = list(col.aggregate(pipeline))
    result = agg_result[0]['total_premium'] if agg_result else 0.0
    return int(result)

def get_active_policies(data):
    email = data.get('email') 
    db = get_db()


    Life=db['life_insurance_payments']
    Travel=db['travel_insurance_payments']
    Flood=db['flood_insurance_payments']
    Health=db['health_insurance_payments']
    Car=db['car_insurance_payments']
    
    all_policies = []
    l1= Life.find_one( {'user_email': email},
        projection={'_id': 0},
        sort=[('payment_date', -1)])
    
    if(l1):
        l1['type']="Life"
        l1['total_premium']=sum_user_premiums(email,Life)
        all_policies.append(l1)

    t1=Travel.find_one({'user_email': email},
       projection={'_id': 0},
        sort=[('payment_date', -1)])
    
    if(t1):
        t1['type']="Travel"
        t1['total_premium']=sum_user_premiums(email,Travel)
        all_policies.append(t1)

    h1=Health.find_one({'user_email': email},
       projection={'_id': 0},
        sort=[('payment_date', -1)])

    if(h1):
        h1['type']="Health"
        h1['total_premium']=sum_user_premiums(email,Health)
        all_policies.append(h1)
    
    c1=Car.find_one({'user_email': email},
       projection={'_id': 0},
        sort=[('payment_date', -1)])
    
    if(c1):
        c1['type']="Car"
        c1['total_premium']=sum_user_premiums(email,Car)
        all_policies.append(c1)
    
    f1=Flood.find_one({'user_email': email},
       projection={'_id': 0},
        sort=[('payment_date', -1)])
    if(f1):
        f1['type']="Flood"
        f1['total_premium']=sum_user_premiums(email,Flood)
        all_policies.append(f1)
    
    print(all_policies)

    return jsonify({"policies": all_policies}), 200


def user_claims_all(data):
    email = data['email']
    print(email)

    db = get_db()
    claims_col=db['claims_requests']

    # fetch user details
    claims = claims_col.find({'user_email': email}, {'_id': 0})

    result = []
    for claim in claims:
        result.append({
            'type': claim.get('type'),
            'status': claim.get('status'),
            'request_date': claim.get('date'),
        })
    print(result)
    return jsonify(result), 200

def user_claims_request():
    email       = request.form.get('email')
    policy_type = request.form.get('policy_type')
    files       = request.files.getlist('documents')
    if not all([email, policy_type, files]):
        return jsonify(message="Missing required form fields"), 400

    db = get_db()
    cr = {
        'user_email': email,
        'type': policy_type,
        'status': 'Pending',
        'date': datetime.utcnow(),
        'documents': []
    }
    result = db['claims_requests'].insert_one(cr)
    claim_id = str(result.inserted_id)

    docs_info = []
    for f in files:
        filename = secure_filename(f.filename)
        file_ext = os.path.splitext(filename)[1]

        # upload to Cloudinary, force PDF delivery
        upload_result = cloudinary.uploader.upload(
            f,                            # the file object
            resource_type="raw", 
            folder=f"claims/{claim_id}/",
            format="pdf"                  # ← ensure deliverable as PDF
        )

        docs_info.append({
            'filename': filename,
            'url': upload_result['secure_url'],
            'uploaded_at': datetime.utcnow().isoformat(),
            'extension': file_ext
        })

    # update record with Cloudinary URLs
    db['claims_requests'].update_one(
        {'_id': result.inserted_id},
        {'$set': {'documents': docs_info}}
    )

    return jsonify({
        "message": "Claim submitted with files",
        "claim_id": claim_id,
        "documents": docs_info
    }), 201

def get_payment_history(data):
    """
    POST /api/insurance/payments/history
    Body: { "email": "user@example.com" }
    Returns:
      {
        "Life":    [ { "date": "...", "amount": 500 }, … ],
        "Car":     [ … ],
        "Health":  [ … ],
        "Flood":   [ … ],
        "Travel":  [ … ]
      }
    """
    email = data.get("email")
    if not email:
        return jsonify({"message": "email required"}), 400

    db = get_db()
    policy_collections = {
        "Life": "life_insurance_payments",
        "Car": "car_insurance_payments",
        "Health": "health_insurance_payments",
        "Flood": "flood_insurance_payments",
        "Travel": "travel_insurance_payments"
    }

    history = {}
    for policy_name, coll in policy_collections.items():
        docs = db[coll].find({"user_email": email}).sort("payment_date", 1)
        history[policy_name] = [
            {
              "date": doc["payment_date"].isoformat(),
              "amount": doc.get("predicted_premium", doc.get("amount", 0))
            }
            for doc in docs
        ]
    return jsonify(history),200


def count_approved_claims(data):
    """
    POST /api/insurance/claims/count
    Body: { "email": "user@example.com" }
    Response: { "approved_count": 3 }
    """
    
    email = data.get("email")
    if not email:
        return jsonify({"message": "email required"}), 400

    db = get_db()
    count = db.claims_requests.count_documents({
        "user_email": email,
        "status": "Approved"
    })
    return jsonify({"approved_count":count}),200