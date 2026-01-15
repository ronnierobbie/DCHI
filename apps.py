import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. Page Configuration ---
st.set_page_config(page_title="Court Inventory Dashboard", layout="wide")

# ========================================== 
# 🔒 PASSWORD PROTECTION SECTION
# ========================================== 
def check_password():
    def password_entered():
        if st.session_state["password"] == "court2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    
    if "password_correct" not in st.session_state:
        st.text_input("Please enter the dashboard password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Please enter the dashboard password:", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # ========================================== 
    # 🎨 THEME TOGGLE INITIALIZATION
    # ========================================== 
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # ========================================== 
    # ✨ BREEZE DASHBOARD STYLING (Custom Colors)
    # ========================================== 
    def get_material_you_css(dark_mode):
        if dark_mode:
            # Dark Mode Palette
            colors = {
                'bg_primary': '#1a1c1e',
                'bg_secondary': '#2b2d30',
                'bg_tertiary': '#3a3d41',
                'surface': '#2b2d30',
                'surface_variant': '#43474e',
                'primary': '#423ABE',
                'primary_container': '#2f2890',
                'secondary': '#00CCCD',
                'secondary_container': '#008b8c',
                'accent_yellow': '#FFC107',
                'accent_pink': '#DC3545',
                'accent_green': '#198754',
                'accent_blue': '#0D6EFD',
                'success': '#81c784',
                'success_container': '#1b5e20',
                'error': '#f28b82',
                'error_container': '#8c1d18',
                'text_primary': '#e3e3e3',
                'text_secondary': '#c4c6c8',
                'text_tertiary': '#9aa0a6',
                'border': '#5f6368',
                'shadow': 'rgba(0, 0, 0, 0.5)',
            }
        else:
            # Light Mode Palette
            colors = {
                'bg_primary': '#f8f9fa',
                'bg_secondary': '#ffffff',
                'bg_tertiary': '#e9ecef',
                'surface': '#ffffff',
                'surface_variant': '#f1f3f5',
                'primary': '#423ABE',
                'primary_container': '#e8e6f7',
                'secondary': '#00CCCD',
                'secondary_container': '#e0f7f7',
                'accent_yellow': '#FFC107',
                'accent_pink': '#DC3545',
                'accent_green': '#198754',
                'accent_blue': '#0D6EFD',
                'success': '#198754',
                'success_container': '#d4edda',
                'error': '#DC3545',
                'error_container': '#f8d7da',
                'text_primary': '#212529',
                'text_secondary': '#495057',
                'text_tertiary': '#6c757d',
                'border': '#dee2e6',
                'shadow': 'rgba(0, 0, 0, 0.1)',
            }
        
        return f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
        
        .stApp {{
            background: linear-gradient(135deg, {colors['bg_primary']} 0%, {colors['bg_secondary']} 100%);
            font-family: 'Roboto', sans-serif;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* Material You Card */
        .material-card {{
            background: {colors['surface']};
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px 1px {colors['shadow']};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid {colors['border']};
        }}
        
        .material-card:hover {{
            box-shadow: 0 4px 8px 3px {colors['shadow']};
            transform: translateY(-2px);
        }}
        
        /* Section Headers */
        .section-header {{
            color: {colors['text_primary']} !important;
            font-weight: 700;
            padding: 16px 0;
            margin: 24px 0 16px 0;
            font-size: 24px;
            letter-spacing: 0.1px;
            border-bottom: 2px solid {colors['primary']};
        }}
        
        /* Fix text visibility in light mode */
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: {colors['text_primary']} !important;
        }}
        
        .stMarkdown {{
            color: {colors['text_primary']} !important;
        }}
        
        [data-testid="stMarkdownContainer"] {{
            color: {colors['text_primary']} !important;
        }}
        
        .stCaption {{
            color: {colors['text_secondary']} !important;
        }}
        
        /* Card Content */
        .card-title {{
            color: {colors['text_tertiary']};
            font-size: 12px;
            text-transform: uppercase;
            font-weight: 500;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .card-value {{
            color: {colors['text_primary']};
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: 0.15px;
        }}
        
        /* Material Badges */
        .badge {{
            padding: 6px 16px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 0.5px;
            display: inline-block;
            transition: all 0.2s ease;
        }}
        
        .badge-green {{
            background: {colors['success_container']};
            color: {colors['success']};
        }}
        
        .badge-red {{
            background: {colors['error_container']};
            color: {colors['error']};
        }}
        
        .badge-grey {{
            background: {colors['surface_variant']};
            color: {colors['text_secondary']};
        }}
        
        /* Streamlit Overrides */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px 1px {colors['shadow']};
        }}
        
        .stMetric {{
            background: {colors['surface']};
            padding: 16px;
            border-radius: 12px;
            border: 1px solid {colors['border']};
        }}
        
        .stMetric label {{
            color: {colors['text_secondary']} !important;
            font-weight: 500 !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            color: {colors['text_primary']} !important;
            font-weight: 700 !important;
        }}
        
        /* Title styling */
        h1 {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: {colors['surface']};
            border-right: 1px solid {colors['border']};
        }}
        
        [data-testid="stSidebar"] .stSelectbox label {{
            color: {colors['text_primary']} !important;
            font-weight: 500 !important;
        }}
        
        [data-testid="stSidebar"] h1 {{
            color: {colors['text_primary']} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Buttons */
        .stDownloadButton button {{
            background: {colors['primary_container']} !important;
            color: {colors['primary']} !important;
            border: none !important;
            border-radius: 20px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stDownloadButton button:hover {{
            box-shadow: 0 4px 8px {colors['shadow']} !important;
            transform: translateY(-2px);
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: {colors['surface_variant']} !important;
            color: {colors['text_primary']} !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }}
        
        /* Theme Toggle Button */
        .theme-toggle {{
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 999;
            background: {colors['primary_container']};
            border: 2px solid {colors['primary']};
            border-radius: 50%;
            width: 56px;
            height: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 8px {colors['shadow']};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .theme-toggle:hover {{
            transform: scale(1.1) rotate(15deg);
            box-shadow: 0 6px 12px {colors['shadow']};
        }}
        
        .theme-icon {{
            font-size: 24px;
        }}
        </style>
        """
    
    st.markdown(get_material_you_css(st.session_state.dark_mode), unsafe_allow_html=True)
    
    # --- 3. Data Loading ---
    @st.cache_data
    def load_data():
        try:
            df = pd.read_excel('data.xlsx', sheet_name='Tooli')
            df.columns = df.columns.str.strip()
            
            string_cols = ['State', 'Session_Division', 'Location_Name', 'Location_Type', 'Hardware_Item', 'Status']
            for col in string_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
            
            if 'State' in df.columns:
                df['State'] = df['State'].replace('nan', pd.NA).ffill()
            if 'Session_Division' in df.columns:
                df['Session_Division'] = df['Session_Division'].replace('nan', pd.NA).ffill()
            
            numeric_cols = ['Required_Qty', 'Distributed_Qty', 'Balance_Qty', 'Courts_Count', 'Family_Courts', 'TJOs', 'Total_Courts']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    df = load_data()
    
    # --- 4. Export Helper ---
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dashboard_Data')
        return output.getvalue()
    
    def render_material_card(title, value_top, value_bottom, balance):
        # Assign color based on hardware item
        color_map = {
            0: 'card-yellow',
            1: 'card-pink',
            2: 'card-blue',
            3: 'card-green',
            4: 'card-purple',
            5: 'card-cyan'
        }
        
        # Icon map for hardware items
        icon_map = {
            0: '💻',
            1: '📊',
            2: '🖥️',
            3: '🔌',
            4: '⚙️',
            5: '📡'
        }
        
        # Get a consistent color based on the title
        color_index = hash(title) % 6
        card_color = color_map[color_index]
        card_icon = icon_map[color_index]
        
        if balance > 0:
            b_class, b_text = "badge-green", "✓ Surplus"
        elif balance < 0:
            b_class, b_text = "badge-red", "⚠ Shortfall"
        else:
            b_class, b_text = "badge-grey", "● Balanced"
        
        html = f"""
        <div class="material-card {card_color}">
            <div class="card-icon">{card_icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-value">${int(value_top):,}</div>
            <div class="card-subtitle">Required: ${int(value_bottom):,}</div>
            <span class="badge {b_class}">{b_text}: {int(abs(balance))}</span>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    # --- 5. Theme Toggle Button ---
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button(theme_icon, key="theme_toggle", help="Toggle Dark/Light Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # --- 6. Navigation & Main Logic ---
    if df is not None:
        st.sidebar.title("🧭 Navigation")
        
        # State Filter
        unique_states = ['All States'] + sorted(df['State'].unique().tolist())
        sel_state = st.sidebar.selectbox("Select State", unique_states, index=0)
        state_df = df if sel_state == 'All States' else df[df['State'] == sel_state]
        
        # Session Division Filter
        unique_divs = ['📊 Overall Summary'] + sorted(state_df['Session_Division'].unique().tolist())
        sel_div = st.sidebar.selectbox("Select Session Division", unique_divs, index=0)
        
        st.title("🏛️ Court Inventory Dashboard")
        
        # --------------------------------------------------------- 
        # CASE 1: OVERALL SUMMARY (Default Landing Page)
        # --------------------------------------------------------- 
        if sel_div == '📊 Overall Summary':
            st.markdown(f'<div class="section-header">🌍 Overall Aggregated Summary: {sel_state}</div>', unsafe_allow_html=True)
            
            # Aggregate Courts
            court_sum_df = state_df.drop_duplicates(subset=['Location_Name'])
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Courts", int(court_sum_df['Total_Courts'].sum()))
            m2.metric("Regular", int(court_sum_df['Courts_Count'].sum()))
            m3.metric("Family", int(court_sum_df['Family_Courts'].sum()))
            m4.metric("TJOs", int(court_sum_df['TJOs'].sum()))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Aggregate Hardware Cards
            hw_summary = state_df.groupby('Hardware_Item')[['Distributed_Qty', 'Required_Qty', 'Balance_Qty']].sum().reset_index()
            cols = st.columns(6)
            for idx, row in hw_summary.iterrows():
                with cols[idx % 6]:
                    render_material_card(row['Hardware_Item'], row['Distributed_Qty'], row['Required_Qty'], row['Balance_Qty'])
            
            # Detailed Table
            st.markdown('<div class="section-header">📋 Detailed Records List</div>', unsafe_allow_html=True)
            final_table = state_df[['State', 'Session_Division', 'Location_Name', 'Hardware_Item', 'Required_Qty', 'Distributed_Qty', 'Balance_Qty', 'Status']]
            st.dataframe(final_table, use_container_width=True, hide_index=True)
        
        # --------------------------------------------------------- 
        # CASE 2: HIERARCHICAL SESSION DIVISION DETAIL
        # --------------------------------------------------------- 
        else:
            div_data = state_df[state_df['Session_Division'] == sel_div]
            
            # A. DIVISION SUMMARY
            st.markdown(f'<div class="section-header">📊 Aggregated District Total: {sel_div}</div>', unsafe_allow_html=True)
            
            unique_locs = div_data.drop_duplicates(subset=['Location_Name'])
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Courts", int(unique_locs['Total_Courts'].sum()))
            m2.metric("Regular", int(unique_locs['Courts_Count'].sum()))
            m3.metric("Family", int(unique_locs['Family_Courts'].sum()))
            m4.metric("TJOs", int(unique_locs['TJOs'].sum()))
            
            agg_hw = div_data.groupby('Hardware_Item')[['Distributed_Qty', 'Required_Qty', 'Balance_Qty']].sum().reset_index()
            cols = st.columns(6)
            for idx, row in agg_hw.iterrows():
                with cols[idx % 6]:
                    render_material_card(row['Hardware_Item'], row['Distributed_Qty'], row['Required_Qty'], row['Balance_Qty'])
            
            # B. HEADQUARTERS
            hq_data = div_data[div_data['Location_Type'] == 'Session']
            if not hq_data.empty:
                hq_name = hq_data.iloc[0]['Location_Name']
                st.markdown(f'<div class="section-header">🏠 Headquarters: {hq_name}</div>', unsafe_allow_html=True)
                
                meta = hq_data.iloc[0]
                st.caption(f"Courts Distribution — Total: {int(meta['Total_Courts'])} | Reg: {int(meta['Courts_Count'])} | Fam: {int(meta['Family_Courts'])} | TJO: {int(meta['TJOs'])}")
                
                cols = st.columns(6)
                for idx, (i, row) in enumerate(hq_data.iterrows()):
                    with cols[idx % 6]:
                        render_material_card(row['Hardware_Item'], row['Distributed_Qty'], row['Required_Qty'], row['Balance_Qty'])
            
            # C. SUB-DIVISIONS
            sub_divs = div_data[div_data['Location_Type'] == 'SubDivision']
            if not sub_divs.empty:
                st.markdown(f'<div class="section-header">📍 Sub-Divisions Detail</div>', unsafe_allow_html=True)
                
                for sub_name in sorted(sub_divs['Location_Name'].unique()):
                    specific_sub = sub_divs[sub_divs['Location_Name'] == sub_name]
                    meta = specific_sub.iloc[0]
                    
                    with st.expander(f"🔹 {sub_name} (Total Courts: {int(meta['Total_Courts'])})", expanded=True):
                        cols = st.columns(6)
                        for idx, (i, row) in enumerate(specific_sub.iterrows()):
                            with cols[idx % 6]:
                                render_material_card(row['Hardware_Item'], row['Distributed_Qty'], row['Required_Qty'], row['Balance_Qty'])
            
            # D. HIERARCHICAL TABLE
            st.markdown('<div class="section-header">📋 Hardware Records Table</div>', unsafe_allow_html=True)
            final_table = div_data[['Location_Name', 'Location_Type', 'Hardware_Item', 'Required_Qty', 'Distributed_Qty', 'Balance_Qty', 'Status']]
            st.dataframe(final_table, use_container_width=True, hide_index=True)
        
        # --------------------------------------------------------- 
        # DOWNLOAD CENTER
        # --------------------------------------------------------- 
        st.markdown("### 📥 Download Center")
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                label="📄 Download CSV",
                data=final_table.to_csv(index=False),
                file_name=f"inventory_{sel_div}.csv",
                mime="text/csv"
            )
        with c2:
            st.download_button(
                label="📊 Download Excel",
                data=to_excel(final_table),
                file_name=f"inventory_{sel_div}.xlsx"
            )
    
    else:
        st.error("Data could not be loaded. Please check data.xlsx.")
