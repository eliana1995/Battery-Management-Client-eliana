import requests

BASE_URL = "http://127.0.0.1:5000"

def get_info():
    return requests.get(f"{BASE_URL}/info").json()

def get_baseload():
    return requests.get(f"{BASE_URL}/baseload").json()

def get_prices():
    return requests.get(f"{BASE_URL}/priceperhour").json()

def start_charging():
    return requests.post(f"{BASE_URL}/charge")

def stop_charging():
    return requests.post(f"{BASE_URL}/discharge")