
import math
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


st.set_page_config(
    page_title="ASTRO Market Intelligence",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded",
)

PUBLIC_ITEM_SEARCH_URL = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"

DEFAULT_ELEMENTS = ",".join(
    [
        "itemName",
        "itemPrice",
        "shopName",
        "shopCode",
        "genreId",
        "itemUrl",
        "mediumImageUrls",
        "availability",
        "reviewCount",
        "reviewAverage",
        "postageFlag",
    ]
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #070b13;
            --panel: rgba(10, 16, 28, 0.78);
            --panel-strong: rgba(14, 22, 38, 0.92);
            --line: rgba(132, 160, 255, 0.18);
            --text: #e8eefb;
            --muted: #8fa3c8;
            --accent: #78b4ff;
            --accent-2: #41ffd6;
            --warn: #ffc857;
            --danger: #ff6b6b;
        }

        html, body, [class*="css"]  {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 20%, rgba(62, 106, 214, 0.18), transparent 25%),
                radial-gradient(circle at 85% 10%, rgba(0, 255, 214, 0.08), transparent 22%),
                radial-gradient(circle at 50% 95%, rgba(120, 180, 255, 0.10), transparent 30%),
                linear-gradient(180deg, #04070d 0%, #07101b 52%, #050811 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(9,15,26,0.97), rgba(6,10,18,0.97));
            border-right: 1px solid var(--line);
        }

        .mission-hero {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 28px 30px 26px 30px;
            background:
                linear-gradient(135deg, rgba(12,22,38,0.96), rgba(7,12,22,0.88));
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.30);
            margin-bottom: 18px;
        }

        .mission-hero:before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 80% 20%, rgba(120, 180, 255, 0.15), transparent 20%),
                linear-gradient(90deg, transparent 0%, rgba(120,180,255,0.03) 50%, transparent 100%);
            pointer-events: none;
        }

        .eyebrow {
            color: var(--accent-2);
            font-size: 12px;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .hero-title {
            color: white;
            font-size: 34px;
            line-height: 1.05;
            font-weight: 800;
            margin: 0 0 10px 0;
        }

        .hero-sub {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.8;
            max-width: 980px;
            margin-bottom: 0;
        }

        .glass-card {
            border: 1px solid var(--line);
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(13,19,32,0.90), rgba(8,12,22,0.80));
            padding: 18px 18px 16px 18px;
            box-shadow: 0 10px 28px rgba(0,0,0,0.22);
        }

        .metric-card {
            border: 1px solid var(--line);
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(13,21,36,0.88), rgba(8,12,20,0.84));
            padding: 16px 18px;
            min-height: 124px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 11px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .metric-value {
            color: #ffffff;
            font-size: 28px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 8px;
        }

        .metric-foot {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .signal-card {
            border: 1px solid var(--line);
            border-left: 3px solid var(--accent);
            border-radius: 18px;
            background: rgba(13, 19, 32, 0.82);
            padding: 14px 16px;
            margin-bottom: 12px;
        }

        .signal-title {
            color: #ffffff;
            font-weight: 700;
            margin-bottom: 6px;
            font-size: 15px;
        }

        .signal-body {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.65;
        }

        .tag-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 14px;
        }

        .tag {
            font-size: 11px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #d8e4ff;
            padding: 7px 10px;
            border-radius: 999px;
            border: 1px solid rgba(120,180,255,0.16);
            background: rgba(120,180,255,0.08);
        }

        .action-card {
            border: 1px solid var(--line);
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(17,24,40,0.92), rgba(9,14,24,0.86));
            padding: 18px;
            min-height: 200px;
        }

        .action-priority {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 11px;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            font-weight: 800;
            margin-bottom: 14px;
        }

        .priority-high {
            background: rgba(255,107,107,0.12);
            color: #ff9f9f;
            border: 1px solid rgba(255,107,107,0.24);
        }

        .priority-mid {
            background: rgba(255,200,87,0.12);
            color: #ffd98a;
            border: 1px solid rgba(255,200,87,0.24);
        }

        .priority-low {
            background: rgba(65,255,214,0.10);
            color: #8fffe8;
            border: 1px solid rgba(65,255,214,0.22);
        }

        .action-title {
            color: white;
            font-size: 18px;
            font-weight: 800;
            line-height: 1.35;
            margin-bottom: 10px;
        }

        .action-body {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.7;
            margin-bottom: 12px;
        }

        .action-next {
            color: #d9e8ff;
            font-size: 13px;
            line-height: 1.7;
            border-top: 1px solid rgba(132,160,255,0.14);
            padding-top: 12px;
        }

        .tiny-note {
            color: var(--muted);
            font-size: 12px;
            line-height: 1.6;
        }

        div[data-baseweb="tab-list"] {
            gap: 10px;
            margin-top: 6px;
        }

        button[data-baseweb="tab"] {
            background: rgba(9, 14, 24, 0.72);
            border: 1px solid var(--line);
            border-radius: 14px;
            color: #d9e8ff;
            padding: 10px 16px;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: rgba(120,180,255,0.10);
            border-color: rgba(120,180,255,0.26);
        }

        .stDownloadButton button, .stButton button {
            border-radius: 14px;
            border: 1px solid rgba(120,180,255,0.18);
            background: linear-gradient(180deg, rgba(18,30,52,1), rgba(10,18,32,1));
            color: white;
            font-weight: 700;
        }

        .section-title {
            font-size: 16px;
            color: white;
            font-weight: 800;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    try:
        return st.secrets[name]
    except Exception:
        return default


def build_headers(access_key: str, allowed_origin: str) -> Dict[str, str]:
    headers = {
        "User-Agent": "ASTRO-Market-Intelligence/2.0",
        "Accept": "application/json",
        "accessKey": access_key,
    }
    allowed_origin = (allowed_origin or "").strip()
    if allowed_origin:
        headers["Origin"] = allowed_origin
        headers["Referer"] = f"{allowed_origin.rstrip('/')}/"
    return headers


def request_json(
    url: str,
    application_id: str,
    access_key: str,
    allowed_origin: str,
    params: Dict[str, Any],
    timeout: int = 20,
) -> Dict[str, Any]:
    final_params = {"format": "json", "applicationId": application_id, **params}
    response = requests.get(
        url,
        params=final_params,
        headers=build_headers(access_key, allowed_origin),
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError(f"{payload.get('error')} / {payload.get('error_description', 'unknown error')}")
    return payload


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_search_page(
    application_id: str,
    access_key: str,
    allowed_origin: str,
    keyword: str,
    page: int,
    hits: int,
    sort: str,
    api_shop_code: str,
    genre_id: str,
    min_price: int,
    max_price: int,
    availability_only: bool,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "keyword": keyword,
        "page": page,
        "hits": hits,
        "sort": sort,
        "formatVersion": 2,
        "elements": DEFAULT_ELEMENTS,
    }
    if api_shop_code:
        params["shopCode"] = api_shop_code
    if genre_id:
        params["genreId"] = genre_id
    if min_price > 0:
        params["minPrice"] = min_price
    if max_price > 0:
        params["maxPrice"] = max_price
    if availability_only:
        params["availability"] = 1

    return request_json(PUBLIC_ITEM_SEARCH_URL, application_id, access_key, allowed_origin, params)


def build_price_band(price_series: pd.Series) -> pd.Series:
    if price_series.empty:
        return pd.Series(dtype="object")

    try:
        band = pd.qcut(price_series.rank(method="first"), q=min(6, max(2, price_series.nunique())), duplicates="drop")
        return band.astype(str)
    except Exception:
        return pd.Series(["single"] * len(price_series), index=price_series.index)


def normalize_items(items: List[Dict[str, Any]], page: int) -> pd.DataFrame:
    rows = []
    for item in items:
        images = item.get("mediumImageUrls", []) or []
        image_url = None
        if images:
            first = images[0]
            if isinstance(first, dict):
                image_url = first.get("imageUrl")
            elif isinstance(first, str):
                image_url = first

        rows.append(
            {
                "取得ページ": page,
                "商品名": item.get("itemName"),
                "価格": item.get("itemPrice"),
                "店舗名": item.get("shopName"),
                "店舗コード": item.get("shopCode"),
                "ジャンルID": item.get("genreId"),
                "レビュー件数": item.get("reviewCount"),
                "レビュー平均": item.get("reviewAverage"),
                "在庫あり": item.get("availability"),
                "送料無料": item.get("postageFlag"),
                "商品URL": item.get("itemUrl"),
                "画像URL": image_url,
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    numeric_cols = ["価格", "レビュー件数", "レビュー平均", "在庫あり", "送料無料"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["価格"] = df["価格"].fillna(0)
    df["レビュー件数"] = df["レビュー件数"].fillna(0)
    df["レビュー平均"] = df["レビュー平均"].fillna(0)
    df["需要ウェイト"] = np.log1p(df["レビュー件数"].clip(lower=0)) * df["レビュー平均"].clip(lower=1)
    df["需要ウェイト"] = df["需要ウェイト"].replace([np.inf, -np.inf], 0).fillna(0)
    df["価格帯ラベル"] = build_price_band(df["価格"])
    return df


def fetch_market_dataset(
    application_id: str,
    access_key: str,
    allowed_origin: str,
    keyword: str,
    pages_to_scan: int,
    hits: int,
    sort: str,
    api_shop_code: str,
    genre_id: str,
    min_price: int,
    max_price: int,
    availability_only: bool,
):
    frames: List[pd.DataFrame] = []
    meta: Dict[str, Any] = {}
    for idx, page in enumerate(range(1, pages_to_scan + 1), start=1):
        raw = fetch_search_page(
            application_id=application_id,
            access_key=access_key,
            allowed_origin=allowed_origin,
            keyword=keyword,
            page=page,
            hits=hits,
            sort=sort,
            api_shop_code=api_shop_code,
            genre_id=genre_id,
            min_price=min_price,
            max_price=max_price,
            availability_only=availability_only,
        )
        if not meta:
            meta = {
                "total_count": raw.get("count"),
                "page_count": raw.get("pageCount"),
                "hits": raw.get("hits"),
            }
        items = raw.get("Items") or raw.get("items") or []
        page_df = normalize_items(items, page)
        if page_df.empty:
            break
        frames.append(page_df)
        if idx < pages_to_scan:
            time.sleep(1.08)

    if not frames:
        return pd.DataFrame(), meta

    market_df = pd.concat(frames, ignore_index=True)
    market_df.drop_duplicates(subset=["商品URL"], inplace=True)
    return market_df, meta


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    if len(values) == 0:
        return float("nan")
    sorter = np.argsort(values)
    values = values[sorter]
    weights = weights[sorter]
    cumulative = np.cumsum(weights)
    if cumulative[-1] == 0:
        return float(np.quantile(values, q))
    cutoff = q * cumulative[-1]
    return float(values[np.searchsorted(cumulative, cutoff, side="left")])


def safe_corr(x: pd.Series, y: pd.Series) -> float:
    if x.dropna().shape[0] < 3 or y.dropna().shape[0] < 3:
        return float("nan")
    return float(x.corr(y))


def estimate_elasticity_proxy(df: pd.DataFrame) -> Dict[str, Any]:
    sample = df[(df["価格"] > 0) & (df["レビュー件数"] >= 0)].copy()
    if len(sample) < 8 or sample["価格"].nunique() < 4:
        return {
            "slope": np.nan,
            "label": "insufficient",
            "summary": "データ点が不足しているため、感応度プロキシの推定は保留。",
        }

    x = np.log(sample["価格"])
    y = np.log1p(sample["レビュー件数"])
    slope, intercept = np.polyfit(x, y, 1)
    corr = safe_corr(x, y)

    if slope <= -1.0:
        label = "high"
        summary = "価格変化に対して反応が強い市場帯。小さな値付け差でも需要差が出やすい。"
    elif slope <= -0.45:
        label = "medium"
        summary = "価格感応は中程度。価格以外の訴求でも勝負できるが、過度な乖離は危険。"
    else:
        label = "low"
        summary = "価格単独では決まりにくい市場帯。レビュー、訴求軸、配送条件の影響が相対的に大きい。"

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "corr": float(corr) if not math.isnan(corr) else np.nan,
        "label": label,
        "summary": summary,
    }


def analyze_market(df: pd.DataFrame, own_shop_code: str, own_shop_name: str) -> Dict[str, Any]:
    if df.empty:
        return {}

    weights = (df["需要ウェイト"].fillna(0) + 1).to_numpy(dtype=float)
    prices = df["価格"].to_numpy(dtype=float)

    equilibrium = weighted_quantile(prices, weights, 0.50)
    lower_band = weighted_quantile(prices, weights, 0.35)
    upper_band = weighted_quantile(prices, weights, 0.65)

    market = {
        "items": int(len(df)),
        "shops": int(df["店舗コード"].nunique()),
        "mean_price": float(df["価格"].mean()) if len(df) else np.nan,
        "median_price": float(df["価格"].median()) if len(df) else np.nan,
        "eq_price": equilibrium,
        "eq_low": lower_band,
        "eq_high": upper_band,
        "avg_review": float(df["レビュー平均"].replace(0, np.nan).mean()) if len(df) else np.nan,
        "median_reviews": float(df["レビュー件数"].median()) if len(df) else np.nan,
        "elasticity": estimate_elasticity_proxy(df),
    }

    own_mask = pd.Series(False, index=df.index)
    if own_shop_code.strip():
        own_mask = own_mask | (df["店舗コード"].fillna("").astype(str).str.lower() == own_shop_code.strip().lower())
    if own_shop_name.strip():
        own_mask = own_mask | df["店舗名"].fillna("").astype(str).str.contains(own_shop_name.strip(), case=False, na=False)

    own_df = df.loc[own_mask].copy()
    market["own_df"] = own_df
    market["market_df"] = df

    if not own_df.empty:
        market["own_median_price"] = float(own_df["価格"].median())
        market["own_avg_review"] = float(own_df["レビュー平均"].replace(0, np.nan).mean()) if len(own_df) else np.nan
        market["own_items"] = int(len(own_df))
        market["own_review_median"] = float(own_df["レビュー件数"].median()) if len(own_df) else np.nan
        market["price_gap_ratio"] = float((market["own_median_price"] / equilibrium) - 1) if equilibrium else np.nan
    else:
        market["own_items"] = 0
        market["price_gap_ratio"] = np.nan

    band_df = (
        df.groupby("価格帯ラベル", dropna=False)
        .agg(
            商品数=("商品名", "count"),
            平均価格=("価格", "mean"),
            平均レビュー件数=("レビュー件数", "mean"),
            平均レビュー評価=("レビュー平均", "mean"),
            需要総量=("需要ウェイト", "sum"),
            店舗数=("店舗コード", "nunique"),
        )
        .reset_index()
    )
    band_df["バンド魅力度"] = (band_df["需要総量"] + 1) / np.sqrt(band_df["商品数"].clip(lower=1))
    band_df = band_df.sort_values("バンド魅力度", ascending=False)
    market["band_df"] = band_df

    market["top_shops"] = (
        df.groupby("店舗名", dropna=False)
        .agg(
            商品数=("商品名", "count"),
            中央価格=("価格", "median"),
            平均レビュー件数=("レビュー件数", "mean"),
        )
        .sort_values(["商品数", "平均レビュー件数"], ascending=False)
        .head(12)
        .reset_index()
    )

    market["top_items"] = (
        df.sort_values(["需要ウェイト", "レビュー件数", "レビュー平均"], ascending=False)
        .head(15)
        .copy()
    )

    return market


def generate_actions(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    if not analysis:
        return []

    actions: List[Dict[str, str]] = []
    eq_price = analysis.get("eq_price", np.nan)
    eq_low = analysis.get("eq_low", np.nan)
    eq_high = analysis.get("eq_high", np.nan)
    elasticity = analysis.get("elasticity", {})
    own_items = analysis.get("own_items", 0)

    if own_items == 0:
        actions.append(
            {
                "priority": "high",
                "title": "自店SKUの照合を先に通す",
                "body": "今回の検索結果内でアストロの商品が同定できていません。市場比較は見えていますが、自店比較の精度が落ちます。",
                "next": "自店ショップコード、商品名接頭辞、またはSKUマスタを内部データと接続し、結果テーブルへフラグ付けしてください。",
            }
        )
    else:
        gap = analysis.get("price_gap_ratio", np.nan)
        own_median_price = analysis.get("own_median_price", np.nan)
        own_review_median = analysis.get("own_review_median", np.nan)
        market_review_median = analysis.get("median_reviews", np.nan)

        if not np.isnan(gap) and gap > 0.08 and own_review_median <= market_review_median:
            actions.append(
                {
                    "priority": "high",
                    "title": "価格を均衡帯へ寄せるABテストを実施",
                    "body": f"自店中央値 ¥{int(own_median_price):,} が市場均衡帯の上側にあります。レビュー反応が市場中央値以下なら、現価格は取りこぼしの可能性があります。",
                    "next": f"対象SKUを絞り、まずは -3% と -6% の二段階テストで均衡帯 ¥{int(eq_low):,} 〜 ¥{int(eq_high):,} への接近効果を確認してください。",
                }
            )
        elif not np.isnan(gap) and gap < -0.08:
            actions.append(
                {
                    "priority": "mid",
                    "title": "値上げ余地のあるSKUを抽出",
                    "body": f"自店中央値 ¥{int(own_median_price):,} は市場均衡帯より下です。レビュー水準が保てているSKUでは粗利余地を捨てている可能性があります。",
                    "next": f"レビュー評価とCVRが崩れていないSKUから、+3% を起点に段階値上げテストを行い、均衡点 ¥{int(eq_price):,} 付近まで探索してください。",
                }
            )
        else:
            actions.append(
                {
                    "priority": "low",
                    "title": "価格そのものより訴求差を詰める",
                    "body": "自店価格は概ね市場の均衡帯にあります。この状態では価格だけでなく、配送条件、画像、レビュー母数、訴求軸の差が効きます。",
                    "next": "同一価格帯でレビュー件数上位の商品群を抜き出し、訴求ワードと画像構成の差分をテンプレ化してください。",
                }
            )

    if elasticity.get("label") == "high":
        actions.append(
            {
                "priority": "high",
                "title": "価格改定は小刻みに運用",
                "body": "価格感応が高い市場帯です。大きな変更はノイズが乗りやすく、原因の特定が難しくなります。",
                "next": "変更幅は 2% から 5% に抑え、レビュー件数、セッション、転換率を週次で観測してください。",
            }
        )
    elif elasticity.get("label") == "low":
        actions.append(
            {
                "priority": "mid",
                "title": "価格より条件面の改善を優先",
                "body": "価格だけでは説明しきれない市場です。レビュー、送料無料、納期、商品画像の品質差が相対的に効いています。",
                "next": "配送条件と商品LP要素を見直し、同価格帯比較でクリック率とレビュー獲得率の改善を先に狙ってください。",
            }
        )

    band_df = analysis.get("band_df")
    if isinstance(band_df, pd.DataFrame) and not band_df.empty:
        best_band = band_df.iloc[0]
        actions.append(
            {
                "priority": "mid",
                "title": "需要密度の高い価格帯へ寄せる",
                "body": f"現在の観測では、最も魅力度が高い価格帯は {best_band['価格帯ラベル']} です。ここは需要総量に対して商品数の密度がまだ過剰ではありません。",
                "next": "価格、訴求、セット構成をこの帯に合わせて設計し、対象SKUの露出を集中的に増やしてください。",
            }
        )

    return actions[:4]


def fmt_yen(value: float) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "-"
    return f"¥{int(round(value)):,}"


def fmt_num(value: float, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "-"
    return f"{value:.{digits}f}"


def render_metric_card(label: str, value: str, foot: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_signal(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="signal-card">
            <div class="signal-title">{title}</div>
            <div class="signal-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_action_card(priority: str, title: str, body: str, next_step: str) -> None:
    class_name = {
        "high": "priority-high",
        "mid": "priority-mid",
        "low": "priority-low",
    }.get(priority, "priority-low")

    label = {
        "high": "Critical",
        "mid": "Priority",
        "low": "Advisory",
    }.get(priority, "Advisory")

    st.markdown(
        f"""
        <div class="action-card">
            <div class="action-priority {class_name}">{label}</div>
            <div class="action-title">{title}</div>
            <div class="action-body">{body}</div>
            <div class="action-next"><strong>Next:</strong> {next_step}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def price_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(df, x="価格", nbins=24, template="plotly_dark", opacity=0.9)
    fig.update_layout(
        title="Price Distribution",
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
    )
    return fig


def shop_bar_chart(shop_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        shop_df.head(10),
        x="商品数",
        y="店舗名",
        orientation="h",
        template="plotly_dark",
        hover_data=["中央価格", "平均レビュー件数"],
    )
    fig.update_layout(
        title="Shop Presence Top 10",
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        yaxis={"categoryorder": "total ascending"},
    )
    return fig


def scatter_price_review(df: pd.DataFrame, own_shop_name: str, own_shop_code: str) -> go.Figure:
    chart_df = df.copy()
    chart_df["自店"] = "Market"
    own_mask = pd.Series(False, index=chart_df.index)
    if own_shop_code.strip():
        own_mask = own_mask | (chart_df["店舗コード"].fillna("").astype(str).str.lower() == own_shop_code.strip().lower())
    if own_shop_name.strip():
        own_mask = own_mask | chart_df["店舗名"].fillna("").astype(str).str.contains(own_shop_name.strip(), case=False, na=False)
    chart_df.loc[own_mask, "自店"] = "ASTRO"

    fig = px.scatter(
        chart_df,
        x="価格",
        y="レビュー件数",
        color="自店",
        size="需要ウェイト",
        hover_name="商品名",
        hover_data=["店舗名", "レビュー平均"],
        template="plotly_dark",
    )
    fig.update_layout(
        title="Price x Review Momentum",
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
    )
    return fig


def elasticity_gauge(elasticity: Dict[str, Any]) -> go.Figure:
    slope = elasticity.get("slope", np.nan)
    value = 0 if np.isnan(slope) else max(min(abs(slope), 2.0), 0.0)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"font": {"size": 34}},
            title={"text": "Elasticity Proxy Intensity"},
            gauge={
                "axis": {"range": [0, 2]},
                "bar": {"color": "#78b4ff"},
                "bgcolor": "rgba(255,255,255,0.02)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 0.45], "color": "rgba(65,255,214,0.15)"},
                    {"range": [0.45, 1.0], "color": "rgba(255,200,87,0.18)"},
                    {"range": [1.0, 2.0], "color": "rgba(255,107,107,0.18)"},
                ],
            },
        )
    )
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        height=300,
    )
    return fig


def make_download_df(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "取得ページ",
        "商品名",
        "価格",
        "店舗名",
        "店舗コード",
        "ジャンルID",
        "レビュー件数",
        "レビュー平均",
        "在庫あり",
        "送料無料",
        "需要ウェイト",
        "商品URL",
        "画像URL",
    ]
    return df[cols].copy()


inject_css()

application_id = get_secret("RAKUTEN_APPLICATION_ID")
access_key = get_secret("RAKUTEN_ACCESS_KEY")
allowed_origin = get_secret("RAKUTEN_ALLOWED_ORIGIN", "")

st.markdown(
    """
    <div class="mission-hero">
        <div class="eyebrow">ASTRO / MARKET INTELLIGENCE COMMAND</div>
        <h1 class="hero-title">市場を観測し、<br>一手だけを前面に出す。</h1>
        <p class="hero-sub">
            楽天市場の公開データを裏で集約・解析し、表では単純なアクション推奨へ落とし込む司令卓です。
            目標は、価格均衡帯の発見、価格感応度の推定、競争密度の把握、そしてアストロ視点での次の一手の明示です。
        </p>
        <div class="tag-row">
            <div class="tag">Equilibrium Mapping</div>
            <div class="tag">Elasticity Proxy</div>
            <div class="tag">Action Recommendation</div>
            <div class="tag">ASTRO Scope</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not application_id or not access_key:
    st.error("Secrets が不足しています。RAKUTEN_APPLICATION_ID と RAKUTEN_ACCESS_KEY を設定してください。")
    st.code(
        """# .streamlit/secrets.toml
RAKUTEN_APPLICATION_ID = "your_application_id"
RAKUTEN_ACCESS_KEY = "your_access_key"
RAKUTEN_ALLOWED_ORIGIN = "https://your-streamlit-app-url"
"""
    )
    st.stop()

with st.sidebar:
    st.markdown("### Mission Setup")
    keyword = st.text_input("観測キーワード", value="収納")
    own_shop_code = st.text_input("自店ショップコード", value="1storage")
    own_shop_name = st.text_input("自店名称キーワード", value="アストロ")
    api_shop_code = st.text_input("APIフィルタ用ショップコード", value="", help="市場全体を見る場合は空欄のままにしてください。")
    genre_id = st.text_input("ジャンルID", value="")
    sort = st.selectbox(
        "ソート",
        options=["standard", "+itemPrice", "-itemPrice", "+reviewCount", "-reviewCount", "+reviewAverage", "-reviewAverage"],
        index=0,
    )
    pages_to_scan = st.slider("取得ページ数", min_value=1, max_value=5, value=3)
    hits = st.slider("1ページ件数", min_value=10, max_value=30, value=30)
    availability_only = st.checkbox("在庫ありのみ", value=False)

    c1, c2 = st.columns(2)
    with c1:
        min_price = st.number_input("最低価格", min_value=0, value=0, step=500)
    with c2:
        max_price = st.number_input("最高価格", min_value=0, value=0, step=500)

    st.caption("公開市場データを使った観測です。真の需要弾力性ではなく、まずは市場感応度のプロキシを出します。")
    run = st.button("INTELLIGENCE RUN", use_container_width=True)

tabs = st.tabs(["Command Deck", "Market Radar", "Equilibrium Lab", "Evidence"])

if run:
    with st.spinner("市場シグナルを収集中..."):
        market_df, meta = fetch_market_dataset(
            application_id=application_id,
            access_key=access_key,
            allowed_origin=allowed_origin,
            keyword=keyword,
            pages_to_scan=int(pages_to_scan),
            hits=int(hits),
            sort=sort,
            api_shop_code=api_shop_code.strip(),
            genre_id=genre_id.strip(),
            min_price=int(min_price),
            max_price=int(max_price),
            availability_only=availability_only,
        )

    if market_df.empty:
        st.warning("データが取得できませんでした。キーワードや価格条件を見直してください。")
        st.stop()

    analysis = analyze_market(market_df, own_shop_code=own_shop_code, own_shop_name=own_shop_name)
    actions = generate_actions(analysis)

    with tabs[0]:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            foot = f"{meta.get('total_count', '-'):,} 件中のサンプル観測" if meta.get("total_count") else "取得サンプル"
            render_metric_card("Observed Items", f"{analysis['items']:,}", foot)
        with m2:
            render_metric_card("Equilibrium", fmt_yen(analysis["eq_price"]), f"均衡帯 {fmt_yen(analysis['eq_low'])} 〜 {fmt_yen(analysis['eq_high'])}")
        with m3:
            render_metric_card("ASTRO Median", fmt_yen(analysis.get("own_median_price", np.nan)), f"同定SKU数 {analysis.get('own_items', 0):,}")
        with m4:
            render_metric_card("Elasticity Proxy", fmt_num(analysis["elasticity"].get("slope", np.nan), 2), analysis["elasticity"].get("summary", "-"))

        st.markdown("#### Recommended Actions")
        cols = st.columns(4)
        for col, action in zip(cols, actions):
            with col:
                render_action_card(action["priority"], action["title"], action["body"], action["next"])

        st.markdown("#### Mission Signals")
        left, right = st.columns([1.1, 1.2])
        with left:
            gap_ratio = analysis.get("price_gap_ratio", np.nan)
            gap_text = "-" if np.isnan(gap_ratio) else f"{gap_ratio * 100:+.1f}%"
            render_signal(
                "Price Positioning",
                f"自店中央値と市場均衡点のギャップは {gap_text}。価格差だけでなく、レビュー密度と価格感応の組み合わせで判断します。",
            )
            render_signal(
                "Competitive Density",
                f"今回の観測では {analysis['shops']:,} 店舗が出現。多店舗市場では価格差よりも訴求差の積み上げが効きます。",
            )
        with right:
            top_band = analysis["band_df"].iloc[0]
            render_signal(
                "Opportunity Band",
                f"最も魅力度が高い価格帯は {top_band['価格帯ラベル']}。平均価格 {fmt_yen(top_band['平均価格'])}、平均レビュー件数 {fmt_num(top_band['平均レビュー件数'], 1)}。",
            )
            render_signal(
                "Interpretation Notice",
                "ここでの弾力性は、価格とレビュー件数の断面関係から推定した感応度プロキシです。真の需要弾力性は時系列またはABテストで別途検証が必要です。",
            )

    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(price_histogram(market_df), use_container_width=True)
        with c2:
            st.plotly_chart(shop_bar_chart(analysis["top_shops"]), use_container_width=True)

        st.plotly_chart(scatter_price_review(market_df, own_shop_name, own_shop_code), use_container_width=True)

        st.markdown("#### Demand Leaders")
        leader_df = analysis["top_items"][["商品名", "価格", "店舗名", "レビュー件数", "レビュー平均", "需要ウェイト", "商品URL"]].copy()
        st.dataframe(leader_df, use_container_width=True, hide_index=True)

    with tabs[2]:
        e1, e2 = st.columns([0.9, 1.1])
        with e1:
            st.plotly_chart(elasticity_gauge(analysis["elasticity"]), use_container_width=True)
        with e2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### Pricing Logic")
            st.write(
                {
                    "market_equilibrium": fmt_yen(analysis["eq_price"]),
                    "equilibrium_low": fmt_yen(analysis["eq_low"]),
                    "equilibrium_high": fmt_yen(analysis["eq_high"]),
                    "market_median_price": fmt_yen(analysis["median_price"]),
                    "market_mean_price": fmt_yen(analysis["mean_price"]),
                    "astro_median_price": fmt_yen(analysis.get("own_median_price", np.nan)),
                    "proxy_slope": fmt_num(analysis["elasticity"].get("slope", np.nan), 3),
                    "proxy_corr": fmt_num(analysis["elasticity"].get("corr", np.nan), 3),
                }
            )
            st.markdown(
                '<p class="tiny-note">均衡価格はレビュー反応を重みとした重み付き中央値で算出しています。'
                '単純平均ではなく、需要が集まっている価格帯へ寄せて推定します。</p>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### Price Band Opportunity Map")
        band_df = analysis["band_df"].copy()
        band_df["平均価格"] = band_df["平均価格"].round(0)
        band_df["平均レビュー件数"] = band_df["平均レビュー件数"].round(1)
        band_df["平均レビュー評価"] = band_df["平均レビュー評価"].round(2)
        band_df["バンド魅力度"] = band_df["バンド魅力度"].round(2)
        st.dataframe(band_df, use_container_width=True, hide_index=True)

    with tabs[3]:
        st.markdown("#### Raw Market Dataset")
        export_df = make_download_df(market_df)
        st.download_button(
            label="CSV Export",
            data=export_df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"astro_market_intelligence_{keyword}.csv",
            mime="text/csv",
            use_container_width=False,
        )
        st.dataframe(export_df, use_container_width=True, hide_index=True)
else:
    with tabs[0]:
        st.markdown("#### Ready")
        st.markdown(
            """
            このUIは、単純な検索画面ではなく、**市場監視から推奨アクションまでを1枚で返す** ことを目的にしています。

            初回は、アストロの主力カテゴリに寄せて次のようなキーワードから始めると使いやすいです。
            `収納 / 収納ボックス / 衣類収納 / 防災 / 園芸 / キッチン収納`
            """
        )
        st.markdown(
            '<p class="tiny-note">アストロ商品が結果内に含まれるほど、自店比較と推奨精度は上がります。'
            '将来的には、RMSや自社SKUマスタと結合して真の価格実験基盤に拡張する前提です。</p>',
            unsafe_allow_html=True,
        )
