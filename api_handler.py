import requests
import logging

# الرابط الذي أرسلته (Web App URL)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwHwUC6G9BB427nSUZy5l7d3k_CKMCFw9MscSyIyNNlEGdCQUbmq5sWj3elIsDtHElD/exec"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_gas_api(action, params=None):
    """دالة موحدة للاتصال بـ Google Apps Script"""
    if params is None:
        params = {}
    params['action'] = action
    try:
        # نستخدم POST لأن Google Apps Script يتعامل معه بشكل أفضل في العمليات المعقدة
        # نستخدم allow_redirects=True لأن GAS يقوم بعمل Redirection دائماً
        response = requests.post(SCRIPT_URL, json=params, follow_redirects=True, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Connection Error: {e}")
        return None

def check_login(username, password):
    """التحقق من الدخول"""
    result = call_gas_api("login", {"username": username, "password": password})
    # يتوقع أن يعيد الـ Script بيانات المستخدم أو None
    return result if result and not result.get('error') else None

def fetch_all_data(user_id):
    """جلب بيانات الباكلوج"""
    result = call_gas_api("getData", {"user_id": user_id})
    return result if result else {}

def delete_user_cloud(user_id):
    """حذف البيانات من السحاب"""
    result = call_gas_api("delete", {"user_id": user_id})
    return result.get('status') == 'success' if result else False

def cloud_action(action_type, payload):
    """تنفيذ أي عملية إضافية"""
    payload['sub_action'] = action_type
    return call_gas_api("sync", payload)

def get_user_plans(user_id):
    """جلب الخطط الدراسية"""
    result = call_gas_api("getPlans", {"user_id": user_id})
    return result if isinstance(result, list) else []