import streamlit as st
import time
import random

# --- 1. การตั้งค่าหน้าจอและ Session State ---
st.set_page_config(page_title="Food Calorie Quiz", page_icon="🎡")

# ตรวจสอบว่ามีตัวแปรในระบบหรือยัง ถ้าไม่มีให้สร้างค่าเริ่มต้นไว้
if "items" not in st.session_state:
    st.session_state.items = []
if "mode" not in st.session_state:
    st.session_state.mode = "start"

# คลังข้อมูลอาหาร
data_source = {
    "Street Food": [
        {"name": "ข้าวขาหมู", "cal": 690},
        {"name": "ข้าวมันไก่", "cal": 596},
        {"name": "ผัดไทย", "cal": 486},
        {"name": "ลูกชิ้นปิ้ง", "cal": 135},
        {"name": "ส้มตำไทย", "cal": 55},
    ]
}

st.title("🎡 เกมสุ่มหมวดวัดความจำแคลลอรี่")
st.write("ทักษะการวิเคราะห์ข้อมูล เริ่มต้นจากการจดจำข้อมูลที่ถูกต้อง!")

# --- 2. ส่วนหน้าแรก (Start Mode) ---
if st.session_state.mode == "start":
    st.info("กดปุ่มด้านล่างเพื่อสุ่มรายการอาหาร")
    if st.button("🎡 เริ่มหมุนวงล้อสุ่มหมวด"):
        # สุ่มและเตรียมข้อมูล
        selected_items = data_source["Street Food"].copy()
        random.shuffle(selected_items)
        
        # บันทึกลง Session State เพื่อให้แอปจำได้แม้จะโดนรันใหม่
        st.session_state.items = selected_items
        st.session_state.mode = "memorize"
        st.rerun()

# --- 3. ส่วนจดจำข้อมูล (Memorize Mode) ---
elif st.session_state.mode == "memorize":
    st.subheader("⚠️ คุณมีเวลา 10 วินาทีในการจำแคลลอรี่!")
    
    # แสดงข้อมูลอาหาร 5 อย่าง
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.items):
        with cols[i]:
            st.markdown(f"**{item['name']}**")
            st.code(f"{item['cal']} kcal")
    
    # ตัวนับถอยหลัง
    progress_text = "กำลังนับถอยหลัง..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.1)  # 0.1s * 100 = 10 วินาที
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    # เมื่อครบเวลา เปลี่ยนโหมด
    st.session_state.mode = "quiz"
    st.rerun()

# --- 4. ส่วนแบบทดสอบ (Quiz Mode) ---
elif st.session_state.mode == "quiz":
    st.subheader("📝 แบบทดสอบ: เรียงลำดับแคลลอรี่")
    st.write("จงเรียงลำดับอาหารจาก **แคลลอรี่มากที่สุด** ไปหา **น้อยที่สุด**")
    
    # สร้าง List ของชื่ออาหาร (แบบสุ่มตำแหน่งเพื่อไม่ให้เดาได้)
    food_names = [i["name"] for i in st.session_state.items]
    
    # ใช้ Multiselect ให้ผู้ใช้เลือกตามลำดับ
    user_answer = st.multiselect("เลือกรายการอาหารตามลำดับ 1-5", food_names)
    
    if st.button("ส่งคำตอบ"):
        # คำนวณคำตอบที่ถูกต้อง
        correct_order = [i["name"] for i in sorted(st.session_state.items, key=lambda x: x['cal'], reverse=True)]
        
        if user_answer == correct_order:
            st.success("🎉 สุดยอด! คุณจำได้ถูกต้องทั้งหมด")
            st.balloons() # แสดงความยินดี
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองพยายามใหม่อีกครั้งนะ!")
            st.write("ลำดับที่ถูกคือ:", " > ".join(correct_order))
        
        # ปุ่มเริ่มใหม่
        if st.button("เล่นรอบใหม่"):
            st.session_state.mode = "start"
            st.session_state.items = []
            st.rerun()
