# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import datetime

# app = Flask(__name__)
# CORS(app)

# # In-memory store (for demo). Replace with real DB in production.
# gps_logs = []

# @app.route("/api/gps", methods=["POST"])
# def receive_gps():
#     data = request.get_json(force=True)
#     # validate required fields
#     for key in ("device_id", "ts", "lat", "lon", "speed_kmh"):
#         if key not in data:
#             return jsonify({"error": f"Missing field {key}"}), 400

#     # enrich & store
#     log_entry = {
#         "device_id": data["device_id"],
#         "timestamp": datetime.datetime.utcfromtimestamp(data["ts"]),
#         "lat": data["lat"],
#         "lon": data["lon"],
#         "speed_kmh": data["speed_kmh"],
#     }
#     gps_logs.append(log_entry)
#     print(f"[{log_entry['timestamp']}] {log_entry['device_id']} → "
#           f"{log_entry['lat']:.5f},{log_entry['lon']:.5f} at {log_entry['speed_kmh']:.1f} km/h")
#     return jsonify({"status": "ok"}), 200

# @app.route("/api/gps/logs", methods=["GET"])
# def get_logs():
#     # return last 20 entries
#     return jsonify(gps_logs[-20:]), 200

# if __name__ == "__main__":
#     # Run on all interfaces, port 5000
#     app.run(host="0.0.0.0", port=5000, debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from driver_score import ingest_gps_point, compute_driver_score, compute_premium

# app = Flask(__name__)
# CORS(app)

# # In-memory store (for demo). Replace with real DB in production.
# gps_logs = []

# @app.route("/api/gps", methods=["POST"])
# def receive_gps():
#     data = request.get_json(force=True)
#     # validate required fields
#     for key in ("device_id", "ts", "lat", "lon", "speed_kmh"):
#         if key not in data or data[key] is None:
#             return jsonify({"error": f"Missing field {key}"}), 400

#     device_id = data["device_id"]
#     ts        = data["ts"]
#     lat       = data["lat"]
#     lon       = data["lon"]
#     speed     = data["speed_kmh"]

#     # store raw log
#     from datetime import datetime
#     log_entry = {
#         "device_id": device_id,
#         "timestamp": datetime.utcfromtimestamp(ts),
#         "lat": lat,
#         "lon": lon,
#         "speed_kmh": speed,
#     }
#     gps_logs.append(log_entry)

#     # process for driver score and premium
#     ingest_gps_point(device_id, ts, lat, lon, speed)
#     score   = compute_driver_score(device_id)
#     premium = compute_premium(device_id, base_rate=50.0)  # example base rate

#     print(f"[SCORE] {device_id} = {score:.1f}, Premium = ₹{premium:.2f}")
#     return jsonify({
#         "status": "ok",
#         "driver_score": score,
#         "daily_premium": premium
#     }), 200

# @app.route("/api/gps/logs", methods=["GET"])
# def get_logs():
#     # return last 20 raw entries
#     return jsonify(gps_logs[-20:]), 200

# if __name__ == "__main__":
#     # Run on all interfaces, port 5000
#     app.run(host="0.0.0.0", port=5000, debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from driver_score import ingest_gps_point, compute_driver_score, compute_premium

# app = Flask(__name__)
# CORS(app)

# # In-memory store (for demo). Replace with real DB in production.
# gps_logs = []

# @app.route("/api/gps", methods=["POST"])
# def receive_gps():
#     data = request.get_json(force=True)
#     # validate required fields
#     for key in ("device_id", "ts", "lat", "lon", "speed_kmh"):
#         if key not in data or data[key] is None:
#             return jsonify({"error": f"Missing field {key}"}), 400

#     device_id = data["device_id"]
#     ts        = data["ts"]
#     lat       = data["lat"]
#     lon       = data["lon"]
#     speed     = data["speed_kmh"]

#     # store raw log
#     from datetime import datetime
#     log_entry = {
#         "device_id": device_id,
#         "timestamp": datetime.utcfromtimestamp(ts),
#         "lat": lat,
#         "lon": lon,
#         "speed_kmh": speed,
#     }
#     gps_logs.append(log_entry)

#     # process for driver score and premium
#     ingest_gps_point(device_id, ts, lat, lon, speed)
#     score   = compute_driver_score(device_id)
#     premium = compute_premium(device_id, base_rate=50.0)  # example base rate

#     # Print latitude, longitude, speed, score, and premium
#     print(
#         f"[GPS] {device_id} → "
#         f"lat={lat:.5f}, lon={lon:.5f}, speed={speed:.1f} km/h | "
#         f"[SCORE] {score:.1f} | [PREMIUM] ₹{premium:.2f}"
#     )

#     return jsonify({
#         "status": "ok",
#         "driver_score": score,
#         "daily_premium": premium
#     }), 200

# @app.route("/api/gps/logs", methods=["GET"])
# def get_logs():
#     # return last 20 raw entries
#     return jsonify(gps_logs[-20:]), 200

# if __name__ == "__main__":
#     # Run on all interfaces, port 5000
#     app.run(host="0.0.0.0", port=5000, debug=True)



from flask import Flask, request, jsonify
from flask_cors import CORS
from driver_score import ingest_gps_point, compute_driver_score, compute_premium, user_events, user_points


gps_logs = []

def receive_gps():
    data = request.get_json(force=True)
    # validate required fields
    for key in ("device_id", "ts", "lat", "lon", "speed_kmh"):
        if key not in data or data[key] is None:
            return jsonify({"error": f"Missing field {key}"}), 400

    device_id = data["device_id"]
    ts        = data["ts"]
    lat       = data["lat"]
    lon       = data["lon"]
    speed     = data["speed_kmh"]

    # store raw log
    from datetime import datetime
    log_entry = {
        "device_id": device_id,
        "timestamp": datetime.utcfromtimestamp(ts),
        "lat": lat,
        "lon": lon,
        "speed_kmh": speed,
    }
    gps_logs.append(log_entry)

    # process for driver score and premium
    ingest_gps_point(device_id, ts, lat, lon, speed)

    # compute raw acceleration from last two points
    acc = None
    pts = user_points[device_id]
    if len(pts) >= 2:
        p1, p2 = pts[-2], pts[-1]
        dt = p2['t'] - p1['t']
        if dt > 0:
            acc = (p2['v'] - p1['v']) / dt  # m/s^2

    # fetch event counters
    events = user_events[device_id]
    brakes = events.get('brakes', 0)
    accels = events.get('accels', 0)
    night  = events.get('night', False)

    score   = compute_driver_score(device_id)
    premium = compute_premium(device_id, base_rate=50.0)  # example base rate

    # Print latitude, longitude, speed, acceleration, event counts, score, and premium
    print(
        f"[GPS] {device_id} → "
        f"lat={lat:.5f}, lon={lon:.5f}, speed={speed:.1f} km/h, "
        f"acc={acc:.2f} m/s², brakes={brakes}, accels={accels}, night={night} | "
        f"[SCORE] {score:.1f} | [PREMIUM] ₹{premium:.2f}"
    )

    return jsonify({
        "status": "ok",
        "driver_score": score,
        "daily_premium": premium
    }), 200


def get_logs():
    # return last 20 raw entries
    return jsonify(gps_logs[-20:]), 200

