import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 設定網頁配置
st.set_page_config(page_title="保險業務超人工具箱", layout="centered")

# --- CSS 樣式優化 (讓手機版更好看) ---
st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
    .greeting-text {
        font-size: 24px;
        color: #1f77b4;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💼 保險業務超人工具箱")
st.caption("專為台灣保險菁英設計的銷售神器")

# 建立分頁
tab1, tab2 = st.tabs(["⚔️ 保單 PK 擂台", "☀️ 早安名片生成"])

# ==========================================
# 功能 1: 保單 PK 擂台 (解決競品比較痛點)
# ==========================================
with tab1:
    st.header("產品優勢對決")
    st.info("💡 輸入兩張保單的關鍵數據，立刻生成對比圖表，讓客戶一眼看出優勢！")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛡️ 我方產品 (凱基)")
        p1_name = st.text_input("產品名稱 A", value="凱基-美元傳承")
        p1_irr = st.number_input("預估 IRR (%)", value=3.8, key="p1_irr")
        p1_premium = st.number_input("總繳保費 (萬)", value=100, key="p1_prem")
        p1_protection = st.number_input("身故保障 (萬)", value=350, key="p1_prot")
        
    with col2:
        st.subheader("⚔️ 他家產品 (競品)")
        p2_name = st.text_input("產品名稱 B", value="他牌-美元儲蓄")
        p2_irr = st.number_input("預估 IRR (%)", value=3.2, key="p2_irr")
        p2_premium = st.number_input("總繳保費 (萬)", value=100, key="p2_prem")
        p2_protection = st.number_input("身故保障 (萬)", value=300, key="p2_prot")

    # 視覺化按鈕
    if st.button("🚀 生成 PK 分析圖"):
        st.markdown("---")
        
        # 1. 關鍵指標長條圖
        categories = ['預估 IRR (%)', '槓桿倍數 (保障/保費)']
        
        # 計算槓桿
        lev1 = p1_protection / p1_premium if p1_premium > 0 else 0
        lev2 = p2_protection / p2_premium if p2_premium > 0 else 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories,
            y=[p1_irr, lev1],
            name=p1_name,
            marker_color='#FF4B4B'
        ))
        fig.add_trace(go.Bar(
            x=categories,
            y=[p2_irr, lev2],
            name=p2_name,
            marker_color='#cccccc'
        ))
        
        fig.update_layout(
            title="關鍵指標對決",
            barmode='group',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 2. 差異分析結論 (AI 話術)
        diff_irr = p1_irr - p2_irr
        diff_prot = p1_protection - p2_protection
        
        st.success(f"### 🏆 {p1_name} 勝出關鍵：")
        if diff_irr > 0:
            st.write(f"✅ **獲利能力更強：** 長期複利效果高出競品 **{diff_irr:.1f}%**，時間越長差距越大。")
        if diff_prot > 0:
            st.write(f"✅ **保障槓桿更高：** 同樣保費下，我們多送您 **{diff_prot} 萬** 的身故保障。")
        
        st.caption("截圖此畫面即可傳送給客戶")

# ==========================================
# 功能 2: 早安名片生成 (解決刷存在感痛點)
# ==========================================
with tab2:
    st.header("☀️ 專業形象日籤")
    st.info("💡 每天早上 1 分鐘，製作帶有你名字的專業問候圖。")
    
    # 輸入區
    agent_name = st.text_input("你的大名", value="陳奕仲")
    agent_title = st.text_input("職稱/單位", value="凱基人壽 經理")
    phone = st.text_input("聯絡電話", value="0972-799-639")
    
    # 選擇金句
    quotes = [
        "早安！風險無法預測，但愛可以提早準備。",
        "保險不是為了改變生活，而是防止生活被改變。",
        "財富自由不是終點，而是讓你擁有選擇權的起點。",
        "週一加油！堅持做對的事，時間會給你答案。",
        "天氣轉涼，記得多添衣物，保重身體！"
    ]
    selected_quote = st.selectbox("選擇今日金句", quotes)
    
    # 選擇背景風格 (這裡用顏色模擬，進階版可換圖)
    theme_color = st.color_picker("選擇卡片主色調", "#E3F2FD")
    
    st.markdown("---")
    st.subheader("🖼️ 預覽結果 (請手機截圖)")
    
    # 使用 HTML/CSS 模擬一張卡片
    card_html = f"""
    <div style="
        background-color: {theme_color};
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #ddd;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    ">
        <h3 style="color: #555; margin-bottom: 5px;">Good Morning</h3>
        <hr style="border-top: 1px solid #bbb;">
        <p style="font-size: 22px; font-weight: bold; color: #333; margin: 20px 0;">
            “{selected_quote}”
        </p>
        <div style="margin-top: 30px; background-color: white; padding: 15px; border-radius: 10px;">
            <p style="margin:0; font-weight:bold; font-size:18px;">{agent_name}</p>
            <p style="margin:0; font-size:14px; color: #666;">{agent_title}</p>
            <p style="margin:0; font-size:14px; color: #666;">📞 {phone}</p>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    st.caption("👆 手機直接截圖這張卡片，即可發送 LINE")
