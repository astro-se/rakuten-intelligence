
import io
import math
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# Optional Google Sheets private access
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except Exception:  # pragma: no cover
    service_account = None
    build = None


st.set_page_config(
    page_title="ASTRO OPERATING SYSTEM",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Design system
# ============================================================
def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root{
            --bg:#0b0f14;
            --bg2:#0e131a;
            --panel:#121821;
            --panel2:#171e29;
            --panel3:#1d2530;
            --line:#26303d;
            --line2:#334050;
            --text:#eef3f7;
            --muted:#98a3b1;
            --muted2:#c2cad4;
            --accent:#dde3ea;
            --nav:#0c1016;
        }

        html, body, [class*="css"] {
            font-family: Inter, "SF Pro Display", "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                linear-gradient(180deg, #0a0d12 0%, #0b0f14 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1600px;
            padding-top: 0.8rem;
            padding-bottom: 1.6rem;
        }

        section[data-testid="stSidebar"] { display:none !important; }
        header[data-testid="stHeader"] { background: transparent; }
        #MainMenu, footer { visibility: hidden; }

        .shell {
            display:grid;
            grid-template-columns: 76px minmax(0, 1fr);
            gap: 14px;
            align-items:start;
        }

        .rail {
            border:1px solid var(--line);
            border-radius: 4px;
            background: linear-gradient(180deg, #11161d 0%, #0c1016 100%);
            min-height: calc(100vh - 90px);
            padding: 10px 8px;
            position: sticky;
            top: 12px;
        }

        .rail-logo {
            width:100%;
            height:54px;
            border:1px solid var(--line2);
            border-radius:3px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:white;
            font-weight:800;
            letter-spacing:0.08em;
            background:#0e1319;
            margin-bottom:12px;
        }

        .rail-item {
            width:100%;
            border:1px solid var(--line);
            border-radius:3px;
            background:#0e1319;
            color:#d8dfe7;
            font-size:10px;
            letter-spacing:0.16em;
            text-transform:uppercase;
            text-align:center;
            padding:10px 4px;
            margin-bottom:8px;
        }

        .viewport {
            min-width: 0;
        }

        .topbar {
            border:1px solid var(--line);
            border-radius:4px;
            background: linear-gradient(180deg, #141a23 0%, #10151c 100%);
            padding: 10px 14px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom: 12px;
        }

        .top-left, .top-right {
            display:flex;
            gap:8px;
            align-items:center;
            flex-wrap:wrap;
        }

        .chip {
            border:1px solid var(--line2);
            border-radius:3px;
            padding: 6px 9px;
            font-size:10px;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:#d6dde6;
            background:#0f141b;
        }

        .hero {
            border:1px solid var(--line);
            border-radius:4px;
            background: linear-gradient(180deg, #171e28 0%, #10151c 100%);
            padding: 24px 24px 20px 24px;
            margin-bottom: 14px;
        }

        .hero-grid {
            display:grid;
            grid-template-columns: 1.45fr 0.85fr;
            gap: 16px;
            align-items:start;
        }

        .hero-title {
            font-size: 38px;
            line-height: 1.00;
            font-weight: 860;
            color: white;
            margin: 0 0 10px 0;
            letter-spacing: 0.005em;
        }

        .hero-sub {
            font-size: 14px;
            line-height: 1.76;
            color: var(--muted2);
            max-width: 980px;
        }

        .hero-panel {
            border:1px solid var(--line);
            border-radius:3px;
            background:#0e1319;
            padding:14px 15px;
        }

        .hero-panel-k {
            font-size:10px;
            color:var(--muted);
            letter-spacing:0.16em;
            text-transform:uppercase;
            margin-bottom:8px;
        }

        .hero-panel-v {
            font-size:13px;
            color:#d9e0e8;
            line-height:1.72;
        }

        .cmd {
            border:1px solid var(--line);
            border-radius:4px;
            background: linear-gradient(180deg, #141a23 0%, #10151c 100%);
            padding: 14px;
            margin-bottom: 14px;
        }

        .section {
            border:1px solid var(--line);
            border-radius:4px;
            background: linear-gradient(180deg, #141a23 0%, #10151c 100%);
            padding: 14px;
        }

        .section-title {
            font-size:11px;
            letter-spacing:0.18em;
            text-transform:uppercase;
            color:#dbe2eb;
            font-weight:800;
            margin-bottom:12px;
        }

        .metric {
            border:1px solid var(--line);
            border-radius:3px;
            background:#0f141b;
            padding:14px 14px 12px 14px;
            min-height:114px;
        }

        .metric-k {
            font-size:10px;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:var(--muted);
            margin-bottom:11px;
        }

        .metric-v {
            font-size:30px;
            line-height:1;
            color:white;
            font-weight:860;
            margin-bottom:8px;
        }

        .metric-f {
            font-size:12px;
            line-height:1.55;
            color:var(--muted2);
        }

        .action {
            border:1px solid var(--line);
            border-left:3px solid #788495;
            border-radius:3px;
            background:#0e1319;
            padding:13px 13px 12px 13px;
            min-height:176px;
        }

        .action-p {
            display:inline-block;
            border:1px solid var(--line2);
            border-radius:3px;
            padding:5px 8px;
            font-size:10px;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:#d9e0e8;
            margin-bottom:11px;
        }

        .action-t {
            font-size:16px;
            line-height:1.35;
            color:white;
            font-weight:820;
            margin-bottom:8px;
        }

        .action-b {
            font-size:13px;
            line-height:1.68;
            color:var(--muted2);
            margin-bottom:10px;
        }

        .action-n {
            font-size:12px;
            line-height:1.68;
            color:#dfe6ee;
            border-top:1px solid #252d39;
            padding-top:10px;
        }

        .signal {
            border-bottom:1px solid #262e39;
            padding:10px 0;
        }
        .signal:last-child { border-bottom:none; }

        .signal-k {
            font-size:10px;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:var(--muted);
            margin-bottom:5px;
        }

        .signal-v {
            font-size:18px;
            color:white;
            font-weight:820;
            margin-bottom:4px;
        }

        .signal-f {
            font-size:12px;
            line-height:1.65;
            color:var(--muted2);
        }

        .note {
            font-size:12px;
            line-height:1.72;
            color:var(--muted2);
        }

        div[data-baseweb="tab-list"] {
            gap:8px;
            margin-top:2px;
            margin-bottom:4px;
        }

        button[data-baseweb="tab"] {
            border-radius:3px;
            border:1px solid var(--line);
            background:#10151c;
            color:#d6dde6;
            padding:10px 14px;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background:#171e28;
            border-color:#404d5c;
        }

        .stButton button, .stDownloadButton button {
            border-radius:3px;
            border:1px solid #3b4452;
            background:#171e28;
            color:white;
            font-weight:700;
        }

        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            background:#0f141b !important;
            border:1px solid #313948 !important;
            color:white !important;
            border-radius:3px !important;
        }

        .stRadio [role="radiogroup"] {
            flex-direction: row;
            gap: 8px;
            flex-wrap: wrap;
        }

        .stRadio label {
            background:#0f141b;
            border:1px solid #313948;
            padding:8px 10px;
            border-radius:3px;
        }

        .stFileUploader section {
            background:#0f141b !important;
            border:1px dashed #313948 !important;
            border-radius:3px !important;
        }

        .dense-table-note {
            font-size:11px;
            color:var(--muted);
            letter-spacing:0.08em;
            text-transform:uppercase;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Utilities
# ============================================================
def fmt_yen(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"¥{int(round(v)):,}"


def fmt_pct(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"{v*100:.1f}%"


def metric_card(label: str, value: str, foot: str) -> None:
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


def action_card(priority: str, title: str, body: str, next_step: str) -> None:
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


def signal_block(name: str, value: str, foot: str) -> None:
    st.markdown(
        f"""
        <div class="signal">
            <div class="signal-k">{name}</div>
            <div class="signal-v">{value}</div>
            <div class="signal-f">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Data loading
# ============================================================
def fetch_public_csv(url: str) -> pd.DataFrame:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return pd.read_csv(io.StringIO(resp.text))


def load_private_sheet_values(spreadsheet_id: str, sheet_name: str, range_a1: str = "A:Z") -> pd.DataFrame:
    if service_account is None or build is None:
        raise RuntimeError("google-api-python-client and google-auth are required for private Google Sheets mode.")

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # Preferred: nested secrets block named [gcp_service_account]
    service_account_info = None
    try:
        if "gcp_service_account" in st.secrets:
            service_account_info = dict(st.secrets["gcp_service_account"])
    except Exception:
        service_account_info = None

    if not service_account_info:
        raise RuntimeError(
            "Private Sheets mode requires a service account in Streamlit secrets. "
            "Add a [gcp_service_account] block with the JSON credentials."
        )

    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=scopes)
    api = build("sheets", "v4", credentials=creds, cache_discovery=False)

    result = (
        api.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!{range_a1}")
        .execute()
    )

    values = result.get("values", [])
    if not values:
        return pd.DataFrame()

    header = values[0]
    rows = values[1:]
    width = len(header)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    return pd.DataFrame(normalized, columns=header)


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


def coerce_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def load_inputs(
    mode: str,
    price_csv_url: str,
    market_csv_url: str,
    price_upload,
    market_upload,
    spreadsheet_id: str,
    price_sheet_name: str,
    market_sheet_name: str,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if mode == "DEMO":
        return demo_price_table(), demo_market_table()

    if mode == "UPLOAD":
        price_df = pd.read_csv(price_upload) if price_upload is not None else demo_price_table()
        market_df = pd.read_csv(market_upload) if market_upload is not None else demo_market_table()
        return price_df, market_df

    if mode == "PUBLIC CSV":
        price_df = fetch_public_csv(price_csv_url.strip()) if price_csv_url.strip() else demo_price_table()
        market_df = fetch_public_csv(market_csv_url.strip()) if market_csv_url.strip() else demo_market_table()
        return price_df, market_df

    # PRIVATE GOOGLE SHEETS
    if not spreadsheet_id.strip():
        raise RuntimeError("Spreadsheet ID is required for PRIVATE GOOGLE SHEETS mode.")
    if not price_sheet_name.strip() or not market_sheet_name.strip():
        raise RuntimeError("Sheet names are required for PRIVATE GOOGLE SHEETS mode.")

    price_df = load_private_sheet_values(spreadsheet_id.strip(), price_sheet_name.strip(), "A:Z")
    market_df = load_private_sheet_values(spreadsheet_id.strip(), market_sheet_name.strip(), "A:Z")
    return price_df, market_df


# ============================================================
# Recommendation engine
# ============================================================
def recommend_prices(price_df: pd.DataFrame, market_df: pd.DataFrame) -> pd.DataFrame:
    price_df = coerce_numeric(
        price_df,
        ["current_price", "cost", "sessions", "orders", "units", "revenue", "gross_profit", "stock"],
    )
    market_df = coerce_numeric(
        market_df,
        ["equilibrium_price", "market_low", "market_high", "elasticity_proxy", "competition_density"],
    )

    df = price_df.merge(market_df, on="sku", how="left")

    df["sessions"] = df["sessions"].fillna(0)
    df["orders"] = df["orders"].fillna(0)
    df["stock"] = df["stock"].fillna(0)
    df["current_price"] = df["current_price"].fillna(0)
    df["cost"] = df["cost"].fillna(0)
    df["equilibrium_price"] = df["equilibrium_price"].fillna(df["current_price"])
    df["market_low"] = df["market_low"].fillna(df["current_price"])
    df["market_high"] = df["market_high"].fillna(df["current_price"])
    df["elasticity_proxy"] = df["elasticity_proxy"].fillna(-0.6)
    df["competition_density"] = df["competition_density"].fillna(0.5)

    df["cvr"] = np.where(df["sessions"] > 0, df["orders"] / df["sessions"], 0)
    df["margin_per_unit"] = df["current_price"] - df["cost"]
    df["margin_rate"] = np.where(df["current_price"] > 0, df["margin_per_unit"] / df["current_price"], 0)

    market_anchor = (
        df["equilibrium_price"] * 0.66
        + df["market_low"] * 0.07
        + df["market_high"] * 0.07
        + df["current_price"] * 0.20
    )

    elasticity_adj = np.where(
        df["elasticity_proxy"] <= -1.0, -0.04 * df["current_price"],
        np.where(df["elasticity_proxy"] <= -0.75, -0.015 * df["current_price"],
                 np.where(df["elasticity_proxy"] >= -0.4, 0.025 * df["current_price"], 0))
    )

    stock_adj = np.where(
        df["stock"] < 40, 0.04 * df["current_price"],
        np.where(df["stock"] > 120, -0.025 * df["current_price"], 0)
    )

    weak_conversion = (df["sessions"] > df["sessions"].median()) & (df["cvr"] < df["cvr"].median())
    traffic_adj = np.where(weak_conversion, -0.02 * df["current_price"], 0)

    density_adj = np.where(df["competition_density"] > 0.85, -0.015 * df["current_price"], 0)

    floor_price = np.where(df["cost"] > 0, df["cost"] / 0.60, 0)
    raw = market_anchor + elasticity_adj + stock_adj + traffic_adj + density_adj
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
            "粗利余地と在庫制約を踏まえると上方向テスト余地あり。",
        ],
        default="価格は概ね妥当。画像・訴求・配送条件の改善を優先。",
    )

    return df


def summarize_kpis(df: pd.DataFrame) -> Dict[str, float]:
    revenue = float(df["revenue"].fillna(0).sum())
    profit = float(df["gross_profit"].fillna(0).sum())
    sessions = float(df["sessions"].fillna(0).sum())
    orders = float(df["orders"].fillna(0).sum())
    cvr = orders / sessions if sessions else 0
    avg_delta = float(df["price_delta_pct"].mean()) if len(df) else 0
    return {
        "revenue": revenue,
        "profit": profit,
        "sessions": sessions,
        "orders": orders,
        "cvr": cvr,
        "avg_delta": avg_delta,
    }


def build_actions(df: pd.DataFrame) -> List[Dict[str, str]]:
    actions = []
    if df.empty:
        return actions

    down_df = df.sort_values("price_delta_pct")
    up_df = df.sort_values("price_delta_pct", ascending=False)
    low_stock_df = df.sort_values("stock")

    x = down_df.iloc[0]
    actions.append({
        "priority": "critical",
        "title": f"{x['sku']} を下方向テスト",
        "body": f"{x['product_name']} は現行 {fmt_yen(x['current_price'])} に対し推薦 {fmt_yen(x['recommended_price'])}。高流入なのに転換が弱く、相場対比でもやや上振れです。",
        "next": "3%刻みで価格テスト。メイン画像と配送文言も同時に差し替え。",
    })

    x = up_df.iloc[0]
    actions.append({
        "priority": "priority",
        "title": f"{x['sku']} は値上げ余地あり",
        "body": f"{x['product_name']} は現行 {fmt_yen(x['current_price'])}、推薦 {fmt_yen(x['recommended_price'])}。粗利回収を優先できる水準です。",
        "next": "+2% から +4% の範囲で段階改定し、CVRの毀損を監視。",
    })

    x = low_stock_df.iloc[0]
    actions.append({
        "priority": "priority",
        "title": f"{x['sku']} は在庫優先管理",
        "body": f"{x['product_name']} の在庫は {int(x['stock'])}。欠品回避が価格最適化より先です。",
        "next": "補充予定を確認し、必要なら価格を上げて需要を平準化。",
    })

    hold_df = df.iloc[(df["price_delta_pct"].abs()).argmin()]
    actions.append({
        "priority": "advisory",
        "title": f"{hold_df['sku']} は価格維持判断",
        "body": f"{hold_df['product_name']} は市場均衡とのズレが小さい商品です。ここは価格より訴求改善が効きます。",
        "next": "価格は維持し、画像・レビュー獲得・送料無料条件を調整。",
    })

    return actions[:4]


# ============================================================
# Charts
# ============================================================
def chart_price_delta(df: pd.DataFrame) -> go.Figure:
    x = df.sort_values("price_delta_pct")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x["sku"],
        y=x["price_delta_pct"] * 100,
        text=[f"{v*100:.1f}%" for v in x["price_delta_pct"]],
        textposition="outside",
        marker_color="#b8c0ca",
        hovertemplate="%{x}<br>%{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title="Recommended Price Delta",
        template="plotly_dark",
        height=330,
        margin=dict(l=20, r=20, t=48, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="SKU",
        yaxis_title="% vs current",
        legend=dict(orientation="h"),
    )
    return fig


def chart_revenue_profit(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue", x=df["sku"], y=df["revenue"], marker_color="#8d98a6"))
    fig.add_trace(go.Bar(name="Gross Profit", x=df["sku"], y=df["gross_profit"], marker_color="#d1d8e0"))
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


# ============================================================
# App shell
# ============================================================
inject_css()

st.markdown(
    """
    <div class="shell">
        <div class="rail">
            <div class="rail-logo">AST</div>
            <div class="rail-item">Ops</div>
            <div class="rail-item">Ctrl</div>
            <div class="rail-item">Prc</div>
            <div class="rail-item">Inv</div>
            <div class="rail-item">Log</div>
        </div>
        <div class="viewport">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="topbar">
        <div class="top-left">
            <div class="chip">ASTRO / OPERATING SYSTEM</div>
            <div class="chip">PRICE · TRAFFIC · PROFIT · STOCK</div>
            <div class="chip">CLOSED-LOOP OPERATIONS</div>
        </div>
        <div class="top-right">
            <div class="chip">RMS 2.0</div>
            <div class="chip">PRIVATE DATA READY</div>
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
                <div class="hero-title">可視化ではなく、<br>意思決定の操作盤へ。</div>
                <div class="hero-sub">
                    市場均衡、価格感応、客足、粗利、在庫を束ねて、SKUごとに推薦価格と次の操作を返す。
                    レイアウトは「AIダッシュボード」ではなく、密度の高い運用OSを意識しています。
                </div>
            </div>
            <div class="hero-panel">
                <div class="hero-panel-k">Private ingress</div>
                <div class="hero-panel-v">
                    社内データは公開CSVにしなくて構いません。<br>
                    この版は <strong>非公開 Google Sheets をサービスアカウントで読む</strong> モードを持っています。<br>
                    共有先は人ではなく、サービスアカウントのメールアドレスです。
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="cmd">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Connection / Input</div>', unsafe_allow_html=True)

with st.form("control_form"):
    row1_a, row1_b, row1_c, row1_d = st.columns([0.95, 1.15, 1.15, 0.75])
    with row1_a:
        mode = st.radio(
            "mode",
            ["DEMO", "UPLOAD", "PUBLIC CSV", "PRIVATE GOOGLE SHEETS"],
            index=0,
            horizontal=False,
        )
    with row1_b:
        spreadsheet_id = st.text_input("spreadsheet id", value="", placeholder="Google Sheets のID")
        price_sheet_name = st.text_input("price sheet name", value="daily_kpi")
    with row1_c:
        price_csv_url = st.text_input("price table csv url", value="", placeholder="公開CSVモード用")
        market_sheet_name = st.text_input("market sheet name", value="market_snapshot")
    with row1_d:
        market_csv_url = st.text_input("market table csv url", value="", placeholder="公開CSVモード用")
        submitted = st.form_submit_button("RUN SYSTEM", use_container_width=True)

    row2_a, row2_b = st.columns(2)
    with row2_a:
        price_upload = st.file_uploader("price table csv", type=["csv"], key="price_upload")
    with row2_b:
        market_upload = st.file_uploader("market table csv", type=["csv"], key="market_upload")

st.markdown('</div>', unsafe_allow_html=True)

tabs = st.tabs(["Control Board", "Recommendation Ledger", "Private Access Setup"])

if submitted:
    try:
        price_df, market_df = load_inputs(
            mode=mode,
            price_csv_url=price_csv_url,
            market_csv_url=market_csv_url,
            price_upload=price_upload,
            market_upload=market_upload,
            spreadsheet_id=spreadsheet_id,
            price_sheet_name=price_sheet_name,
            market_sheet_name=market_sheet_name,
        )
        rec_df = recommend_prices(price_df, market_df)
        summary = summarize_kpis(rec_df)
        actions = build_actions(rec_df)

        with tabs[0]:
            m1, m2, m3, m4, m5 = st.columns(5)
            with m1:
                metric_card("Revenue", fmt_yen(summary["revenue"]), "対象SKU群の売上合計")
            with m2:
                metric_card("Gross Profit", fmt_yen(summary["profit"]), "粗利合計")
            with m3:
                metric_card("Sessions", f"{int(summary['sessions']):,}", "流入合計")
            with m4:
                metric_card("CVR", f"{summary['cvr']*100:.2f}%", "注文 / セッション")
            with m5:
                metric_card("Avg Price Delta", fmt_pct(summary["avg_delta"]), "推薦価格の平均差分")

            st.markdown("")
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Recommended Operations</div>', unsafe_allow_html=True)
            cols = st.columns(4)
            for col, item in zip(cols, actions):
                with col:
                    action_card(item["priority"], item["title"], item["body"], item["next"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("")
            left, right = st.columns([0.92, 1.28])
            with left:
                st.markdown('<div class="section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Signal Summary</div>', unsafe_allow_html=True)

                down_cnt = int((rec_df["recommended_action"] == "PRICE_DOWN_TEST").sum())
                up_cnt = int((rec_df["recommended_action"] == "PRICE_UP_TEST").sum())
                hold_cnt = int((rec_df["recommended_action"] == "HOLD_PRICE").sum())
                low_stock_cnt = int((rec_df["stock"] < 40).sum())

                signal_block("price down candidates", str(down_cnt), "均衡対比で価格が上振れているSKU数")
                signal_block("price up candidates", str(up_cnt), "値上げ余地が残るSKU数")
                signal_block("hold price candidates", str(hold_cnt), "価格より訴求改善を優先すべきSKU数")
                signal_block("low stock watch", str(low_stock_cnt), "欠品回避を優先すべきSKU数")
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                st.plotly_chart(chart_price_delta(rec_df), use_container_width=True)

        with tabs[1]:
            left, right = st.columns([1.35, 0.95])
            with left:
                st.markdown('<div class="dense-table-note">recommendation ledger</div>', unsafe_allow_html=True)
                ledger = rec_df[[
                    "sku", "product_name", "current_price", "recommended_price", "price_delta", "price_delta_pct",
                    "revenue", "gross_profit", "sessions", "orders", "stock",
                    "equilibrium_price", "elasticity_proxy", "competition_density",
                    "recommended_action", "reason"
                ]].copy()
                ledger["price_delta_pct"] = ledger["price_delta_pct"].map(lambda x: f"{x*100:.1f}%")
                st.dataframe(ledger, use_container_width=True, hide_index=True)

                csv_bytes = rec_df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "EXPORT RECOMMENDATION LEDGER",
                    data=csv_bytes,
                    file_name="astro_operating_system_recommendations.csv",
                    mime="text/csv",
                )

            with right:
                st.plotly_chart(chart_revenue_profit(rec_df), use_container_width=True)
                st.markdown('<div class="section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Interpretation</div>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="note">
                    推薦価格は市場価格だけで決めていません。<br><br>
                    均衡価格に対して、価格感応、在庫制約、競争密度、流入効率、粗利下限を加味しています。<br><br>
                    つまりこの画面は BI ではなく、価格運用と SKU 運用のための操作盤です。
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

        with tabs[2]:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Private Google Sheets setup</div>', unsafe_allow_html=True)

            setup_df = pd.DataFrame([
                {"step": 1, "task": "Google Cloud で Sheets API を有効化", "detail": "対象プロジェクトで Google Sheets API を ON"},
                {"step": 2, "task": "サービスアカウントを作成", "detail": "JSON キーを発行"},
                {"step": 3, "task": "スプレッドシートを共有", "detail": "サービスアカウントの email に Viewer 権限を付与"},
                {"step": 4, "task": "Streamlit secrets に格納", "detail": "[gcp_service_account] ブロックとして JSON を保存"},
                {"step": 5, "task": "spreadsheet id と sheet 名を入力", "detail": "daily_kpi / market_snapshot などを指定"},
            ])
            st.dataframe(setup_df, use_container_width=True, hide_index=True)

            st.code(
                """# .streamlit/secrets.toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"
""",
                language="toml",
            )

            st.markdown(
                """
                <div class="note">
                価格推薦の入力元として最小構成で必要なのは <strong>daily_kpi</strong> と <strong>market_snapshot</strong> の2シートです。<br><br>
                次段階では <strong>inventory_snapshot</strong> と <strong>recommendation_log</strong> を追加すると、閉ループ運用に寄せられます。
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Execution error: {e}")

else:
    with tabs[0]:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ready state</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="note">
            この版はサイドバー中心の管理画面ではなく、左レールと上部コマンドバーを持つ業務OS型のレイアウトです。<br><br>
            初期確認は <strong>DEMO</strong>、社内データ接続は <strong>PRIVATE GOOGLE SHEETS</strong> を使ってください。
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
