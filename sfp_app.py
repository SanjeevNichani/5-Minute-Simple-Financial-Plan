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

# Custom CSS for styling
st.markdown("""
<style>
.main-title {
    background-color: #4A5568;
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 30px;
}
.input-tile {
    background-color: #F7FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
}
.metric-tile {
    background-color: #EDF2F7;
    border: 1px solid #CBD5E0;
    border-radius: 10px;
    padding: 15px;
    margin: 5px 0;
    text-align: center;
}
.notes-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Main title with grey background
st.markdown("""
<div class="main-title">
    <h1> SMART MONEY MAP</h1>
    <h3>Get a Super Simple Financial Plan in 5 minutes!</h3>
</div>
""", unsafe_allow_html=True)

# Intro text
st.markdown("""
Enter your CTC and savings rate below, and this tool will show you saving, spending, and investing limits 
based on widely accepted financial "thumb rules". Think of it as your first-cut financial plan and checklist.
""")

# User Input Section - 2 tiles side by side
st.markdown("### 📊 Enter Your Details")
input_col1, input_col2 = st.columns(2)

with input_col1:
    st.markdown('<div class="input-tile">', unsafe_allow_html=True)
    st.markdown("#### 💰 Annual CTC (Lakhs)")
    ctc_method = st.radio(
        "Choose input method:",
        ["Number Input", "Slider"],
        key="ctc_method",
        horizontal=True
    )
    
    if ctc_method == "Number Input":
        ctc = st.number_input(
            "Enter your CTC:", 
            min_value=0.0, 
            value=25.0,
            step=0.5,
            help="Your gross annual income in lakhs"
        )
    else:
        ctc = st.slider(
            "Select your CTC:",
            min_value=10.0,
            max_value=100.0,
            value=25.0,
            step=1.0,
            help="Your gross annual income in lakhs"
        )
    st.markdown('</div>', unsafe_allow_html=True)

with input_col2:
    st.markdown('<div class="input-tile">', unsafe_allow_html=True)
    st.markdown("#### 💵 Savings Rate (%)")
    savings_method = st.radio(
        "Choose input method:",
        ["Number Input", "Slider"],
        key="savings_method", 
        horizontal=True
    )
    
    if savings_method == "Number Input":
        savings_rate = st.number_input(
            "Enter % you can save:", 
            min_value=0.0, 
            max_value=100.0,
            value=50.0,
            step=5.0,
            help="What percentage of your monthly take-home can you save?"
        )
    else:
        savings_rate = st.slider(
            "Select % you can save:",
            min_value=10.0,
            max_value=100.0, 
            value=50.0,
            step=5.0,
            help="What percentage of your monthly take-home can you save?"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Your original calculations (unchanged)
monthly_take_home = 0.75 * ctc * 1e5 / 12  # assuming 25% deductions
monthly_expenses = (100 - savings_rate) * 1e-2 * monthly_take_home

# Calculated Metrics - 2 tiles side by side
st.markdown("### 📈 Your Financial Summary")
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.markdown('<div class="metric-tile">', unsafe_allow_html=True)
    st.markdown("#### 💳 Monthly Take-Home")
    st.markdown(f"### ₹{monthly_take_home*1e-5:.2f} L")
    st.caption("*After 25% deductions for PF+Tax")
    st.markdown('</div>', unsafe_allow_html=True)

with metric_col2:
    st.markdown('<div class="metric-tile">', unsafe_allow_html=True)
    st.markdown("#### 💰 Monthly Savings")
    st.markdown(f"### ₹{savings_rate*1e-2*monthly_take_home*1e-3:.1f} K")
    st.caption(f"*{savings_rate:.0f}% of your take-home salary")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Instructions
st.info("💡 **How to use**: Check the boxes below for areas where you meet the suggested ranges. Your progress will be counted!")

# Initialize session state for checkboxes
if 'checkboxes' not in st.session_state:
    st.session_state.checkboxes = [False] * 9  # 9 total checkboxes

# Table 1: PROTECTION (replaces your df1)
st.markdown("### 🛡️ STAGE 1: PROTECTION")

# Create checkboxes for table 1
col1, col2 = st.columns([4, 1])
with col1:
    df1 = pd.DataFrame({
        "Category": ["Emergency Fund", "Health Insurance", "Life Insurance"],
        "Thumb Rule": ["3–6× Monthly Expenses", "₹5L – ₹10L", "10–15× Annual CTC"],
        "Min Value": [f"₹{monthly_expenses*3/1e5:.1f} L", "₹5L", f"₹{ctc*10*1e-2:.2f} Cr"],
        "Max Value": [f"₹{monthly_expenses*6/1e5:.1f} L", "₹10L", f"₹{ctc*15*1e-2:.2f} Cr"]
    })
    st.dataframe(df1, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**I'm on track:**")
    st.session_state.checkboxes[0] = st.checkbox("Emergency Fund", key="check0")
    st.session_state.checkboxes[1] = st.checkbox("Health Insurance", key="check1") 
    st.session_state.checkboxes[2] = st.checkbox("Life Insurance", key="check2")

# Table 2: SPENDING LIMITS (replaces your df2)
st.markdown("### 💳 STAGE 2: SPENDING LIMITS")

col3, col4 = st.columns([4, 1])
with col3:
    df2 = pd.DataFrame({
        "Category": ["Car Budget", "Home Purchase Price", "Personal Loans + Credit Card Dues", "All EMIs Combined"],
        "Thumb Rule": ["≤ 60% of CTC", "≤ 4× Annual CTC", "Ideally zero", "≤ 45% of Monthly Take Home"],
        "Max Value": [f"₹{ctc*0.6:.2f} L", f"₹{ctc*4*1e-2:.2f} Cr", "Zero", f"₹{monthly_take_home*0.45*1e-3:.1f} K"]
    })
    st.dataframe(df2, use_container_width=True, hide_index=True)

with col4:
    st.markdown("**I'm on track:**")
    st.session_state.checkboxes[3] = st.checkbox("Car Budget", key="check3")
    st.session_state.checkboxes[4] = st.checkbox("Home Price", key="check4")
    st.session_state.checkboxes[5] = st.checkbox("No Personal Loans", key="check5")
    st.session_state.checkboxes[6] = st.checkbox("EMI Limit", key="check6")

# Table 3: WEALTH BUILDING (replaces your df3)
st.markdown("### 📈 STAGE 3: WEALTH BUILDING")

col5, col6 = st.columns([4, 1])
with col5:
    df3 = pd.DataFrame({
        "Category": ["Monthly SIP", "Retirement Corpus"],
        "Thumb Rule": ["> 20% of CTC", ">10x Annual CTC"],
        "Min Value": [f"₹{ctc*0.20*1e2/12:.0f} K", f"₹{ctc*10*1e-2:.2f} Cr"]
    })
    st.dataframe(df3, use_container_width=True, hide_index=True)

with col6:
    st.markdown("**I'm on track:**")
    st.session_state.checkboxes[7] = st.checkbox("Monthly SIP", key="check7")
    st.session_state.checkboxes[8] = st.checkbox("Retirement Planning", key="check8")

# Count checked boxes and show progress
total_checked = sum(st.session_state.checkboxes)
st.markdown("---")
st.success(f"🎯 **Progress: {total_checked}/9 thumb rules completed!**")

# Notes section with attractive styling
st.markdown("""
<div class="notes-section">
    <h3>📝 Notes & Assumptions</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
        <div>
            <p><strong>💼 CTC:</strong> Gross annual income in LPA</p>
            <p><strong>💰 Deductions:</strong> 25% assumed for tax + PF</p>
        </div>
        <div>
            <p><strong>⚖️ Disclaimer:</strong> Thumb-rule suggestions, NOT personalized advice</p>
            <p><strong>📊 Rounding:</strong> Values rounded to nearest ₹K, ₹L or ₹Cr</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Download functionality (NEW FEATURE!)
st.markdown("---")
today = datetime.now().strftime("%d-%b-%Y")
st.markdown(f"📅 **Snapshot Date:** {today}")

# Create detailed status for each rule
rule_names = [
    "Emergency Fund", "Health Insurance", "Life Insurance",
    "Car Budget", "Home Purchase Price", "Personal Loans + Credit Cards", "All EMIs Combined",
    "Monthly SIP", "Retirement Corpus Planning"
]

rule_details = [
    f"Emergency Fund: {monthly_expenses*3/1e5:.1f}L - {monthly_expenses*6/1e5:.1f}L",
    "Health Insurance: ₹5L - ₹10L",
    f"Life Insurance: {ctc*10*1e-2:.2f}Cr - {ctc*15*1e-2:.2f}Cr",
    f"Car Budget: ≤ ₹{ctc*0.6:.2f}L",
    f"Home Purchase: ≤ ₹{ctc*4*1e-2:.2f}Cr", 
    "Personal Loans & Credit Cards: Zero",
    f"Total EMIs: ≤ ₹{monthly_take_home*0.45*1e-3:.1f}K",
    f"Monthly SIP: > ₹{ctc*0.20*1e2/12:.0f}K",
    f"Retirement Corpus: > ₹{ctc*10*1e-2:.2f}Cr"
]

# Create a summary for download with checkbox status
summary_text = f"""
SMART MONEY MAP - Financial Plan Summary
Generated on: {today}

INPUT DETAILS:
- Annual CTC: ₹{ctc:.2f} L
- Savings Rate: {savings_rate:.0f}%
- Monthly Take-Home: ₹{monthly_take_home*1e-5:.2f} L
- Monthly Savings: ₹{savings_rate*1e-2*monthly_take_home*1e-3:.1f} K

THUMB RULE CHECKLIST:
"""

# Add each rule with Met/Not Met status
for i, (name, detail) in enumerate(zip(rule_names, rule_details)):
    status = "✅ MET" if st.session_state.checkboxes[i] else "❌ NOT MET"
    summary_text += f"{i+1}. {detail} - {status}\n"

summary_text += f"""
PROGRESS SUMMARY: {total_checked}/9 thumb rules completed

"""

# Add congratulations text at the bottom
congratulations_text = ""
if total_checked == 9:
    congratulations_text = f"🎉 CONGRATULATIONS! You've completed all {total_checked} out of 9 thumb rules. You're on an excellent financial track!"
elif total_checked >= 6:
    congratulations_text = f"👏 Great progress! You've completed {total_checked} out of 9 thumb rules. You're doing well financially."
elif total_checked >= 3:
    congratulations_text = f"👍 Good start! You've completed {total_checked} out of 9 thumb rules. Keep working on the remaining areas."
else:
    congratulations_text = f"💪 You've completed {total_checked} out of 9 thumb rules. There's room for improvement - focus on the basics first!"

summary_text += f"""{congratulations_text}

NOTES:
- CTC is gross annual income in LPA
- 25% deductions assumed for tax + PF
- These are thumb-rule suggestions, NOT personalized financial advice
- All values rounded to nearest ₹K, ₹L or ₹Cr as needed
"""

st.download_button(
    label="📄 Download Your Financial Plan",
    data=summary_text,
    file_name=f"financial_plan_{today}.txt",
    mime="text/plain"
)

# Footer
st.markdown("---")
