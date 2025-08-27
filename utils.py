import requests

BASE_URL = "http://127.0.0.1:5000"

def get_info():
    try:
        r = requests.get(f"{BASE_URL}/info")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[utils.py] Fel i get_info(): {e}")
        return None

def start_charging():
    try:
        r = requests.post(f"{BASE_URL}/charge")
        r.raise_for_status()
    except Exception as e:
        print(f"[utils.py] Fel i start_charging(): {e}")

def stop_charging():
    try:
        r = requests.post(f"{BASE_URL}/discharge")
        r.raise_for_status()
    except Exception as e:
        print(f"[utils.py] Fel i stop_charging(): {e}")

def get_baseload():
    return {
        "0": 0.88, "1": 0.77, "2": 2.2, "3": 1.98, "4": 2.75, "5": 3.85,
        "6": 4.51, "7": 3.74, "8": 3.85, "9": 4.4, "10": 4.73, "11": 6.16,
        "12": 4.62, "13": 3.74, "14": 3.52, "15": 3.63, "16": 5.83, "17": 11.0,
        "18": 8.91, "19": 6.05, "20": 4.29, "21": 2.64, "22": 1.87, "23": 0.99
    }

def get_prices():
    try:
        r = requests.get(f"{BASE_URL}/price")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[utils.py] Fel i get_prices(): {e}")
        return {}
