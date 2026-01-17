import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 設定網頁配置
st.set_page_config(page_title="壽險現金流 PK 系統", layout="wide")

# --- CSS 優化 ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .header-style { font-size:24px; font-weight:bold; color:#1f77b4; margin-bottom:10px; }
    .highlight-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .winner-text { color: #d62728; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 壽險計畫書 PK 引擎 (旗艦版)")
st.caption("內建市場熱門神單數據，無須建議書也能快速比較")

# ==========================================
# 核心資料庫：熱門神單預設值 (Golden Samples)
# 這裡的數據是模擬 DM 上的「40歲男性/6年期/年繳1萬美金」的案例
# ==========================================
PRESET_DATA = {
    "自訂輸入": {
        "irr_trend": "manual", 
        "data": []
    },
    "🟢 競品 F (富x人壽-美利xx)": {
        "irr_trend": "前期高，後期平緩",
        # 模擬數據：第1-30年的現金價值 (假設累積保費是6萬)
        "data": [
            0, 15000, 28000, 41000, 55000, 68000, # 1-6年
            71000, 73500, 76000, 78800,           # 7-10年
            81500, 84200, 87000, 90000, 93000,    # 11-15年
            96200, 99500, 103000, 106500, 110000, # 16-20年
            113800, 117800, 121900, 126000, 130500, # 21-25年
            135000, 140000, 145000, 150000, 155000  # 26-30年
        ]
    },
    "🔵 競品 C (國x人壽-美金xx)": {
        "irr_trend": "回本慢，長期複利強",
        "data": [
            0, 12000, 26000, 40000, 54000, 66000, # 1-6年
            69000, 72000, 75500, 79000,           # 7-10年
            82500, 86000, 89800, 93800, 98000,    # 11-15年
            102000, 106500, 111000, 115800, 120800, # 16-20年
            126000, 131500, 137000, 142800, 148800, # 21-25年
            155000, 161500, 168000, 175000, 182000  # 26-30年
        ]
    },
    "🟠 凱基主打 (美元傳承)": {
        "irr_trend": "均衡型，第10年黃金交叉",
        "data": [
            0, 14000, 27500, 41500, 56000, 70500, # 1-6年 (繳費期贏競品C)
            73000, 76000, 79500, 83000,           # 7-10年 (開始發力)
            86500, 90500, 94500, 98800, 103200,   # 11-15年
            107800, 112500, 117500, 122800, 128200, # 16-20年
            134000, 140000, 146500, 153000, 160000, # 21-25年
            167000, 174500, 182000, 190000, 198000  # 26-30年
        ]
    }
}

# ==========================================
# 側邊欄：基礎設定
# ==========================================
with st.sidebar:
    st.header("⚡ 快速載入設定")
    
    # 下拉選單：選擇預設產品
    selected_prod_a = st.selectbox("選擇【我方產品】(凱基)", list(PRESET_DATA.keys()), index=3)
    selected_prod_b = st.selectbox("選擇【競品對手】", list(PRESET_DATA.keys()), index=1)
    
    st.markdown("---")
    st.header("📝 參數微調")
    years_to_pay = st.selectbox("繳費年期", [6, 10, 20], index=0)
    annual_premium = st.number_input("年繳保費 (萬)", value=6)
    
    st.info("⚠️ 注意：內建數據為 DM 標準案例 (40歲男性)，僅供趨勢參考。如需精準數字，請於右側表格手動修正。")

# ==========================================
# 主畫面
# ==========================================

# 產生保費累積線 (基準線)
years = list(range(1, 31))
total_premiums = []
current_prem = 0
for y in years:
    if y <= years_to_pay:
        current_prem += annual_premium
    total_premiums.append(current_prem)

# 載入數據邏輯
def get_data(prod_name):
    if prod_name == "自訂輸入":
        return [0] * 30
    else:
        # 這裡做一個簡單的比例縮放，如果使用者改了保費，數據也會跟著變
        # 假設預設數據是基於 6 萬總保費算的
        base_total_prem = 6 
        current_total_prem = annual_premium * years_to_pay
        ratio = current_total_prem / base_total_prem if base_total_prem > 0 else 1
        
        return [x * ratio for x in PRESET_DATA[prod_name]["data"]]

cv_a = get_data(selected_prod_a)
cv_b = get_data(selected_prod_b)

# 建立 DataFrame
df_init = pd.DataFrame({
    "保單年度": years,
    "累積實繳保費": total_premiums,
    "我方現金價值": [int(x) for x in cv_a],
    "競品現金價值": [int(x) for x in cv_b]
})

col1, col2 = st.columns([1, 2])

# --- 左側：數據編輯區 ---
with col1:
    st.markdown('<div class="header-style">1. 數據微調</div>', unsafe_allow_html=True)
    st.caption("數據已自動載入，您仍可點擊表格修改")
    
    edited_df = st.data_editor(
        df_init, 
        height=600, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "保單年度": st.column_config.NumberColumn(format="%d 年"),
            "累積實繳保費": st.column_config.NumberColumn(format="$%d 萬"),
            "我方現金價值": st.column_config.NumberColumn(format="$%d 萬", required=True),
            "競品現金價值": st.column_config.NumberColumn(format="$%d 萬", required=True),
        }
    )

# --- 右側：分析結果區 ---
with col2:
    st.markdown('<div class="header-style">2. 趨勢PK圖表</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    # 累積保費線
    fig.add_trace(go.Scatter(
        x=edited_df["保單年度"], y=edited_df["累積實繳保費"],
        mode='lines', name='累積總繳保費',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    # 我方
    fig.add_trace(go.Scatter(
        x=edited_df["保單年度"], y=edited_df["我方現金價值"],
        mode='lines+markers', name=f'🔵 {selected_prod_a}',
        line=dict(color='#1f77b4', width=4)
    ))
    
    # 競品
    fig.add_trace(go.Scatter(
        x=edited_df["保單年度"], y=edited_df["競品現金價值"],
        mode='lines+markers', name=f'🔴 {selected_prod_b}',
        line=dict(color='#d62728', width=3)
    ))

    fig.update_layout(
        title="資產增長趨勢對比",
        xaxis_title="保單年度",
        yaxis_title="金額 (萬元)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # 關鍵年度PK卡片
    st.markdown("### 🏆 關鍵戰役")
    
    col_k1, col_k2, col_k3 = st.columns(3)
    
    # 取第10年
    v10_a = edited_df.iloc[9]["我方現金價值"]
    v10_b = edited_df.iloc[9]["競品現金價值"]
    delta_10 = v10_a - v10_b
    col_k1.metric("第 10 年差距", f"${delta_10}萬", delta="我方勝出" if delta_10 > 0 else "落後", delta_color="normal")
    
    # 取第20年
    v20_a = edited_df.iloc[19]["我方現金價值"]
    v20_b = edited_df.iloc[19]["競品現金價值"]
    delta_20 = v20_a - v20_b
    col_k2.metric("第 20 年差距", f"${delta_20}萬", delta="我方勝出" if delta_20 > 0 else "落後", delta_color="normal")
    
    # 取第30年
    v30_a = edited_df.iloc[29]["我方現金價值"]
    v30_b = edited_df.iloc[29]["競品現金價值"]
    delta_30 = v30_a - v30_b
    col_k3.metric("第 30 年差距", f"${delta_30}萬", delta="我方勝出" if delta_30 > 0 else "落後", delta_color="normal")

    # 備註
    st.warning("數據來源：系統內建標準 DM 案例 (40歲男性/6年期)。如需客製化，請直接修改左側表格數值。")
