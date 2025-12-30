import requests
import json
import streamlit as st

# ضع الرابط الجديد هنا
API_URL = "https://script.google.com/macros/s/AKfycbwXxWmK1MkVUzEqBJIYGjTZY9FQMoVdDwjnqnNFvNs4J7RipjTaq0UH70Pgv8oCOwkn/exec"

def check_login(u, p):
    try:
        res = requests.get(f"{API_URL}?sheet=Users", timeout=5)
        users = res.json()
        u_in, p_in = str(u).strip().lower(), str(p).strip()
        for user in users:
            if str(user.get('username')).strip().lower() == u_in and str(user.get('password')).strip() == p_in:
                return user.get('role', 'student')
        return None
    except: return None

def get_user_plans(username):
    """جلب الخطط مع نسبة التقدم المحفوظة"""
    try:
        res = requests.get(f"{API_URL}?sheet=RescuePlans&user={username}", timeout=5)
        return res.json()
    except: return []

def cloud_action(action, data):
    try:
        requests.post(API_URL, data=json.dumps({"action": action, "data": data}), timeout=5)
        return True
    except: return False

def fetch_all_data(sheet):
    try: return requests.get(f"{API_URL}?sheet={sheet}", timeout=5).json()
    except: return []

def delete_user_cloud(u):
    return cloud_action("delete_user", {"username": u})