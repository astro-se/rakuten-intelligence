
import io
import math
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


st.set_page_config(
    page_title="ASTRO RMS 2.0 Console",
    layout="wide",
    page_icon="▣",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root{
            --bg:#0a0d12;
            --panel:#12171f;
            --panel2:#171d27;
            --line:#2c3442;
            --soft:#7e8795;
            --text:#e8edf4;
            --white:#ffffff;
            --accent:#d4d9df;
            --good:#c7d2bf;
            --warn:#d5c7a1;
            --bad:#d1b3b3;
        }

        html, body, [class*="css"]  {
            font-family: "Inter", "SF Pro Display", "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                linear-gradient(180deg, #080a0f 0%, #0a0d12 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1520px;
            padding-top: 1.1rem;
            padding-bottom: 2rem;
        }

        section[data-testid="stSidebar"]{
            background: linear-gradient(180deg, #0d1118 0%, #0a0d12 100%);
            border-right: 1px solid var(--line);
        }

        .hero {
            border: 1px solid var(--line);
            background:
                linear-gradient(180deg, rgba(23,29,39,0.96), rgba(13,17,24,0.96));
            border-radius: 6px;
            padding: 26px 28px 22px 28px;
            margin-bottom: 16px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        }

        .hero-top {
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:14px;
        }

        .hero-badge {
            display:inline-block;
            border:1px solid #3b4554;
            color:#cfd6df;
            font-size:11px;
            padding:6px 10px;
            border-radius:3px;
            letter-spacing:0.14em;
            text-transform:uppercase;
        }

        .hero-grid {
            display:grid;
            grid-template-columns: 1.3fr 0.9fr;
            gap:18px;
            align-items:start;
        }

        .hero-title {
            font-size:34px;
            line-height:1.08;
            font-weight:800;
            letter-spacing:0.01em;
            color:var(--white);
            margin:0 0 10px 0;
        }

        .hero-sub {
            font-size:14px;
            color:#a8b1bd;
            line-height:1.75;
            max-width:900px;
        }

        .hero-plate {
            border:1px solid var(--line);
            background:rgba(6,8,12,0.34);
            padding:14px 16px;
            border-radius:4px;
        }

        .plate-label {
            font-size:10px;
            text-transform:uppercase;
            letter-spacing:0.18em;
            color:#8d97a5;
            margin-bottom:8px;
        }

        .plate-body {
            font-size:13px;
            line-height:1.65;
            color:#d7dde6;
        }

        .metric {
            border:1px solid var(--line);
            background:linear-gradient(180deg, #151b23 0%, #10151c 100%);
            border-radius:4px;
            padding:16px 16px 14px 16px;
            min-height:116px;
        }

        .metric-label {
            font-size:10px;
            text-transform:uppercase;
            letter-spacing:0.18em;
            color:#8d97a5;
            margin-bottom:12px;
        }

        .metric-value {
            font-size:30px;
            line-height:1;
            font-weight:800;
            color:#ffffff;
            margin-bottom:8px;
        }

        .metric-foot {
            font-size:12px;
            line-height:1.6;
            color:#a5afbb;
        }

        .section {
            border:1px solid var(--line);
            background:linear-gradient(180deg, #131821 0%, #0f141b 100%);
            border-radius:6px;
            padding:16px 16px 14px 16px;
        }

        .section-title {
            color:#ffffff;
            font-size:14px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:0.12em;
            margin-bottom:14px;
        }

        .action-box {
            border:1px solid var(--line);
            background:#0f141a;
            border-left:3px solid #7d8898;
            padding:14px 14px 13px 14px;
            border-radius:3px;
            min-height:176px;
        }

        .action-priority {
            display:inline-block;
            border:1px solid #404958;
            padding:5px 8px;
            border-radius:3px;
            font-size:10px;
            text-transform:uppercase;
            letter-spacing:0.16em;
            color:#dde3ea;
            margin-bottom:12px;
        }

        .action-title {
            color:#ffffff;
            font-size:16px;
            font-weight:800;
            line-height:1.35;
            margin-bottom:8px;
        }

        .action-body {
            color:#aeb7c3;
            font-size:13px;
            line-height:1.7;
            margin-bottom:10px;
        }

        .action-next {
            color:#dce3eb;
            font-size:12px;
            line-height:1.7;
            padding-top:10px;
            border-top:1px solid #252d39;
        }

        .signal-line {
            border-bottom:1px solid #252d39;
            padding:10px 0;
        }

        .signal-line:last-child { border-bottom:none; }

        .signal-name {
            font-size:11px;
            color:#8f99a7;
            text-transform:uppercase;
            letter-spacing:0.16em;
            margin-bottom:4px;
        }

        .signal-value {
            color:#ffffff;
            font-weight:700;
            font-size:16px;
            margin-bottom:4px;
        }

        .signal-note {
            color:#a9b3bf;
            font-size:12px;
            line-height:1.6;
        }

        .small-note {
            color:#8f99a7;
            font-size:12px;
            line-height:1.7;
        }

        div[data-baseweb="tab-list"]{
            gap:8px;
            margin-top:2px;
            margin-bottom:4px;
        }

        button[data-baseweb="tab"]{
            border-radius:3px;
            border:1px solid var(--line);
            background:#10151c;
            color:#d5dce5;
            padding:10px 14px;
        }

        button[data-baseweb="tab"][aria-selected="true"]{
            background:#171d26;
            border-color:#434d5d;
        }

        .stButton button, .stDownloadButton button {
            border-radius:3px;
            background:#161c24;
            color:#ffffff;
            border:1px solid #394350;
            font-weight:700;
        }

        .stDataFrame, div[data-testid="stMetric"]{
            border-radius:4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def fmt_yen(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"¥{int(round(v)):,}"


def fmt_pct(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "-"
    return f"{v*100:.1f}%"


def load_csv_from_url(url: str) -> pd.DataFrame:
    text = requests.get(url, timeout=20).text
    return pd.read_csv(io.StringIO(text))


def load_source(sheet_url: str, uploaded_file, fallback_df: pd.DataFrame) -> pd.DataFrame:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if sheet_url.strip():
        try:
            return load_csv_from_url(sheet_url.strip())
        except Exception:
            return fallback_df.copy()
    return fallback_df.copy()


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


def build_recommendation_table(price_df: pd.DataFrame, market_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.merge(market_df, on="sku", how="left")

    df["cvr"] = np.where(df["sessions"] > 0, df["orders"] / df["sessions"], 0)
    df["units_per_order"] = np.where(df["orders"] > 0, df["units"] / df["orders"], 1)
    df["margin_per_unit"] = df["current_price"] - df["cost"]
    df["gross_margin_rate"] = np.where(df["current_price"] > 0, df["margin_per_unit"] / df["current_price"], 0)

    market_anchor = (
        df["equilibrium_price"].fillna(df["current_price"]) * 0.60
        + df["market_low"].fillna(df["current_price"]) * 0.10
        + df["market_high"].fillna(df["current_price"]) * 0.10
        + df["current_price"] * 0.20
    )

    elasticity_adj = np.where(
        df["elasticity_proxy"].fillna(-0.5) <= -0.9,
        -0.03 * df["current_price"],
        np.where(df["elasticity_proxy"].fillna(-0.5) >= -0.45, 0.02 * df["current_price"], 0)
    )

    stock_adj = np.where(df["stock"] < 40, 0.03 * df["current_price"], np.where(df["stock"] > 120, -0.02 * df["current_price"], 0))
    margin_floor = df["cost"] / 0.62

    raw_recommended = market_anchor + elasticity_adj + stock_adj
    df["recommended_price"] = np.maximum(raw_recommended, margin_floor).round(-1)

    df["price_delta"] = df["recommended_price"] - df["current_price"]
    df["price_delta_pct"] = np.where(df["current_price"] > 0, df["price_delta"] / df["current_price"], 0)

    df["recommendation_reason"] = np.select(
        [
            df["price_delta_pct"] <= -0.03,
            df["price_delta_pct"] >= 0.03,
        ],
        [
            "市場均衡帯に対して上振れ。価格感応と在庫水準を踏まえ調整推奨。",
            "現在価格に値上げ余地。粗利改善余地が残る。",
        ],
        default="価格は概ね妥当。画像・訴求・配送条件を優先改善。"
    )

    df["recommended_action"] = np.select(
        [
            df["price_delta_pct"] <= -0.03,
            df["price_delta_pct"] >= 0.03,
        ],
        [
            "PRICE_DOWN_TEST",
            "PRICE_UP_TEST",
        ],
        default="HOLD_PRICE"
    )

    return df


def build_overview_kpis(rec_df: pd.DataFrame) -> Dict[str, float]:
    total_revenue = rec_df["revenue"].sum()
    total_profit = rec_df["gross_profit"].sum()
    total_sessions = rec_df["sessions"].sum()
    total_orders = rec_df["orders"].sum()
    cvr = total_orders / total_sessions if total_sessions else 0
    avg_delta = rec_df["price_delta_pct"].mean()
    return {
        "revenue": total_revenue,
        "profit": total_profit,
        "sessions": total_sessions,
        "orders": total_orders,
        "cvr": cvr,
        "avg_delta": avg_delta,
    }


def build_actions(rec_df: pd.DataFrame):
    actions = []
    down = rec_df.sort_values("price_delta_pct").head(2)
    up = rec_df.sort_values("price_delta_pct", ascending=False).head(2)

    if len(down):
        sku = down.iloc[0]
        actions.append({
            "priority":"critical",
            "title": f"{sku['sku']} を即テスト対象へ",
            "body": f"{sku['product_name']} は現行 {fmt_yen(sku['current_price'])} に対し推薦 {fmt_yen(sku['recommended_price'])}。価格感応と競争密度の観点で取りこぼしが疑われます。",
            "next": "3%刻みの価格テストと、メイン画像差し替えを同時実施。",
        })
    if len(up):
        sku = up.iloc[0]
        actions.append({
            "priority":"priority",
            "title": f"{sku['sku']} は値上げ余地あり",
            "body": f"{sku['product_name']} は現行 {fmt_yen(sku['current_price'])} に対し推薦 {fmt_yen(sku['recommended_price'])}。粗利改善余地が見込めます。",
            "next": "CVRが崩れない範囲で +2〜4% の段階改定。",
        })

    low_stock = rec_df.sort_values("stock").head(1).iloc[0]
    actions.append({
        "priority":"priority",
        "title": f"在庫監視 SKU: {low_stock['sku']}",
        "body": f"{low_stock['product_name']} は在庫 {int(low_stock['stock'])}。価格改定より欠品回避を優先すべき水準です。",
        "next": "価格を上げて需要を平準化するか、補充計画を前倒し。",
    })

    hold = rec_df.iloc[(rec_df["price_delta_pct"].abs()).argmin()]
    actions.append({
        "priority":"advisory",
        "title": f"{hold['sku']} は価格維持判断",
        "body": f"{hold['product_name']} は市場均衡帯と概ね整合。ここは値段よりも画像・レビュー・配送文言の改善が効きます。",
        "next": "価格は保持し、転換率改善のテストへ回す。",
    })
    return actions[:4]


def metric_card(label: str, value: str, foot: str):
    st.markdown(
        f"""
        <div class="metric">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def action_card(item: Dict[str, str]):
    st.markdown(
        f"""
        <div class="action-box">
          <div class="action-priority">{item['priority']}</div>
          <div class="action-title">{item['title']}</div>
          <div class="action-body">{item['body']}</div>
          <div class="action-next"><strong>NEXT</strong> {item['next']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def price_delta_chart(rec_df: pd.DataFrame):
    chart_df = rec_df.sort_values("price_delta_pct")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=chart_df["sku"],
        y=chart_df["price_delta_pct"] * 100,
        text=[f"{x*100:.1f}%" for x in chart_df["price_delta_pct"]],
        textposition="outside",
        marker_color="#9aa4b2",
    ))
    fig.update_layout(
        title="Recommended Price Delta by SKU",
        template="plotly_dark",
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="SKU",
        yaxis_title="% vs Current Price",
    )
    return fig


def revenue_profit_chart(rec_df: pd.DataFrame):
    chart_df = rec_df.copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue", x=chart_df["sku"], y=chart_df["revenue"]))
    fig.add_trace(go.Bar(name="Gross Profit", x=chart_df["sku"], y=chart_df["gross_profit"]))
    fig.update_layout(
        barmode="group",
        template="plotly_dark",
        title="Revenue / Gross Profit by SKU",
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


inject_css()

st.markdown(
    """
    <div class="hero">
      <div class="hero-top">
        <div class="hero-badge">ASTRO / RMS 2.0 CONSOLE</div>
        <div class="hero-badge">TACTICAL OPERATIONS PANEL</div>
      </div>
      <div class="hero-grid">
        <div>
          <div class="hero-title">価格、客足、利益を<br>一つの操作盤に集約する。</div>
          <div class="hero-sub">
            これは市場俯瞰BIではなく、アストロ向けの軽量RMSを意識した運用画面です。
            商品ごとの現行価格、推薦価格、売上、客足、利益、在庫、競争密度を束ね、
            最後は「何をどう触るか」だけを前面に出します。
          </div>
        </div>
        <div class="hero-plate">
          <div class="plate-label">Operational Doctrine</div>
          <div class="plate-body">
            価格推薦は単発計算ではなく、履歴の蓄積からしか精度が出ません。
            したがって、この種の画面には最低限のデータベースが必要です。
            無料で始めるなら、まずは Google Sheets をテーブル代わりに使うのが最も速いです。
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Data Source")
    mode = st.radio("source mode", ["DEMO", "CSV / SHEETS"], index=0)

    price_sheet_url = st.text_input("price table csv url", value="", help="Google Sheets を CSV 公開したURLを想定")
    market_sheet_url = st.text_input("market table csv url", value="", help="Google Sheets を CSV 公開したURLを想定")
    price_upload = st.file_uploader("price table csv", type=["csv"])
    market_upload = st.file_uploader("market table csv", type=["csv"])

    run = st.button("RUN CONSOLE", use_container_width=True)

tabs = st.tabs(["Control Board", "Price Recommendations", "Operations Ledger", "Data Model"])

if run:
    if mode == "CSV / SHEETS":
        price_df = load_source(price_sheet_url, price_upload, demo_price_table())
        market_df = load_source(market_sheet_url, market_upload, demo_market_table())
    else:
        price_df = demo_price_table()
        market_df = demo_market_table()

    rec_df = build_recommendation_table(price_df, market_df)
    kpis = build_overview_kpis(rec_df)
    actions = build_actions(rec_df)

    with tabs[0]:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            metric_card("Revenue", fmt_yen(kpis["revenue"]), "対象SKU群の売上合計")
        with c2:
            metric_card("Gross Profit", fmt_yen(kpis["profit"]), "粗利合計")
        with c3:
            metric_card("Sessions", f"{int(kpis['sessions']):,}", "流入合計")
        with c4:
            metric_card("CVR", f"{kpis['cvr']*100:.2f}%", "注文 / セッション")
        with c5:
            metric_card("Avg Price Delta", fmt_pct(kpis["avg_delta"]), "推薦価格の平均差分")

        st.markdown("#### Tactical Actions")
        cols = st.columns(4)
        for col, item in zip(cols, actions):
            with col:
                action_card(item)

        st.markdown("#### Mission Signals")
        left, right = st.columns([1, 1.2])
        with left:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Signal Summary</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="signal-line">
                  <div class="signal-name">price down candidates</div>
                  <div class="signal-value">{int((rec_df['recommended_action'] == 'PRICE_DOWN_TEST').sum())}</div>
                  <div class="signal-note">市場均衡に対して上振れているSKU数</div>
                </div>
                <div class="signal-line">
                  <div class="signal-name">price up candidates</div>
                  <div class="signal-value">{int((rec_df['recommended_action'] == 'PRICE_UP_TEST').sum())}</div>
                  <div class="signal-note">粗利改善余地が残るSKU数</div>
                </div>
                <div class="signal-line">
                  <div class="signal-name">low stock units</div>
                  <div class="signal-value">{int((rec_df['stock'] < 40).sum())}</div>
                  <div class="signal-note">欠品警戒SKU数</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
        with right:
            st.plotly_chart(price_delta_chart(rec_df), use_container_width=True)

    with tabs[1]:
        table = rec_df[[
            "sku","product_name","current_price","recommended_price","price_delta","price_delta_pct",
            "revenue","gross_profit","sessions","orders","stock",
            "equilibrium_price","elasticity_proxy","competition_density",
            "recommended_action","recommendation_reason"
        ]].copy()
        table["price_delta_pct"] = table["price_delta_pct"].map(lambda x: f"{x*100:.1f}%")
        st.dataframe(table, use_container_width=True, hide_index=True)

        csv = rec_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("EXPORT RECOMMENDATIONS CSV", data=csv, file_name="astro_rms20_recommendations.csv", mime="text/csv")

    with tabs[2]:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(revenue_profit_chart(rec_df), use_container_width=True)
        with right:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Operational Interpretation</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="small-note">
                この画面は BI より一段運用寄りです。<br><br>
                必要なのは単なる市場価格ではなく、SKUごとの<br>
                ・現行価格<br>
                ・売上<br>
                ・客足（セッション）<br>
                ・注文数 / CVR<br>
                ・粗利<br>
                ・在庫<br>
                ・競合均衡価格<br>
                の履歴です。<br><br>
                これらを持って初めて、推薦価格が「単なる相場追随」ではなく、
                自店の利益関数を踏まえた判断になります。
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("#### Minimum Tables")
        schema_df = pd.DataFrame([
            {"table":"sku_master","purpose":"商品マスタ","key columns":"sku, product_name, category, cost, listing_url"},
            {"table":"daily_kpi","purpose":"日次実績","key columns":"date, sku, price, sessions, orders, units, revenue, gross_profit"},
            {"table":"market_snapshot","purpose":"市場均衡観測","key columns":"date, sku, keyword, equilibrium_price, market_low, market_high, elasticity_proxy, competition_density"},
            {"table":"inventory_snapshot","purpose":"在庫記録","key columns":"date, sku, stock, inbound_qty"},
            {"table":"recommendation_log","purpose":"推薦履歴","key columns":"date, sku, current_price, recommended_price, action, reason"},
        ])
        st.dataframe(schema_df, use_container_width=True, hide_index=True)

        st.markdown(
            """
            **Google Sheets で始める場合**  
            1つのスプレッドシートの中に、`sku_master` `daily_kpi` `market_snapshot` `inventory_snapshot` `recommendation_log`
            を別タブで持つだけで始められます。  

            **このコードの使い方**  
            CSVをアップロードするか、Google Sheets を「CSV公開URL」にして読み込ませます。  
            最初は価格推薦の確認画面として使い、あとから自動取得へ寄せる想定です。
            """
        )
else:
    with tabs[0]:
        st.markdown(
            """
            #### What this should become

            これは市場レーダーではなく、**価格推薦リストを出す軽量RMS** の入口です。  
            まずは `DEMO` で実行し、次に Google Sheets の CSV をつないで実データへ差し替えるのが最短です。
            """
        )
