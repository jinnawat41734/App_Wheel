import streamlit as st
import time
import random
import pandas as pd
from streamlit_sortables import sort_items # นำเข้า Library ลากวาง

st.set_page_config(page_title="Calorie Master Pro", page_icon="🍔", layout="centered")

# --- 1. การตั้งค่า Session State ---
if "food_list" not in st.session_state:
    st.session_state.food_list = []
if "mode" not in st.session_state:
    st.session_state.mode = "start"
if "category" not in st.session_state:
    st.session_state.category = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = []

# --- 2. คลังข้อมูลอาหาร ---
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
        {"name": "พิซซ่า (2 ชิ้น)", "cal": 550, "img": "🍕"},
        {"name": "แฮมเบอร์เกอร์", "cal": 490, "img": "🍔"},
        {"name": "เฟรนช์ฟรายส์", "cal": 365, "img": "🍟"},
        {"name": "ไก่ทอด (1 ชิ้น)", "cal": 320, "img": "🍗"},
        {"name": "น้ำอัดลม", "cal": 140, "img": "🥤"},
    ],
    "ผลไม้ (Fruits)": [
        {"name": "ทุเรียน (1 พู)", "cal": 350, "img": "🍈"},
        {"name": "มะม่วงสุก (ครึ่งซีก)", "cal": 100, "img": "🥭"},
        {"name": "กล้วยหอม", "cal": 120, "img": "🍌"},
        {"name": "แอปเปิ้ล", "cal": 52, "img": "🍎"},
        {"name": "แตงโม (1 ชิ้น)", "cal": 30, "img": "🍉"},
    ]
}

# --- ตกแต่ง CSS เล็กน้อยให้ดูเป็นแอปมากขึ้น ---
st.markdown("""
    <style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .emoji-font { font-size: 50px !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🍔 Calorie Master Pro")

# --- 3. โหมดหน้าแรก ---
if st.session_state.mode == "start":
    st.markdown('<p class="big-font">มาทดสอบความจำกัน!</p>', unsafe_allow_html=True)
    st.info("ระบบจะสุ่มหมวดหมู่อาหารให้คุณจำแคลลอรี่ภายในเวลา 10 วินาที จากนั้นคุณต้อง 'ลากและวาง' เพื่อเรียงลำดับให้ถูกต้อง")
    
    st.write("")
    if st.button("🎰 เริ่มสุ่มหมวดหมู่ (Start Game)", type="primary", use_container_width=True):
        st.session_state.mode = "spinning"
        st.rerun()

# --- 4. โหมดแอนิเมชันสุ่ม (Slot Machine) ---
elif st.session_state.mode == "spinning":
    st.subheader("🎲 กำลังสุ่มหมวดหมู่...")
    spin_placeholder = st.empty()
    categories = list(data_source.keys())
    
    # เอฟเฟกต์หมุนสล็อต
    for _ in range(15):
        temp_cat = random.choice(categories)
        spin_placeholder.markdown(f"<div class='emoji-font' style='color: gray;'>🔄<br>{temp_cat}</div>", unsafe_allow_html=True)
        time.sleep(0.1) 
    
    chosen_category = random.choice(categories)
    spin_placeholder.markdown(f"<div class='emoji-font' style='color: #ff4b4b;'>🎯<br>{chosen_category}</div>", unsafe_allow_html=True)
    st.balloons()
    
    temp_list = list(data_source[chosen_category])
    random.shuffle(temp_list)
    
    st.session_state.category = chosen_category
    st.session_state.food_list = temp_list
    
    time.sleep(2.0)
    st.session_state.mode = "memorize"
    st.rerun()

# --- 5. โหมดจดจำ (10 วินาที) ---
elif st.session_state.mode == "memorize":
    if not st.session_state.food_list:
        st.session_state.mode = "start"
        st.rerun()
        
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

# --- 6. โหมดแบบทดสอบ (Drag & Drop) ---
elif st.session_state.mode == "quiz":
    st.subheader(f"📝 ทดสอบ: {st.session_state.category}")
    st.write("👉 **ลากและวาง (Drag & Drop)** รายการด้านล่างเพื่อเรียงลำดับจาก **แคลลอรี่มากที่สุด (บนสุด) ไปหา น้อยที่สุด (ล่างสุด)**")
    
    if not st.session_state.food_list:
        st.session_state.mode = "start"
        st.rerun()
         
    # สร้างรูปแบบข้อมูลที่จะให้แสดงตอนลากวาง (เอาภาพและชื่อมารวมกัน)
    sortable_items = [f"{i['img']} {i['name']}" for i in st.session_state.food_list]
    
    # *** ฟังก์ชันพระเอกของเรา: ระบบลากวาง ***
    user_sorted = sort_items(sortable_items)
    
    st.write("")
    if st.button("ส่งคำตอบ (Submit)", type="primary"):
        # ตัดเอาแค่ชื่ออาหารออกมาตรวจ (ลบ Emoji ออก)
        # รูปแบบคือ "🍔 ชื่ออาหาร" เราจึงแยกด้วยช่องว่างตัวแรก
        st.session_state.user_answer = [item.split(" ", 1)[1] for item in user_sorted]
        st.session_state.mode = "result"
        st.rerun()

# --- 7. โหมดเฉลย ---
elif st.session_state.mode == "result":
    correct_items = sorted(st.session_state.food_list, key=lambda x: x['cal'], reverse=True)
    correct_order = [i["name"] for i in correct_items]
    user_answer = st.session_state.user_answer
    
    score = 0
    results_data = []
    
    for i in range(5):
        is_correct = (user_answer[i] == correct_order[i])
        if is_correct:
            score += 1
        
        results_data.append({
            "อันดับที่": i + 1,
            "คำตอบของคุณ": user_answer[i],
            "คำตอบที่ถูกต้อง": f"{correct_order[i]}",
            "แคลลอรี่": f"{correct_items[i]['cal']} kcal",
            "ผลตรวจ": "✅" if is_correct else "❌"
        })
    
    st.markdown("---")
    st.markdown(f'<p class="big-font">📊 ผลคะแนนของคุณ: {score}/5</p>', unsafe_allow_html=True)
    
    if score == 5:
        st.success("อัจฉริยะ! ความจำคุณระดับเทพ 💯")
        st.balloons()
    elif score >= 3:
        st.info("ทำได้ดีมาก! พลาดไปแค่นิดเดียว 👍")
    else:
        st.error("ไม่เป็นไร ลองฝึกความจำใหม่อีกรอบนะ ✌️")
    
    st.write("**วิเคราะห์ข้อผิดพลาด:**")
    df_results = pd.DataFrame(results_data)
    st.table(df_results)
    
    st.write("")
    if st.button("🔄 เล่นรอบใหม่ (Play Again)", use_container_width=True):
        st.session_state.mode = "start"
        st.session_state.food_list = []
        st.session_state.category = ""
        st.session_state.user_answer = []
        st.rerun()
