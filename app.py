import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="Calorie Master", page_icon="🎡", layout="centered")

# --- 1. การตั้งค่า Session State ---
if "food_list" not in st.session_state or not isinstance(st.session_state.food_list, list):
    st.session_state.food_list = []
if "mode" not in st.session_state:
    st.session_state.mode = "start"
if "category" not in st.session_state:
    st.session_state.category = ""

# --- 2. คลังข้อมูลอาหาร (แบ่ง 4 หมวดหมู่) ---
# ตรง "img" สามารถเปลี่ยนจาก Emoji เป็นชื่อไฟล์รูปเช่น "apple.jpg" ได้ (ถ้าอัปโหลดรูปลง GitHub ด้วย)
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

# --- 3. โหมดหน้าแรก: วงล้อสุ่มหมวด ---
if st.session_state.mode == "start":
    st.write("มาทดสอบความจำกัน! ระบบจะสุ่มหมวดหมู่อาหารให้คุณจำแคลลอรี่ 10 วินาที")
    
    if st.button("🎡 กดเพื่อสุ่มหมวดหมู่อาหาร", use_container_width=True):
        with st.spinner("กำลังหมุนวงล้อ..."):
            time.sleep(1.5) # จำลองเวลาหมุนวงล้อ
            
            # สุ่มหมวดหมู่
            categories = list(data_source.keys())
            chosen_category = random.choice(categories)
            
            # สุ่มอาหารในหมวดนั้น
            temp_list = list(data_source[chosen_category])
            random.shuffle(temp_list)
            
            # บันทึกค่า
            st.session_state.category = chosen_category
            st.session_state.food_list = temp_list
            st.session_state.mode = "memorize"
            st.rerun()

# --- 4. โหมดจดจำ (10 วินาที) ---
elif st.session_state.mode == "memorize":
    if not st.session_state.food_list:
        st.session_state.mode = "start"
        st.rerun()
        
    st.success(f"🎉 คุณได้หมวด: **{st.session_state.category}**")
    st.subheader("⚠️ จำแคลลอรี่ให้ดี! (10 วินาที)")
    
    # แสดงรูป/Emoji และแคลลอรี่
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.food_list):
        if i < 5: 
            with cols[i]:
                # ถ้าใช้รูปจริง ให้เปลี่ยนเป็น st.image(item['img'])
                st.markdown(f"<h1 style='text-align: center;'>{item['img']}</h1>", unsafe_allow_html=True)
                st.markdown(f"**{item['name']}**")
                st.error(f"{item['cal']} kcal")
    
    # แถบจับเวลา
    progress_text = "กำลังนับถอยหลัง..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.1) # 10 วินาที
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    st.session_state.mode = "quiz"
    st.rerun()

# --- 5. โหมดแบบทดสอบและตรวจคำตอบ ---
elif st.session_state.mode == "quiz":
    st.subheader(f"📝 ทดสอบหมวด: {st.session_state.category}")
    st.write("จงเลือกรายการอาหารเรียงตามลำดับจาก **แคลลอรี่มากที่สุด (1) ไปหา น้อยที่สุด (5)**")
    
    if not st.session_state.food_list:
        st.session_state.mode = "start"
        st.rerun()
         
    # แสดงรูปภาพให้ดูอีกครั้งแบบไม่มีแคลลอรี่
    cols = st.columns(5)
    for i, item in enumerate(st.session_state.food_list):
        if i < 5: 
            with cols[i]:
                st.markdown(f"<h1 style='text-align: center;'>{item['img']}</h1>", unsafe_allow_html=True)
                st.markdown(f"**{item['name']}**")

    # ตัวเลือกให้ผู้ใช้ตอบ (ดึงแค่ชื่อมาให้เลือก)
    food_names = [i["name"] for i in st.session_state.food_list]
    user_answer = st.multiselect("คลิกเลือกอาหารตามลำดับที่ถูกต้อง:", food_names)
    
    if st.button("ส่งคำตอบ", type="primary"):
        if len(user_answer) != 5:
            st.warning("⚠️ กรุณาเลือกรายการอาหารให้ครบทั้ง 5 อย่างก่อนส่งคำตอบครับ")
        else:
            # คำนวณคำตอบที่ถูกต้อง
            correct_items = sorted(st.session_state.food_list, key=lambda x: x['cal'], reverse=True)
            correct_order = [i["name"] for i in correct_items]
            
            # ตรวจสอบและให้คะแนน
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
                    "ผลลัพธ์": "✅ ถูกต้อง" if is_correct else "❌ ผิด"
                })
            
            st.markdown("---")
            st.subheader("📊 ผลคะแนนของคุณ")
            
            # แสดงคะแนน
            if score == 5:
                st.success(f"ยอดเยี่ยม! คุณได้คะแนน {score}/5 เต็ม 💯")
                st.balloons()
            elif score >= 3:
                st.info(f"ทำได้ดี! คุณได้คะแนน {score}/5 👍")
            else:
                st.error(f"ยังต้องฝึกอีกนิดนะ คุณได้คะแนน {score}/5 ✌️")
            
            # แสดงตารางวิเคราะห์ความผิดพลาด
            st.write("**รายละเอียดการตอบ:**")
            df_results = pd.DataFrame(results_data)
            st.table(df_results)
            
            if st.button("🔄 เล่นรอบใหม่"):
                st.session_state.mode = "start"
                st.session_state.food_list = []
                st.rerun()
