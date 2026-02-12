import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.daily_decision import LatexDecisionEngine

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="ระบบตัดสินใจการผลิตยาง",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS สำหรับตัวเลขที่เข้มขึ้น
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700;800&display=swap');
    
    /* ฟอนต์หลัก */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Sarabun', sans-serif !important;
    }
    
    /* ตัวเลขใน Metrics - ทำให้เข้มมาก */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1a202c !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Label ของ Metrics */
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
    }
    
    /* Delta (ตัวเลขเปลี่ยนแปลง) */
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 700 !important;
    }
    
    /* ตัวเลขในตาราง */
    .stTable td {
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* ตัวเลขใน Info/Success/Warning box */
    .stAlert strong, .stAlert b {
        font-weight: 800 !important;
        color: #1a202c !important;
    }
    
    /* ตัวเลขทั่วไป */
    p strong, p b, li strong, li b {
        font-weight: 700 !important;
    }
    
    /* หัวข้อ */
    h1 {
        color: #1a202c !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #2d3748;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
    }
    
    /* ปุ่ม */
    .stButton>button {
        background-color: #dc2626 !important;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #b91c1c !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Input fields */
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        font-size: 1.05rem;
        font-weight: 600;
        padding: 0.5rem;
        color: #1a202c;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Label ของ Input */
    .stNumberInput label {
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .stSuccess {
        background-color: #f0fdf4;
        border-left-color: #22c55e;
    }
    
    .stWarning {
        background-color: #fffbeb;
        border-left-color: #f59e0b;
    }
    
    .stInfo {
        background-color: #eff6ff;
        border-left-color: #3b82f6;
    }
    
    /* Checkbox */
    .stCheckbox {
        font-size: 1.05rem;
        font-weight: 600;
    }
    
    /* ซ่อน Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# สร้าง instance ของ engine
engine = LatexDecisionEngine()

# หัวข้อหลักพร้อมไอคอน
st.title("🏭 ระบบตัดสินใจการผลิตยางแผ่นรมควัน")


# แสดงวันที่ปัจจุบันมุมขวา
st.markdown(f"""
<div style='text-align: right; margin-bottom: 1rem;'>
    <span style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 color: white; 
                 padding: 0.5rem 1.5rem; 
                 border-radius: 20px; 
                 font-weight: 600;
                 font-size: 1rem;'>
        📅 {datetime.now().strftime('%d/%m/%Y')}
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ตั้งค่าโรงงาน (แก้ไขได้)
st.markdown("""
<div style='margin-bottom: 1rem;'>
    <h2>⚙️ ตั้งค่าพารามิเตอร์โรงงาน</h2>
</div>
""", unsafe_allow_html=True)
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
st.markdown("""
<div style='margin-bottom: 1rem;'>
    <h2>📊 กรอกข้อมูลประจำวัน</h2>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📦 ข้อมูลน้ำยาง")
    
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
    st.markdown("### 💰 ราคา")
    
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
    st.markdown("""
    <div style='margin: 2rem 0 1rem 0;'>
        <h2>✅ ผลการวิเคราะห์</h2>
    </div>
    """, unsafe_allow_html=True)
    
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
            "📦 เก็บใน Stock (รวม)",
            f"{decision['stock_old'] + decision['stock_new']:,.0f} กก.",
            delta=f"{((decision['stock_old'] + decision['stock_new'])/max_stock)*100:.1f}% ของ Stock สูงสุด"
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
    
    # แสดง Stock Update (ถ้ามี stock)
    if decision['stock_old'] > 0 or decision['stock_new'] > 0:
        st.markdown("---")
        st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <h2>📊 Stock Update</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col_stock1, col_stock2, col_stock3 = st.columns(3)
        
        with col_stock1:
            st.metric(
                "📦 Stock เดิม (คงเหลือ)",
                f"{decision['stock_old']:,.0f} กก.",
                help="น้ำยางที่เก็บไว้จากวันก่อนหน้า"
            )
        
        with col_stock2:
            st.metric(
                "📦 Stock ใหม่ (เพิ่มวันนี้)",
                f"{decision['stock_new']:,.0f} กก.",
                delta=f"+{decision['stock_new']:,.0f} กก." if decision['stock_new'] > 0 else "ไม่มี",
                help="น้ำยางที่เก็บเพิ่มจากวันนี้"
            )
        
        with col_stock3:
            total_stock = decision['stock_old'] + decision['stock_new']
            st.metric(
                "📦 Stock รวมทั้งหมด",
                f"{total_stock:,.0f} กก.",
                delta=f"{(total_stock/max_stock)*100:.1f}% ของความจุ",
                help="น้ำยางรวมที่เก็บไว้ทั้งหมด"
            )
        
        # แสดงรายละเอียด Stock
        st.markdown("**รายละเอียด Stock:**")
        if decision['stock_old'] > 0:
            st.write(f"- 🔹 Stock เดิม: {decision['stock_old']:,.0f} กก. (จากวันก่อนหน้า)")
        if decision['stock_new'] > 0:
            st.write(f"- 🔹 Stock ใหม่: {decision['stock_new']:,.0f} กก. (เก็บจากน้ำยางวันนี้)")
        st.write(f"- 🔹 พื้นที่ว่างคงเหลือ: {max_stock - total_stock:,.0f} กก.")
    
    # คำนวณต้นทุนและรายได้
    st.markdown("---")
    st.markdown("""
    <div style='margin-bottom: 1rem;'>
        <h2>💰 การวิเคราะห์ทางการเงิน</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # ตัวแปรเก็บค่ากำไร
    profit_production = 0
    profit_fresh_sale = 0
    has_production = False
    has_disposal = False
    
    # สำหรับการผลิตแผ่นยาง
    if decision['produce'] > 0 and price_today_plus_4:
        has_production = True
        # คำนวณต้นทุนและรายได้
        cost_production = decision['produce'] * engine.PRODUCTION_COST  # ต้นทุนการผลิต
        revenue_production = decision['produce'] * price_today_plus_4  # รายได้จากขาย
        profit_production = revenue_production - cost_production
        
        st.write("**📊 การผลิตแผ่นยางรมควัน:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ต้นทุนการผลิต", f"{cost_production:,.2f} บาท",
                     help=f"{engine.PRODUCTION_COST:.2f} บาท/กก. × {decision['produce']:,.0f} กก.")
        with col2:
            st.metric("รายได้จากขาย", f"{revenue_production:,.2f} บาท",
                     help=f"{price_today_plus_4:.2f} บาท/กก. × {decision['produce']:,.0f} กก.")
        with col3:
            st.metric("รายได้สุทธิ", f"{profit_production:,.2f} บาท",
                     delta=f"{profit_production:,.2f} บาท")
    
    # สำหรับการขายน้ำยางสด
    if decision['dispose'] > 0:
        has_disposal = True
        transport_cost = engine.calculate_fresh_latex_sale_cost(decision['dispose'])
        fresh_revenue = decision['dispose'] * price_today_fresh
        profit_fresh_sale = fresh_revenue - transport_cost
        
        st.write("**🚚 การขายน้ำยางสดทิ้ง:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ค่าขนส่ง", f"{transport_cost:,.2f} บาท")
        with col2:
            st.metric("รายได้จากขาย", f"{fresh_revenue:,.2f} บาท")
        with col3:
            st.metric("รายได้สุทธิ", f"{profit_fresh_sale:,.2f} บาท",
                     delta=f"{profit_fresh_sale:,.2f} บาท")
    
    # เปรียบเทียบทางเลือกสำหรับน้ำยางส่วนเกิน (60,000-80,000 กก.)
    if decision['produce'] > 0 and price_today_plus_4 and (R_today + current_stock) > production_capacity and (R_today + current_stock) < 80000:
        st.markdown("---")
        st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <h2>📊 การเปรียบเทียบ: น้ำยางส่วนเกิน</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # คำนวณน้ำยางส่วนเกิน (นับรวม stock เดิม)
        total_latex = R_today + current_stock
        excess_amount = total_latex - production_capacity
        
        st.write(f"**🔍 วิเคราะห์สำหรับน้ำยางส่วนเกิน {excess_amount:,.0f} กก.**")
        st.write("")
        
        # ===== ทางเลือกที่ 1: เก็บไว้ผลิตในวันถัดไป =====
        if price_today_plus_5:
            # รายได้
            hold_revenue = excess_amount * price_today_plus_5
            
            # ค่าใช้จ่ายเพิ่มเติม (ไม่นับต้นทุนน้ำยาง)
            hold_storage_cost = excess_amount * engine.calculate_storage_cost(1)
            hold_production_cost = excess_amount * engine.PRODUCTION_COST
            hold_additional_cost = hold_storage_cost + hold_production_cost
            
            # กำไรสุทธิ = รายได้ - ค่าใช้จ่ายเพิ่มเติม
            hold_profit = hold_revenue - hold_additional_cost
            hold_profit_per_kg = hold_profit / excess_amount
        
        # ===== ทางเลือกที่ 2: ขายน้ำยางสดทันที =====
        # รายได้
        sell_revenue = excess_amount * price_today_fresh
        
        # ค่าใช้จ่ายเพิ่มเติม (เฉพาะค่าขนส่ง)
        sell_transport_cost = engine.calculate_fresh_latex_sale_cost(excess_amount)
        
        # กำไรสุทธิ = รายได้ - ค่าขนส่ง
        sell_profit = sell_revenue - sell_transport_cost
        sell_profit_per_kg = sell_profit / excess_amount
        
        # แสดงการเปรียบเทียบแบบ Side-by-Side
        if price_today_plus_5:
            col_left, col_right = st.columns(2, gap="large")
            
            with col_left:
                st.markdown("### 💾 ทางเลือกที่ 1: เก็บไว้ผลิตในวันถัดไป")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; 
                            padding: 1.5rem; 
                            border-radius: 15px;
                            margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0 0 1rem 0;'>💰 กำไรรวม</h3>
                    <h1 style='color: white; margin: 0; font-size: 2.5rem;'>{hold_profit:,.2f} บาท</h1>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>({hold_profit_per_kg:.2f} บาท/กก.)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**📝 รายละเอียด:**")
                st.write(f"- ปริมาณ: {excess_amount:,.0f} กก.")
                st.write(f"- ราคาขาย: {price_today_plus_5:.2f} บาท/กก.")
                st.write(f"- รายได้รวม: {hold_revenue:,.2f} บาท")
                st.write("")
                st.write("**💸 ค่าใช้จ่ายเพิ่มเติม:**")
                st.write(f"- ค่าเก็บรักษา 1 วัน: {hold_storage_cost:,.2f} บาท")
                st.write(f"  ({engine.calculate_storage_cost(1):.2f} บาท/กก.)")
                st.write(f"- ต้นทุนการผลิต: {hold_production_cost:,.2f} บาท")
                st.write(f"  ({engine.PRODUCTION_COST:.2f} บาท/กก.)")
                st.write(f"- **รวมค่าใช้จ่าย: {hold_additional_cost:,.2f} บาท**")
                st.write("")
                st.write(f"**🎯 สูตร:** {hold_revenue:,.2f} (รายได้) - {hold_additional_cost:,.2f} (ค่าใช้จ่าย) = **{hold_profit:,.2f} บาท**")
            
            with col_right:
                st.markdown("### 🚚 ทางเลือกที่ 2: ขายน้ำยางสดทันที")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            color: white; 
                            padding: 1.5rem; 
                            border-radius: 15px;
                            margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0 0 1rem 0;'>💰 กำไรรวม</h3>
                    <h1 style='color: white; margin: 0; font-size: 2.5rem;'>{sell_profit:,.2f} บาท</h1>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>({sell_profit_per_kg:.2f} บาท/กก.)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**📝 รายละเอียด:**")
                st.write(f"- ปริมาณ: {excess_amount:,.0f} กก.")
                st.write(f"- ราคาขาย: {price_today_fresh:.2f} บาท/กก.")
                st.write(f"- รายได้รวม: {sell_revenue:,.2f} บาท")
                st.write("")
                st.write("**💸 ค่าใช้จ่ายเพิ่มเติม:**")
                st.write(f"- ค่าขนส่ง: {sell_transport_cost:,.2f} บาท")
                transport_per_kg = sell_transport_cost / excess_amount
                st.write(f"  ({transport_per_kg:.2f} บาท/กก.)")
                st.write(f"- **รวมค่าใช้จ่าย: {sell_transport_cost:,.2f} บาท**")
                st.write("")
                st.write(f"**🎯 สูตร:** {sell_revenue:,.2f} (รายได้) - {sell_transport_cost:,.2f} (ค่าขนส่ง) = **{sell_profit:,.2f} บาท**")
            
            # สรุปผลเปรียบเทียบ
            st.markdown("---")
            profit_diff = hold_profit - sell_profit
            profit_diff_per_kg = hold_profit_per_kg - sell_profit_per_kg
            
            if profit_diff > 0:
                st.success(f"""
                ### ✅ **ผลสรุป: เก็บไว้ผลิตคุ้มค่ากว่า!**
                
                - 💰 **ได้กำไรมากกว่า: {profit_diff:,.2f} บาท** ({profit_diff_per_kg:+.2f} บาท/กก.)
                - 📈 เพิ่มกำไร **{(profit_diff/sell_profit*100):.1f}%** เมื่อเทียบกับการขายสด
                - 🎯 คำแนะนำ: **ควรเก็บไว้ผลิต** เพื่อกำไรสูงสุด
                """)
            elif profit_diff < 0:
                st.error(f"""
                ### ⚠️ **ผลสรุป: ขายน้ำยางสดคุ้มค่ากว่า!**
                
                - 💸 **เสียโอกาสกำไร: {abs(profit_diff):,.2f} บาท** ({profit_diff_per_kg:.2f} บาท/กก.)
                - 📉 ขาดทุนกว่า **{abs(profit_diff/hold_profit*100):.1f}%** หากเก็บไว้ผลิต
                - 🎯 คำแนะนำ: **ควรขายน้ำยางสดทิ้ง** เพื่อกำไรสูงสุด
                - ⚡ ราคาคุ้มทุน: {engine.calculate_breakeven_price(price_today_fresh, 1):.2f} บาท/กก. (ราคาวันที่ +5: {price_today_plus_5:.2f} บาท/กก.)
                """)
            else:
                st.info("""
                ### ℹ️ **ผลสรุป: กำไรเท่ากัน**
                
                - 💰 ทั้ง 2 ทางเลือกให้กำไรเท่ากัน
                - 🎯 คำแนะนำ: เลือกได้ตามความสะดวก
                """)
            
            # แสดงตารางเปรียบเทียบ
            st.markdown("### 📋 ตารางเปรียบเทียบรายละเอียด")
            comparison_data = {
                "รายการ": [
                    "ปริมาณ (กก.)",
                    "ราคาขาย (บาท/กก.)",
                    "รายได้รวม (บาท)",
                    "ค่าใช้จ่ายเพิ่มเติม (บาท)",
                    "กำไรสุทธิ (บาท)",
                    "กำไร/กก. (บาท)"
                ],
                "เก็บไว้ผลิต 💾": [
                    f"{excess_amount:,.0f}",
                    f"{price_today_plus_5:,.2f}",
                    f"{hold_revenue:,.2f}",
                    f"{hold_additional_cost:,.2f}",
                    f"{hold_profit:,.2f}",
                    f"{hold_profit_per_kg:.2f}"
                ],
                "ขายสดทันที 🚚": [
                    f"{excess_amount:,.0f}",
                    f"{price_today_fresh:,.2f}",
                    f"{sell_revenue:,.2f}",
                    f"{sell_transport_cost:,.2f}",
                    f"{sell_profit:,.2f}",
                    f"{sell_profit_per_kg:.2f}"
                ],
                "ส่วนต่าง": [
                    "-",
                    f"{price_today_plus_5 - price_today_fresh:+.2f}",
                    f"{hold_revenue - sell_revenue:+,.2f}",
                    f"{hold_additional_cost - sell_transport_cost:+,.2f}",
                    f"{profit_diff:+,.2f}",
                    f"{profit_diff_per_kg:+.2f}"
                ]
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        else:
            # ถ้าไม่มีราคา day+5 แสดงแค่การขายทิ้ง
            st.warning("⚠️ ไม่สามารถเปรียบเทียบได้ เนื่องจากไม่ทราบราคาแผ่นยางวันที่ +5")
            st.write(f"**กำไรจากการขายสดทันที:** {sell_profit:,.2f} บาท ({sell_profit_per_kg:.2f} บาท/กก.)")
    
    # ถ้ามีการเก็บ stock
    if decision['stock_old'] > 0 or decision['stock_new'] > 0:
        st.markdown("---")
        st.write("**ค่าเก็บรักษา Stock:**")
        
        # ค่าเก็บรักษา stock เดิม (นับต่อจากวันที่เคยเก็บ)
        if decision['stock_old'] > 0:
            st.write(f"- Stock เดิม {decision['stock_old']:,.0f} กก.: ต้องเพิ่มค่าเก็บรักษาต่อไปอีก {engine.STORAGE_COST_DAY2_10} บาท/กก./วัน")
        
        # ค่าเก็บรักษา stock ใหม่
        if decision['stock_new'] > 0:
            storage_cost_day1 = decision['stock_new'] * engine.STORAGE_COST_DAY1
            st.write(f"- Stock ใหม่ {decision['stock_new']:,.0f} กก.: ค่าเก็บรักษาวันแรก {storage_cost_day1:,.2f} บาท")
            st.write(f"  - ค่าเก็บรักษาวันที่ 2-10: {engine.STORAGE_COST_DAY2_10} บาท/กก./วัน")
        
        # คำนวณจุดคุ้มทุน
        if price_today_plus_5:
            breakeven = engine.calculate_breakeven_price(price_today_fresh, storage_days=1)
            st.write(f"- 📊 ราคาคุ้มทุน (เก็บ 1 วัน): **{breakeven:.2f} บาท/กก.**")
            
            if price_today_plus_5 >= breakeven:
                st.success(f"✅ ราคาวันที่ +5 ({price_today_plus_5:.2f} บาท) สูงกว่าจุดคุ้มทุน → คุ้มค่าที่จะเก็บ")
            else:
                st.warning(f"⚠️ ราคาวันที่ +5 ({price_today_plus_5:.2f} บาท) ต่ำกว่าจุดคุ้มทุน → ไม่คุ้มค่าที่จะเก็บ")