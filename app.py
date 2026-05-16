import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG
st.set_page_config(
    page_title="PhonePe Dashboard",
    layout="wide"
)

# LOAD DATA FROM CSV (works on Streamlit Cloud)
df_agg_txn  = pd.read_csv("aggregated_transaction.csv")
df_agg_user = pd.read_csv("aggregated_user.csv")
df_agg_ins  = pd.read_csv("aggregated_insurance.csv")
df_map_txn  = pd.read_csv("map_transaction.csv")
df_map_user = pd.read_csv("map_user.csv")

# TITLE
st.title("📱 PhonePe Transaction Insights Dashboard")

st.markdown("---")

# SIDEBAR
st.sidebar.header("FILTERS")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df_agg_txn["year"].unique())
)

quarter = st.sidebar.selectbox(
    "Select Quarter",
    sorted(df_agg_txn["quarter"].unique())
)

# FILTER DATA
filtered_txn = df_agg_txn[
    (df_agg_txn["year"] == year) &
    (df_agg_txn["quarter"] == quarter)
]

filtered_user = df_agg_user[
    (df_agg_user["year"] == year) &
    (df_agg_user["quarter"] == quarter)
]

# KPI SECTION
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_amount       = filtered_txn["amount"].sum()
total_transactions = filtered_txn["count"].sum()
total_users        = filtered_user["count"].sum()
avg_transaction    = total_amount / total_transactions if total_transactions > 0 else 0

col1.metric("Total Transaction Amount", f"₹ {total_amount:,.0f}")
col2.metric("Total Transactions",       f"{total_transactions:,.0f}")
col3.metric("Total Users",              f"{total_users:,.0f}")
col4.metric("Average Transaction",      f"₹ {avg_transaction:.2f}")

st.markdown("---")

# TOP STATES
st.subheader("🏆 Top 10 States by Transaction Amount")

top_states = (
    filtered_txn.groupby("state")["amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))
top_states.plot(kind="bar", ax=ax1, color="#6366f1")
ax1.set_xlabel("State")
ax1.set_ylabel("Amount (₹)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig1)

# TRANSACTION TYPES
st.subheader("💳 Transaction Type Distribution")

txn_type = filtered_txn.groupby("transaction_type")["count"].sum()

fig2, ax2 = plt.subplots(figsize=(8, 8))
txn_type.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
plt.tight_layout()
st.pyplot(fig2)

# YEARLY GROWTH
st.subheader("📈 Yearly Transaction Growth")

yearly = df_agg_txn.groupby("year")["amount"].sum()

fig3, ax3 = plt.subplots(figsize=(10, 5))
yearly.plot(marker="o", ax=ax3, color="#22c55e", linewidth=2)
ax3.set_ylabel("Transaction Amount (₹)")
ax3.set_xlabel("Year")
plt.tight_layout()
st.pyplot(fig3)

# TOP MOBILE BRANDS
st.subheader("📱 Top Mobile Brands")

brands = (
    filtered_user.groupby("brand")["count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4, ax4 = plt.subplots(figsize=(10, 5))
brands.plot(kind="bar", ax=ax4, color="#f59e0b")
ax4.set_xlabel("Brand")
ax4.set_ylabel("User Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig4)

# DISTRICT ANALYSIS
st.subheader("🗺️ Top Districts by Transaction Amount")

districts = (
    df_map_txn.groupby("district")["amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig5, ax5 = plt.subplots(figsize=(10, 5))
districts.plot(kind="bar", ax=ax5, color="#3b82f6")
ax5.set_xlabel("District")
ax5.set_ylabel("Amount (₹)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig5)

# INSURANCE ANALYSIS
st.subheader("🛡️ Insurance Growth Over Years")

insurance = df_agg_ins.groupby("year")["amount"].sum()

fig6, ax6 = plt.subplots(figsize=(10, 5))
insurance.plot(marker="o", ax=ax6, color="#ec4899", linewidth=2)
ax6.set_ylabel("Insurance Amount (₹)")
ax6.set_xlabel("Year")
plt.tight_layout()
st.pyplot(fig6)

# USER ENGAGEMENT
st.subheader("👥 Top 10 States by App Opens")

engagement = (
    df_map_user.groupby("state")["app_opens"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig7, ax7 = plt.subplots(figsize=(10, 5))
engagement.plot(kind="bar", ax=ax7, color="#10b981")
ax7.set_xlabel("State")
ax7.set_ylabel("App Opens")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig7)

# INSIGHTS SECTION
st.markdown("---")
st.subheader("📌 Business Insights")

st.write("""
1. Maharashtra and Karnataka dominate digital payments.
2. Peer-to-peer payments contribute the highest transaction share.
3. Xiaomi and Samsung are the most popular mobile brands.
4. Insurance adoption has rapidly increased after 2021.
5. User engagement is highest in metro states.
6. Transaction growth has increased consistently every year.
""")