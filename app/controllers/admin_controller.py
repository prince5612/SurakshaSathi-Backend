from flask import jsonify
from app import get_db

from flask import jsonify
from bson import ObjectId
from app import get_db

def get_all_claims():
    db = get_db()  # Get the MongoDB instance
    claims = db.claims_requests.find()  # Retrieve all claims from the claims_requests collection

    # Convert the cursor to a list and handle serialization
    claims_list = []
    for claim in claims:
        # Serialize the _id field (ObjectId) to a string
        claim['_id'] = str(claim['_id'])

        # Ensure the documents array is also serializable
        if 'documents' in claim:
            for doc in claim['documents']:
                # Serialize any ObjectId or non-serializable fields if needed in documents
                doc['uploaded_at'] = str(doc['uploaded_at'])  # Convert datetime to string

        claims_list.append(claim)

    return jsonify({"claims": claims_list}), 200

def change_claim_status(claim_id, data):
    db = get_db()

    # Extract new status from request data
    new_status = data.get("status")
    if not new_status:
        return jsonify({"msg": "Status is required"}), 400

    try:
        # Convert claim_id to ObjectId (if it's a string)
        claim_id = ObjectId(claim_id)
    except Exception as e:
        return jsonify({"msg": f"Invalid claim ID: {e}"}), 400

    # Update the status of the claim in the database
    result = db["claims_requests"].update_one(
        {"_id": claim_id}, {"$set": {"status": new_status}}  # Update the claim's status
    )

    if result.matched_count:
        return jsonify({"msg": "Claim status updated"}), 200
    else:
        return jsonify({"msg": "Claim not found"}), 404

def get_user_details_by_email(email):
    db = get_db()
    user = db["users"].find_one({"email": email})

    if user:
        user_data = {
            "name": user.get("name"),
            "email": user.get("email")
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"msg": "User not found"}), 404