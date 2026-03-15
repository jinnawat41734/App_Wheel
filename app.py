import streamlit as st
import time
import random
import pandas as pd
import os
from datetime import datetime
from streamlit_sortables import sort_items

st.set_page_config(page_title="Calorie Master Pro", page_icon="🍔", layout="centered")

# --- 1. ไฟล์สำหรับเก็บฐานข้อมูล (Database) ---
CSV_FILE = "score_history.csv"

# ตรวจสอบว่ามีไฟล์ CSV หรือยัง ถ้าไม่มีให้สร้างใหม่พร้อมหัวข้อคอลัมน์
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Timestamp", "Player_Name", "Category", "Score"])
    df_init.to_csv(CSV_FILE, index=False)

# --- 2. การตั้งค่า Session State ---
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "food_list" not in st.session_state:
    st.session_state.food_list = []
if "mode" not in st.session_state:
    st.session_state.mode = "login" # เริ่มต้นที่หน้า Login
if "category" not in st.session_state:
    st.session_state.category = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = []
if "current_score" not in st.session_state:
    st.session_state.current_score = 0

# --- 3. คลังข้อมูลอาหาร ---
data_source = {
    "ของคาว (Savory)": [
        {"name": "ข้าวขาหมู", "cal": 690, "img": "🍛"},
        {"name": "ข้าวมันไก่", "cal": 596, "img": "🍗"},
        {"name": "ผัดไทย", "cal": 486, "img": "🍜"},
        {"name": "ลูกชิ้นปิ้ง", "cal": 135, "img": "🍡"},
        {"name": "ส้มตำไทย", "cal": 55, "img": "🥗"},
    ],
    "ของหวาน (Dessert)": [
        {"name": "บิงซู", "cal": 750, "img": "🍧"},
        {"name": "ฮันนี่โทสต์", "cal": 800, "img": "🍞"},
        {"name": "เค้กช็อกโกแลต", "cal": 450, "img": "🍰"},
        {"name": "ไอศกรีม 1 สกู๊ป", "cal": 250, "img": "🍦"},
        {"name": "มาการอง", "cal": 150, "img": "🥯"},
    ],
    "Fast Food": [
        {"name": "พิซซ่า", "cal": 550, "img": "🍕"},
        {"name": "แฮมเบอร์เกอร์", "cal": 490, "img": "🍔"},
        {"name": "เฟรนช์ฟรายส์", "cal": 365, "img": "🍟"},
        {"name": "ไก่ทอด", "cal": 320, "img": "🍗"},
        {"name": "น้ำอัดลม", "cal": 140, "img": "🥤"},
    ],
    "ผลไม้ (Fruits)": [
        {"name": "ทุเรียน", "cal": 350, "img": "🍈"},
        {"name": "มะม่วงสุก", "cal": 100, "img": "🥭"},
        {"name": "กล้วยหอม", "cal": 120, "img": "🍌"},
        {"name": "แอปเปิ้ล", "cal": 52, "img": "🍎"},
        {"name": "แตงโม", "cal": 30, "img": "🍉"},
    ]
}

# --- CSS สำหรับทำวงล้อหมุน และตกแต่ง ---
st.markdown("""
    <style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .emoji-font { font-size: 50px !important; text-align: center; }
    /* แอนิเมชันวงล้อหมุน */
    .spin-wheel { 
        font-size: 100px !important; 
        text-align: center; 
        animation: spin 1s linear infinite; 
        display: inline-block;
        width: 100%;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    </style>
""", unsafe_allow_html=True)

st.title("🍔 Calorie Master Pro")

# --- สร้างระบบ Tab เพื่อแยกหน้าเล่นเกม กับ หน้าประวัติคะแนน ---
tab1, tab2 = st.tabs(["🎮 เล่นเกม", "🏆 ตารางคะแนน (Leaderboard)"])

with tab1:
    # --- โหมด 1: Login ---
    if st.session_state.mode == "login":
        st.subheader("👋 ยินดีต้อนรับ! กรุณากรอกชื่อก่อนเล่น")
        name_input = st.text_input("ชื่อผู้เล่น (Player Name):", max_chars=20)
        
        if st.button("เข้าสู่ระบบ (Login)", type="primary"):
            if name_input.strip() == "":
                st.warning("⚠️ กรุณากรอกชื่อก่อนนะครับ")
            else:
                st.session_state.player_name = name_input.strip()
                st.session_state.mode = "start"
                st.rerun()

    # --- โหมด 2: หน้าแรก (รอสุ่ม) ---
    elif st.session_state.mode == "start":
        st.success(f"👤 ผู้เล่นปัจจุบัน: **{st.session_state.player_name}**")
        st.write("ระบบจะสุ่มหมวดหมู่อาหารให้คุณจำแคลลอรี่ภายในเวลา 10 วินาที")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🎰 เริ่มหมุนวงล้อ!", type="primary", use_container_width=True):
                st.session_state.mode = "spinning"
                st.rerun()
        with col2:
            if st.button("เปลี่ยนชื่อผู้เล่น", use_container_width=True):
                st.session_state.mode = "login"
                st.session_state.player_name = ""
                st.rerun()

    # --- โหมด 3: แอนิเมชันวงล้อหมุน (อัปเกรด CSS) ---
    elif st.session_state.mode == "spinning":
        st.subheader("🎡 กำลังหมุนวงล้อ...")
        
        # แสดงวงล้อหมุนแบบ CSS
        spin_placeholder = st.empty()
        spin_placeholder.markdown("<div class='spin-wheel'>🎡</div>", unsafe_allow_html=True)
        time.sleep(2.5) # ให้วงล้อหมุน 2.5 วินาที
        
        # สุ่มหมวดหมู่
        categories = list(data_source.keys())
        chosen_category = random.choice(categories)
        
        # หยุดวงล้อและแสดงผล
        spin_placeholder.markdown(f"<div class='emoji-font' style='color: #ff4b4b;'>🎯 ได้หมวด:<br>{chosen_category}</div>", unsafe_allow_html=True)
        st.balloons()
        
        # เตรียมข้อมูล
        temp_list = list(data_source[chosen_category])
        random.shuffle(temp_list)
        st.session_state.category = chosen_category
        st.session_state.food_list = temp_list
        
        time.sleep(2.0)
        st.session_state.mode = "memorize"
        st.rerun()

    # --- โหมด 4: จดจำ (10 วินาที) ---
    elif st.session_state.mode == "memorize":
        st.success(f"📌 หมวดที่ได้: **{st.session_state.category}**")
        st.subheader("⚠️ จำแคลลอรี่ให้ดี! (10 วินาที)")
        
        cols = st.columns(5)
        for i, item in enumerate(st.session_state.food_list):
            if i < 5: 
                with cols[i]:
                    st.markdown(f"<div class='emoji-font'>{item['img']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center;'><b>{item['name']}</b></div>", unsafe_allow_html=True)
                    st.error(f"{item['cal']} kcal", icon="🔥")
        
        progress_text = "⏱️ กำลังนับถอยหลัง..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.1) 
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        st.session_state.mode = "quiz"
        st.rerun()

    # --- โหมด 5: แบบทดสอบ (ลากวาง) & บันทึกคะแนน ---
    elif st.session_state.mode == "quiz":
        st.subheader(f"📝 ทดสอบ: {st.session_state.category}")
        st.write("👉 **ลากและวาง** เรียงลำดับจาก **แคลลอรี่มากที่สุด (บน) ไปหา น้อยที่สุด (ล่าง)**")
        
        sortable_items = [f"{i['img']} {i['name']}" for i in st.session_state.food_list]
        user_sorted = sort_items(sortable_items)
        
        st.write("")
        if st.button("ส่งคำตอบ (Submit)", type="primary"):
            user_answer = [item.split(" ", 1)[1] for item in user_sorted]
            correct_items = sorted(st.session_state.food_list, key=lambda x: x['cal'], reverse=True)
            correct_order = [i["name"] for i in correct_items]
            
            # คำนวณคะแนน
            score = sum([1 for i in range(5) if user_answer[i] == correct_order[i]])
            
            # 💾 บันทึกข้อมูลลง CSV 💾
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Player_Name": st.session_state.player_name,
                "Category": st.session_state.category,
                "Score": score
            }])
            new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
            
            # เก็บค่าไว้โชว์หน้า Result
            st.session_state.current_score = score
            st.session_state.user_answer = user_answer
            st.session_state.mode = "result"
            st.rerun()

    # --- โหมด 6: เฉลยผลลัพธ์ ---
    elif st.session_state.mode == "result":
        score = st.session_state.current_score
        st.markdown(f'<p class="big-font">📊 ผลคะแนนของคุณ {st.session_state.player_name}: {score}/5</p>', unsafe_allow_html=True)
        
        if score == 5:
            st.success("อัจฉริยะ! ความจำระดับเทพ 💯")
            st.balloons()
        elif score >= 3:
            st.info("ทำได้ดีมาก! 👍")
        else:
            st.error("ลองฝึกใหม่อีกรอบนะ ✌️")
        
        if st.button("🔄 เล่นรอบใหม่ (Play Again)", use_container_width=True):
            st.session_state.mode = "start"
            st.session_state.food_list = []
            st.session_state.category = ""
            st.session_state.user_answer = []
            st.rerun()

# --- ส่วนของ Tab 2: ตารางคะแนน (Leaderboard) ---
with tab2:
    st.subheader("🏆 ประวัติการเล่นทั้งหมด")
    st.write("ข้อมูลนี้ถูกดึงมาจากไฟล์ `score_history.csv` แบบ Real-time")
    
    # อ่านไฟล์ CSV มาแสดงเป็นตาราง Dataframe
    try:
        df_history = pd.read_csv(CSV_FILE)
        if df_history.empty:
            st.info("ยังไม่มีข้อมูลประวัติการเล่นครับ")
        else:
            # เรียงลำดับจากคะแนนมากไปน้อย และเวลาล่าสุด
            df_history = df_history.sort_values(by=["Score", "Timestamp"], ascending=[False, False])
            
            # ใช้ Pandas ปรับแต่ง Index ใหม่ให้ดูเป็นอันดับ
            df_history.reset_index(drop=True, inplace=True)
            df_history.index += 1 
            
            st.dataframe(df_history, use_container_width=True)
            
            # กิมมิคสำหรับสาย Data: โชว์สถิติเล็กๆ น้อยๆ
            st.write("📊 **สถิติแบบย่อ (Data Summary):**")
            st.write(f"- จำนวนครั้งที่มีการเล่นทั้งหมด: **{len(df_history)}** ครั้ง")
            st.write(f"- คะแนนเฉลี่ย (Mean): **{df_history['Score'].mean():.2f}** คะแนน")
            
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ฐานข้อมูล")
