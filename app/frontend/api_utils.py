import requests
import json

BASE_URL = "http://127.0.0.1:8000"  # Replace with your API base URL

def register_user(email, password, is_admin):
    url = f"{BASE_URL}/auth/register"
    payload = {"email": email, "password": password, "is_admin": is_admin}
    response = requests.post(url, json=payload)
    return response.json()

def login_user(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        token = response.json()["access_token"]
        save_token(token)
    return response.json()

def save_token(token):
    with open("auth.json", "w") as f:
        json.dump({"token": token}, f)

def load_token():
    try:
        with open("auth.json", "r") as f:
            return json.load(f)["token"]
    except FileNotFoundError:
        return None

def call_api(endpoint, method="GET", data=None):
    token = load_token()
    if not token:
        return {"error": "User not logged in"}

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, params=data)
    else:
        return {"error": "Invalid HTTP method"}
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text