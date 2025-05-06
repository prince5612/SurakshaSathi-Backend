from flask import Blueprint, request
from app.ml_model.life.life_insurance import life_predict_premium
from app.controllers.insurance_controller import pay_life_insurance_premium,pay_flood_insurance_premium,pay_travel_insurance_premium,create_life_details,update_life_details,get_life_details,get_last_flood_payment,get_car_details,create_car_details,update_car_details,pay_car_premium,get_health_details,create_health_details,update_health_details,pay_health_insurance_premium,get_travel_details
from app.ml_model.flood.flood_insurance import flood_predict_premium
from app.ml_model.travel.travel_insurance import travel_predict_premium
from app.ml_model.car.car_insurance import predict_premium
from app.ml_model.health.health_insurance import health_predict_premium

insurance_bp = Blueprint('insurance_bp', __name__)

@insurance_bp.route('/life/premium', methods=['POST'])
def life_premium():
    data = request.get_json()
    return life_predict_premium(data)

@insurance_bp.route('/life/pay', methods=['POST'])
def life_pay():
    data = request.get_json()
    return pay_life_insurance_premium(data)

@insurance_bp.route('/life/create', methods=['POST'])
def create_life():
    data = request.get_json()
    return create_life_details(data)

@insurance_bp.route('/life/update', methods=['POST'])
def update_life():
    data = request.get_json()
    return update_life_details(data)

@insurance_bp.route('/life/details', methods=['POST'])
def get_life():
    data = request.get_json()
    return get_life_details(data)

@insurance_bp.route('/flood/premium', methods=['POST'])
def flood_premium():
    data = request.get_json()
    return flood_predict_premium(data)

@insurance_bp.route('/flood/pay', methods=['POST'])
def flood_pay():
    data = request.get_json()
    return pay_flood_insurance_premium(data)

@insurance_bp.route('/flood/last_payment', methods=['POST'])
def get_flood():
    data = request.get_json()
    return get_last_flood_payment(data)

@insurance_bp.route('/travel/premium', methods=['POST'])
def travel_premium():
    data = request.get_json()
    return travel_predict_premium(data)

@insurance_bp.route('/travel/pay', methods=['POST'])
def travel_pay():
    data = request.get_json()
    return pay_travel_insurance_premium(data)

@insurance_bp.route('/travel/last_payment', methods=['POST'])
def get_travel():
    data = request.get_json()
    return get_travel_details(data)

@insurance_bp.route('/car/premium', methods=['POST'])
def car_premium():
    data = request.get_json()
    return predict_premium(data)

@insurance_bp.route('/car/pay', methods=['POST'])
def car_pay():
    data = request.get_json()
    return pay_car_premium(data)

@insurance_bp.route('/car/create', methods=['POST'])
def create_car():
    data = request.get_json()
    return create_car_details(data)

@insurance_bp.route('/car/update', methods=['POST'])
def update_car():
    data = request.get_json()
    return update_car_details(data)


@insurance_bp.route('car/details', methods=['POST'])
def get_car():
    data = request.get_json()
    return get_car_details(data)


@insurance_bp.route('/health/premium', methods=['POST'])
def health_premium():
    data = request.get_json()
    return health_predict_premium(data)

@insurance_bp.route('/health/pay', methods=['POST'])
def health_pay():
    data = request.get_json()
    return pay_health_insurance_premium(data)

@insurance_bp.route('/health/create', methods=['POST'])
def create_health():
    data = request.get_json()
    return create_health_details(data)

@insurance_bp.route('/health/update', methods=['POST'])
def update_health():
    data = request.get_json()
    return update_health_details(data)


@insurance_bp.route('/health/details', methods=['POST'])
def get_health():
    data = request.get_json()
    return get_health_details(data)

# @insurance_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     return login_user(data)
