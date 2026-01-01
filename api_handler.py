import requests
import logging

# إعدادات الرابط الأساسي (استبدله برابط الـ API الخاص بك)
BASE_URL = "https://your-api-url.com"

# إعداد التسجيل للأخطاء
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_login(username, password):
    """التحقق من بيانات تسجيل الدخول"""
    try:
        response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Login error: {e}")
        return None

def fetch_all_data(user_id):
    """جلب كافة البيانات الخاصة بالمستخدم"""
    try:
        response = requests.get(f"{BASE_URL}/data/{user_id}")
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return {}

def delete_user_cloud(user_id):
    """حذف بيانات المستخدم من السحاب"""
    try:
        response = requests.delete(f"{BASE_URL}/delete/{user_id}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Delete error: {e}")
        return False

def cloud_action(action_type, payload):
    """تنفيذ عمليات عامة على السحاب (مثل الرفع أو التحديث)"""
    try:
        response = requests.post(f"{BASE_URL}/action", json={"type": action_type, "data": payload})
        return response.json()
    except Exception as e:
        logger.error(f"Cloud action error: {e}")
        return {"error": str(e)}

def get_user_plans(user_id):
    """جلب الخطط الدراسية الخاصة بالمستخدم"""
    try:
        response = requests.get(f"{BASE_URL}/plans/{user_id}")
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        logger.error(f"Get plans error: {e}")
        return []