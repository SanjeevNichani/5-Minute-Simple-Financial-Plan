import streamlit as st
from datetime import datetime

# Set page config
st.set_page_config(page_title="Smart Money Map", page_icon="💰", layout="wide")

# Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h1>💰 SMART MONEY MAP</h1>
        <h3>Get a Super Simple Financial Plan in 5 Minutes</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("Using your annual CTC and savings rate, get personalized thumb-rule guidance across protection, spending, and wealth-building.")

# User input
st.markdown("### 👤 Enter Your Info")
ctc = st.slider("Annual CTC (₹ Lakhs)", 10.0, 100.0, 25.0, step=1.0)
savings_rate = st.slider("Monthly Savings Rate (%)", 10.0, 100.0, 50.0, step=5.0)

# Calculations
monthly_take_home = 0.75 * ctc * 1e5 / 12
monthly_savings = (savings_rate / 100) * monthly_take_home
monthly_expenses = monthly_take_home - monthly_savings

# Define rules
rules = [
    {
        "name": "Emergency Fund",
        "rule": "3–6× Monthly Expenses",
        "min": 3 * monthly_expenses,
        "max": 6 * monthly_expenses,
        "user": 4 * monthly_expenses
    },
    {
        "name": "Health Insurance",
        "rule": "₹5L – ₹10L",
        "min": 5e5,
        "max": 10e5,
        "user": 6e5
    },
    {
        "name": "Life Insurance",
        "rule": "10–15× Annual CTC",
        "min": 10 * ctc * 1e5,
        "max": 15 * ctc * 1e5,
        "user": 12 * ctc * 1e5
    },
    {
        "name": "Car Budget",
        "rule": "≤ 60% of CTC",
        "max": 0.6 * ctc * 1e5,
        "user": 0.5 * ctc * 1e5
    },
    {
        "name": "Home Purchase",
        "rule": "≤ 4× CTC",
        "max": 4 * ctc * 1e5,
        "user": 3 * ctc * 1e5
    },
    {
        "name": "Personal Loans + Credit Cards",
        "rule": "Ideally zero",
        "max": 0,
        "user": 0
    },
    {
        "name": "All EMIs",
        "rule": "≤ 45% of Take-Home",
        "max": 0.45 * monthly_take_home,
        "user": 0.4 * monthly_take_home
    },
    {
        "name": "Monthly SIP",
        "rule": "> 20% of CTC",
        "min": 0.20 * ctc * 1e5 / 12,
        "user": monthly_savings
    },
    {
        "name": "Retirement Corpus",
        "rule": "> 10× CTC",
        "min": 10 * ctc * 1e5,
        "user": 11 * ctc * 1e5
    }
]

# Evaluate and display
st.markdown("### 📋 Your Results")
met_count = 0
summary_lines = []

for r in rules:
    status = ""
    if "min" in r and "max" in r:
        if r["min"] <= r["user"] <= r["max"]:
            status = "🟢 On Track"
        elif r["user"] >= 0.5 * r["min"]:
            status = "🟡 Almost There"
        else:
            status = "🔴 Needs Attention"
    elif "min" in r:
        status = "🟢 On Track" if r["user"] >= r["min"] else "🔴 Needs Attention"
    elif "max" in r:
        status = "🟢 On Track" if r["user"] <= r["max"] else "🔴 Needs Attention"

    if status.startswith("🟢"):
        met_count += 1

    st.write(f"**{r['name']}** — {r['rule']} → {status}")
    summary_lines.append(f"{r['name']} ({r['rule']}): {status}")

# Progress message
st.success(f"🎯 Progress: {met_count}/9 rules met")

# Create downloadable TXT summary
today = datetime.now().strftime("%d-%b-%Y")
txt_summary = f"""SMART MONEY MAP – Financial Summary
Generated on: {today}

INPUTS:
- Annual CTC: ₹{ctc:.2f} L
- Savings Rate: {savings_rate:.0f}%
- Monthly Take-Home: ₹{monthly_take_home / 1e5:.2f} L
- Monthly Savings: ₹{monthly_savings / 1e3:.1f} K

RULE CHECK RESULTS:
"""

for line in summary_lines:
    txt_summary += f"- {line}\n"

txt_summary += f"\nTOTAL: {met_count}/9 thumb rules met.\n"

if met_count == 9:
    txt_summary += "🎉 CONGRATULATIONS! You're on top of your finances.\n"
elif met_count >= 6:
    txt_summary += "👏 You're doing well! Tidy up the rest.\n"
elif met_count >= 3:
    txt_summary += "👍 You're getting started. Focus on protection and planning.\n"
else:
    txt_summary += "💪 It's never too late to take control. Start with the basics.\n"

txt_summary += "\nDISCLAIMER: This is a thumb-rule-based tool, not personalized advice.\n"

# Download button
st.download_button(
    label="📄 Download My Financial Plan (TXT)",
    data=txt_summary,
    file_name=f"smart_money_map_{today}.txt",
    mime="text/plain"
)
