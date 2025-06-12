from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data
battery = 10.0  # kWh

@app.route("/info")
def get_info():
    return jsonify({
        "ev_battery": battery,
        "total_consumption": 8.5
    })

@app.route("/baseload")
def get_baseload():
    return jsonify({str(h): round(2.0 + 0.5 * (h % 4), 1) for h in range(24)})

@app.route("/priceperhour")
def get_prices():
    return jsonify({str(h): round(100 - (h * 2), 1) for h in range(24)})

@app.route("/charge", methods=["POST"])
def start_charging():
    global battery
    battery = min(battery + 1.0, 40.0)
    return "Charging started", 200

@app.route("/discharge", methods=["POST"])
def stop_charging():
    return "Charging stopped", 200

if __name__ == "__main__":
    app.run(port=5000)
