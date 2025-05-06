# app/controllers/notifications.py
from app import get_db, mail
from datetime import datetime, timedelta
from flask_mail import Message
from flask import current_app
from bson import ObjectId

def create_notification(user_email, notif_type, payload, channels):
    db = get_db()
    notif = {
        "user_email": user_email,
        "type": notif_type,
        "payload": payload,
        "channel": channels,
        "scheduled_at": datetime.utcnow(),
        "sent_at": None,
        "read": False
    }
    return db.notifications.insert_one(notif).inserted_id

def mark_sent(nid):
    db = get_db()
    db.notifications.update_one({"_id": nid}, {"$set": {"sent_at": datetime.utcnow()}})

def send_email(to, subject, html_body):
    with current_app.app_context():
        msg = Message(subject, recipients=[to], html=html_body)
        mail.send(msg)

def send_notification(nid):
    db = get_db()
    notif = db.notifications.find_one({"_id": ObjectId(nid)})
    if not notif:
        return

    channels = notif['channel']
    payload  = notif['payload']
    user     = notif['user_email']

    if 'email' in channels:
        if notif['type'] == 'premium_reminder':
            sub = "Your premium is due soon"
            html = f"""
              <p>Dear user,</p>
              <p>Your <strong>{payload['policy']}</strong> premium of ₹{payload['amount_due']} 
                 is due on <strong>{payload['due_date']}</strong> ({payload['days_left']} days left).</p>
              <p><a href="https://app.surakshasathi.com/pay">Pay Now</a></p>
              <p>Thank you,<br/>SurakshaSathi Team</p>
            """
        elif notif['type'] == 'claim_status':
            sub = f"Your claim {payload['claim_id']} is now {payload['new_status']}"
            html = f"""
              <p>Dear user,</p>
              <p>Your claim <strong>{payload['claim_id']}</strong> status has been updated to 
                 <strong>{payload['new_status']}</strong>.</p>
              <p>Visit your dashboard for details.</p>
              <p>Thank you,<br/>SurakshaSathi Team</p>
            """
        else:
            sub = "SurakshaSathi Notification"
            html = "<p>You have a new notification.</p>"

        send_email(user, sub, html)

    mark_sent(nid)

def premium_reminder_job():
    db = get_db()
    payments = db.life_insurance_payments
    today = datetime.utcnow().date()

    for p in payments.find({}):
        due = p['payment_date'].date() + timedelta(days=30)
        days_left = (due - today).days
        if days_left in (30,7, 1, 0):
            payload = {
                "policy": "life",
                "amount_due": p['predicted_premium'],
                "due_date": due.isoformat(),
                "days_left": days_left
            }
            nid = create_notification(p['user_email'], "premium_reminder", payload, ["in_app","email"])
            send_notification(nid)

# def claim_status_update_job():
#     db = get_db()
#     claims = db.claims_requests
#     recent = datetime.utcnow() - timedelta(minutes=10)  # assume update within last 10 min

#     for c in claims.find({"updated_at": {"$gte": recent}}):
#         payload = {
#             "claim_id": str(c['_id']),
#             "new_status": c['status']
#         }
#         nid = create_notification(c['user_email'], "claim_status", payload, ["in_app", "email"])
#         send_notification(nid)

def send_claim_acknowledgement(user_email, claim_id):
    """
    Notify user by email that their claim request has been received.
    """
    # 1) Create the notification record with payload AND channels
    nid = create_notification(
        user_email,
        "claim_request",
        {"claim_id": claim_id},  # <-- payload
        ["email"]                # <-- channels
    )

    # 2) Send the email
    subject = "Your claim request has been received"
    html = f"""
      <p>Dear user,</p>
      <p>We have received your claim request with ID <strong>{claim_id}</strong>. 
         Our team will review it and get back to you shortly.</p>
      <p>Thank you for choosing SurakshaSathi!</p>
    """
    send_email(user_email, subject, html)

    # 3) Mark that notification as sent
    mark_sent(nid)
