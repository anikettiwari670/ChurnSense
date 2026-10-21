from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from theme import apply_theme


# =========================================================
# CONFIGURATION
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

apply_theme()


# =========================================================
# HOME PAGE STYLING
# =========================================================

st.markdown(
    """
<style>
.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
}

/* HERO BANNER */

.hero {
    padding: 34px 36px;
    border-radius: 20px;
    background:
        radial-gradient(
            circle at 90% 15%,
            rgba(94, 234, 212, 0.16),
            transparent 32%
        ),
        linear-gradient(
            125deg,
            #14213D,
            #173B55 65%,
            #164E63
        );
    border: 1px solid #2C536B;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
}

.hero-eyebrow {
    color: #5EEAD4;
    text-transform: uppercase;
    letter-spacing: 2.2px;
    font-size: 11px;
    font-weight: 750;
    margin-bottom: 12px;
}

.hero-title {
    color: #F8FAFC;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.2px;
    margin: 0 0 10px 0;
    line-height: 1.15;
}

.hero-description {
    color: #CBDDEE;
    font-size: 15px;
    line-height: 1.7;
    max-width: 750px;
    margin: 0;
}

.hero-tag {
    display: inline-block;
    margin-top: 20px;
    padding: 7px 12px;
    border: 1px solid #387486;
    border-radius: 20px;
    background: rgba(15, 118, 110, 0.18);
    color: #99F6E4;
    font-size: 11px;
    font-weight: 650;
}

/* SECTION HEADINGS */

.section-heading {
    color: #F1F5F9;
    font-size: 21px;
    font-weight: 750;
    letter-spacing: -0.4px;
    margin: 12px 0 4px 0;
}

.section-subtitle {
    color: #A7B7CB;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 18px;
}

/* KPI CARDS */

.kpi-card {
    background: linear-gradient(
        145deg,
        #18263D,
        #111C2F
    );
    border: 1px solid #2A3C56;
    border-radius: 16px;
    padding: 21px;
    min-height: 145px;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.12);
    transition: border-color 0.2s ease,
                transform 0.2s ease;
}

.kpi-card:hover {
    border-color: #438A91;
    transform: translateY(-2px);
}

.kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 16px;
}

.kpi-label {
    color: #A7B7CB;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 1px;
}

.kpi-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: #20384B;
    color: #5EEAD4;
    font-size: 17px;
}

.kpi-value {
    color: #F8FAFC;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.8px;
    line-height: 1.2;
}

.kpi-note {
    color: #A7B7CB;
    font-size: 12px;
    margin-top: 10px;
}

/* CHART CONTAINERS */

[data-testid="stPlotlyChart"] {
    background: linear-gradient(
        145deg,
        #141F32,
        #101A2B
    );
    border: 1px solid #273851;
    border-radius: 16px;
    padding: 8px 8px 2px 8px;
    margin-bottom: 12px;
}

/* FOOTER */

.footer {
    border-top: 1px solid #26364D;
    color: #94A3B8;
    text-align: center;
    font-size: 12px;
    padding-top: 22px;
    margin-top: 25px;
    line-height: 1.8;
}

/* RESPONSIVE LAYOUT */

@media (max-width: 768px) {
    .hero {
        padding: 24px 21px;
    }

    .hero-title {
        font-size: 30px;
    }

    .kpi-card {
        padding: 16px;
        min-height: 130px;
    }

    .kpi-value {
        font-size: 25px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        f"Dataset not found: {DATA_PATH}. "
        "Ensure the CSV exists in the repository's data folder."
    )
    st.stop()

except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.stop()


# =========================================================
# VALIDATE DATA
# =========================================================

required_columns = {"Churn", "Contract"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(
        "Dataset is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

if df.empty:
    st.warning("The dataset contains no customer records.")
    st.stop()


# =========================================================
# BUSINESS METRICS
# =========================================================

churn_text = df["Churn"].astype(str).str.strip().str.lower()
churn_mask = churn_text.eq("yes")

total_customers = len(df)
churned = int(churn_mask.sum())
retained = total_customers - churned

churn_rate = churned / total_customers * 100
retention_rate = retained / total_customers * 100


# =========================================================
# HERO SECTION
# IMPORTANT: Keep HTML tags unindented inside this string.
# This prevents Markdown from displaying them as code.
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-eyebrow">CUSTOMER INTELLIGENCE PLATFORM</div>
<div class="hero-title">ChurnSense</div>
<p class="hero-description">Turn Customer Data into Actionable Retention Insights. Monitor Churn Patterns, Explore Customer Behaviour, and Support Smarter, Data-Driven Retention Decisions.</p>
<div class="hero-tag">CUSTOMER ANALYTICS | CHURN INTELLIGENCE</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# BUSINESS OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-heading">Business Overview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">'
    'Monitor the Key Indicators of Customer Retention and Churn.'
    '</div>',
    unsafe_allow_html=True,
)

kpis = [
    (
        "TOTAL CUSTOMERS",
        f"{total_customers:,}",
        "Customer Records Analyzed",
        "👥",
    ),
    (
        "CHURNED CUSTOMERS",
        f"{churned:,}",
        "Customers who Left",
        "↗",
    ),
    (
        "RETENTION RATE",
        f"{retention_rate:.1f}%",
        "Customers Retained",
        "✓",
    ),
    (
        "CHURN RATE",
        f"{churn_rate:.1f}%",
        "Customers who Churned",
        "⚠",
    ),
]

columns = st.columns(4, gap="medium")

for col, (label, value, note, symbol) in zip(columns, kpis):
    with col:
        st.markdown(
            f"""
<div class="kpi-card">
<div class="kpi-top">
<div class="kpi-label">{label}</div>
<div class="kpi-icon">{symbol}</div>
</div>
<div class="kpi-value">{value}</div>
<div class="kpi-note">{note}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.write("")


# =========================================================
# CHART STYLING
# =========================================================

def style_chart(fig, height=365):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=20, r=20, t=65, b=30),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#CBD5E1",
        ),
        title=dict(
            font=dict(size=16, color="#F1F5F9"),
            x=0.03,
            xanchor="left",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color="#CBD5E1",
                size=11,
            ),
        ),
        xaxis=dict(
            gridcolor="#26364D",
            linecolor="#35465F",
            zerolinecolor="#35465F",
            tickfont=dict(color="#CBD5E1"),
            title_font=dict(color="#CBD5E1"),
        ),
        yaxis=dict(
            gridcolor="#26364D",
            linecolor="#35465F",
            zerolinecolor="#35465F",
            tickfont=dict(color="#CBD5E1"),
            title_font=dict(color="#CBD5E1"),
        ),
    )

    return fig


# =========================================================
# CUSTOMER ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-heading">Customer Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">'
    'Understand Customer Outcomes and Identify Patterns Associated with Churn.'
    '</div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")


# =========================================================
# CHART 1: CUSTOMER RETENTION MIX
# =========================================================

with left:
    churn_counts = pd.DataFrame(
        {
            "Churn Status": ["Retained", "Churned"],
            "Customers": [retained, churned],
        }
    )

    fig = px.pie(
        churn_counts,
        names="Churn Status",
        values="Customers",
        hole=0.68,
        title="Customer Retention Mix",
        color="Churn Status",
        color_discrete_map={
            "Retained": "#5EEAD4",
            "Churned": "#FB7185",
        },
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(size=13, color="#FFFFFF"),
        marker=dict(
            line=dict(color="#141F32", width=3)
        ),
        sort=False,
    )

    fig.add_annotation(
        text=f"<b>{total_customers:,}</b><br>Customers",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=17, color="#F1F5F9"),
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# CHART 2: CUSTOMER OUTCOMES BY CONTRACT
# =========================================================

with right:
    contract_data = df[["Contract"]].copy()

    contract_data["Churn Status"] = churn_text.map(
        {
            "yes": "Churned",
            "no": "Retained",
        }
    )

    contract_counts = (
        contract_data
        .dropna()
        .groupby(
            ["Contract", "Churn Status"],
            observed=True,
        )
        .size()
        .reset_index(name="Customers")
    )

    fig = px.bar(
        contract_counts,
        x="Contract",
        y="Customers",
        color="Churn Status",
        barmode="group",
        title="Customer Outcomes by Contract",
        color_discrete_map={
            "Retained": "#5EEAD4",
            "Churned": "#FB7185",
        },
        category_orders={
            "Churn Status": ["Retained", "Churned"]
        },
    )

    fig.update_layout(
        xaxis_title="Contract Type",
        yaxis_title="Number of Customers",
        bargap=0.25,
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# CHART 3: MONTHLY CHARGES
# =========================================================

if "MonthlyCharges" in df.columns:
    st.markdown(
        '<div class="section-heading">Customer Spending</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Compare Monthly Charges Between Retained and Churned Customers.'
        '</div>',
        unsafe_allow_html=True,
    )

    charges_df = pd.DataFrame(
        {
            "MonthlyCharges": pd.to_numeric(
                df["MonthlyCharges"],
                errors="coerce",
            ),
            "Churn Status": churn_text.map(
                {
                    "yes": "Churned",
                    "no": "Retained",
                }
            ),
        }
    ).dropna()

    fig = px.box(
        charges_df,
        x="Churn Status",
        y="MonthlyCharges",
        color="Churn Status",
        color_discrete_map={
            "Retained": "#5EEAD4",
            "Churned": "#FB7185",
        },
        title="Monthly Charges by Churn Status",
        points=False,
        category_orders={
            "Churn Status": ["Retained", "Churned"]
        },
    )

    fig.update_layout(
        xaxis_title="Customer Outcome",
        yaxis_title="Monthly Charges",
        showlegend=False,
    )

    st.plotly_chart(
        style_chart(fig, height=390),
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# CUSTOMER DATA EXPLORER
# =========================================================

with st.expander("🔎 Explore the Underlying Customer Data"):
    st.caption(
        f"Previewing the first 100 rows of "
        f"{total_customers:,} customer records."
    )

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="⬇ Download Customer Dataset",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="churnsense_customer_data.csv",
        mime="text/csv",
        type="primary",
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
ChurnSense · Customer Analytics &amp; Churn Intelligence
<br><br>
Transforming Customer Data into Actionable Insights
</div>
""",
    unsafe_allow_html=True,
)