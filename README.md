# Latex-Management-02

โปรแกรมตัดสินใจการผลิตยางที่รวมเครื่องมือช่วยจัดการเอกสารและอินเตอร์เฟซผ่าน Streamlit

สรุป
-**จุดประสงค์:** เพื่อพัฒนาระบบช่วยตัดสินใจในการบริหารจัดการน้ำยางสดของสหกรณ์แปรรูปยางแผ่นรมควันภายใต้ข้อจำกัดด้านกำลังการผลิตและการเก็บรักษา
- **เทคโนโลยีหลัก:** Python, Streamlit

คุณสมบัติเด่น
- เปิดใช้งานผ่าน `streamlit_app.py` เพื่อรัน UI อย่างรวดเร็ว
- มีโมดูลช่วยประมวลผลและตัดสินใจรายวันใน `utils/daily_decision.py`

ข้อกำหนด (Requirements)
- ติดตั้งแพ็กเกจจากไฟล์ `requirments.txt`

การติดตั้งและรัน
1. สร้าง virtual environment
	- Windows PowerShell:
	  ```powershell
	  python -m venv .venv
	  .\.venv\Scripts\Activate.ps1
	  ```
2. ติดตั้ง dependencies
	```powershell
	pip install -r requirments.txt
	```
3. รันแอป Streamlit
	```powershell
	streamlit run streamlit_app.py
	```

โครงสร้างโปรเจกต์
- `streamlit_app.py` : entry point ของเว็บแอป
- `utils/` : ฟังก์ชันช่วยเหลือต่าง ๆ เช่น `daily_decision.py`
- `requirments.txt` : รายการไลบรารีที่ต้องติดตั้ง

