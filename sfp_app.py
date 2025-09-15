# Smart Money Map - Streamlit Web App Version
import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Smart Money Map",
    page_icon="💰",
    layout="wide"
)

# Main title
st.title("💰 SMART MONEY MAP")
st.subheader("Your Super Simple Financial Plan")
st.markdown("---")

# Sidebar for inputs (this replaces your input() functions)
st.sidebar.header("📊 Enter Your Details")

# Replace get_float() with Streamlit input widgets
ctc = st.sidebar.number_input(
    "Enter your CTC in Lakhs per annum:", 
    min_value=0.0, 
    value=25.0,  # Default value
    step=0.5,
    help="Your gross annual income in lakhs"
)

savings_rate = st.sidebar.number_input(
    "Enter % of monthly salary you can save:", 
    min_value=0.0, 
    max_value=100.0,
    value=50.0,  # Default value
    step=5.0,
    help="What percentage of your monthly take-home can you save?"
)

# Your original calculations (unchanged)
monthly_take_home = 0.75 * ctc * 1e5 / 12  # assuming 25% deductions
monthly_expenses = (100 - savings_rate) * 1e-2 * monthly_take_home

# Display key metrics at the top (replaces your print statements)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Annual CTC", f"₹{ctc:.2f} L")
with col2:
    st.metric("Savings Rate", f"{savings_rate:.0f}%")
with col3:
    st.metric("Monthly Take-Home", f"₹{monthly_take_home*1e-5:.2f} L")
with col4:
    st.metric("Monthly Savings", f"₹{savings_rate*1e-2*monthly_take_home*1e-3:.1f} K")

st.caption("*Assumption: 25% deductions for PF+Tax")
st.markdown("---")

# Instructions
st.info("💡 **How to use**: Review each table below and mentally check off ✅ areas where you're within the suggested range.")

# Table 1: PROTECTION (replaces your df1)
st.markdown("### 🛡️ STAGE 1: PROTECTION")
df1 = pd.DataFrame({
    "Category": ["Emergency Fund", "Health Insurance", "Life Insurance"],
    "Thumb Rule": ["3–6× Monthly Expenses", "₹5L – ₹10L", "10–15× Annual CTC"],
    "Min Value": [f"₹{monthly_expenses*3/1e5:.1f} L", "₹5L", f"₹{ctc*10*1e-2:.2f} Cr"],
    "Max Value": [f"₹{monthly_expenses*6/1e5:.1f} L", "₹10L", f"₹{ctc*15*1e-2:.2f} Cr"],
    "Status": ["⬜", "⬜", "⬜"]  # Checkboxes for user reference
})
st.dataframe(df1, use_container_width=True, hide_index=True)

# Table 2: SPENDING LIMITS (replaces your df2)
st.markdown("### 💳 STAGE 2: SPENDING LIMITS")
df2 = pd.DataFrame({
    "Category": ["Car Budget", "Home Purchase Price", "Personal Loans + Credit Card Dues", "All EMIs Combined"],
    "Thumb Rule": ["≤ 60% of CTC", "≤ 4× Annual CTC", "Ideally zero", "≤ 45% of Monthly Take Home"],
    "Max Value": [f"₹{ctc*0.6:.2f} L", f"₹{ctc*4*1e-2:.2f} Cr", "Zero", f"₹{monthly_take_home*0.45*1e-3:.1f} K"],
    "Status": ["⬜", "⬜", "⬜", "⬜"]
})
st.dataframe(df2, use_container_width=True, hide_index=True)

# Table 3: WEALTH BUILDING (replaces your df3)
st.markdown("### 📈 STAGE 3: WEALTH BUILDING")
df3 = pd.DataFrame({
    "Category": ["Monthly SIP", "Retirement Corpus"],
    "Thumb Rule": ["> 20% of CTC", ">10x Annual CTC"],
    "Min Value": [f"₹{ctc*0.20*1e2/12:.0f} K", f"₹{ctc*10*1e-2:.2f} Cr"],
    "Status": ["⬜", "⬜"]
})
st.dataframe(df3, use_container_width=True, hide_index=True)

# Notes section (replaces your print statements)
st.markdown("---")
st.markdown("### 📝 Notes & Assumptions")
st.markdown("""
1. CTC is gross annual income in LPA.
2. Approx 25% of CTC is assumed for tax + PF deductions.
3. These are thumb-rule suggestions, NOT personalized financial advice.
4. All values rounded to nearest ₹K, ₹L or ₹Cr as needed.
""")

# Download functionality (NEW FEATURE!)
st.markdown("---")
today = datetime.now().strftime("%d-%b-%Y")
st.markdown(f"📅 **Snapshot Date:** {today}")

# Create a summary for download
summary_text = f"""
SMART MONEY MAP - Financial Plan Summary
Generated on: {today}

INPUT DETAILS:
- Annual CTC: ₹{ctc:.2f} L
- Savings Rate: {savings_rate:.0f}%
- Monthly Take-Home: ₹{monthly_take_home*1e-5:.2f} L
- Monthly Savings: ₹{savings_rate*1e-2*monthly_take_home*1e-3:.1f} K

PROTECTION TARGETS:
- Emergency Fund: ₹{monthly_expenses*3/1e5:.1f} L - ₹{monthly_expenses*6/1e5:.1f} L
- Health Insurance: ₹5L - ₹10L
- Life Insurance: ₹{ctc*10*1e-2:.2f} Cr - ₹{ctc*15*1e-2:.2f} Cr

SPENDING LIMITS:
- Car Budget: ≤ ₹{ctc*0.6:.2f} L
- Home Price: ≤ ₹{ctc*4*1e-2:.2f} Cr
- Personal Loans: Zero
- Total EMIs: ≤ ₹{monthly_take_home*0.45*1e-3:.1f} K

WEALTH BUILDING TARGETS:
- Monthly SIP: > ₹{ctc*0.20*1e2/12:.0f} K
- Retirement Corpus: > ₹{ctc*10*1e-2:.2f} Cr
"""

st.download_button(
    label="📄 Download Your Financial Plan",
    data=summary_text,
    file_name=f"financial_plan_{today}.txt",
    mime="text/plain"
)

# Footer
st.markdown("---")
st.markdown("*💡 Save this page or download the summary for future reference!*")