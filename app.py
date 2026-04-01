
import io
import math
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="ASTRO OPS CONSOLE",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# Visual system
# --------------------------------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root{
            --bg:#0b0e13;
            --panel:#131821;
            --panel2:#171d27;
            --panel3:#1b212c;
            --line:#2d3543;
            --line2:#3d4656;
            --text:#eef2f7;
            --muted:#98a2b0;
            --muted2:#b7c0cb;
            --accent:#d7dde5;
            --ok:#d5e1d0;
            --warn:#e0d6b9;
            --bad:#e1c4c4;
        }

        html, body, [class*="css"] {
            font-family: Inter, "SF Pro Display", "Segoe UI", sans-serif;
        }

        .stApp{
            background:
                linear-gradient(180deg, #090c11 0%, #0b0e13 100%);
            color: var(--text);
        }

        .block-container{
            max-width: 1580px;
            padding-top: 0.9rem;
            padding-bottom: 1.8rem;
        }

        section[data-testid="stSidebar"]{display:none !important;}
        header[data-testid="stHeader"]{background:transparent;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .topbar{
            border:1px solid var(--line);
            border-radius: 4px;
            padding: 10px 14px;
            background: linear-gradient(180deg, #141922 0%, #11161d 100%);
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom: 12px;
        }

        .topbar-left{
            display:flex;
            gap:10px;
            align-items:center;
        }

        .topbar-chip{
            border:1px solid var(--line2);
            border-radius:3px;
            padding: 6px 10px;
            font-size: 10px;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--muted2);
            background:#0e1319;
        }

        .hero{
            border:1px solid var(--line);
            border-radius: 4px;
            background: linear-gradient(180deg, #171d27 0%, #0f141b 100%);
            padding: 24px 26px 20px 26px;
            margin-bottom: 14px;
        }

        .hero-grid{
            display:grid;
            grid-template-columns: 1.4fr 0.8fr;
            gap: 18px;
            align-items:start;
        }

        .hero-title{
            font-size: 36px;
            line-height: 1.02;
            font-weight: 850;
            color: white;
            margin: 0 0 10px 0;
            letter-spacing: 0.01em;
        }

        .hero-sub{
            font-size: 14px;
            line-height: 1.78;
            color: var(--muted2);
            max-width: 980px;
        }

        .plate{
            border:1px solid var(--line);
            background:#0e1319;
            border-radius:3px;
            padding: 14px 16px;
        }

        .plate-k{
            font-size:10px;
            color: var(--muted);
            text-transform:uppercase;
            letter-spacing:0.16em;
            margin-bottom:8px;
        }

        .plate-v{
            font-size:13px;
            color:#dce3eb;
            line-height:1.7;
        }

        .control-wrap{
            border:1px solid var(--line);
            border-radius:4px;
            background: linear-gradient(180deg, #121720 0%, #10141b 100%);
            padding: 14px;
            margin-bottom: 14px;
        }

        .section{
            border:1px solid var(--line);
            border-radius: 4px;
            background: linear-gradient(180deg, #141a23 0%, #10151c 100%);
            padding: 14px;
        }

        .section-title{
            font-size: 12px;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #dce2ea;
            font-weight: 800;
            margin-bottom: 12px;
        }

        .metric{
            border:1px solid var(--line);
            border-radius: 3px;
            padding: 14px 14px 12px 14px;
            background:#0f141b;
            min-height:112px;
        }

        .metric-k{
            font-size:10px;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            margin-bottom: 11px;
        }

        .metric-v{
            font-size: 30px;
            line-height: 1;
            font-weight: 850;
            color: white;
            margin-bottom: 8px;
        }

        .metric-f{
            font-size: 12px;
            line-height: 1.55;
            color: var(--muted2);
        }

        .action{
            border:1px solid var(--line);
            border-left: 3px solid #6f7a89;
            border-radius: 3px;
            padding: 13px 13px 12px 13px;
            background:#0e1319;
            min-height: 168px;
        }

        .action-p{
            display:inline-block;
            border:1px solid var(--line2);
            border-radius:3px;
            padding: 5px 8px;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: #d7dde6;
            margin-bottom: 11px;
        }

        .action-t{
            font-size:16px;
            line-height:1.35;
            font-weight:800;
            color:white;
            margin-bottom:8px;
        }

        .action-b{
            font-size:13px;
            line-height:1.68;
            color:var(--muted2);
            margin-bottom:10px;
        }

        .action-n{
            font-size:12px;
            line-height:1.7;
            color:#dfe5ed;
            border-top:1px solid #252d39;
            padding-top:10px;
        }

        .note{
            font-size:12px;
            line-height:1.7;
            color:var(--muted);
        }

        .signal{
            border-bottom:1px solid #262e39;
            padding:10px 0;
        }
        .signal:last-child{border-bottom:none;}

        .signal-k{
            font-size:10px;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:var(--muted);
            margin-bottom:5px;
        }

        .signal-v{
            font-size:18px;
            color:white;
            font-weight:800;
            margin-bottom:4px;
        }

        .signal-f{
            font-size:12px;
            line-height:1.65;
            color:var(--muted2);
        }

        div[data-baseweb="tab-list"]{
            gap: 8px;
            margin-top: 2px;
            margin-bottom: 4px;
        }

        button[data-baseweb="tab"]{
            border-radius:3px;
            border:1px solid var(--line);
            background:#11161d;
            color:#d6dde6;
            padding:10px 14px;
        }

        button[data-baseweb="tab"][aria-selected="true"]{
            background:#171d26;
            border-color:#434d5d;
        }

        .stButton button, .stDownloadButton button{
            border-radius:3px;
            border:1px solid #3b4452;
            background:#171d26;
            color:white;
            font-weight:700;
        }

        div[data-testid="stHorizontalBlock"] > div:has(.stTextInput), 
        div[data-testid="stHorizontalBlock"] > div:has(.stSelectbox),
        div[data-testid="stHorizontalBlock"] > div:has(.stNumberInput),
        div[data-testid="stHorizontalBlock"] > div:has(.stRadio),
        div[data-testid="stHorizontalBlock"] > div:has(.stFileUploader){
            background: transparent;
        }

        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea{
            background:#0f141b !important;
            border:1px solid #313948 !important;
            color:white !important;
            border-radius:3px !important;
        }

        .stRadio [role="radiogroup"]{
            flex-direction: row;
            gap: 8px;
        }

        .stRadio label{
            background:#0f141b;
            border:1px solid #313948;
            padding: 8px 10px;
            border-radius: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def fmt_yen(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"¥{int(round(v)):,}"


def fmt_pct(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"{v*100:.1f}%"


def card_metric(label: str, value: str, foot: str) -> None:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-k">{label}</div>
            <div class="metric-v">{value}</div>
            <div class="metric-f">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_action(priority: str, title: str, body: str, next_step: str) -> None:
    st.markdown(
        f"""
        <div class="action">
            <div class="action-p">{priority}</div>
            <div class="action-t">{title}</div>
            <div class="action-b">{body}</div>
            <div class="action-n"><strong>NEXT</strong> {next_step}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def fetch_public_csv(url: str) -> pd.DataFrame:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return pd.read_csv(io.StringIO(resp.text))


def demo_price_table() -> pd.DataFrame:
    return pd.DataFrame([
        {"sku":"AST-1001","product_name":"収納ケース M","current_price":2480,"cost":1180,"sessions":940,"orders":34,"units":36,"revenue":89280,"gross_profit":46800,"stock":84},
        {"sku":"AST-1002","product_name":"収納ケース L","current_price":2980,"cost":1510,"sessions":880,"orders":27,"units":28,"revenue":83440,"gross_profit":41160,"stock":62},
        {"sku":"AST-2101","product_name":"衣類収納ボックス","current_price":2180,"cost":980,"sessions":1260,"orders":51,"units":54,"revenue":117720,"gross_profit":64800,"stock":107},
        {"sku":"AST-2204","product_name":"布団圧縮収納","current_price":3480,"cost":1810,"sessions":610,"orders":19,"units":19,"revenue":66120,"gross_profit":31730,"stock":33},
        {"sku":"AST-3102","product_name":"キッチンラック","current_price":4280,"cost":2360,"sessions":430,"orders":11,"units":11,"revenue":47080,"gross_profit":21120,"stock":41},
        {"sku":"AST-4105","product_name":"防災トイレセット","current_price":1980,"cost":790,"sessions":1480,"orders":67,"units":74,"revenue":146520,"gross_profit":88060,"stock":210},
    ])


def demo_market_table() -> pd.DataFrame:
    return pd.DataFrame([
        {"sku":"AST-1001","equilibrium_price":2380,"market_low":2280,"market_high":2480,"elasticity_proxy":-0.92,"competition_density":0.84},
        {"sku":"AST-1002","equilibrium_price":2890,"market_low":2780,"market_high":2980,"elasticity_proxy":-0.76,"competition_density":0.72},
        {"sku":"AST-2101","equilibrium_price":2090,"market_low":1980,"market_high":2180,"elasticity_proxy":-1.04,"competition_density":0.89},
        {"sku":"AST-2204","equilibrium_price":3320,"market_low":3180,"market_high":3480,"elasticity_proxy":-0.61,"competition_density":0.58},
        {"sku":"AST-3102","equilibrium_price":4390,"market_low":4180,"market_high":4580,"elasticity_proxy":-0.38,"competition_density":0.49},
        {"sku":"AST-4105","equilibrium_price":2050,"market_low":1980,"market_high":2180,"elasticity_proxy":-1.12,"competition_density":0.93},
    ])


def load_inputs(mode: str, price_csv_url: str, market_csv_url: str, price_upload, market_upload) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if mode == "DEMO":
        return demo_price_table(), demo_market_table()

    fallback_price = demo_price_table()
    fallback_market = demo_market_table()

    if price_upload is not None:
        price_df = pd.read_csv(price_upload)
    elif price_csv_url.strip():
        price_df = fetch_public_csv(price_csv_url.strip())
    else:
        price_df = fallback_price

    if market_upload is not None:
        market_df = pd.read_csv(market_upload)
    elif market_csv_url.strip():
        market_df = fetch_public_csv(market_csv_url.strip())
    else:
        market_df = fallback_market

    return price_df, market_df


def recommend_prices(price_df: pd.DataFrame, market_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.merge(market_df, on="sku", how="left")

    df["cvr"] = np.where(df["sessions"] > 0, df["orders"] / df["sessions"], 0)
    df["margin_per_unit"] = df["current_price"] - df["cost"]
    df["margin_rate"] = np.where(df["current_price"] > 0, df["margin_per_unit"] / df["current_price"], 0)

    market_anchor = (
        df["equilibrium_price"].fillna(df["current_price"]) * 0.64
        + df["market_low"].fillna(df["current_price"]) * 0.08
        + df["market_high"].fillna(df["current_price"]) * 0.08
        + df["current_price"] * 0.20
    )

    elasticity_adj = np.where(
        df["elasticity_proxy"].fillna(-0.5) <= -1.0, -0.04 * df["current_price"],
        np.where(df["elasticity_proxy"].fillna(-0.5) <= -0.7, -0.015 * df["current_price"],
                 np.where(df["elasticity_proxy"].fillna(-0.5) >= -0.4, 0.025 * df["current_price"], 0))
    )

    stock_adj = np.where(
        df["stock"] < 40, 0.04 * df["current_price"],
        np.where(df["stock"] > 120, -0.025 * df["current_price"], 0)
    )

    traffic_adj = np.where(
        (df["sessions"] > df["sessions"].median()) & (df["cvr"] < df["cvr"].median()),
        -0.02 * df["current_price"], 0
    )

    floor_price = df["cost"] / 0.60
    raw = market_anchor + elasticity_adj + stock_adj + traffic_adj
    df["recommended_price"] = np.maximum(raw, floor_price).round(-1)

    df["price_delta"] = df["recommended_price"] - df["current_price"]
    df["price_delta_pct"] = np.where(df["current_price"] > 0, df["price_delta"] / df["current_price"], 0)

    df["recommended_action"] = np.select(
        [
            df["price_delta_pct"] <= -0.03,
            df["price_delta_pct"] >= 0.03,
        ],
        [
            "PRICE_DOWN_TEST",
            "PRICE_UP_TEST",
        ],
        default="HOLD_PRICE",
    )

    df["reason"] = np.select(
        [
            df["recommended_action"] == "PRICE_DOWN_TEST",
            df["recommended_action"] == "PRICE_UP_TEST",
        ],
        [
            "競争密度・価格感応・流入効率の観点から下方向テストが妥当。",
            "粗利と在庫制約の観点から上方向テスト余地あり。",
        ],
        default="価格は概ね妥当。画像・訴求・配送文言の改善を優先。",
    )

    return df


def build_actions(df: pd.DataFrame):
    out = []

    down_df = df.sort_values("price_delta_pct")
    up_df = df.sort_values("price_delta_pct", ascending=False)
    low_stock_df = df.sort_values("stock")

    if not down_df.empty:
        x = down_df.iloc[0]
        out.append({
            "priority":"critical",
            "title":f"{x['sku']} を下方向テスト",
            "body":f"{x['product_name']} は現行 {fmt_yen(x['current_price'])} に対し推薦 {fmt_yen(x['recommended_price'])}。高流入なのに転換が弱く、相場対比でもやや上振れです。",
            "next":"3%刻みで価格テスト。メイン画像と配送文言も同時に差し替え。",
        })

    if not up_df.empty:
        x = up_df.iloc[0]
        out.append({
            "priority":"priority",
            "title":f"{x['sku']} は値上げ余地あり",
            "body":f"{x['product_name']} は現行 {fmt_yen(x['current_price'])}、推薦 {fmt_yen(x['recommended_price'])}。粗利回収を優先しても良い水準です。",
            "next":"+2% から +4% の範囲で段階改定し、CVRの毀損を監視。",
        })

    if not low_stock_df.empty:
        x = low_stock_df.iloc[0]
        out.append({
            "priority":"priority",
            "title":f"{x['sku']} は在庫優先管理",
            "body":f"{x['product_name']} の在庫は {int(x['stock'])}。欠品回避が価格最適化より先です。",
            "next":"補充予定を確認し、必要なら価格を引き上げて需要を平準化。",
        })

    hold_df = df.iloc[(df["price_delta_pct"].abs()).argmin()]
    out.append({
        "priority":"advisory",
        "title":f"{hold_df['sku']} は価格維持でよい",
        "body":f"{hold_df['product_name']} は市場均衡とのズレが小さい商品です。ここは価格より訴求改善が効きます。",
        "next":"価格は触らず、画像・レビュー獲得・送料無料条件を調整。",
    })
    return out[:4]


def kpis(df: pd.DataFrame) -> Dict[str, float]:
    revenue = float(df["revenue"].sum())
    profit = float(df["gross_profit"].sum())
    sessions = float(df["sessions"].sum())
    orders = float(df["orders"].sum())
    cvr = orders / sessions if sessions else 0
    avg_delta = float(df["price_delta_pct"].mean())
    return {
        "revenue": revenue,
        "profit": profit,
        "sessions": sessions,
        "orders": orders,
        "cvr": cvr,
        "avg_delta": avg_delta,
    }


def chart_price_delta(df: pd.DataFrame) -> go.Figure:
    x = df.sort_values("price_delta_pct")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x["sku"],
        y=x["price_delta_pct"] * 100,
        text=[f"{v*100:.1f}%" for v in x["price_delta_pct"]],
        textposition="outside",
        marker_color="#AEB6C0",
        hovertemplate="%{x}<br>%{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title="Recommended Price Delta",
        template="plotly_dark",
        height=320,
        margin=dict(l=20, r=20, t=48, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="SKU",
        yaxis_title="% vs current",
    )
    return fig


def chart_revenue_profit(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue", x=df["sku"], y=df["revenue"], marker_color="#8C96A3"))
    fig.add_trace(go.Bar(name="Gross Profit", x=df["sku"], y=df["gross_profit"], marker_color="#C3CAD4"))
    fig.update_layout(
        barmode="group",
        title="Revenue / Gross Profit",
        template="plotly_dark",
        height=340,
        margin=dict(l=20, r=20, t=48, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


inject_css()

st.markdown(
    """
    <div class="topbar">
        <div class="topbar-left">
            <div class="topbar-chip">ASTRO / OPS CONSOLE</div>
            <div class="topbar-chip">PRICE · TRAFFIC · PROFIT · STOCK</div>
        </div>
        <div class="topbar-left">
            <div class="topbar-chip">RMS 2.0 PROTOTYPE</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-grid">
            <div>
                <div class="hero-title">BIではなく、<br>運用判断のための操作盤。</div>
                <div class="hero-sub">
                    価格均衡、市場感応、客足、粗利、在庫を束ねて、SKUごとに推薦価格と次の操作を返す。
                    目的は可視化ではなく、<strong>毎日触れる運用画面</strong> にすることです。
                </div>
            </div>
            <div class="plate">
                <div class="plate-k">Data ingress doctrine</div>
                <div class="plate-v">
                    公開CSVなら Google API は不要です。<br>
                    非公開のまま読むなら OAuth 2.0 かサービスアカウントが必要です。<br>
                    初期は <strong>Google Sheets をCSV公開</strong> して接続し、後で private 接続へ移るのが最速です。
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="control-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Connection / Input</div>', unsafe_allow_html=True)

    with st.form("control_form"):
        c1, c2, c3 = st.columns([1.1, 1.2, 1.2])
        with c1:
            mode = st.radio("data mode", ["DEMO", "PUBLIC CSV / UPLOAD"], index=0, horizontal=True)
        with c2:
            price_csv_url = st.text_input("price table csv url", value="", placeholder="https://docs.google.com/...output=csv")
        with c3:
            market_csv_url = st.text_input("market table csv url", value="", placeholder="https://docs.google.com/...output=csv")

        u1, u2, u3 = st.columns([1, 1, 0.55])
        with u1:
            price_upload = st.file_uploader("price table csv", type=["csv"], key="price_upload")
        with u2:
            market_upload = st.file_uploader("market table csv", type=["csv"], key="market_upload")
        with u3:
            submitted = st.form_submit_button("RUN CONSOLE", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

tabs = st.tabs(["Control Board", "Recommendation Ledger", "Data Architecture"])

if submitted:
    price_df, market_df = load_inputs(mode, price_csv_url, market_csv_url, price_upload, market_upload)
    rec_df = recommend_prices(price_df, market_df)
    summary = kpis(rec_df)
    actions = build_actions(rec_df)

    with tabs[0]:
        r1, r2, r3, r4, r5 = st.columns(5)
        with r1:
            card_metric("Revenue", fmt_yen(summary["revenue"]), "対象SKU群の売上合計")
        with r2:
            card_metric("Gross Profit", fmt_yen(summary["profit"]), "粗利合計")
        with r3:
            card_metric("Sessions", f"{int(summary['sessions']):,}", "流入合計")
        with r4:
            card_metric("CVR", f"{summary['cvr']*100:.2f}%", "注文 / セッション")
        with r5:
            card_metric("Avg Price Delta", fmt_pct(summary["avg_delta"]), "推薦価格の平均差分")

        st.markdown("")
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recommended Operations</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for col, item in zip(cols, actions):
            with col:
                card_action(item["priority"], item["title"], item["body"], item["next"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")
        s1, s2 = st.columns([0.95, 1.25])
        with s1:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Signal Summary</div>', unsafe_allow_html=True)

            down_cnt = int((rec_df["recommended_action"] == "PRICE_DOWN_TEST").sum())
            up_cnt = int((rec_df["recommended_action"] == "PRICE_UP_TEST").sum())
            low_stock_cnt = int((rec_df["stock"] < 40).sum())
            hold_cnt = int((rec_df["recommended_action"] == "HOLD_PRICE").sum())

            st.markdown(
                f"""
                <div class="signal">
                    <div class="signal-k">price down candidates</div>
                    <div class="signal-v">{down_cnt}</div>
                    <div class="signal-f">均衡対比で価格がやや上振れているSKU数</div>
                </div>
                <div class="signal">
                    <div class="signal-k">price up candidates</div>
                    <div class="signal-v">{up_cnt}</div>
                    <div class="signal-f">値上げ余地が残るSKU数</div>
                </div>
                <div class="signal">
                    <div class="signal-k">hold price candidates</div>
                    <div class="signal-v">{hold_cnt}</div>
                    <div class="signal-f">価格より訴求改善を優先すべきSKU数</div>
                </div>
                <div class="signal">
                    <div class="signal-k">low stock watch</div>
                    <div class="signal-v">{low_stock_cnt}</div>
                    <div class="signal-f">欠品回避を優先すべきSKU数</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with s2:
            st.plotly_chart(chart_price_delta(rec_df), use_container_width=True)

    with tabs[1]:
        left, right = st.columns([1.3, 1.0])

        with left:
            ledger = rec_df[[
                "sku","product_name","current_price","recommended_price","price_delta","price_delta_pct",
                "revenue","gross_profit","sessions","orders","stock",
                "equilibrium_price","elasticity_proxy","competition_density","recommended_action","reason"
            ]].copy()
            ledger["price_delta_pct"] = ledger["price_delta_pct"].map(lambda x: f"{x*100:.1f}%")
            st.dataframe(ledger, use_container_width=True, hide_index=True)

            csv = rec_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "EXPORT RECOMMENDATION LEDGER",
                data=csv,
                file_name="astro_ops_console_recommendations.csv",
                mime="text/csv",
            )

        with right:
            st.plotly_chart(chart_revenue_profit(rec_df), use_container_width=True)
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Operational note</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="note">
                推薦価格は市場価格だけで決めていません。<br><br>
                均衡価格に対して、価格感応、在庫制約、流入効率、粗利下限を加味しています。<br><br>
                そのため、この画面は可視化ツールというより、<strong>価格運用とSKU運用の管制盤</strong> に近い設計です。
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Minimum free architecture</div>', unsafe_allow_html=True)

        schema = pd.DataFrame([
            {"table":"sku_master","role":"商品マスタ","columns":"sku, product_name, category, cost"},
            {"table":"daily_kpi","role":"日次運用実績","columns":"date, sku, price, sessions, orders, units, revenue, gross_profit"},
            {"table":"market_snapshot","role":"市場均衡観測","columns":"date, sku, equilibrium_price, market_low, market_high, elasticity_proxy, competition_density"},
            {"table":"inventory_snapshot","role":"在庫記録","columns":"date, sku, stock"},
            {"table":"recommendation_log","role":"推薦履歴","columns":"date, sku, current_price, recommended_price, action, reason"},
        ])
        st.dataframe(schema, use_container_width=True, hide_index=True)

        st.markdown(
            """
            <div class="note">
            <strong>初期の最適解</strong><br>
            1冊の Google Sheets の中に上の5シートを作り、必要なタブだけ CSV 公開してこの画面に読む。<br><br>
            <strong>Google API が不要なケース</strong><br>
            公開されたCSVリンクを読むだけのとき。通常のHTTP取得で足ります。<br><br>
            <strong>Google API が必要なケース</strong><br>
            非公開シートを読みたいとき、書き戻したいとき、ユーザー権限を保ったまま操作したいとき。<br><br>
            <strong>運用のすすめ方</strong><br>
            まずは Sheets で価格推薦ロジックを固める。次に private 化や自動更新が必要になった段階で Sheets API または Apps Script Web App へ移行する。
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    with tabs[0]:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ready state</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="note">
            これはサイドバー中心の古い管理画面ではなく、上部コマンドバー型の運用画面です。<br><br>
            まずは <strong>DEMO</strong> で見た目と操作感を確認し、その後 Google Sheets の公開CSVか実CSVを接続してください。
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
