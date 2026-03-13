import streamlit as st
import time
import random

# 1. ข้อมูลอาหาร (Mockup Data)
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

# 2. ส่วนวงล้อ (จำลองด้วยปุ่มสุ่ม)
if st.button("🎡 หมุนวงล้อสุ่มหมวด"):
    st.session_state.mode = "memorize"
    st.session_state.items = data["Street Food"]
    random.shuffle(st.session_state.items)

# 3. ส่วนจดจำข้อมูล (10 วินาที)
if "mode" in st.session_state and st.session_state.mode == "memorize":
    st.subheader("จดจำแคลลอรี่ให้ดี! (10 วินาที)")
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.items):
        cols[i].metric(item["name"], f"{item['cal']} kcal")
    
    # Progress Bar แทนนาฬิกา
    bar = st.progress(0)
    for p in range(100):
        time.sleep(0.1)
        bar.progress(p + 1)
    
    st.session_state.mode = "quiz"
    st.rerun()

# 4. ส่วนคำถาม
if "mode" in st.session_state and st.session_state.mode == "quiz":
    st.subheader("📝 เรียงลำดับจาก แคลลอรี่มาก -> น้อย")
    options = [i["name"] for i in st.session_state.items]
    user_answer = st.multiselect("เลือกชื่ออาหารตามลำดับ (ตัวที่ 1 คือมากสุด)", options)
    
    if st.button("ส่งคำตอบ"):
        correct_order = [i["name"] for i in sorted(st.session_state.items, key=lambda x: x['cal'], reverse=True)]
        if user_answer == correct_order:
            st.success("ถูกต้อง! คุณคือยอดนักจำ")
        else:
            st.error(f"ยังไม่ถูก! ลำดับที่ถูกคือ: {' > '.join(correct_order)}")