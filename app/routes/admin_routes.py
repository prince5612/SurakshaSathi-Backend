from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.admin_controller import get_all_claims, change_claim_status, get_user_details_by_email
from app import get_db
from datetime import datetime
from bson import ObjectId
from app.controllers.notifications import send_claim_status_notification
admin_bp = Blueprint("admin_bp", __name__)

# Get all claims for admin
@admin_bp.route("/claims", methods=["GET"])
# @jwt_required()  # Ensure the request is authenticated
def get_claims():
    return get_all_claims()

# Change the status of a claim (e.g., "Approved", "Rejected")
# @admin_bp.route("/claims/<claim_id>/status", methods=["PUT"])
# # @jwt_required()
# def change_status(claim_id):
#     data = request.get_json()
#     return change_claim_status(claim_id, data)
@admin_bp.route('/claims/<claim_id>/status', methods=['PUT'])
def change_claim_status(claim_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    if new_status not in ("Approved","Rejected"):
      return jsonify({"message":"Invalid status"}), 400

    db = get_db()
    result = db.claims_requests.update_one(
      {"_id": ObjectId(claim_id)},
      {"$set":{"status":new_status, "updated_at": datetime.utcnow()}}
    )
    if result.matched_count==0:
      return jsonify({"message":"Not found"}), 404

    # fetch user_email so we can notify
    rec = db.claims_requests.find_one({"_id": ObjectId(claim_id)}, {"user_email":1})
    user_email = rec["user_email"]

    # send the notification/email
    send_claim_status_notification(user_email, claim_id, new_status)

    return jsonify({"message":"Status updated"}), 200

# Get user details (name, email) based on user email
@admin_bp.route("/users/email/<email>", methods=["GET"])
# @jwt_required()
def get_user_by_email(email):
    return get_user_details_by_email(email)

