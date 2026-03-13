import streamlit as st
import time
import random

st.set_page_config(page_title="Food Calorie Quiz", page_icon="🎡")

# --- 1. การตั้งค่าหน้าจอและ Session State แบบกันพังขั้นสูงสุด ---
# เช็คเลยว่า items เป็น List จริงไหม ถ้าไม่ใช่บังคับล้างค่าใหม่
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = []
if "mode" not in st.session_state:
    st.session_state.mode = "start"

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

# --- 2. ส่วนหน้าแรก ---
if st.session_state.mode == "start":
    st.info("กดปุ่มด้านล่างเพื่อสุ่มรายการอาหาร")
    if st.button("🎡 เริ่มหมุนวงล้อสุ่มหมวด"):
        # ใช้ list() เพื่อให้แน่ใจว่าดึงข้อมูลมาสร้าง List ใหม่จริงๆ
        st.session_state.items = list(data_source["Street Food"])
        random.shuffle(st.session_state.items)
        st.session_state.mode = "memorize"
        st.rerun()

# --- 3. ส่วนจดจำข้อมูล ---
elif st.session_state.mode == "memorize":
    # ตัวดัก Error: ถ้าไม่มีข้อมูลให้เด้งกลับหน้าแรกทันที
    if not st.session_state.items:
        st.session_state.mode = "start"
        st.rerun()
        
    st.subheader("⚠️ คุณมีเวลา 10 วินาทีในการจำแคลลอรี่!")
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.items):
        if i < 5: # ป้องกันกรณีข้อมูลเกิน 5 ช่อง
            with cols[i]:
                st.markdown(f"**{item['name']}**")
                st.code(f"{item['cal']} kcal")
    
    progress_text = "กำลังนับถอยหลัง..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    st.session_state.mode = "quiz"
    st.rerun()

# --- 4. ส่วนแบบทดสอบ ---
elif st.session_state.mode == "quiz":
    st.subheader("📝 แบบทดสอบ: เรียงลำดับแคลลอรี่")
    
    # ตัวดัก Error: ถ้าไม่มีข้อมูลให้เด้งกลับหน้าแรก
    if not st.session_state.items:
        st.session_state.mode = "start"
        st.rerun()
         
    food_names = [i["name"] for i in st.session_state.items]
    user_answer = st.multiselect("เลือกรายการอาหารตามลำดับจาก มากไปน้อย (1-5)", food_names)
    
    if st.button("ส่งคำตอบ"):
        correct_order = [i["name"] for i in sorted(st.session_state.items, key=lambda x: x['cal'], reverse=True)]
        if user_answer == correct_order:
            st.success("🎉 สุดยอด! คุณจำได้ถูกต้องทั้งหมด")
            st.balloons()
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองพยายามใหม่อีกครั้งนะ!")
            st.write("ลำดับที่ถูกคือ:", " > ".join(correct_order))
        
        if st.button("เล่นรอบใหม่"):
            st.session_state.mode = "start"
            st.session_state.items = []
            st.rerun()
