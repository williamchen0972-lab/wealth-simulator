import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 設定網頁配置
st.set_page_config(page_title="家族傳承稅務沙盤", layout="wide")

# --- CSS 優化 (打造私人銀行尊榮感) ---
st.markdown("""
    <style>
    .stApp { background-color: #f5f7fa; }
    .header-style { font-size:26px; font-weight:bold; color:#1a3c5e; margin-bottom:15px; border-bottom: 2px solid #bfa05b; padding-bottom:10px;}
    .gold-card { 
        background-color: #fff; 
        padding: 25px; 
        border-radius: 8px; 
        border-left: 6px solid #bfa05b; /* 金色邊框代表財富 */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .tax-alert { color: #d62728; font-weight: bold; font-size: 20px; }
    .highlight-val { color: #1a3c5e; font-weight: bold; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ 家族財富傳承沙盤 (HNW Edition)")
st.caption("專為高資產客戶設計：遺產稅試算與預留稅源規劃")

# ==========================================
# 1. 側邊欄：資產盤點 (KYC)
# ==========================================
with st.sidebar:
    st.header("1. 客戶資產盤點")
    st.info("請輸入客戶目前的資產結構（以市價或公告現值估算）")
    
    asset_real_estate = st.number_input("🏠 不動產 (公告現值總額)", value=8000, step=100, help="請輸入房屋評定現值+土地公告現值")
    asset_cash = st.number_input("💰 現金/存款", value=2000, step=100)
    asset_stock = st.number_input("📈 股票/基金/投資", value=3000, step=100)
    asset_other = st.number_input("💎 其他 (珠寶/債權)", value=500, step=100)
    
    # 計算總資產
    total_assets = asset_real_estate + asset_cash + asset_stock + asset_other
    st.metric("總資產評估", f"${total_assets:,} 萬")
    
    st.markdown("---")
    st.header("2. 家庭結構 (扣除額)")
    has_spouse = st.checkbox("配偶健在?", value=True)
    num_children = st.number_input("子女繼承人數", value=2, min_value=0)
    
    st.markdown("---")
    st.header("3. 傳承方案規劃")
    insurance_plan = st.number_input("規劃壽險保額 (預留稅源)", value=1000, step=100, help="建議輸入預估的遺產稅額")

# ==========================================
# 2. 核心運算邏輯 (依據台灣遺產稅法)
# ==========================================
def calculate_estate_tax(total_assets, has_spouse, num_children):
    # 免稅額 (2024年標準：1333萬)
    exemption = 1333
    
    # 扣除額
    deduction_spouse = 553 if has_spouse else 0
    deduction_children = 56 * num_children
    deduction_funeral = 138 # 喪葬費
    total_deduction = deduction_spouse + deduction_children + deduction_funeral
    
    # 遺產淨額
    net_estate = total_assets - exemption - total_deduction
    
    # 計算稅額 (累進稅率)
    # 0-5000萬: 10%
    # 5000萬-1億: 15% - 250萬
    # 1億以上: 20% - 750萬
    
    if net_estate <= 0:
        tax = 0
        rate = 0
    elif net_estate <= 5000:
        tax = net_estate * 0.10
        rate = 10
    elif net_estate <= 10000:
        tax = net_estate * 0.15 - 250
        rate = 15
    else:
        tax = net_estate * 0.20 - 750
        rate = 20
        
    return {
        "net_estate": max(0, net_estate),
        "tax": max(0, tax),
        "rate": rate,
        "total_deduction": total_deduction + exemption
    }

result = calculate_estate_tax(total_assets, has_spouse, num_children)
tax_bill = result["tax"]
cash_gap = tax_bill - asset_cash # 現金缺口 (若現金不足以繳稅)

# ==========================================
# 3. 主畫面展示
# ==========================================

# --- 區塊 A: 現況風險分析 ---
st.markdown('<div class="header-style">🧐 現況風險診斷</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("遺產淨額 (扣除免稅額後)", f"${result['net_estate']:,} 萬")
col2.metric("適用最高稅率", f"{result['rate']}%")
col3.metric("預估應繳遺產稅", f"${tax_bill:,.0f} 萬", delta_color="inverse", delta="資產縮水")

# 現金流動性危機警示
if cash_gap > 0:
    st.error(f"⚠️ **流動性危機警告**：您的現金僅有 {asset_cash} 萬，不足以支付 {tax_bill:,.0f} 萬的稅金！繼承人可能面臨「無法繼承」或「被迫變賣房產/股票」的困境，缺口達 **${cash_gap:,.0f} 萬**。")
else:
    st.success(f"✅ 流動性安全：現有現金足以支付遺產稅。但現金資產將會減少 {tax_bill:,.0f} 萬。")

# --- 區塊 B: 視覺化圖表 ---
st.markdown("---")
col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    st.markdown('<div class="header-style">📊 資產傳承分配模擬</div>', unsafe_allow_html=True)
    
    # 繪製瀑布圖 (Waterfall Chart) 顯示資產如何被稅吃掉
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "total", "relative", "total"],
        x = ["總資產", "免稅扣除額", "遺產淨額", "應繳稅金 (流失)", "實際繼承金額"],
        textposition = "outside",
        text = [f"{total_assets}", f"-{result['total_deduction']}", f"{result['net_estate']}", f"-{tax_bill:.0f}", f"{total_assets - tax_bill:.0f}"],
        y = [total_assets, -result['total_deduction'], 0, -tax_bill, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#d62728"}}, # 紅色代表減少
        increasing = {"marker":{"color":"#2ca02c"}}, 
        totals = {"marker":{"color":"#1f77b4"}}
    ))
    fig.update_layout(title = "資產傳承流失圖", showlegend = False, height=400)
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.markdown('<div class="header-style">🍰 資產結構</div>', unsafe_allow_html=True)
    # 圓餅圖
    labels = ['不動產', '現金', '股票', '其他']
    values = [asset_real_estate, asset_cash, asset_stock, asset_other]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 針對不動產佔比高的警語
    real_estate_ratio = asset_real_estate / total_assets
    if real_estate_ratio > 0.5:
        st.warning("🏠 **不動產佔比過高**：遺產稅必須用「現金」繳納，房產變現不易，是稅務規劃的重災區。")

# --- 區塊 C: 保險解決方案 (預留稅源) ---
st.markdown('<div class="header-style">🛡️ 凱基傳承方案：預留稅源效應</div>', unsafe_allow_html=True)

with st.container():
    st.markdown(f"""
    <div class="gold-card">
        <h4>💡 規劃策略：指定受益人壽險 ${insurance_plan:,} 萬</h4>
        <p>透過保險規劃，將應稅資產轉化為免稅(或低稅)的身故保險金，直接提供子女繳稅現金。</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    # 方案前
    heir_get_before = total_assets - tax_bill
    c1.metric("未規劃前：實際繼承", f"${heir_get_before:,.0f} 萬", "資產縮水")
    
    # 方案後 (假設保險金不計入遺產總額，這在實務上需符合實質課稅原則，此處為簡易MVP)
    # 繼承 = 原資產 - 稅 + 保險金
    heir_get_after = heir_get_before + insurance_plan
    delta = heir_get_after - heir_get_before
    
    c2.metric("規劃後：實際繼承", f"${heir_get_after:,.0f} 萬", delta=f"多傳承 {delta:,.0f} 萬")
    
    # 槓桿效應 (簡單估算保費，假設槓桿 3 倍)
    estimated_premium = insurance_plan / 3 
    c3.metric("預估保費成本 (概算)", f"${estimated_premium:,.0f} 萬", help="假設保單槓桿約 3 倍 (視年齡體況而定)")

    st.info(f"🔑 **關鍵價值**：這一筆 {insurance_plan} 萬的保險金，不僅填補了 {tax_bill:.0f} 萬的稅金缺口，更讓子女不需要變賣 {asset_real_estate} 萬的房產，實現「資產無損傳承」。")
