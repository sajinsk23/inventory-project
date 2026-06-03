import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Inventory Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# PREMIUM UI CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* MAIN APP */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 40%,
        #1e3a8a 100%
    );
    color: white;
}

/* REMOVE STREAMLIT DEFAULTS */
header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* MAIN TITLE */
h1 {
    text-align: center;
    color: white !important;
    font-size: 52px !important;
    font-weight: 800 !important;
}

/* HEADINGS */
h2, h3, h4 {
    color: white !important;
    font-weight: 700 !important;
}

/* PARAGRAPHS */
p {
    color: #d1d5db !important;
}

/* KPI CARDS */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 18px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

/* KPI LABELS */
div[data-testid="metric-container"] label {
    color: #cbd5e1 !important;
    font-weight: 600;
}

/* KPI VALUES */
div[data-testid="metric-container"] div {
    color: white !important;
}

/* TABS */
button[data-baseweb="tab"] {
    color: white !important;
    font-size: 16px;
    font-weight: 700;
}

/* ACTIVE TAB */
button[aria-selected="true"] {
    border-bottom: 3px solid #60a5fa !important;
}

/* TABLES */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* TABLE HEADER */
thead tr th {
    background-color: #1e293b !important;
    color: white !important;
}

/* TABLE BODY */
tbody tr td {
    background-color: #f8fafc !important;
    color: #111827 !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton button {
    background: linear-gradient(
        to right,
        #2563eb,
        #1d4ed8
    );
    color: white !important;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #3b82f6;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("inventory_data.csv")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.title("Filters")

warehouse = st.sidebar.selectbox(
    "Select Warehouse",
    ["All"] + list(df["Location"].unique())
)

sku_filter = st.sidebar.selectbox(
    "Select SKU",
    ["All"] + list(df["SKU"].unique())
)

# ---------------------------------------------------
# FILTER LOGIC
# ---------------------------------------------------

filtered_df = df.copy()

if warehouse != "All":
    filtered_df = filtered_df[
        filtered_df["Location"] == warehouse
    ]

if sku_filter != "All":
    filtered_df = filtered_df[
        filtered_df["SKU"] == sku_filter
    ]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Inventory Dashboard")

st.markdown("""
<p style='text-align:center; font-size:18px;'>
Real-Time Inventory Visibility and Analytics Dashboard
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Inventory",
        int(filtered_df["qty"].sum())
    )

with col2:
    st.metric(
        "Total SKUs",
        filtered_df["SKU"].nunique()
    )

with col3:
    st.metric(
        "Warehouses",
        filtered_df["Location"].nunique()
    )

with col4:
    st.metric(
        "Low Stock Items",
        len(filtered_df[filtered_df["qty"] < 20])
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# COMMON CHART LAYOUT
# ---------------------------------------------------

common_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    legend_font_color='white',

    xaxis=dict(
        tickfont=dict(
            color='white',
            size=12
        ),
        showgrid=True,
        gridcolor='rgba(255,255,255,0.15)',
        zeroline=False
    ),

    yaxis=dict(
        tickfont=dict(
            color='white',
            size=12
        ),
        showgrid=True,
        gridcolor='rgba(255,255,255,0.15)',
        zeroline=False
    )
)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Warehouse Analytics",
    "Aging & Dead Stock",
    "Reports"
])

# ===================================================
# TAB 1 - OVERVIEW
# ===================================================

with tab1:

    st.subheader("Inventory Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # INVENTORY BY SKU

    with col1:

        st.subheader("Inventory by SKU")

        stock_by_sku = (
            filtered_df.groupby("SKU")["qty"]
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            stock_by_sku,
            x="SKU",
            y="qty",
            color="qty",
            template="plotly_dark"
        )

        fig1.update_layout(**common_layout)

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # INVENTORY TREND

    with col2:

        st.subheader("Inventory Trend")

        fig2 = px.line(
            filtered_df,
            x="Date",
            y="qty",
            markers=True,
            template="plotly_dark"
        )

        fig2.update_layout(**common_layout)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ===================================================
# TAB 2 - WAREHOUSE ANALYTICS
# ===================================================

with tab2:

    col1, col2 = st.columns(2)

    # INVENTORY DISTRIBUTION

    with col1:

        st.subheader("Inventory Distribution")

        location_stock = (
            filtered_df.groupby("Location")["qty"]
            .sum()
            .reset_index()
        )

        fig3 = px.pie(
            location_stock,
            names="Location",
            values="qty",
            hole=0.4,
            template="plotly_dark"
        )

        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            legend_font_color='white'
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # INVENTORY MOVEMENT

    with col2:

        st.subheader("Inventory Movement")

        movement = (
            filtered_df.groupby("Movement")["qty"]
            .sum()
            .reset_index()
        )

        fig4 = px.bar(
            movement,
            x="Movement",
            y="qty",
            color="Movement",
            template="plotly_dark"
        )

        fig4.update_layout(**common_layout)

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # INVENTORY BY LOCATION

    st.subheader("Inventory by Location")

    fig5 = px.bar(
        location_stock,
        x="Location",
        y="qty",
        color="Location",
        template="plotly_dark"
    )

    fig5.update_layout(**common_layout)

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ===================================================
# TAB 3 - AGING & DEAD STOCK
# ===================================================

with tab3:

    st.subheader("Aging Data")

    aging_data = filtered_df[
        ["SKU", "days_old", "aging_bucket"]
    ]

    st.dataframe(
        aging_data,
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # AGING DISTRIBUTION

    st.subheader("Inventory Aging Distribution")

    aging_count = (
        filtered_df["aging_bucket"]
        .value_counts()
        .reset_index()
    )

    aging_count.columns = [
        "aging_bucket",
        "count"
    ]

    fig6 = px.bar(
        aging_count,
        x="aging_bucket",
        y="count",
        color="aging_bucket",
        template="plotly_dark"
    )

    fig6.update_layout(**common_layout)

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # DEAD STOCK

    st.subheader("Dead Stock")

    dead_stock = filtered_df[
        filtered_df["days_old"] > 90
    ]

    st.dataframe(
        dead_stock,
        use_container_width=True
    )

# ===================================================
# TAB 4 - REPORTS
# ===================================================

with tab4:

    # LOW STOCK REPORT

    st.subheader("Low Stock Report")

    low_stock = filtered_df[
        filtered_df["qty"] < 20
    ]

    st.dataframe(
        low_stock,
        use_container_width=True
    )

    low_stock_csv = low_stock.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Low Stock Report",
        data=low_stock_csv,
        file_name="low_stock_report.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # DEAD STOCK REPORT

    st.subheader("Dead Stock Report")

    st.dataframe(
        dead_stock,
        use_container_width=True
    )

    dead_stock_csv = dead_stock.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Dead Stock Report",
        data=dead_stock_csv,
        file_name="dead_stock_report.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # WAREHOUSE REPORT

    st.subheader("Warehouse Report")

    warehouse_report = (
        filtered_df.groupby("Location")["qty"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        warehouse_report,
        use_container_width=True
    )

    warehouse_csv = warehouse_report.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Warehouse Report",
        data=warehouse_csv,
        file_name="warehouse_report.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # SKU REPORT

    st.subheader("SKU Report")

    sku_report = (
        filtered_df.groupby("SKU")["qty"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        sku_report,
        use_container_width=True
    )

    sku_csv = sku_report.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download SKU Report",
        data=sku_csv,
        file_name="sku_report.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # AGING REPORT

    st.subheader("Aging Report")

    aging_report = filtered_df[
        ["SKU", "days_old", "aging_bucket"]
    ]

    st.dataframe(
        aging_report,
        use_container_width=True
    )

    aging_csv = aging_report.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Aging Report",
        data=aging_csv,
        file_name="aging_report.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # FULL INVENTORY REPORT

    st.subheader("Full Inventory Report")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    inventory_csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Full Inventory Report",
        data=inventory_csv,
        file_name="full_inventory_report.csv",
        mime="text/csv"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<br><br>
<h4 style='text-align:center; color:white;'>
Developed by Sajin SK | Inventory Visibility Engine | ©2026
</h4>
""", unsafe_allow_html=True)