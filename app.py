import streamlit as st
import pandas as pd

# 設定網頁配置
st.set_page_config(page_title="複利的威力", layout="centered")

def calculate_wealth(initial_wan, monthly_deposit, rate, years):
    """
    計算每年的資產變化
    """
    initial_principal = initial_wan * 10000
    months = years * 12
    monthly_rate = rate / 100 / 12
    
    data = []
    
    # 初始狀態 (第0年)
    current_asset = initial_principal
    current_principal = initial_principal
    data.append({
        "年": 0,
        "總投入本金 (單利)": int(current_principal),
        "複利後總資產": int(current_asset)
    })
    
    # 開始逐月計算，但為了圖表簡潔，我們每年紀錄一次數據
    for y in range(1, years + 1):
        for _ in range(12):
            # 複利公式：上個月餘額 * (1+月利率) + 本月投入
            current_asset = current_asset * (1 + monthly_rate) + monthly_deposit
            current_principal += monthly_deposit
            
        data.append({
            "年": y,
            "總投入本金 (單利)": int(current_principal),
            "複利後總資產": int(current_asset)
        })
        
    return pd.DataFrame(data)

# --- 側邊欄輸入區 ---
st.sidebar.header("⚙️ 參數設定")

initial_wan = st.sidebar.number_input(
    "初始本金 (萬)", 
    min_value=0, 
    value=10, 
    step=1,
    help="客戶目前手邊已有的單筆資金"
)

monthly_deposit = st.sidebar.number_input(
    "每月投入金額 (元)", 
    min_value=0, 
    value=5000, 
    step=1000,
    help="客戶計畫每月定期定額存入的金額"
)

rate = st.sidebar.slider(
    "年化報酬率 (%)", 
    min_value=1, 
    max_value=15, 
    value=5,
    format="%d%%"
)

years = st.sidebar.slider(
    "投資年期 (年)", 
    min_value=1, 
    max_value=50, 
    value=20
)

# --- 主畫面 ---
st.title("📈 複利的威力 - 財富增長模擬器")
st.markdown("---")

# 計算數據
df = calculate_wealth(initial_wan, monthly_deposit, rate, years)

# 取得最終數值
final_principal = df.iloc[-1]["總投入本金 (單利)"]
final_asset = df.iloc[-1]["複利後總資產"]
gap = final_asset - final_principal

# 顯示關鍵指標 (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("總投入本金", f"${final_principal:,.0f}")
col2.metric("複利後總資產", f"${final_asset:,.0f}")
col3.metric("時間創造的財富", f"${gap:,.0f}", delta="額外獲利", delta_color="normal")

st.markdown("### 📊 資產增長趨勢圖")

# 繪製圖表
# Streamlit 的 line_chart 會自動根據 column 分不同顏色
st.line_chart(
    df.set_index("年")[["總投入本金 (單利)", "複利後總資產"]],
    color=["#FF4B4B", "#00CC96"]  # 設定顏色：本金(紅/警示)，資產(綠/獲利)
)

# --- AI 銷售金句區 ---
st.markdown("---")
st.subheader("💡 AI 財富洞察")

# 動態生成金句
if gap > 0:
    st.info(f"👉 **看見了嗎？除了你自己存的錢，時間額外送了你 {gap:,.0f} 元的禮物！這就是「複利」幫你工作的結果。**")
elif gap == 0:
    st.warning("👉 目前還沒有產生複利效應，試著增加投入金額或時間看看？")
else:
    st.error("👉 參數設定可能有誤，資產不應低於本金。")

# 頁尾
st.markdown(
    """
    <style>
    .small-font {
        font-size:12px;
        color: gray;
        text-align: center;
    }
    </style>
    <div class="small-font">此模擬僅供參考，實際報酬視市場狀況而定。</div>
    """, 
    unsafe_allow_html=True
)
