

# from collections import defaultdict, deque
# import datetime

# # In-memory stores (replace with real DB in production)
# # Sliding window of recent GPS points per device
# user_points = defaultdict(lambda: deque(maxlen=1000))
# # Event counters per device and last acceleration and last event timestamp
# user_events = defaultdict(lambda: {"brakes": 0, "accels": 0, "night": False, "last_acc": None, "last_event_ts": None , "safe":0})
# # Latest computed score and premium per device
# user_score = {}
# user_premium = {}


# def ingest_gps_point(device_id: str, ts: int, lat: float, lon: float, speed_kmh: float):
#     """
#     Append a new GPS point and detect events.
#     """
#     # Convert speed to m/s
#     speed_ms = speed_kmh / 3.6
#     user_points[device_id].append({"t": ts, "lat": lat, "lon": lon, "v": speed_ms})
#     detect_events(device_id)


# def detect_events(device_id: str, brake_thresh=-0.5, accel_thresh=0.5):
#     """
#     Update event counters, record last acceleration, and timestamp of last harsh event.
#     """
#     pts = user_points[device_id]
#     if len(pts) < 2:
#         return

#     p1, p2 = pts[-2], pts[-1]
#     dt = p2["t"] - p1["t"]
#     if dt <= 0:
#         return

#     # Compute acceleration in m/s^2
#     a = (p2["v"] - p1["v"]) / dt
#     # store last acceleration
#     user_events[device_id]["last_acc"] = a

#     # count events and record timestamp
#     if a <= brake_thresh:
#         user_events[device_id]["brakes"] += 1
#         user_events[device_id]["last_event_ts"] = p2["t"]
#     elif a >= accel_thresh:
#         user_events[device_id]["accels"] += 1
#         user_events[device_id]["last_event_ts"] = p2["t"]

#     # Night driving flag
#     hour = datetime.datetime.fromtimestamp(p2["t"]).hour
#     if hour >= 22 or hour < 5:
#         user_events[device_id]["night"] = True


# def compute_driver_score(device_id: str,
#                          w_brake=3.0, w_accel=3.0, w_night=10.0,
#                          safe_minute_bonus=5.0) -> float:
#     """
#     Compute a driver safety score (0-100) using weighted penalties.
#     If the driver has gone at least 60s since the last harsh event (or start) without any new harsh events,
#     award a bonus, capped at 100.
#     """
#     events = user_events[device_id]
#     pts = user_points[device_id]
#     # Start at perfect score
#     score = 100.0
#     # Deduct weighted penalties
#     score -= events["brakes"] * w_brake
#     score -= events["accels"] * w_accel
#     if events["night"]:
#         score -= w_night

#     # Bonus for safe driving interval
#     if pts:
#         last_ts = pts[-1]["t"]
#         # determine time since last harsh event or start of trip
#         ref_ts = events.get("last_event_ts") or pts[0]["t"]
#         safe_dur = last_ts - ref_ts
#         # if safe duration ≥ 60s and no new events in that period
#         if safe_dur >= 60:
#             user_events[device_id]["safe"] += 1
#             user_events[device_id]["last_event_ts"] = last_ts

#     # Clamp
#     score += events["safe"] * safe_minute_bonus
#     score = max(0.0, min(100.0, score))
#     user_score[device_id] = score
#     return score


# def get_driver_metrics(device_id: str) -> dict:
#     """
#     Return current metrics: score, last_acceleration, brakes, accels, night flag, safe_duration.
#     """
#     pts = user_points[device_id]
#     events = user_events[device_id]
#     safe_dur = None
#     if pts:
#         last_ts = pts[-1]["t"]
#         ref_ts = events.get("last_event_ts") or pts[0]["t"]
#         safe_dur = last_ts - ref_ts
#     return {
#         "score": user_score.get(device_id, 100.0),
#         "last_acceleration": events.get("last_acc"),
#         "brakes": events.get("brakes", 0),
#         "accels": events.get("accels", 0),
#         "night": events.get("night", False),
#         "safe_duration_s": safe_dur
#     }


# def rate_multiplier(score: float) -> float:
#     """
#     Map score into premium multiplier with finer bands.
#     """
#     if score >= 80:
#         return 0.90   # 10% discount
#     if score >= 60:
#         return 1.10   # 10% surcharge
#     if score >= 40:
#         return 1.30   # 30% surcharge
#     return 1.50       # 50% surcharge


# def compute_premium(device_id: str, base_rate: float) -> float:
#     """
#     Compute premium based on latest score. Does NOT reset state.
#     """
#     score = user_score.get(device_id, 100.0)
#     mult = rate_multiplier(score)
#     premium = base_rate * mult
#     user_premium[device_id] = premium
#     return premium


# def reset_trip(device_id: str):
#     """
#     Clear stored points and events for a new trip.
#     """
#     user_points[device_id].clear()
#     user_events[device_id] = {"brakes": 0, "accels": 0, "night": False, "last_acc": None, "last_event_ts": None}
#     user_score.pop(device_id, None)
#     user_premium.pop(device_id, None)


from collections import defaultdict, deque
import datetime
import os
from pymongo import MongoClient
from urllib.parse import urlparse
import urllib.parse
from dotenv import load_dotenv
load_dotenv()
# Connect to MongoDB Atlas
# Expect MONGODB_URI to include credentials and host, e.g.:
# "mongodb+srv://user:pass@cluster0.mongodb.net/?retryWrites=true&w=majority"
username = os.getenv('MONGO_USER')
password = os.getenv('MONGO_PASSWORD')
# URL-encode username and password
username_esc = urllib.parse.quote_plus(username)
password_esc = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://{username_esc}:{password_esc}@surakshasathi.d2azkdd.mongodb.net/?retryWrites=true&w=majority&appName=SurakshaSathi"

if not MONGO_URI:
    raise RuntimeError("MONGODB_URI environment variable is required")
client = MongoClient(MONGO_URI)
db=client["SurkshaSathi"]
driver_score = db["driver_score"]

# In-memory stores (replace with real DB in production)
user_points = defaultdict(lambda: deque(maxlen=1000))
user_events = defaultdict(lambda: {"brakes": 0, "accels": 0, "night": False, "last_acc": None, "last_event_ts": None, "safe": 0})
user_score = {}
user_premium = {}


def store_score_to_db(device_id: str, score: float):
    """
    Persist the driver score for this device into MongoDB with current UTC timestamp.
    """
    doc = {
        "device_id": device_id,
        "timestamp": datetime.datetime.utcnow(),
        "score": score
    }
    driver_score.insert_one(doc)



def ingest_gps_point(device_id: str, ts: int, lat: float, lon: float, speed_kmh: float):
    """
    Append a new GPS point and detect events.
    """
    speed_ms = speed_kmh / 3.6
    user_points[device_id].append({"t": ts, "lat": lat, "lon": lon, "v": speed_ms})
    detect_events(device_id)


def detect_events(device_id: str, brake_thresh=-0.5, accel_thresh=0.5):
    """
    Update event counters, record last acceleration, and timestamp of last harsh event.
    """
    pts = user_points[device_id]
    if len(pts) < 2:
        return

    p1, p2 = pts[-2], pts[-1]
    dt = p2["t"] - p1["t"]
    if dt <= 0:
        return

    a = (p2["v"] - p1["v"]) / dt
    user_events[device_id]["last_acc"] = a

    if a <= brake_thresh:
        user_events[device_id]["brakes"] += 1
        user_events[device_id]["last_event_ts"] = p2["t"]
    elif a >= accel_thresh:
        user_events[device_id]["accels"] += 1
        user_events[device_id]["last_event_ts"] = p2["t"]

    hour = datetime.datetime.fromtimestamp(p2["t"]).hour
    if hour >= 22 or hour < 5:
        user_events[device_id]["night"] = True


# def compute_driver_score(device_id: str,
#                          w_brake=3.0, w_accel=3.0, w_night=10.0,
#                          safe_minute_bonus=5.0) -> float:
#     """
#     Compute a driver safety score (0-100) using weighted penalties.
#     Every 60s without harsh events adds a bonus; every 80min store to MongoDB and reset.
#     """
#     events = user_events[device_id]
#     pts = user_points[device_id]
#     score = 100.0
#     score -= events["brakes"] * w_brake
#     score -= events["accels"] * w_accel
#     if events["night"]:
#         score -= w_night

#     if pts:
#         last_ts = pts[-1]["t"]
#         ref_ts = events.get("last_event_ts") or pts[0]["t"]
#         safe_dur = last_ts - ref_ts
#         if safe_dur >= 60:
#             events["safe"] += 1
#             events["last_event_ts"] = last_ts
#     score += events["safe"] * safe_minute_bonus
#     score = max(0.0, min(100.0, score))
#     if pts:
#         trip_duration = pts[-1]["t"] - pts[0]["t"]
#         if trip_duration >= 1 * 60:
#             # persist to MongoDB and reset
#             store_score_to_db(device_id, score)
#             reset_trip(device_id)
#             user_score[device_id] = score
#             return score

    
#     user_score[device_id] = score
#     return score

def compute_driver_score(device_id: str,
                         w_brake=3.0, w_accel=3.0, w_night=10.0,
                         safe_minute_bonus=5.0) -> float:
    """
    Compute a driver safety score (0-100) using weighted penalties.
    Every 60s without harsh events adds a bonus.
    If trip duration >= 1 min, store score to MongoDB and reset in-memory tracking.
    """
    events = user_events[device_id]
    pts = user_points[device_id]
    score = 100.0

    # Apply penalties
    score -= events["brakes"] * w_brake
    score -= events["accels"] * w_accel
    if events["night"]:
        score -= w_night

    # Reward for safe driving duration
    if pts:
        last_ts = pts[-1]["t"]
        ref_ts = events.get("last_event_ts") or pts[0]["t"]
        safe_dur = last_ts - ref_ts
        if safe_dur >= 60:
            events["safe"] += 1
            events["last_event_ts"] = last_ts

    # Add safe driving bonus
    score += events["safe"] * safe_minute_bonus

    # Clamp score to [0, 100]
    score = max(0.0, min(100.0, score))

    # Persist score if trip duration exceeds threshold
    if pts:
        trip_duration = pts[-1]["t"] - pts[0]["t"]
        if trip_duration >= 5*60:  # 5 min
            store_score_to_db(device_id, score)
            reset_trip(device_id)
            user_score[device_id] = score
            return score

    user_score[device_id] = score
    return score

def get_driver_metrics(device_id: str) -> dict:
    pts = user_points[device_id]
    events = user_events[device_id]
    safe_dur = None
    if pts:
        last_ts = pts[-1]["t"]
        ref_ts = events.get("last_event_ts") or pts[0]["t"]
        safe_dur = last_ts - ref_ts
    return {
        "score": user_score.get(device_id, 100.0),
        "last_acceleration": events.get("last_acc"),
        "brakes": events.get("brakes", 0),
        "accels": events.get("accels", 0),
        "night": events.get("night", False),
        "safe_duration_s": safe_dur
    }


def rate_multiplier(score: float) -> float:
    if score >= 80:
        return 0.90
    if score >= 60:
        return 1.10
    if score >= 40:
        return 1.30
    return 1.50


def compute_premium(device_id: str, base_rate: float) -> float:
    score = user_score.get(device_id, 100.0)
    mult = rate_multiplier(score)
    premium = base_rate * mult
    user_premium[device_id] = premium
    return premium


def reset_trip(device_id: str):
    user_points[device_id].clear()
    user_events[device_id] = {"brakes": 0, "accels": 0, "night": False, "last_acc": None, "last_event_ts": None, "safe": 0}
    user_score.pop(device_id, None)
    user_premium.pop(device_id, None)
