import streamlit as st
import pandas as pd
from ui_components import atomic_progress_3d, render_mission_card

# 1. إعداد الصفحة
st.set_page_config(page_title="StudyFlow AI Elite", layout="wide")

# 2. التصميم السينمائي
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
.stApp { background: radial-gradient(circle at center, #050a0f 0%, #010203 100%) !important; font-family: 'Tajawal', sans-serif !important; color: #fff !important; }
h1,h2,h3,h4,p,div,label,span { color: #fff !important; }
[data-testid="stSidebar"] { background: rgba(13, 27, 42, 0.95) !important; border-right: 2px solid #00f2fe; }
.atom-container-3d { margin: 20px auto; perspective: 1000px; width: 160px; height: 160px; position: relative; }
.nucleus-3d { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80px; height: 80px; border-radius: 50%; background: rgba(0,0,0,0.6); border: 2px solid var(--atom-color, #00f2fe); display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.5rem; color: #fff; box-shadow: 0 0 25px var(--atom-color, #00f2fe); }
.orbit-3d { position: absolute; top: 50%; left: 50%; width: 100%; height: 100%; border: 1px solid rgba(255,255,255,0.2); border-radius: 50%; transform-style: preserve-3d; }
.orbit-1 { transform: translate(-50%, -50%) rotateZ(0deg); } .orbit-2 { transform: translate(-50%, -50%) rotateX(65deg) rotateY(30deg); } .orbit-3 { transform: translate(-50%, -50%) rotateX(-65deg) rotateY(30deg); }
.electron-3d { position: absolute; top: 0; left: 50%; width: 12px; height: 12px; border-radius: 50%; background: #fff; box-shadow: 0 0 10px #fff; animation: orbit3D 3s linear infinite; }
.orbit-1 .electron-3d { animation-delay: 0s; } .orbit-2 .electron-3d { animation-delay: -1s; } .orbit-3 .electron-3d { animation-delay: -2s; } @keyframes orbit3D { 0% { transform: translateX(-50%) rotateZ(0deg) translateY(-80px) rotateZ(0deg); } 100% { transform: translateX(-50%) rotateZ(360deg) translateY(-80px) rotateZ(-360deg); } }
.judge-box { background: rgba(0, 242, 254, 0.05); border: 2px dashed #00f2fe; border-radius: 15px; padding: 15px; margin-bottom: 25px; text-align: center; }
.glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; margin-bottom: 20px; }
div[data-testid="stMetricValue"] { color: #00f2fe !important; }
</style>""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# واجهة الدخول
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown("<h1 style='text-align:center; color:#00f2fe;'>StudyFlow AI</h1>", unsafe_allow_html=True)
        st.markdown('<div class="judge-box"><h4>💎 لجنة التحكيم</h4><p>admin | 123 <br> student | 456</p></div>', unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔒 دخول", "✨ تسجيل"])
        with t1:
            u = st.text_input("اسم المستخدم", key="L_u")
            p = st.text_input("كلمة المرور", type="password", key="L_p")
            if st.button("انطلاق", use_container_width=True):
                role = check_login(u, p)
                if role:
                    st.session_state.auth, st.session_state.role, st.session_state.username = True, role, u
                    st.rerun()
                else: st.error("بيانات غير صحيحة")
        with t2:
            nu = st.text_input("يوزر جديد", key="R_u")
            np = st.text_input("سر جديد", type="password", key="R_p")
            if st.button("إنشاء حساب"):
                if cloud_action("register", {"username": nu, "password": np, "role": "student"}): st.success("تم!")

# النظام الداخلي
else:
    with st.sidebar:
        if st.session_state.role == "admin": 
            st.markdown("### 🛡️ مركز القيادة")
            menu = st.radio("التحكم", ["📊 لوحة القيادة", "👥 إدارة المحاربين", "🆘 مراقبة العمليات", "خروج"])
        else: 
            st.markdown(f"### 🚀 البطل: {st.session_state.username}")
            menu = st.radio("غرفة العمليات", ["🏠 لوحة التحكم", "🆘 خطة الإنقاذ", "خروج"])

    if menu == "خروج": st.session_state.auth = False; st.rerun()

    # ==========================
    # واجهة الطالب
    # ==========================
    if st.session_state.role == "student":
        user_plans = get_user_plans(st.session_state.username)

        if menu == "🏠 لوحة التحكم":
            st.title("📈 رادار التقدم (3D)")
            with st.expander("➕ إضافة مادة للرادار"):
                with st.form("add"):
                    s = st.text_input("المادة")
                    c = st.number_input("الدروس", min_value=1)
                    if st.form_submit_button("إضافة"):
                        cloud_action("save_rescue", {"username":st.session_state.username, "subject":s, "total":c, "days":5})
                        st.rerun()
            
            if user_plans:
                st.divider()
                cols = st.columns(len(user_plans)) if len(user_plans) <= 4 else st.columns(4)
                colors = ["#00f2fe", "#4facfe", "#f59e0b", "#ec4899", "#10b981"]
                for i, plan in enumerate(user_plans):
                    # === حماية ضد القيم الفارغة في السحابة ===
                    try:
                        done = int(float(str(plan.get('completed', 0)).strip() or 0))
                    except: done = 0
                    
                    try:
                        total = int(float(str(plan.get('total', 1)).strip() or 1))
                    except: total = 1
                    # ========================================
                    
                    percent = (done / total * 100) if total > 0 else 0
                    col_idx = i if i < len(cols) else i % 4
                    with cols[col_idx]: atomic_progress_3d(plan['subject'], percent, colors[i%5])
            else: st.info("الرادار فارغ.")

        elif menu == "🆘 خطة الإنقاذ":
            st.title("🆘 تنفيذ المهام")
            if user_plans:
                selected_subject = st.selectbox("اختر المادة:", [p['subject'] for p in user_plans])
                target_plan = next((p for p in user_plans if p['subject'] == selected_subject), None)
                if target_plan:
                    new_count = render_mission_card(target_plan)
                    
                    # === نفس الحماية هنا ===
                    try:
                        old_count = int(float(str(target_plan.get('completed', 0)).strip() or 0))
                    except: old_count = 0
                    # =======================

                    if new_count != old_count:
                        if cloud_action("update_progress", {"username": st.session_state.username, "subject": selected_subject, "completed": new_count}):
                            st.toast("✅ تم الحفظ!"); st.rerun()
            else: st.info("أضف مواد أولاً.")

    # ==========================
    # واجهة المدير
    # ==========================
    elif st.session_state.role == "admin":
        if menu == "📊 لوحة القيادة":
            st.title("📊 المؤشرات الاستراتيجية")
            users = fetch_all_data("Users")
            plans = fetch_all_data("RescuePlans")
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("عدد المحاربين المسجلين", len(users))
            with c2: st.metric("الخطط النشطة حالياً", len(plans))
            with c3: st.metric("حالة السيرفر", "متصل 🟢")
            st.markdown("---")
            st.info("💡 هذه اللوحة تعطيك نظرة شاملة على نشاط المنصة.")

        elif menu == "👥 إدارة المحاربين":
            st.title("👥 سجلات المحاربين")
            users = fetch_all_data("Users")
            st.dataframe(pd.DataFrame(users), use_container_width=True)
            st.divider()
            st.subheader("🚫 منطقة العقاب (الحذف)")
            student_list = [u['username'] for u in users if u.get('role') != 'admin']
            if student_list:
                c1, c2 = st.columns([3, 1])
                with c1: target_user = st.selectbox("اختر محارباً لاستبعاده نهائياً:", student_list)
                with c2: 
                    st.write(""); st.write("") 
                    if st.button("🔴 تنفيذ قرار الطرد", use_container_width=True):
                        if delete_user_cloud(target_user):
                            st.success(f"تم استبعاد {target_user} بنجاح."); st.rerun()
            else: st.info("لا يوجد طلاب لحذفهم حالياً.")

        elif menu == "🆘 مراقبة العمليات":
            st.title("🆘 غرفة العمليات الحية")
            plans = fetch_all_data("RescuePlans")
            if plans:
                st.dataframe(pd.DataFrame(plans), use_container_width=True)
                st.success(f"يوجد {len(plans)} عملية إنقاذ جارية.")
            else: st.warning("لا توجد خطط نشطة.")