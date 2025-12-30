import streamlit as st
import pandas as pd
import math

def atomic_progress_3d(label, percent, color="#00f2fe"):
    """رسم ذرة ثلاثية الأبعاد (3D Atom) تفاعلية"""
    # حماية ضد القيم غير الرقمية
    try:
        percent_val = int(float(percent))
    except:
        percent_val = 0
        
    st.markdown(f"""
        <div class="atom-container-3d" style="--atom-color: {color};">
            <div class="nucleus-3d">{percent_val}%</div>
            <div class="orbit-3d orbit-1"><div class="electron-3d"></div></div>
            <div class="orbit-3d orbit-2"><div class="electron-3d"></div></div>
            <div class="orbit-3d orbit-3"><div class="electron-3d"></div></div>
        </div>
        <p style="text-align:center; font-weight:900; color:{color}; margin-top:20px; font-size: 1.2rem;">{label}</p>
    """, unsafe_allow_html=True)

def render_mission_card(subject_data):
    """الجدول الذكي: يظهر علامات الصح المحفوظة سابقاً"""
    
    subject = subject_data['subject']
    # حماية إضافية هنا أيضاً
    try: total = int(subject_data['total'])
    except: total = 0
    
    # === هنا كان سبب الخطأ وتم إصلاحه ===
    # نحضر القيمة، ولو كانت نصاً فارغاً نعتبرها صفراً
    raw_completed = subject_data.get('completed', 0)
    if raw_completed == "" or raw_completed is None:
        completed_stored = 0
    else:
        try:
            completed_stored = int(float(raw_completed))
        except ValueError:
            completed_stored = 0
    # ====================================

    st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid #00f2fe;">
            <h3 style="color:#00f2fe; margin:0;">🚀 خطة {subject}</h3>
            <p style="color:#fff;">تم إنجاز <b>{completed_stored}</b> من أصل <b>{total}</b> درس.</p>
        </div>
    """, unsafe_allow_html=True)

    # بناء الجدول بناءً على ما تم حفظه
    tasks = []
    for i in range(total):
        # إذا كان رقم الدرس أقل من عدد المنجزات، نضع عليه علامة صح
        is_done = True if i < completed_stored else False
        tasks.append({"المادة": subject, "الدرس": f"درس {i+1}", "تم": is_done})

    # عرض الجدول
    df = pd.DataFrame(tasks)
    edited_df = st.data_editor(
        df,
        column_config={"تم": st.column_config.CheckboxColumn("إنجاز", default=False)},
        use_container_width=True, hide_index=True, key=f"editor_{subject}"
    )
    
    # حساب العدد الجديد بعد تعديل الطالب للجدول
    new_completed_count = edited_df["تم"].sum()
    
    return new_completed_count