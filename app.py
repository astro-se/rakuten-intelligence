
import time
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import streamlit as st


# =========================
# Streamlit config
# =========================
st.set_page_config(
    page_title="Rakuten Intelligence",
    layout="wide",
    page_icon="📈",
)

PUBLIC_ITEM_SEARCH_URL = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"
PUBLIC_RANKING_URL = "https://openapi.rakuten.co.jp/ichibaranking/api/IchibaItem/Ranking/20220601"

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


# =========================
# Utilities
# =========================
def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    try:
        return st.secrets[name]
    except Exception:
        return default


def ensure_rate_limit() -> None:
    """
    Rakuten Web Service is documented at <= 1 request per second per application_id.
    """
    last_called = st.session_state.get("_rakuten_last_called", 0.0)
    elapsed = time.time() - last_called
    wait = max(0.0, 1.05 - elapsed)
    if wait > 0:
        time.sleep(wait)
    st.session_state["_rakuten_last_called"] = time.time()


class RakutenAPIError(Exception):
    pass


class RakutenClient:
    def __init__(self, application_id: str, access_key: str, timeout: int = 20):
        self.application_id = application_id
        self.access_key = access_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Rakuten-Intelligence/1.0",
                "Accept": "application/json",
            }
        )

    def _get(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        ensure_rate_limit()

        params = {
            "format": "json",
            "applicationId": self.application_id,
            "accessKey": self.access_key,
            **params,
        }

        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, dict) and "error" in data:
            raise RakutenAPIError(
                f"{data.get('error')} / {data.get('error_description', 'unknown error')}"
            )
        return data

    @st.cache_data(ttl=3600, show_spinner=False)
    def search_items_cached(
        _self,
        keyword: str,
        page: int,
        hits: int,
        sort: str,
        shop_code: str,
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

        if shop_code:
            params["shopCode"] = shop_code
        if genre_id:
            params["genreId"] = genre_id
        if min_price > 0:
            params["minPrice"] = min_price
        if max_price > 0:
            params["maxPrice"] = max_price
        if availability_only:
            params["availability"] = 1

        return _self._get(PUBLIC_ITEM_SEARCH_URL, params)

    @st.cache_data(ttl=3600, show_spinner=False)
    def ranking_cached(
        _self,
        genre_id: str,
        age: str,
        sex: str,
        page: int,
        realtime: bool,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "page": page,
            "formatVersion": 2,
        }
        if genre_id:
            params["genreId"] = genre_id
        if age:
            params["age"] = age
        if sex != "":
            params["sex"] = sex
        if realtime:
            params["period"] = "realtime"

        return _self._get(PUBLIC_RANKING_URL, params)


def normalize_items(items: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in items:
        images = item.get("mediumImageUrls", []) or []
        image_url = None
        if images:
            first_img = images[0]
            if isinstance(first_img, dict):
                image_url = first_img.get("imageUrl")
            elif isinstance(first_img, str):
                image_url = first_img

        rows.append(
            {
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
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def normalize_ranking_items(items: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in items:
        rows.append(
            {
                "順位": item.get("rank"),
                "商品名": item.get("itemName"),
                "価格": item.get("itemPrice"),
                "店舗名": item.get("shopName"),
                "レビュー件数": item.get("reviewCount"),
                "レビュー平均": item.get("reviewAverage"),
                "商品URL": item.get("itemUrl"),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        for col in ["順位", "価格", "レビュー件数", "レビュー平均"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def show_market_kpis(df: pd.DataFrame) -> None:
    if df.empty:
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("商品件数", f"{len(df):,}")
    c2.metric("平均価格", f"¥{int(df['価格'].dropna().mean()):,}" if df["価格"].dropna().size else "-")
    c3.metric("中央値価格", f"¥{int(df['価格'].dropna().median()):,}" if df["価格"].dropna().size else "-")
    c4.metric("平均レビュー", f"{df['レビュー平均'].dropna().mean():.2f}" if df["レビュー平均"].dropna().size else "-")
    c5.metric("ユニーク店舗数", f"{df['店舗コード'].nunique():,}")

    st.caption("公開APIベースの市場ビューです。受注・出荷・在庫・広告実績などの店舗内部データは別系統です。")


def show_market_charts(df: pd.DataFrame) -> None:
    if df.empty:
        return

    left, right = st.columns(2)

    with left:
        st.subheader("価格分布")
        price_hist = (
            df["価格"]
            .dropna()
            .astype(int)
            .value_counts(bins=10, sort=False)
            .rename_axis("価格帯")
            .reset_index(name="件数")
        )
        if not price_hist.empty:
            st.bar_chart(price_hist.set_index("価格帯"))

    with right:
        st.subheader("店舗出現数 上位10")
        shop_counts = (
            df.groupby("店舗名", dropna=False)
            .size()
            .sort_values(ascending=False)
            .head(10)
            .rename("商品数")
            .to_frame()
        )
        st.bar_chart(shop_counts)

    st.subheader("取得データ")
    st.dataframe(df, use_container_width=True, hide_index=True)


def explain_architecture() -> None:
    st.info(
        """
        このMVPは **公開APIで市場データを可視化する層** です。  
        真の店舗BIにする場合は、次の2層構成が現実的です。

        1. **公開市場データ層**  
           商品検索API / ランキングAPI / ジャンルAPIで、市場価格帯・競合店・ランキング変動を取得

        2. **店舗内部データ層**  
           RMS系APIまたは外部連携で、受注・出荷・在庫・広告・SKU別粗利を取得

        そのうえで BigQuery などに蓄積し、Streamlit は可視化フロントとして使うのが筋です。
        """
    )


# =========================
# App
# =========================
st.title("⚡ Rakuten Intelligence")
st.caption("楽天市場の公開データを使って、市場俯瞰と競合観測を行うBIのMVPです。")

application_id = get_secret("RAKUTEN_APPLICATION_ID")
access_key = get_secret("RAKUTEN_ACCESS_KEY")

if not application_id or not access_key:
    st.error(
        "Secrets が未設定です。`RAKUTEN_APPLICATION_ID` と `RAKUTEN_ACCESS_KEY` を Streamlit Secrets に設定してください。"
    )
    st.code(
        """# .streamlit/secrets.toml
RAKUTEN_APPLICATION_ID = "your_application_id"
RAKUTEN_ACCESS_KEY = "your_access_key"
"""
    )
    st.stop()

client = RakutenClient(application_id=application_id, access_key=access_key)

with st.sidebar:
    st.header("検索条件")
    mode = st.radio("モード", ["市場検索", "ランキング"], index=0)

    if mode == "市場検索":
        keyword = st.text_input("キーワード", value="バッグ")
        shop_code = st.text_input("店舗コード（任意）", value="")
        genre_id = st.text_input("ジャンルID（任意）", value="")
        hits = st.slider("取得件数 / ページ", min_value=1, max_value=30, value=30)
        page = st.number_input("ページ", min_value=1, max_value=100, value=1, step=1)
        sort = st.selectbox(
            "並び順",
            [
                "standard",
                "+itemPrice",
                "-itemPrice",
                "+reviewCount",
                "-reviewCount",
                "+reviewAverage",
                "-reviewAverage",
            ],
            index=0,
        )

        col1, col2 = st.columns(2)
        with col1:
            min_price = st.number_input("最低価格", min_value=0, value=0, step=500)
        with col2:
            max_price = st.number_input("最高価格", min_value=0, value=0, step=500)

        availability_only = st.checkbox("在庫ありのみ", value=False)
        run_btn = st.button("市場分析を実行", use_container_width=True)

    else:
        genre_id = st.text_input("ジャンルID（任意）", value="")
        age = st.selectbox("年代", ["", "10", "20", "30", "40", "50"], index=0)
        sex = st.selectbox("性別", [("", "指定なし"), ("0", "男性"), ("1", "女性")], index=0, format_func=lambda x: x[1])[0]
        page = st.number_input("ページ", min_value=1, max_value=34, value=1, step=1)
        realtime = st.checkbox("リアルタイムランキング", value=True)
        run_btn = st.button("ランキング取得", use_container_width=True)

tab1, tab2 = st.tabs(["ダッシュボード", "設計メモ"])

with tab1:
    if run_btn:
        try:
            if mode == "市場検索":
                raw = client.search_items_cached(
                    keyword=keyword,
                    page=int(page),
                    hits=int(hits),
                    sort=sort,
                    shop_code=shop_code.strip(),
                    genre_id=genre_id.strip(),
                    min_price=int(min_price),
                    max_price=int(max_price),
                    availability_only=availability_only,
                )

                items = raw.get("Items") or raw.get("items") or []
                df = normalize_items(items)

                if df.empty:
                    st.warning("データが取得できませんでした。検索条件を見直してください。")
                else:
                    show_market_kpis(df)
                    show_market_charts(df)

                    with st.expander("APIレスポンス概要"):
                        st.write(
                            {
                                "count": raw.get("count"),
                                "page": raw.get("page"),
                                "pageCount": raw.get("pageCount"),
                                "hits": raw.get("hits"),
                            }
                        )

            else:
                raw = client.ranking_cached(
                    genre_id=genre_id.strip(),
                    age=age,
                    sex=sex,
                    page=int(page),
                    realtime=realtime,
                )
                items = raw.get("Items") or raw.get("items") or []
                df = normalize_ranking_items(items)

                c1, c2, c3 = st.columns(3)
                c1.metric("取得件数", f"{len(df):,}")
                c2.metric("タイトル", raw.get("title", "-"))
                c3.metric("最終更新", raw.get("lastBuildDate", "-"))

                st.dataframe(df, use_container_width=True, hide_index=True)

        except requests.HTTPError as e:
            st.error(f"HTTPエラー: {e}")
        except RakutenAPIError as e:
            st.error(f"Rakuten APIエラー: {e}")
        except Exception as e:
            st.exception(e)
    else:
        st.write("左の条件を指定して実行してください。")
        explain_architecture()

with tab2:
    st.markdown(
        """
### このコードで直した点

- `applicationSecret` を使う設計をやめ、`applicationId + accessKey` に変更
- エンドポイントを `openapi.rakuten.co.jp` に更新
- `formatVersion=2` を使い、JSON構造をシンプル化
- `elements` を指定して必要項目だけ取得
- 1秒1回のレート制限に合わせた簡易スロットリングを実装
- `st.cache_data` でAPI呼び出しを抑制
- BIらしく、平均価格・中央値・店舗数・レビューを可視化
- 将来のRMS連携を見据え、公開市場データ層と内部データ層を分離

### 次にやるべきこと

1. **市場データBIとして磨く**  
   キーワード別価格帯、店舗シェア、ランキング変動、レビュー構造を追加する

2. **店舗BIに進む**  
   RMS系APIの申請・権限整理を行い、自社受注・SKU在庫・広告費を別テーブルで統合する

3. **データ基盤化する**  
   Streamlit 直叩きではなく、定期取得 → DWH格納 → BI表示の流れにする
        """
    )
