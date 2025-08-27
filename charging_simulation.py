from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# Simulerad tid
sim_hour = 0
sim_min = 0

# Batteridata
battery_max_kwh = 40.0
battery_current_kwh = 8.0  # Start på 20%
charging_enabled = False

# Hushållsbelastning (kW)
max_house_power = 11  
base_load_percent = [
    0.08, 0.07, 0.20, 0.18, 0.25, 0.35, 0.41, 0.34,
    0.35, 0.40, 0.43, 0.56, 0.42, 0.34, 0.32, 0.33,
    0.53, 1.00, 0.81, 0.55, 0.39, 0.24, 0.17, 0.09
]
base_load_kwh = [round(p * max_house_power, 2) for p in base_load_percent]

# Laddning
charging_power = 7.4  # kW
seconds_per_hour = 4  # 1 simulerad timme = 4 sekunder

def simulate():
    global sim_hour, sim_min, battery_current_kwh, charging_enabled

    while True:
        current_base_load = base_load_kwh[sim_hour]

        for i in range(seconds_per_hour):
            if charging_enabled and battery_current_kwh < battery_max_kwh:
                energy_added = charging_power / seconds_per_hour
                battery_current_kwh += energy_added
                if battery_current_kwh > battery_max_kwh:
                    battery_current_kwh = battery_max_kwh

            sim_min = int((60 / seconds_per_hour) * i) % 60
            time.sleep(1)

        sim_hour = (sim_hour + 1) % 24
        sim_min = 0

@app.route('/info')
def get_info():
    total_load = base_load_kwh[sim_hour]
    if charging_enabled and battery_current_kwh < battery_max_kwh:
        total_load += charging_power

    return jsonify({
        "sim_time_hour": sim_hour,
        "sim_time_min": sim_min,
        "base_current_load_kW": base_load_kwh[sim_hour],
        "total_current_load_kW": round(total_load, 2),
        "battery_capacity_kWh": round(battery_current_kwh, 2),
        "charging_enabled": charging_enabled
    })

@app.route('/charge', methods=['POST'])
def start_charge():
    global charging_enabled
    charging_enabled = True
    return jsonify({"status": "Laddning startad", "charging_enabled": True}), 200

@app.route('/discharge', methods=['POST'])
def stop_charge():
    global charging_enabled
    charging_enabled = False
    return jsonify({"status": "Laddning stoppad", "charging_enabled": False}), 200

@app.route('/price')
def get_price():
    energy_price = [
        85.28, 70.86, 68.01, 67.95, 68.01, 85.04, 87.86, 100.26, 118.45, 116.61,
        105.93, 91.95, 90.51, 90.34, 90.80, 88.85, 90.39, 99.03, 87.11, 82.90,
        80.45, 76.48, 32.00, 34.29
    ]
    return jsonify({str(i): energy_price[i] for i in range(24)})

if __name__ == '__main__':
    thread = threading.Thread(target=simulate)
    thread.daemon = True
    thread.start()
    app.run(port=5000)
