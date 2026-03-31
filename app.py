import streamlit as st
import pandas as pd
import requests
import time

# --- ページ設定 ---
st.set_page_config(page_title="Rakuten Intelligence", layout="wide")

# --- 楽天API 接続関数 (Signature認証対応版) ---
def fetch_rakuten_data(keyword):
    # Secretsから「表示されているID」と「キー」を取得
    app_id = st.secrets["RAKUTEN_APP_ID"]
    app_secret = st.secrets["RAKUTEN_APPLICATION_SECRET"]

    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
    
    # ご指摘の通り、IDをapplicationIdとして、
    # もし認証エラーが出る場合は、paramsにapplicationIdとシークレットを直接含めます
    params = {
        "applicationId": app_id,
        "applicationSecret": app_secret, # アクセスキーをここで利用
        "keyword": keyword,
        "format": "json",
        "hits": 20,
    }
    
    try:
        response = requests.get(url, params=params)
        res = response.json()
        
        if "error" in res:
            st.error(f"APIエラーメッセージ: {res.get('error_description', res['error'])}")
            return pd.DataFrame()
            
        items = []
        if "Items" in res:
            for i in res["Items"]:
                item = i["Item"]
                items.append({
                    "商品名": item["itemName"],
                    "価格": item["itemPrice"],
                    "店舗名": item["shopName"]
                })
        return pd.DataFrame(items)
    except Exception as e:
        st.error(f"システムエラー: {e}")
        return pd.DataFrame()

# --- メイン画面 ---
st.title("⚡ RAKUTEN INTELLIGENCE")

with st.sidebar:
    target_keyword = st.text_input("キーワード", value="バッグ")
    run_btn = st.button("分析実行")

if run_btn:
    df = fetch_rakuten_data(target_keyword)
    if not df.empty:
        st.success(f"{len(df)}件のデータを取得しました")
        st.dataframe(df)
