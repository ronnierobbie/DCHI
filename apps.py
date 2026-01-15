import streamlit as st
import pandas as pd
from io import BytesIO

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Court Inventory Dashboard",
    layout="wide",
)

# ======================================================
# PASSWORD PROTECTION
# ======================================================
def check_password():
    def password_entered():
        st.session_state["password_correct"] = (
            st.session_state["password"] == "court2026"
        )
        del st.session_state["password"]

    if "password_correct" not in st.session_state:
        st.text_input(
            "Please enter the dashboard password:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False

    if not st.session_state["password_correct"]:
        st.text_input(
            "Please enter the dashboard password:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("Password incorrect")
        return False

    return True


# ======================================================
# MATERIAL 3 THEME SYSTEM
# ======================================================
def inject_material_theme(theme: str):
    if theme == "Dark":
        palette = {
            "primary": "#D0BCFF",
            "on_primary": "#381E72",
            "surface": "#1C1B1F",
            "surface_variant": "#49454F",
            "background": "#141218",
            "on_surface": "#E6E1E5",
            "error": "#F2B8B5",
            "secondary": "#CCC2DC",
        }
    else:
        palette = {
            "primary": "#6750A4",
            "on_primary": "#FFFFFF",
            "surface": "#FFFBFE",
            "surface_variant": "#E7E0EC",
            "background": "#F5F3F7",
            "on_surface": "#1C1B1F",
            "error": "#B3261E",
            "secondary": "#625B71",
        }

    st.markdown(
        f"""
        <style>
        :root {{
            --md-primary: {palette["primary"]};
            --md-on-primary: {palette["on_primary"]};
            --md-surface: {palette["surface"]};
            --md-surface-variant: {palette["surface_variant"]};
            --md-background: {palette["background"]};
            --md-on-surface: {palette["on_surface"]};
            --md-error: {palette["error"]};
            --md-secondary: {palette["secondary"]};
        }}

        .stApp {{
            background-color: var(--md-background);
            color: var(--md-on-surface);
            font-family: Roboto, Segoe UI, sans-serif;
        }}

        .material-card {{
            background-color: var(--md-surface);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.3);
            border: 1px solid var(--md-surface-variant);
            margin-bottom: 16px;
        }}

        .card-title {{
            font-size: 12px;
            font-weight: 500;
            color: var(--md-secondary);
            text-transform: uppercase;
            margin-bottom: 4px;
        }}

        .card-value {{
            font-size: 22px;
            font-weight: 600;
        }}

        .badge {{
            margin-top: 8px;
            display: inline-block;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 500;
        }}

        .badge-green {{
            background-color: #1E4620;
            color: #C8E6C9;
        }}

        .badge-red {{
            background-color: var(--md-error);
            color: #000000;
        }}

        .badge-grey {{
            background-color: var(--md-surface-variant);
        }}

        .section-header {{
            font-size: 22px;
            font-weight: 600;
            color: var(--md-primary);
            margin: 32px 0 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# MATERIAL ICONS (INLINE SVG)
# ======================================================
def material_icon(name):
    icons = {
        "court": """<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M3 21h18v-2H3v2zm2-4h14V3H5v14zm2-2V5h10v10H7z"/></svg>""",
        "download": """<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M5 20h14v-2H5v2zm7-18l-5 5h3v6h4v-6h3l-5-5z"/></svg>""",
    }
    return icons.get(name, "")


# ======================================================
# MATERIAL CARD COMPONENTS
# ======================================================
def metric_card(title, value, icon=None):
    icon_html = material_icon(icon) if icon else ""
    st.markdown(
        f"""
        <div class="material-card">
            <div>{icon_html}</div>
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hardware_card(title, distributed, required, balance):
    if balance > 0:
        cls, txt = "badge-green", "Surplus"
    elif balance < 0:
        cls, txt = "badge-red", "Shortfall"
    else:
        cls, txt = "badge-grey", "Balanced"

    st.markdown(
        f"""
        <div class="material-card">
            <div class="card-title">{title}</div>
            <div class="card-value">{int(distributed)} / {int(required)}</div>
            <span class="badge {cls}">{txt}: {abs(int(balance))}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# DATA LOADING
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx", sheet_name="Tooli")
    df.columns = df.columns.str.strip()
    df["State"] = df["State"].ffill()
    df["Session_Division"] = df["Session_Division"].ffill()
    numeric = [
        "Required_Qty",
        "Distributed_Qty",
        "Balance_Qty",
        "Courts_Count",
        "Family_Courts",
        "TJOs",
        "Total_Courts",
    ]
    df[numeric] = df[numeric].apply(pd.to_numeric, errors="coerce").fillna(0)
    return df


# ======================================================
# EXPORT
# ======================================================
def to_excel(df):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buf.getvalue()


# ======================================================
# MAIN APP
# ======================================================
if check_password():

    st.sidebar.title("Settings")
    theme = st.sidebar.radio("Theme", ["Light", "Dark"], horizontal=True)
    inject_material_theme(theme)

    df = load_data()

    st.title("Court Inventory Dashboard")

    states = ["All States"] + sorted(df["State"].unique().tolist())
    sel_state = st.sidebar.selectbox("State", states)
    data = df if sel_state == "All States" else df[df["State"] == sel_state]

    divisions = ["Overall Summary"] + sorted(data["Session_Division"].unique())
    sel_div = st.sidebar.selectbox("Session Division", divisions)

    if sel_div == "Overall Summary":
        st.markdown("<div class='section-header'>Overall Summary</div>", unsafe_allow_html=True)

        courts = data.drop_duplicates("Location_Name")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Total Courts", int(courts["Total_Courts"].sum()), "court")
        with c2:
            metric_card("Regular Courts", int(courts["Courts_Count"].sum()))
        with c3:
            metric_card("Family Courts", int(courts["Family_Courts"].sum()))
        with c4:
            metric_card("TJOs", int(courts["TJOs"].sum()))

        hw = (
            data.groupby("Hardware_Item")[
                ["Distributed_Qty", "Required_Qty", "Balance_Qty"]
            ]
            .sum()
            .reset_index()
        )

        cols = st.columns(6)
        for i, r in hw.iterrows():
            with cols[i % 6]:
                hardware_card(
                    r["Hardware_Item"],
                    r["Distributed_Qty"],
                    r["Required_Qty"],
                    r["Balance_Qty"],
                )

        st.dataframe(
            data[
                [
                    "State",
                    "Session_Division",
                    "Location_Name",
                    "Hardware_Item",
                    "Required_Qty",
                    "Distributed_Qty",
                    "Balance_Qty",
                    "Status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("<div class='section-header'>Download</div>", unsafe_allow_html=True)
    st.download_button(
        "Download Excel",
        data=to_excel(data),
        file_name="inventory.xlsx",
    )
