import streamlit as st
import time
import random

# --- 1. ตั้งค่าเริ่มต้นให้กับ Session State (ป้องกัน Error นี้) ---
if "items" not in st.session_state:
    st.session_state.items = []
if "mode" not in st.session_state:
    st.session_state.mode = "start"

# ข้อมูลอาหาร
data = {
    "Street Food": [
        {"name": "ข้าวขาหมู", "cal": 690},
        {"name": "ข้าวมันไก่", "cal": 596},
        {"name": "ผัดไทย", "cal": 486},
        {"name": "ลูกชิ้นปิ้ง", "cal": 135},
        {"name": "ส้มตำไทย", "cal": 55},
    ]
}

st.title("🎡 วงล้อวัดความจำแคลลอรี่")

# --- 2. ส่วนวงล้อ ---
if st.button("🎡 หมุนวงล้อสุ่มหมวด"):
    # ดึงข้อมูลใหม่และสับเปลี่ยนตำแหน่งก่อนเก็บลง session_state
    temp_items = data["Street Food"].copy()
    random.shuffle(temp_items)
    st.session_state.items = temp_items
    st.session_state.mode = "memorize"
    st.rerun() # สั่งให้รันใหม่เพื่อเข้าสู่โหมดจดจำทันที

# --- 3. ส่วนจดจำข้อมูล (แสดงเฉพาะเมื่อโหมดคือ memorize) ---
if st.session_state.mode == "memorize" and st.session_state.items:
    st.subheader("จดจำแคลลอรี่ให้ดี! (10 วินาที)")
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.items):
        cols[i].metric(item["name"], f"{item['cal']} kcal")
    
    bar = st.progress(0)
    for p in range(100):
        time.sleep(0.1)
        bar.progress(p + 1)
    
    st.session_state.mode = "quiz"
    st.rerun()

# --- 4. ส่วนคำถาม ---
if st.session_state.mode == "quiz":
    st.subheader("📝 เรียงลำดับจาก แคลลอรี่มาก -> น้อย")
    options = [i["name"] for i in st.session_state.items]
    user_answer = st.multiselect("เลือกชื่ออาหารตามลำดับ (ตัวที่ 1 คือมากสุด)", options)
    
    if st.button("ส่งคำตอบ"):
        correct_order = [i["name"] for i in sorted(st.session_state.items, key=lambda x: x['cal'], reverse=True)]
        if user_answer == correct_order:
            st.success("ถูกต้อง! คุณคือยอดนักจำ")
            if st.button("เล่นใหม่อีกครั้ง"):
                st.session_state.mode = "start"
                st.rerun()
        else:
            st.error(f"ยังไม่ถูก! ลำดับที่ถูกต้องคือ: {' > '.join(correct_order)}")
