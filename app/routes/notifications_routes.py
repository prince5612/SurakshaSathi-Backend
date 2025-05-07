# app/routes/notifications_routes.py
from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.controllers.notifications import premium_reminder_job,send_claim_acknowledgement,send_claim_status_notification
from app import get_db
from datetime import datetime

notif_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notif_bp.route('', methods=['GET'])
def list_notifications():
    email = request.args.get('email')
    notifs = list(get_db().notifications.find({"user_email": email}, {'_id':0}))
    return jsonify(notifs), 200

@notif_bp.route('/<id>/read', methods=['POST'])
def mark_read(id):
    get_db().notifications.update_one({"_id": ObjectId(id)}, {"$set":{"read":True}})
    return jsonify({"message":"Marked read"}), 200

# Test endpoint to trigger reminder job manually
@notif_bp.route('/test-reminder', methods=['GET'])
def test_reminder():
    premium_reminder_job()
    return jsonify({"message": "Test premium reminders sent"}), 200

# @notif_bp.route('/test-claim-update', methods=['POST'])
# def test_claim_update():
#     send_claim_acknowledgement()
#     return jsonify({"message": "Test claim notifications sent"}), 200

@notif_bp.route('/claim-ack', methods=['POST'])
def claim_ack():
    data = request.get_json()
    email    = data.get('email')
    claim_id = data.get('claim_id')
    if not email or not claim_id:
        return jsonify({"message":"Missing email or claim_id"}), 400

    send_claim_acknowledgement(email, claim_id)
    return jsonify({"message":"Claim acknowledgement sent"}), 200

# from flask import Blueprint, jsonify
from flask_mail import Message
from app import mail
from flask import current_app

# notif_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notif_bp.route('/test-email', methods=['GET'])
def test_email():
    try:
        with current_app.app_context():
            msg = Message(
                subject="Test Premium Reminder",
                recipients=["kishorpatel5612@gmail.com"],  # CHANGE THIS to your target address
                html="""
                    <h3>Premium Reminder</h3>
                    <p>This is a test email from SurakshaSathi backend.</p>
                    <p>Please remember to pay your upcoming premium.</p>
                """
            )
            mail.send(msg)
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



