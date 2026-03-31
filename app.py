import streamlit as st
import pandas as pd
import requests

# --- ページ設定 ---
st.set_page_config(page_title="Rakuten Intelligence", layout="wide")

def fetch_rakuten_data(keyword):
    # Secretsから画面上のIDとキーを取得
    # ID: 1d63949f-... / Secret: pk_VDqp...
    app_id = st.secrets["RAKUTEN_APP_ID"]
    app_secret = st.secrets["RAKUTEN_APPLICATION_SECRET"]

    # エンドポイントの確認（通常の商品検索API）
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
    
    # 💡 重要なポイント：
    # 楽天の新しいUIで発行されたIDを使う場合、
    # 'applicationId' だけでなく 'application_id' や 
    # ヘッダーでの認証が必要なケースがありますが、まずは以下の標準形式で試します。
    params = {
        "applicationId": app_id,
        "applicationSecret": app_secret,
        "keyword": keyword,
        "format": "json",
        "hits": 20,
    }
    
    try:
        response = requests.get(url, params=params)
        res = response.json()
        
        # エラー詳細の表示
        if "error" in res:
            st.error(f"詳細エラー: {res.get('error_description', res['error'])}")
            # デバッグ用：送っているIDの先頭を表示
            st.write(f"送信中ID: {app_id[:5]}...") 
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
        st.error(f"接続エラー: {e}")
        return pd.DataFrame()

# --- UI ---
st.title("⚡ RAKUTEN INTELLIGENCE")

with st.sidebar:
    target_keyword = st.text_input("キーワード", value="バッグ")
    run_btn = st.button("分析実行")

if run_btn:
    df = fetch_rakuten_data(target_keyword)
    if not df.empty:
        st.success(f"{len(df)}件のデータを取得しました")
        st.dataframe(df)
