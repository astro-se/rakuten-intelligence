import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# --- 1. ページ設定とデザイン (HTMLのCSSを移植) ---
st.set_page_config(page_title="Rakuten Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0f; color: #e8e8f0; }
    .stMetric { background-color: #1a1a2e; border: 1px solid #ff4d4d; border-radius: 10px; padding: 20px; }
    h1, h2, h3 { font-family: 'Syne', sans-serif; color: #ff4d4d; text-shadow: 0 0 10px rgba(255,77,77,0.3); }
    .stButton>button { background: linear-gradient(135deg, #ff4d4d, #ff8c00); color: white; border: none; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 楽天API 連携関数 ---
def fetch_rakuten_data(keyword):
    try:
        # Secretsから取得できているかチェック
        app_id = st.secrets["RAKUTEN_APP_ID"]
    except Exception as e:
        st.error(f"Secretsエラー: {e}")
        return pd.DataFrame()

    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
    params = {
        "applicationId": app_id,
        "keyword": keyword,
        "format": "json",
        "hits": 10,  # 最初は少なめでテスト
        "sort": "standard", # 並び替えを標準に戻す
    }
    
    response = requests.get(url, params=params)
    res = response.json()
    
    # 💡 ここが重要：エラーが出ている場合、その内容を画面に出す
    if "error" in res:
        st.error(f"楽天APIエラー: {res['error_description']}")
        return pd.DataFrame()
    
    # 中身があるか確認
    items = []
    if "Items" in res:
        for i in res["Items"]:
            item = i["Item"]
            items.append({
                "商品名": item["itemName"][:50],
                "価格": item["itemPrice"],
                "店舗名": item["shopName"]
            })
    return pd.DataFrame(items)

# --- 3. メイン画面の構成 ---
st.title("⚡ RAKUTEN INTELLIGENCE SYSTEM")
st.subheader("楽天市場 リアルタイム市場分析・プライシング")

# サイドバーで操作
with st.sidebar:
    st.header("⚙️ 設定")
    target_keyword = st.text_input("分析キーワード", value="不織布 収納")
    analyze_btn = st.button("市場データを取得・分析")

if analyze_btn:
    with st.spinner("楽天APIからデータを取得中..."):
        df = fetch_rakuten_data(target_keyword)
        
    if not df.empty:
        # 指標の表示
        col1, col2, col3 = st.columns(3)
        avg_price = int(df["価格"].mean())
        min_price = int(df["価格"].min())
        col1.metric("市場平均価格", f"¥{avg_price:,}")
        col2.metric("最安値", f"¥{min_price:,}")
        col3.metric("競合数", f"{len(df)}店舗")

        # グラフ表示 (BI要素)
        st.markdown("### 📈 価格分布アナリティクス")
        fig = px.bar(df, x="商品名", y="価格", color="価格", color_continuous_scale="Reds")
        fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        # プライシング推薦
        st.markdown("### 🎯 AI変数アクション推薦")
        suggested_price = int(min_price * 0.99)
        st.info(f"💡 【推奨アクション】競合最安値を下回る **¥{suggested_price:,}** への価格調整、またはポイント倍率の+2%設定を推奨します。")
        
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("データが見つかりませんでした。キーワードを変えてみてください。")

st.markdown("---")
st.caption("Supported by Rakuten Developers")
