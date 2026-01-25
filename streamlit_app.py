import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from daily_decision import LatexDecisionEngine

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบตัดสินใจการผลิตยาง",
    page_icon="🏭",
    layout="wide"
)

# สร้าง instance ของ engine
engine = LatexDecisionEngine()

# หัวข้อหลัก
st.title("🏭 ระบบตัดสินใจการผลิตแผ่นยางรมควัน")


# แสดงวันที่ปัจจุบันมุมขวา
col_title, col_date = st.columns([3, 1])
with col_title:
    pass
with col_date:
    st.markdown(f"**📅 วันที่:** {datetime.now().strftime('%d/%m/%Y')}")


# ตั้งค่าโรงงาน (แก้ไขได้)
st.subheader("⚙️ Parameters")
col1, col2, col3, col4 = st.columns(4)

with col1:
    production_capacity = st.number_input(
        "กำลังการผลิต (กก./วัน)",
        min_value=10000,
        max_value=200000,
        value=60000,
        step=5000
    )

with col2:
    max_stock = st.number_input(
        "Stock สูงสุด (กก.)",
        min_value=5000,
        max_value=50000,
        value=20000,
        step=1000
    )

with col3:
    production_cost = st.number_input(
        "ต้นทุนการผลิต (บาท/กก.)",
        min_value=0.0,
        max_value=20.0,
        value=5.0,
        step=0.5,
        format="%.2f"
    )

with col4:
    production_days = st.number_input(
        "ระยะเวลาผลิต (วัน)",
        min_value=1,
        max_value=10,
        value=4,
        step=1
    )

# อัพเดทค่าใน engine
engine.PRODUCTION_CAPACITY = production_capacity
engine.MAX_STOCK = max_stock
engine.PRODUCTION_COST = production_cost
engine.PRODUCTION_DAYS = production_days

st.markdown("---")

# ส่วนกรอกข้อมูล
st.header("📊 กรอกข้อมูลประจำวัน")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("ข้อมูลน้ำยาง")
    
    # น้ำยางที่เข้ามา
    R_today = st.number_input(
        "น้ำยางสดที่เข้ามาวันนี้ (กก.)",
        min_value=0,
        max_value=200000,
        value=75000,
        step=1000
    )
    
    # Stock ปัจจุบัน
    current_stock = st.number_input(
        "น้ำยางใน Stock ปัจจุบัน (กก.)",
        min_value=0,
        max_value=max_stock,
        value=0,
        step=1000
    )
    
    st.info(f"💡 น้ำยางรวมทั้งหมด: **{R_today + current_stock:,} กก.**")

with col_right:
    st.subheader("ราคา")
    
    # ราคาน้ำยางสด
    price_today_fresh = st.number_input(
        "ราคาน้ำยางสดวันนี้ (บาท/กก.)",
        min_value=0.0,
        value=45.0,
        step=0.5,
        format="%.2f"
    )
    
    # ราคาแผ่นยางรมควัน (ถ้ามี)
    know_future_price = st.checkbox("ทราบราคาแผ่นยางรมควันในอนาคต")
    
    price_today_plus_4 = None
    price_today_plus_5 = None
    
    if know_future_price:
        date_today = datetime.now()
        price_today_plus_4 = st.number_input(
            f"ราคาแผ่นยางรมควันวันที่ {(date_today + timedelta(days=production_days)).strftime('%d/%m/%Y')} (บาท/กก.)",
            min_value=0.0,
            value=52.0,
            step=0.5,
            format="%.2f"
        )
        
        price_today_plus_5 = st.number_input(
            f"ราคาแผ่นยางรมควันวันที่ {(date_today + timedelta(days=production_days+1)).strftime('%d/%m/%Y')} (บาท/กก.)",
            min_value=0.0,
            value=53.0,
            step=0.5,
            format="%.2f"
        )

st.markdown("---")

# คำนวณและแสดงผล
if st.button("🔍 วิเคราะห์และแนะนำการตัดสินใจ", type="primary", use_container_width=True):
    
    # เรียกใช้ logic
    decision = engine.daily_decision(
        R_today=R_today,
        current_stock=current_stock,
        price_today_fresh=price_today_fresh,
        price_today_plus_4=price_today_plus_4,
        price_today_plus_5=price_today_plus_5
    )
    
    # แสดงผลการตัดสินใจ
    st.header("✅ ผลการวิเคราะห์")
    
    # แสดงการตัดสินใจหลัก
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🏭 ผลิตทันที",
            f"{decision['produce']:,.0f} กก.",
            delta=f"{(decision['produce']/production_capacity)*100:.1f}% ของกำลังการผลิต"
        )
    
    with col2:
        st.metric(
            "📦 เก็บใน Stock",
            f"{decision['hold']:,.0f} กก.",
            delta=f"{(decision['hold']/max_stock)*100:.1f}% ของ Stock สูงสุด" if decision['hold'] > 0 else None
        )
    
    with col3:
        st.metric(
            "🚚 ขายน้ำยางสดทิ้ง",
            f"{decision['dispose']:,.0f} กก.",
            delta=f"-{decision['dispose']:,.0f} กก." if decision['dispose'] > 0 else "ไม่มี",
            delta_color="inverse"
        )
    
    # แสดงเหตุผล
    st.info(f"**เหตุผล:** {decision['reason']}")
    
    # คำนวณต้นทุนและรายได้
    st.markdown("---")
    st.subheader("💰 การวิเคราะห์ทางการเงิน")
    
    # สำหรับการผลิตทันที
    if decision['produce'] > 0 and price_today_plus_4:
        finance_produce = engine.calculate_costs_and_revenue(
            {'produce': decision['produce'], 'dispose': 0, 'hold': 0},
            price_today_fresh=price_today_fresh,
            price_sale_sheet=price_today_plus_4,
            storage_days=0
        )
        
        st.write("**การผลิตทันที:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ต้นทุนรวม", f"{finance_produce['total_cost']:,.2f} บาท")
        with col2:
            st.metric("รายได้", f"{finance_produce['total_revenue']:,.2f} บาท")
        with col3:
            st.metric("กำไร", f"{finance_produce['profit']:,.2f} บาท",
                     delta=f"{finance_produce['profit']:,.2f} บาท")
    
    # สำหรับการขายน้ำยางสด
    if decision['dispose'] > 0:
        transport_cost = engine.calculate_fresh_latex_sale_cost(decision['dispose'])
        fresh_revenue = decision['dispose'] * price_today_fresh
        fresh_profit = fresh_revenue - transport_cost
        
        st.write("**การขายน้ำยางสด:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ค่าขนส่ง", f"{transport_cost:,.2f} บาท")
        with col2:
            st.metric("รายได้", f"{fresh_revenue:,.2f} บาท")
        with col3:
            st.metric("กำไรสุทธิ", f"{fresh_profit:,.2f} บาท",
                     delta=f"{fresh_profit:,.2f} บาท")
    
    # ถ้ามีการเก็b stock
    if decision['hold'] > 0:
        st.write("**การเก็บ Stock:**")
        storage_cost_day1 = decision['hold'] * engine.STORAGE_COST_DAY1
        st.write(f"- ค่าเก็บรักษาวันแรก: {storage_cost_day1:,.2f} บาท")
        st.write(f"- ค่าเก็บรักษาวันที่ 2-10: {engine.STORAGE_COST_DAY2_10} บาท/กก./วัน")
        
        # คำนวณจุดคุ้มทุน
        if price_today_plus_5:
            breakeven = engine.calculate_breakeven_price(price_today_fresh, storage_days=1)
            st.write(f"- 📊 ราคาคุ้มทุน (เก็บ 1 วัน): **{breakeven:.2f} บาท/กก.**")
            
            if price_today_plus_5 >= breakeven:
                st.success(f"✅ ราคาวันที่ +5 ({price_today_plus_5:.2f} บาท) สูงกว่าจุดคุ้มทุน → คุ้มค่าที่จะเก็บ")
            else:
                st.warning(f"⚠️ ราคาวันที่ +5 ({price_today_plus_5:.2f} บาท) ต่ำกว่าจุดคุ้มทุน → ไม่คุ้มค่าที่จะเก็บ")

# Sidebar - คำอธิบาย
with st.sidebar:
    st.header("📖 คำอธิบายระบบ")
    
    st.markdown("""
    ### Logic การตัดสินใจ:
    
    **1. น้ำยางรวม < 60,000 กก.**
    - ผลิตทันทีทั้งหมด
    
    **2. น้ำยางรวม 60,000-80,000 กก.**
    - ผลิต 60,000 กก. ทันที
    - ส่วนเกิน: เปรียบเทียบจุดคุ้มทุน
        - ถ้าราคาอนาคต ≥ จุดคุ้มทุน → เก็บ stock
        - ถ้าราคาอนาคต < จุดคุ้มทุน → ขายทิ้ง
    
    **3. น้ำยางรวม ≥ 80,000 กก.**
    - ผลิต 60,000 กก.
    - เก็บ stock 20,000 กก.
    - ขายส่วนเกินทิ้ง
    
    ---
    
    ### ต้นทุนการผลิต:
    - ราคาน้ำยางสด
    - ค่าเก็บรักษา (ถ้ามี)
    - ต้นทุนการผลิต 5 บาท/กก.
    
    ### ต้นทุนการขาย:
    - ค่าขนส่ง 17,000 บาท/20,000 กก.
    """)
    
    st.markdown("---")
    st.caption("พัฒนาโดย: ระบบสนับสนุนการตัดสินใจ")