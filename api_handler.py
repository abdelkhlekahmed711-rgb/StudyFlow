import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_login(username, password):
    """التحقق من البيانات بناءً على صورة لجنة التحكيم"""
    # تحويل القيم لنصوص لضمان المقارنة الصحيحة
    u = str(username).strip()
    p = str(password).strip()

    # فحص الحساب الأول (admin)
    if u == "admin" and p == "123":
        return {"user_id": "admin_01", "name": "Admin User", "type": "jury"}
    
    # فحص الحساب الثاني (student)
    elif u == "student" and p == "456":
        return {"user_id": "std_01", "name": "Abdelkhalek", "type": "student"}
    
    return None

def fetch_all_data(user_id):
    """بيانات تجريبية للباكلوج تظهر فور تسجيل الدخول"""
    return {
        "رياضيات": 18,
        "كيمياء": 10,
        "فيزياء": 10,
        "إنجازات": "65%"
    }

def get_user_plans(user_id):
    """خطط دراسية وهمية للعرض"""
    return ["خطة الـ 30 يوم", "مراجعة ليلة الامتحان"]

def cloud_action(action, data):
    """محاكاة حفظ البيانات على السحاب"""
    return {"status": "success"}

def delete_user_cloud(user_id):
    """محاكاة حذف البيانات"""
    return True