
import pandas as pd
import streamlit as st

from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Google Sheets Connection Check", layout="wide")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_service():
    if "gcp_service_account" not in st.secrets:
        raise RuntimeError("st.secrets に [gcp_service_account] がありません。")
    info = dict(st.secrets["gcp_service_account"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def load_sheet(spreadsheet_id: str, sheet_name: str, range_a1: str = "A:Z") -> pd.DataFrame:
    service = get_service()
    result = (
        service.spreadsheets()
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
    rows = [row + [""] * (width - len(row)) for row in rows]
    return pd.DataFrame(rows, columns=header)


st.title("Google Sheets Private Connection Check")

with st.form("conn"):
    spreadsheet_id = st.text_input("Spreadsheet ID")
    sheet_1 = st.text_input("Sheet 1", value="daily_kpi")
    sheet_2 = st.text_input("Sheet 2", value="market_snapshot")
    submitted = st.form_submit_button("CHECK CONNECTION")

if submitted:
    try:
        df1 = load_sheet(spreadsheet_id, sheet_1)
        df2 = load_sheet(spreadsheet_id, sheet_2)

        st.success("接続成功")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader(sheet_1)
            st.write({"rows": len(df1), "columns": list(df1.columns)})
            st.dataframe(df1.head(10), use_container_width=True, hide_index=True)
        with c2:
            st.subheader(sheet_2)
            st.write({"rows": len(df2), "columns": list(df2.columns)})
            st.dataframe(df2.head(10), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"接続失敗: {e}")

st.markdown(
    """
```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "..."
token_uri = "https://oauth2.googleapis.com/token"
```
"""
)
