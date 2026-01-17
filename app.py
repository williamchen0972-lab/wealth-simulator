# ==========================================
# 這就是你的「本地端資料庫」
# 你只需要維護這個區塊，把保發中心的 PDF 數據「人工」填進來一次
# ==========================================

MEDICAL_DB = {
    # --- 凱基人壽 (我方) ---
    "KG_A": {
        "company": "凱基人壽",
        "name": "好康泰 (MA)",
        "room_daily": 3000,       # 病房費限額
        "surgery_limit": 200000,  # 住院手術限額
        "misc_limit": 150000,     # 雜費限額
        "outpatient_surgery": True, # 是否賠門診手術
        "outpatient_misc": True,    # 是否賠門診雜費 (關鍵!)
        "note": "✅ 概括式條款，門診手術雜費比照住院額度，業界前段班。"
    },
    
    # --- 競爭對手 ---
    "FB_B": {
        "company": "富x人壽",
        "name": "享安心 (HS)",
        "room_daily": 2000,
        "surgery_limit": 150000,
        "misc_limit": 100000,     # 雜費較低
        "outpatient_surgery": True,
        "outpatient_misc": False,   # ❌ 缺點：條款不賠門診雜費
        "note": "⚠️ 注意：門診手術僅賠「手術費」，不賠「雜費」(如水晶體自費)。"
    },
    "GL_C": {
        "company": "全x人壽",
        "name": "實在醫靠 (XHB)",
        "room_daily": 4000,
        "surgery_limit": 180000,
        "misc_limit": 200000,
        "outpatient_surgery": True,
        "outpatient_misc": True,
        "note": "⚠️ 雖然額度高，但手術費有倍數限制，需對照手術表。"
    }
}

# 之後你的程式只需要呼叫 MEDICAL_DB["KG_A"] 就能拿到所有資料
# 速度是 0.001 秒
