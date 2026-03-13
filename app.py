import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="Calorie Master", page_icon="🎡", layout="centered")

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

st.title("🎡 เกมสุ่มหมวดวัดความจำแคลลอรี่")

# --- 3. โหมดหน้าแรก ---
if st.session_state.mode == "start":
    st.write("มาทดสอบความจำกัน! กดปุ่มด้านล่างเพื่อสุ่มหมวดหมู่อาหาร (คุณจะมีเวลาจำ 10 วินาที)")
    
    if st.button("🎰 กดเพื่อเริ่มสุ่มหมวดหมู่!", use_container_width=True):
        st.session_state.mode = "spinning"
        st.rerun()

# --- 4. โหมดแอนิเมชันสุ่ม ---
elif st.session_state.mode == "spinning":
    st.subheader("กำลังสุ่มหมวดหมู่...")
    spin_placeholder = st.empty()
    categories = list(data_source.keys())
    
    for _ in range(15): # สลับ 15 ครั้ง
        temp_cat = random.choice(categories)
        spin_placeholder.markdown(f"<h1 style='text-align: center; color: gray;'>🔄 {temp_cat} 🔄</h1>", unsafe_allow_html=True)
        time.sleep(0.1) 
    
    chosen_category = random.choice(categories)
    spin_placeholder.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>🎯 ได้หมวด: {chosen_category} 🎯</h1>", unsafe_allow_html=True)
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
        
    st.success(f"📌 หมวดปัจจุบัน: **{st.session_state.category}**")
    st.subheader("⚠️ จำแคลลอรี่ให้ดี! (10 วินาที)")
    
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.food_list):
        if i < 5: 
            with cols[i]:
                st.markdown(f"<h1 style='text-align: center;'>{item['img']}</h1>", unsafe_allow_html=True)
                st.markdown(f"**{item['name']}**")
                st.error(f"{item['cal']} kcal")
    
    progress_text = "กำลังนับถอยหลัง..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.1) 
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    st.session_state.mode = "quiz"
    st.rerun()

# --- 6. โหมดแบบทดสอบ ---
elif st.session_state.mode == "quiz":
    st.subheader(f"📝 ทดสอบหมวด: {st.session_state.category}")
    st.write("จงเลือกรายการอาหารเรียงตามลำดับจาก **แคลลอรี่มากที่สุด (1) ไปหา น้อยที่สุด (5)**")
    
    if not st.session_state.food_list:
        st.session_state.mode = "start"
        st.rerun()
         
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.food_list):
        if i < 5: 
            with cols[i]:
                st.markdown(f"<h1 style='text-align: center;'>{item['img']}</h1>", unsafe_allow_html=True)
                st.markdown(f"**{item['name']}**")

    food_names = [i["name"] for i in st.session_state.food_list]
    user_answer = st.multiselect("คลิกเลือกอาหารตามลำดับที่ถูกต้อง:", food_names)
    
    if st.button("ส่งคำตอบ", type="primary"):
        if len(user_answer) != 5:
            st.warning("⚠️ กรุณาเลือกรายการอาหารให้ครบทั้ง 5 อย่างก่อนส่งคำตอบครับ")
        else:
            # เก็บคำตอบลง Session แล้วเปลี่ยนหน้าไปโหมดเฉลย (Result) ทันที
            st.session_state.user_answer = user_answer
            st.session_state.mode = "result"
            st.rerun()

# --- 7. โหมดเฉลยและปุ่มเริ่มใหม่ (แยกออกมาเป็น State ใหม่) ---
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
            "คำตอบที่ถูกต้อง": f"{correct_order[i]} ({correct_items[i]['cal']} kcal)",
            "ผลลัพธ์": "✅ ถูก" if is_correct else "❌ ผิด"
        })
    
    st.markdown("---")
    st.subheader("📊 ผลคะแนนของคุณ")
    
    if score == 5:
        st.success(f"ยอดเยี่ยม! คุณได้คะแนน {score}/5 เต็ม 💯")
        st.balloons()
    elif score >= 3:
        st.info(f"ทำได้ดี! คุณได้คะแนน {score}/5 👍")
    else:
        st.error(f"ยังต้องฝึกอีกนิดนะ คุณได้คะแนน {score}/5 ✌️")
    
    st.write("**รายละเอียดการตอบ:**")
    df_results = pd.DataFrame(results_data)
    st.table(df_results)
    
    # ปุ่มนี้ทำงานได้ 100% แล้ว เพราะไม่ได้อยู่ซ้อนกับปุ่มไหน
    if st.button("🔄 เล่นรอบใหม่ (สุ่มใหม่)", use_container_width=True):
        st.session_state.mode = "start"
        st.session_state.food_list = []
        st.session_state.category = ""
        st.session_state.user_answer = []
        st.rerun()
