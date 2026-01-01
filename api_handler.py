import requests
import logging

# إعداد التسجيل لمراقبة الأخطاء
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIHandler:
    def __init__(self, base_url, api_key=None):
        """
        تهيئة مدير الـ API.
        :param base_url: الرابط الأساسي للموقع (Base URL).
        :param api_key: مفتاح التحقق (Token) إن وجد.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def _handle_response(self, response):
        """معالجة استجابة السيرفر وفحص الأخطاء."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP Error: {err} | Status: {response.status_code}")
            return {"error": str(err), "status": response.status_code}
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return {"error": "Unknown error occurred"}

    def get_data(self, endpoint, params=None):
        """إرسال طلب GET لاسترجاع البيانات."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e}")
            return {"error": "Could not connect to the server"}

    def post_data(self, endpoint, data):
        """إرسال طلب POST لإرسال بيانات جديدة."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e}")
            return {"error": "Could not connect to the server"}

# مثال للاستخدام السريع (Testing)
if __name__ == "__main__":
    # تجربة بسيطة باستخدام API تجريبي
    handler = APIHandler("https://jsonplaceholder.typicode.com")
    data = handler.get_data("posts/1")
    print(data)