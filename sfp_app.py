import streamlit as st
from datetime import datetime
from fpdf import FPDF
import base64

# Set page config
st.set_page_config(page_title="Smart Money Map", page_icon="💰", layout="wide")

# Main Title
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h1>💰 SMART MONEY MAP</h1>
        <h3>Get a super simple financial plan in 5 minutes</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("Using your annual CTC and savings rate, get personalized financial thumb-rule checks.")

# User Input
st.markdown("### 🔢 Input Your Info")
ctc = st.slider("Annual CTC (in ₹ Lakhs)", 10.0, 100.0, 25.0, step=1.0)
savings_rate = st.slider("Savings Rate (%)", 10.0, 100.0, 50.0, step=5.0)

# Calculations
monthly_take_home = 0.75 * ctc * 1e5 / 12
monthly_savings = (savings_rate / 100) * monthly_take_home
monthly_expenses = monthly_take_home - monthly_savings

# Rule definitions
rules = [
    {
        "category": "Emergency Fund",
        "rule": "3–6× Monthly Expenses",
        "min": 3 * monthly_expenses,
        "max": 6 * monthly_expenses,
        "user_value": monthly_savings * 2  # Placeholder
    },
    {
        "category": "Health Insurance",
        "rule": "₹5L – ₹10L",
        "min": 5e5,
        "max": 10e5,
        "user_value": 6e5  # Placeholder
    },
    {
        "category": "Life Insurance",
        "rule": "10–15× Annual CTC",
        "min": 10 * ctc * 1e5,
        "max": 15 * ctc * 1e5,
        "user_value": 12 * ctc * 1e5  # Placeholder
    },
    {
        "category": "Car Budget",
        "rule": "≤ 60% of CTC",
        "max": 0.6 * ctc * 1e5,
        "user_value": 0.5 * ctc * 1e5
    },
    {
        "category": "Home Purchase",
        "rule": "≤ 4× Annual CTC",
        "max": 4 * ctc * 1e5,
        "user_value": 3 * ctc * 1e5
    },
    {
        "category": "Personal Loans + Credit Cards",
        "rule": "Ideally zero",
        "max": 0,
        "user_value": 0  # Assume no loans
    },
    {
        "category": "Total EMIs",
        "rule": "≤ 45% of Take-Home",
        "max": 0.45 * monthly_take_home,
        "user_value": 0.4 * monthly_take_home
    },
    {
        "category": "Monthly SIP",
        "rule": "> 20% of CTC (Annual)",
        "min": 0.20 * ctc * 1e5 / 12,
        "user_value": monthly_savings
    },
    {
        "category": "Retirement Corpus",
        "rule": "> 10× Annual CTC",
        "min": 10 * ctc * 1e5,
        "user_value": 11 * ctc * 1e5
    }
]

# Evaluate rules
def evaluate_rule(rule):
    if "min" in rule and "max" in rule:
        if rule["min"] <= rule["user_value"] <= rule["max"]:
            return "🟢 On Track"
        elif rule["user_value"] >= 0.5 * rule["min"]:
            return "🟡 Almost There"
        else:
            return "🔴 Needs Attention"
    elif "min" in rule:
        return "🟢 On Track" if rule["user_value"] >= rule["min"] else "🔴 Needs Attention"
    elif "max" in rule:
        return "🟢 On Track" if rule["user_value"] <= rule["max"] else "🔴 Needs Attention"
    return "❓"

# Display Results
st.markdown("### 📊 Your Financial Rule Check")

met_count = 0
for r in rules:
    status = evaluate_rule(r)
    if status.startswith("🟢"):
        met_count += 1
    st.write(f"**{r['category']}** — {r['rule']} → **{status}**")

st.success(f"🎯 You’ve met {met_count}/9 financial thumb rules.")

# PDF generation
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Smart Money Map – Financial Summary", ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%d-%b-%Y')}", 0, 0, 'C')

    def add_summary(self, ctc, savings_rate, monthly_take_home, monthly_savings, rules):
        self.set_font("Arial", size=12)
        self.ln(10)
        self.cell(0, 10, f"Annual CTC: ₹{ctc:.2f} L", ln=True)
        self.cell(0, 10, f"Savings Rate: {savings_rate:.0f}%", ln=True)
        self.cell(0, 10, f"Monthly Take-Home: ₹{monthly_take_home/1e5:.2f} L", ln=True)
        self.cell(0, 10, f"Monthly Savings: ₹{monthly_savings/1e3:.1f} K", ln=True)
        self.ln(5)

        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, "Rule Check Summary:", ln=True)
        self.set_font("Arial", size=11)

        for r in rules:
            status = evaluate_rule(r)
            self.multi_cell(0, 8, f"- {r['category']} ({r['rule']}): {status}")

        self.ln(5)
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, f"Progress: {met_count}/9 rules met", ln=True)

# Create and serve PDF
pdf = PDF()
pdf.add_page()
pdf.add_summary(ctc, savings_rate, monthly_take_home, monthly_savings, rules)
pdf_output = pdf.output(dest='S').encode('latin-1')

b64_pdf = base64.b64encode(pdf_output).decode()
href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="Smart_Money_Map.pdf">📄 Download Your Financial Plan (PDF)</a>'
st.markdown(href, unsafe_allow_html=True)
