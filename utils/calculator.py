def daily_decision(
    R_today: float,
    price_today_plus_4: float,
    price_today_plus_5: float
) -> dict:
    """
    Decision logic for TODAY only
    """

    C = 60000
    S_MAX = 20000
    PROD_COST = 5
    HOLD_COST_DAY1 = 0.28

    decision = {
        "produce": 0,
        "hold": 0,
        "dispose": 0,
        "reason": ""
    }

    # Case 1
    if R_today < C:
        decision["produce"] = R_today
        decision["reason"] = "น้ำยางน้อยกว่ากำลังผลิต → ผลิตทั้งหมด"

    # Case 2
    elif C <= R_today <= C + S_MAX:
        decision["produce"] = C
        excess = R_today - C

        profit_produce = price_today_plus_4 - PROD_COST
        profit_hold = price_today_plus_5 - PROD_COST - HOLD_COST_DAY1

        if profit_hold > profit_produce:
            decision["hold"] = excess
            decision["reason"] = "เก็บคุ้มกว่าผลิต (ราคาขายอนาคตสูงกว่า)"
        else:
            decision["produce"] += excess
            decision["reason"] = "ผลิตทันทีคุ้มกว่าเก็บ"

    # Case 3
    else:
        decision["produce"] = C
        decision["hold"] = S_MAX
        decision["dispose"] = R_today - C - S_MAX
        decision["reason"] = "น้ำยางเกินกำลังผลิตและ stock → ขายทิ้งส่วนเกิน"

    return decision
