"""
app.py
------
Financial Emotional Damage Simulator
Main Streamlit application entry point.

Run with: streamlit run app.py
"""

import random
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import streamlit as st
import plotly.express as px
import pandas as pd

from risk_engine import load_transactions, calculate_analytics, get_gamification_level
from personality_engine import detect_personality, ADVISOR_TONES
from nudge_engine import generate_nudge

load_dotenv()

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Emotional Damage Simulator 📉💀",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main { background-color: #0E1117; }
    .risk-score-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid #2d2d5e;
    }
    .risk-number {
        font-size: 72px;
        font-weight: 900;
        line-height: 1;
    }
    .nudge-box {
        background: linear-gradient(135deg, #1e3a5f, #0d2137);
        border-left: 4px solid #4fc3f7;
        border-radius: 12px;
        padding: 20px 24px;
        font-size: 18px;
        font-style: italic;
        color: #e0f7fa;
        margin-top: 12px;
    }
    .personality-box {
        background: linear-gradient(135deg, #1b2838, #2a1f3d);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid #3d3060;
    }
    .stMetric > div { background: #1a1a2e; border-radius: 10px; padding: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Email → CSV Mapping ───────────────────────────────────────────────────────
EMAIL_TO_CSV = {
    "mouni@example.com": "data/mouni.csv",
    "demo@example.com": "data/mouni.csv",
}
DEFAULT_CSV = "data/mouni.csv"


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: OTP LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def send_otp_email(receiver_email: str, otp: str):
    """Send OTP via Gmail SMTP."""
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not sender_password:
        return False, "Email credentials missing (EMAIL_SENDER or EMAIL_APP_PASSWORD). Check .env."

    try:
        # SMTP Server setup
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        message = MIMEMultipart()
        message["From"] = f"Emotional Damage Simulator <{sender_email}>"
        message["To"] = receiver_email
        message["Subject"] = "Your Financial Roast Access Code"

        body = f"""
        <html>
        <body>
            <h3>💀 Financial Emotional Damage Simulator</h3>
            <p>Your Secure OTP is: <b>{otp}</b></p>
            <p>Enter this to see how badly you're failing your budget.</p>
            <hr/>
            <p><small>If you didn't request this roast, please ignore this email.</small></p>
        </body>
        </html>
        """
        message.attach(MIMEText(body, "html"))

        # Connect and send
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()

        return True, f"OTP sent to {receiver_email}"
    except Exception as e:
        return False, f"Email Error: {str(e)}"


def send_dashboard_notification(receiver_email: str, nudge_text: str):
    """Send the 'Emotional Damage' roast via email."""
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not sender_password:
        return False, "Email credentials missing."

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        message = MIMEMultipart()
        message["From"] = f"Emotional Damage Agent 💀 <{sender_email}>"
        message["To"] = receiver_email
        message["Subject"] = "🚨 URGENT: Your Financial Reality Check"

        body = f"""
        <html>
        <body>
            <h2 style='color: #FF4B4B;'>💀 FINANCIAL EMOTIONAL DAMAGE RECEIVED</h2>
            <p style='font-size: 18px; font-style: italic;'>"{nudge_text}"</p>
            <p>Stop everything. Check your dashboard before you're completely broke.</p>
            <br/>
            <a href='https://emotional-damage-simulator.streamlit.app' style='background: #FF4B4B; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>OPEN DASHBOARD</a>
            <hr/>
            <p><small>Sent by the Financial Emotional Damage Simulator.</small></p>
        </body>
        </html>
        """
        message.attach(MIMEText(body, "html"))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
        return True, "Roast emailed successfully!"
    except Exception as e:
        return False, f"Email Error: {str(e)}"


def otp_login_screen():
    """Render the OTP login UI."""
    st.markdown("## ✨ Financial Emotional Damage Simulator ✨")
    st.markdown("### 🔐 Enter the Roast Zone")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input(
            "📧 Enter your email",
            placeholder="e.g. user@example.com",
        )

        if st.button("📨 Send OTP", use_container_width=True, type="primary"):
            if "@" in email and "." in email:
                otp = str(random.randint(1000, 9999))
                st.session_state["otp"] = otp
                st.session_state["email"] = email

                # Real Email Attempt
                success, msg = send_otp_email(email, otp)

                if success:
                    st.success(f"✅ {msg}")
                    st.session_state["otp_sent"] = True
                    st.session_state["real_otp_sent"] = True
                else:
                    st.warning(f"⚠️ Could not send real Email: {msg}")
                    st.info("💡 Falling back to on-screen OTP for demo purposes.")
                    st.session_state["otp_sent"] = True
                    st.session_state["real_otp_sent"] = False
            else:
                st.error("❌ Please enter a valid email address.")

        # OTP verification step
        if st.session_state.get("otp_sent"):
            if not st.session_state.get("real_otp_sent"):
                st.info(
                    f"🔑 **On-Screen OTP:** `{st.session_state['otp']}`",
                    icon="ℹ️",
                )
            else:
                st.info("📩 Check your inbox for the OTP.")
            entered_otp = st.text_input("🔢 Enter OTP", max_chars=4, placeholder="4-digit OTP")

            if st.button("✅ Verify OTP", use_container_width=True):
                if entered_otp == st.session_state["otp"]:
                    # Connection Simulation
                    with st.status("🔗 Connecting to food platforms...", expanded=True) as status:
                        platforms = ["Swiggy", "Zomato", "Blinkit", "EatClub"]
                        for p in platforms:
                            st.write(f"🔄 Fetching data from {p}...")
                            time.sleep(0.6)
                        status.update(label="✅ All platforms connected!", state="complete", expanded=False)

                    st.balloons()
                    time.sleep(1)

                    st.session_state["logged_in"] = True
                    # Resolve CSV path from email
                    csv_path = EMAIL_TO_CSV.get(
                        st.session_state["email"], DEFAULT_CSV
                    )
                    st.session_state["csv_path"] = csv_path
                    st.session_state["extra_food"] = 0.0  # simulation counter
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP. Please try again.")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def dashboard_screen():
    """Render the full analytics dashboard."""

    # ── Load data & compute analytics ─────────────────────────────────────
    df = load_transactions(st.session_state["csv_path"])
    extra_food = st.session_state.get("extra_food", 0.0)
    analytics = calculate_analytics(df, extra_food=extra_food)

    risk_score = analytics["risk_score"]
    risk_level = analytics["risk_level"]
    personality_data = detect_personality(analytics["food_ratio"])
    gamification = get_gamification_level(risk_score)

    # ── Header ─────────────────────────────────────────────────────────────
    col_logo, col_title, col_logout = st.columns([1, 6, 1])
    with col_logo:
        st.markdown("# 📉💀")
    with col_title:
        st.markdown("## ✨ Financial Emotional Damage Simulator ✨")
        st.caption(f"📧 Logged in as: {st.session_state.get('email', 'N/A')} &nbsp;|&nbsp; 📅 Jan 2024")
    with col_logout:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("---")

    # ── ROW 1: Key Metrics ─────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            "💳 Total Burn",
            f"₹{analytics['total_spend']:,.0f}",
            delta=f"₹{analytics['overspend_amount']:,.0f} over budget" if analytics["overspend_amount"] > 0 else "Within budget",
            delta_color="inverse",
        )
    with m2:
        st.metric("🍕 Food Junkie Spend", f"₹{analytics['food_spend']:,.0f}")
    with m3:
        st.metric("🎯 Monthly Budget", f"₹{analytics['budget']:,}")
    with m4:
        food_pct = analytics["food_ratio"] * 100
        st.metric("📊 Food Ratio", f"{food_pct:.1f}%")

    st.markdown("---")

    # ── ROW 2: Risk Score + Personality + Pie Chart ────────────────────────
    col_risk, col_personality, col_pie = st.columns([1.2, 1.2, 2])

    # Risk Score
    with col_risk:
        risk_color = {"Low": "#21C55D", "Medium": "#F0A500", "High": "#FF4B4B"}[risk_level]
        st.markdown(
            f"""
            <div class="risk-score-box">
                <div style="color: #aaa; font-size: 14px; margin-bottom: 8px;">EMOTIONAL DAMAGE POTENTIAL</div>
                <div class="risk-number" style="color: {risk_color};">{risk_score}</div>
                <div style="font-size: 22px; font-weight: 700; color: {risk_color}; margin-top: 6px;">
                    {risk_level} Risk
                </div>
                <div style="color: #888; font-size: 12px; margin-top: 6px;">out of 100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(int(risk_score), text=f"Risk Level: {risk_level}")

    # Personality Box
    with col_personality:
        p = personality_data
        st.markdown(
            f"""
            <div class="personality-box">
                <div style="font-size: 48px;">{p['emoji']}</div>
                <div style="font-size: 20px; font-weight: 700; color: {p['color']}; margin-top: 8px;">
                    {p['name']}
                </div>
                <div style="color: #aaa; font-size: 13px; margin: 8px 0;">{p['description']}</div>
                <div style="color: #777; font-size: 12px;">Confidence: {p['confidence']}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Gamification Badge
        g = gamification
        st.markdown(
            f"""
            <div style="background:#111827; border-radius:10px; padding:12px; margin-top:12px; text-align:center; border:1px solid #2d2d5e;">
                <div style="font-size:28px;">{g['emoji']}</div>
                <div style="font-weight:700; color:{g['color']};">{g['level']}</div>
                {"<div style='color:#888;font-size:11px;'>MAX LEVEL 🎉</div>" if not g['next_level'] else
                 f"<div style='color:#888;font-size:11px;'>↓ {g['points_to_next']} pts to {g['next_level']}</div>"}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if g["next_level"]:
            st.progress(g["progress"] / 100, text=f"Progress to {g['next_level']}")

    # Pie Chart
    with col_pie:
        category_totals = analytics["category_totals"]
        pie_df = pd.DataFrame(
            list(category_totals.items()), columns=["Category", "Amount"]
        )
        fig = px.pie(
            pie_df,
            names="Category",
            values="Amount",
            title="💰 Where is your money dying?",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        )
        fig.update_traces(textinfo="label+percent", hovertemplate="%{label}: ₹%{value:,.0f}")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── ROW 3: Nudge Generator ─────────────────────────────────────────────
    st.markdown("### 🤖 Behavioral Roast Generator")

    nudge_col1, nudge_col2 = st.columns([1, 3])
    with nudge_col1:
        selected_tone = st.selectbox(
            "🎭 Advisor Tone",
            list(ADVISOR_TONES.keys()),
            help="Choose how your financial advisor should roast you",
            index=2 # Default to Savage Roaster
        )
        generate_btn = st.button("⚡ Generate Roast", use_container_width=True, type="primary")

    if generate_btn or "nudge_data" not in st.session_state:
        nudge_data = generate_nudge(
            risk_score=risk_score,
            risk_level=risk_level,
            personality=personality_data["name"],
            overspend_amount=analytics["overspend_amount"],
            tone=selected_tone,
        )
        st.session_state["nudge_data"] = nudge_data

        # Trigger Notification & Sound on generation
        st.toast(nudge_data["text"], icon="💀" if risk_level == "High" else "⚠️" if risk_level == "Medium" else "✅")
        st.audio(nudge_data["sound"], autoplay=True)

    with nudge_col2:
        nudge_data = st.session_state.get("nudge_data", {})
        ai_badge = "🤖 AI-Roasted" if nudge_data.get("used_ai") else "📋 Pre-cooked Roast"
        st.caption(ai_badge)

        n_col_text, n_col_img = st.columns([2, 1])
        with n_col_text:
            st.markdown(
                f'<div class="nudge-box">"{nudge_data.get("text", "")}"</div>',
                unsafe_allow_html=True,
            )
            # Email roast button
            if st.button("📧 Email me this Roast"):
                success, msg = send_dashboard_notification(st.session_state["email"], nudge_data["text"])
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
        with n_col_img:
            if nudge_data.get("image"):
                st.image(nudge_data["image"], use_container_width=True)

    st.markdown("---")

    # ── ROW 4: Simulation Mode ─────────────────────────────────────────────
    st.markdown("### 🎮 Financial Doom Simulation")

    sim_col1, sim_col2 = st.columns([1, 3])
    with sim_col1:
        sim_amount = st.number_input("Simulate order (₹)", min_value=100, max_value=2000, value=500, step=100)
        sim_platform = st.selectbox("Platform", ["Swiggy", "Zomato", "Blinkit", "EatClub"])

        if st.button(f"🛵 Order ₹{sim_amount} on {sim_platform}", use_container_width=True):
            st.session_state["extra_food"] = st.session_state.get("extra_food", 0.0) + sim_amount
            # Clear cached nudge so it regenerates
            if "nudge_data" in st.session_state:
                del st.session_state["nudge_data"]
            st.rerun()

        if st.session_state.get("extra_food", 0) > 0:
            st.warning(f"⚡ Simulated Damage: +₹{st.session_state['extra_food']:,.0f}")
            if st.button("↩️ Reset Financial Ruin"):
                st.session_state["extra_food"] = 0.0
                if "nudge_data" in st.session_state:
                    del st.session_state["nudge_data"]
                st.rerun()

    with sim_col2:
        # Show transaction history table
        st.markdown("#### 📋 Crimes Against your Wallet")
        display_df = df[["date", "platform", "category", "amount"]].copy()
        display_df["date"] = display_df["date"].dt.strftime("%d %b %Y")
        display_df["amount"] = display_df["amount"].apply(lambda x: f"₹{x:,.0f}")
        if extra_food > 0:
            sim_rows = []
            for _ in range(int(extra_food // sim_amount)):
                sim_rows.append({
                    "date": "Today (Sim)",
                    "platform": sim_platform,
                    "category": "Food",
                    "amount": f"₹{sim_amount:,.0f}",
                })
            display_df = pd.concat([pd.DataFrame(sim_rows), display_df], ignore_index=True)

        st.dataframe(display_df, use_container_width=True, height=250)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main application router based on login state."""
    if not st.session_state.get("logged_in"):
        otp_login_screen()
    else:
        dashboard_screen()


if __name__ == "__main__":
    main()
