# 💰 AI-Powered Behavioral Budget Nudge Agent

> A behavioral finance intelligence app that analyzes spending patterns, detects personality types, and delivers AI-powered nudges to improve financial health.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 OTP Login | Phone-based simulated OTP authentication |
| 📊 Spending Analytics | Total spend, food ratio, overspend detection |
| 🧠 Risk Score | Behavioral risk score (0–100) with classification |
| 🎭 Personality Detection | Impulsive / Balanced / Disciplined spender detection |
| 🤖 AI Nudges | OpenAI-powered nudges with 3 advisor tones |
| 📈 Interactive Dashboard | Plotly charts + Streamlit metrics |
| 🎮 Simulation Mode | Add virtual orders and watch risk update live |
| 🏅 Gamification | Bronze / Silver / Gold Saver level progression |

---

## ⚙️ Setup Instructions

### 1. Clone / Download the project
```bash
git clone https://github.com/yourname/budget-nudge-agent
cd budget-nudge-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key (optional)
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🔑 Adding OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Add it to your `.env` file:
   ```
   OPENAI_API_KEY=sk-...your-key-here...
   ```

> **Without a key**, the app automatically uses rule-based nudges — no features are lost!

---

## 📱 Demo Login Credentials

| Phone | OTP |
|---|---|
| 9999999999 | (shown on screen) |
| 8888888888 | (shown on screen) |
| 7777777777 | (shown on screen) |

OTPs are randomly generated and displayed on screen for hackathon demo purposes.

---

## 📁 Project Structure

```
budget-nudge-agent/
│
├── app.py                  # Main Streamlit app & UI router
├── risk_engine.py          # Analytics + risk score calculation
├── personality_engine.py   # Spending personality detection
├── nudge_engine.py         # AI nudge generation (OpenAI + fallback)
│
├── data/
│   └── mouni.csv           # Mock transaction data (Jan 2024)
│
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧮 Risk Score Formula

```
food_ratio     = food_spend / total_spend
overspend_ratio = max(0, total_spend - budget) / budget

risk_score = (food_ratio × 50) + (overspend_ratio × 50)
risk_score = min(risk_score, 100)
```

| Score | Level |
|---|---|
| 0–30 | 🟢 Low |
| 31–60 | 🟡 Medium |
| 61–100 | 🔴 High |

---

## 🏅 Gamification Levels

| Level | Condition |
|---|---|
| 🥇 Gold Saver | Risk Score < 15 |
| 🥈 Silver Saver | Risk Score < 25 |
| 🥉 Bronze Saver | Risk Score < 40 |
| 🌱 Beginner | Risk Score ≥ 40 |

---

## 🔮 Future Scalability

- **Bank Integration**: Connect real UPI/bank APIs (Plaid, Setu, Fi Money)
- **Multi-user Support**: Firebase/Supabase backend with real auth
- **Weekly Reports**: Automated email nudges via SendGrid
- **ML Personality Model**: Train on real behavioral data for better classification
- **Budget Goals**: Let users set category-wise monthly budgets
- **WhatsApp Nudges**: Send nudges via Twilio WhatsApp API
- **Voice Mode**: Integrate ElevenLabs for spoken nudges

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data**: Pandas
- **Visualization**: Plotly
- **AI**: OpenAI GPT-3.5 (with rule-based fallback)
- **Config**: python-dotenv

---

## ☁️ Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `app.py` as entry point
4. Add `OPENAI_API_KEY` in Secrets settings
5. Deploy 🚀

---

*Built for Hackathon 2024 — Behavioral Finance × AI*
