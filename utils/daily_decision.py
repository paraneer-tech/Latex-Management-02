"""
Logic สำหรับการตัดสินใจผลิตยางรายวัน
"""

class LatexDecisionEngine:
    def __init__(self):
        # ค่าคงที่
        self.PRODUCTION_CAPACITY = 60000  # กก./วัน
        self.MAX_STOCK = 20000  # กก.
        self.MAX_STORAGE_DAYS = 10  # วัน
        self.PRODUCTION_COST = 5  # บาท/กก.
        self.PRODUCTION_DAYS = 4  # วัน
        self.STORAGE_COST_DAY1 = 0.28  # บาท/กก.
        self.STORAGE_COST_DAY2_10 = 0.14  # บาท/กก./วัน
        self.TRANSPORT_COST_PER_20K = 17000  # บาท
        
    def calculate_storage_cost(self, days):
        """คำนวณค่าเก็บรักษารวม (บาท/กก.)"""
        if days < 1:
            return 0
        if days == 1:
            return self.STORAGE_COST_DAY1
        else:
            return self.STORAGE_COST_DAY1 + (days - 1) * self.STORAGE_COST_DAY2_10
    
    def calculate_fresh_latex_sale_cost(self, amount_kg):
        """คำนวณต้นทุนการขายน้ำยางสด (ค่าขนส่ง)"""
        trips = amount_kg / 20000
        return trips * self.TRANSPORT_COST_PER_20K
    
    def calculate_breakeven_price(self, price_today_fresh, storage_days=0):
        """
        คำนวณราคาคุ้มทุนในการผลิต
        
        ถ้าราคาขายแผ่นยางรมควันในอนาคต >= ราคานี้ ควรผลิต
        ถ้าราคาขายแผ่นยางรมควันในอนาคต < ราคานี้ ควรขายน้ำยางสดทิ้ง
        
        Parameters:
        - price_today_fresh: ราคาน้ำยางสดวันนี้ (บาท/กก.)
        - storage_days: จำนวนวันที่ต้องเก็บก่อนผลิต (0 ถ้าผลิตทันที)
        
        Returns:
        - ราคาคุ้มทุน (บาท/กก. ยางแห้ง)
        
        สูตร:
        ราคาคุ้มทุน = กำไรจากขายน้ำยางสด + ต้นทุนเพิ่มเติมจากการผลิต
                   = (ราคาน้ำยางสด - ค่าขนส่ง) + (ค่าเก็บรักษา + ต้นทุนการผลิต)
        """
        # กำไรสุทธิจากขายน้ำยางสด (= ค่าเสียโอกาส)
        transport_cost_per_kg = self.TRANSPORT_COST_PER_20K / 20000
        fresh_sale_profit = price_today_fresh - transport_cost_per_kg
        
        # ต้นทุนเพิ่มเติมจากการผลิต (ไม่นับต้นทุนน้ำยาง)
        storage_cost = self.calculate_storage_cost(storage_days)
        additional_production_cost = storage_cost + self.PRODUCTION_COST
        
        # ราคาคุ้มทุน
        breakeven = fresh_sale_profit + additional_production_cost
        
        return breakeven
    
    def daily_decision(self, R_today, current_stock, price_today_fresh, 
                       price_today_plus_4=None, price_today_plus_5=None):
        """
        ตัดสินใจรายวันว่าจะทำอย่างไรกับน้ำยางที่เข้ามา
        
        Parameters:
        - R_today: น้ำยางที่เข้ามาวันนี้ (กก.)
        - current_stock: น้ำยางใน stock ปัจจุบัน (กก.)
        - price_today_fresh: ราคาน้ำยางสดวันนี้ (บาท/กก.)
        - price_today_plus_4: ราคาแผ่นยางรมควันในวันที่ +4 (ถ้ารู้)
        - price_today_plus_5: ราคาแผ่นยางรมควันในวันที่ +5 (ถ้ารู้)
        
        Returns:
        - dict ที่มี: produce (กก.), hold (กก.), dispose (กก.), reason (เหตุผล),
                      stock_old (stock เดิม), stock_new (stock ใหม่ที่เก็บวันนี้)
        """
        result = {
            'produce': 0,
            'hold': 0,
            'dispose': 0,
            'stock_old': current_stock,  # stock เดิมที่มีอยู่แล้ว
            'stock_new': 0,  # stock ใหม่ที่เก็บจากน้ำยางวันนี้
            'reason': ''
        }
        
        # น้ำยางสดที่เข้ามาวันนี้
        available_fresh = R_today
        
        # คำนวณน้ำยางรวมทั้งหมด
        total_latex = available_fresh + current_stock
        
        # กรณีที่ 1: น้ำยางรวม <= 60,000 กก. -> ผลิตหมดเลย
        if total_latex <= self.PRODUCTION_CAPACITY:
            result['produce'] = total_latex
            result['stock_old'] = 0  # ใช้ stock เดิมหมด
            result['stock_new'] = 0  # ไม่มี stock ใหม่
            result['reason'] = f"น้ำยางรวม {total_latex:,.0f} กก. (Stock เดิม {current_stock:,.0f} + ใหม่ {available_fresh:,.0f}) น้อยกว่าหรือเท่ากับกำลังการผลิต → ผลิตหมด"
            
        # กรณีที่ 2: 60,000 < น้ำยางรวม < 80,000 กก. -> ผลิต 60,000 (ใช้ stock เดิมก่อน)
        elif total_latex < 80000:
            result['produce'] = self.PRODUCTION_CAPACITY
            
            # ใช้ stock เดิมก่อน
            if current_stock >= self.PRODUCTION_CAPACITY:
                # stock เดิมพอผลิต -> ใช้เฉพาะ stock เดิม
                result['stock_old'] = current_stock - self.PRODUCTION_CAPACITY
                result['stock_new'] = available_fresh  # น้ำยางใหม่ทั้งหมดกลายเป็น stock
                result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. (Stock เดิม {current_stock:,.0f} + ใหม่ {available_fresh:,.0f}) → "
                                  f"ผลิต {self.PRODUCTION_CAPACITY:,} กก. จาก Stock เดิม | "
                                  f"Stock คงเหลือ: เดิม {result['stock_old']:,.0f} + ใหม่ {result['stock_new']:,.0f} = {result['stock_old'] + result['stock_new']:,.0f} กก.")
            else:
                # stock เดิมไม่พอ -> ใช้ stock เดิมหมด + น้ำยางใหม่
                result['stock_old'] = 0  # ใช้ stock เดิมหมด
                used_fresh = self.PRODUCTION_CAPACITY - current_stock  # น้ำยางใหม่ที่ใช้ผลิต
                remaining_fresh = available_fresh - used_fresh  # น้ำยางใหม่ที่เหลือ
                
                # ตัดสินใจว่าจะเก็บหรือขายส่วนเกิน
                if price_today_plus_5 is not None and remaining_fresh > 0:
                    # คำนวณจุดคุ้มทุนสำหรับการเก็บ 1 วัน
                    breakeven = self.calculate_breakeven_price(price_today_fresh, storage_days=1)
                    
                    if price_today_plus_5 >= breakeven:
                        # คุ้มค่าเก็บ - ตรวจสอบพื้นที่ว่าง
                        space_available = self.MAX_STOCK
                        can_hold = min(remaining_fresh, space_available)
                        
                        result['stock_new'] = can_hold
                        
                        if remaining_fresh > space_available:
                            result['dispose'] = remaining_fresh - space_available
                            result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. → ผลิต {self.PRODUCTION_CAPACITY:,} กก. "
                                              f"(Stock เดิม {current_stock:,.0f} + ใหม่ {used_fresh:,.0f}) | "
                                              f"ส่วนเกิน {remaining_fresh:,.0f} กก.: ราคาคุ้มทุน → เก็บใหม่ {can_hold:,.0f} กก., "
                                              f"Stock เต็ม ขายทิ้ง {result['dispose']:,.0f} กก.")
                        else:
                            result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. → ผลิต {self.PRODUCTION_CAPACITY:,} กก. "
                                              f"(Stock เดิม {current_stock:,.0f} + ใหม่ {used_fresh:,.0f}) | "
                                              f"ส่วนเกิน {remaining_fresh:,.0f} กก.: ราคาคุ้มทุน ({price_today_plus_5:.2f} >= {breakeven:.2f} บาท) "
                                              f"→ เก็บใหม่ {can_hold:,.0f} กก.")
                    else:
                        # ไม่คุ้มค่า ขายทิ้ง
                        result['dispose'] = remaining_fresh
                        result['stock_new'] = 0
                        result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. → ผลิต {self.PRODUCTION_CAPACITY:,} กก. "
                                          f"(Stock เดิม {current_stock:,.0f} + ใหม่ {used_fresh:,.0f}) | "
                                          f"ส่วนเกิน {remaining_fresh:,.0f} กก.: ราคาไม่คุ้มทุน ({price_today_plus_5:.2f} < {breakeven:.2f} บาท) "
                                          f"→ ขายทิ้ง {result['dispose']:,.0f} กก.")
                else:
                    # ไม่รู้ราคาอนาคต หรือไม่มีส่วนเกิน
                    if remaining_fresh > 0:
                        space_available = self.MAX_STOCK
                        can_hold = min(remaining_fresh, space_available)
                        
                        result['stock_new'] = can_hold
                        
                        if remaining_fresh > space_available:
                            result['dispose'] = remaining_fresh - space_available
                        
                        result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. → ผลิต {self.PRODUCTION_CAPACITY:,} กก. "
                                          f"(Stock เดิม {current_stock:,.0f} + ใหม่ {used_fresh:,.0f}) | "
                                          f"ส่วนเกิน {remaining_fresh:,.0f} กก.: ไม่ทราบราคา → เก็บใหม่ {can_hold:,.0f} กก.")
                        if result['dispose'] > 0:
                            result['reason'] += f", ขายส่วนเกิน {result['dispose']:,.0f} กก."
                    else:
                        result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. (Stock เดิม {current_stock:,.0f} + ใหม่ {available_fresh:,.0f}) → "
                                          f"ผลิต {self.PRODUCTION_CAPACITY:,} กก. (ใช้หมด)")
        
        # กรณีที่ 3: น้ำยางรวม >= 80,000 กก. -> ผลิต 60,000 ขายส่วนเกินทิ้ง
        else:
            result['produce'] = self.PRODUCTION_CAPACITY
            
            # ใช้ stock เดิมก่อน
            if current_stock >= self.PRODUCTION_CAPACITY:
                # stock เดิมพอผลิต
                result['stock_old'] = current_stock - self.PRODUCTION_CAPACITY
                
                # น้ำยางใหม่ทั้งหมดเป็นส่วนเกิน
                space_available = self.MAX_STOCK - result['stock_old']
                can_hold = min(available_fresh, space_available)
                
                result['stock_new'] = can_hold
                result['dispose'] = available_fresh - can_hold
            else:
                # stock เดิมไม่พอ
                result['stock_old'] = 0
                used_fresh = self.PRODUCTION_CAPACITY - current_stock
                remaining_fresh = available_fresh - used_fresh
                
                # ส่วนเกิน
                space_available = self.MAX_STOCK
                can_hold = min(remaining_fresh, space_available)
                
                result['stock_new'] = can_hold
                result['dispose'] = remaining_fresh - can_hold
            
            result['reason'] = (f"น้ำยางรวม {total_latex:,.0f} กก. เกิน 80,000 → "
                              f"ผลิต {self.PRODUCTION_CAPACITY:,} กก.")
            if result['stock_new'] > 0:
                result['reason'] += f", เก็บใหม่ {result['stock_new']:,.0f} กก."
            if result['dispose'] > 0:
                result['reason'] += f", ขายทิ้ง {result['dispose']:,.0f} กก."
        
        return result
    
    def calculate_costs_and_revenue(self, decision, price_today_fresh, 
                                   price_sale_sheet, storage_days=0):
        """
        คำนวณต้นทุนและรายได้จากการตัดสินใจ
        
        Returns:
        - dict ที่มีรายละเอียดทางการเงิน
        """
        costs = {}
        revenue = {}
        
        # ต้นทุนการผลิตแผ่นยาง
        if decision['produce'] > 0:
            storage_cost = self.calculate_storage_cost(storage_days)
            costs['production'] = decision['produce'] * (price_today_fresh + storage_cost + self.PRODUCTION_COST)
            revenue['sheet_sales'] = decision['produce'] * price_sale_sheet
        
        # รายได้จากการขายน้ำยางสด
        if decision['dispose'] > 0:
            transport_cost = self.calculate_fresh_latex_sale_cost(decision['dispose'])
            costs['disposal'] = transport_cost
            revenue['fresh_sales'] = decision['dispose'] * price_today_fresh
        
        # ต้นทุนการเก็บ stock
        if decision['hold'] > 0:
            costs['storage_day1'] = decision['hold'] * self.STORAGE_COST_DAY1
        
        total_cost = sum(costs.values())
        total_revenue = sum(revenue.values())
        profit = total_revenue - total_cost
        
        return {
            'costs': costs,
            'revenue': revenue,
            'total_cost': total_cost,
            'total_revenue': total_revenue,
            'profit': profit
        }