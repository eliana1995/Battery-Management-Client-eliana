from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

sim_hour = 0
sim_min = 0
battery_max_kwh = 40.0
battery_current_kwh = 8.0  # Start på ca 20%
charging_enabled = False

max_house_power = 11  # kW
base_load_percent = [
    0.08, 0.07, 0.20, 0.18, 0.25, 0.35, 0.41, 0.34,
    0.35, 0.40, 0.43, 0.56, 0.42, 0.34, 0.32, 0.33,
    0.53, 1.00, 0.81, 0.55, 0.39, 0.24, 0.17, 0.09
]
base_load_kwh = [round(p * max_house_power, 2) for p in base_load_percent]

charging_power = 7.4  # kW
seconds_per_hour = 4  # 1 simulerad timme = 4 sekunder i verklig tid

def simulate():
    global sim_hour, sim_min, battery_current_kwh, charging_enabled

    while True:
        current_load = base_load_kwh[sim_hour]

        for i in range(seconds_per_hour):
            if charging_enabled and battery_current_kwh < battery_max_kwh:
                battery_current_kwh += charging_power / seconds_per_hour
                if battery_current_kwh > battery_max_kwh:
                    battery_current_kwh = battery_max_kwh
                current_load += charging_power / seconds_per_hour

            sim_min = int((60 / seconds_per_hour) * i) % 60
            time.sleep(1)

        sim_hour = (sim_hour + 1) % 24
        sim_min = 0

@app.route('/info')
def get_info():
    return jsonify({
        "sim_time_hour": sim_hour,
        "sim_time_min": sim_min,
        "base_current_load": base_load_kwh[sim_hour],
        "battery_capacity_kWh": round(battery_current_kwh, 2),
        "charging_enabled": charging_enabled
    })

@app.route('/charge', methods=['POST'])
def start_charge():
    global charging_enabled
    charging_enabled = True
    return "Laddning startad", 200

@app.route('/discharge', methods=['POST'])
def stop_charge():
    global charging_enabled
    charging_enabled = False
    return "Laddning stoppad", 200

if __name__ == '__main__':
    thread = threading.Thread(target=simulate)
    thread.daemon = True
    thread.start()
    app.run(port=5000)
