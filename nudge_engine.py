"""
nudge_engine.py
---------------
Generates AI-powered (or rule-based fallback) behavioral nudges.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Rule-based nudge library ──────────────────────────────────────────────────

RULE_BASED_NUDGES = {
    # tone → risk_level → message
    "supportive": {
        "Low": "You're doing great! 🌟 Keep this up and your savings will thank you.",
        "Medium": "You're close! 💪 Cut one Swiggy order and you'll be in the green.",
        "High": "Hey, you got this! 🤗 Let's reset and aim for a lighter wallet week.",
    },
    "strict": {
        "Low": "Acceptable. Maintain discipline and do not slip up next month.",
        "Medium": "Your spending is borderline reckless. Immediate correction required.",
        "High": "STOP. You have blown your budget. No more food orders this month.",
    },
    "sarcastic": {
        "Low": "Oh wow, you only spent a little? Should we give you a medal? 🏅",
        "Medium": "Halfway to broke — impressive achievement unlocked! 🎮",
        "High": "Congrats! Your wallet is now officially on life support. Swiggy thanks you! 🍕",
    },
}


def _rule_based_nudge(risk_level: str, tone: str) -> str:
    """Return a pre-written nudge based on risk level and tone."""
    tone_map = {
        "Supportive Coach": "supportive",
        "Strict Advisor": "strict",
        "Sarcastic Friend": "sarcastic",
    }
    tone_key = tone_map.get(tone, "supportive")
    return RULE_BASED_NUDGES[tone_key][risk_level]


def _openai_nudge(
    risk_score: float,
    risk_level: str,
    personality: str,
    overspend_amount: float,
    tone: str,
) -> str:
    """
    Call OpenAI API to generate a personalized nudge.
    Falls back to rule-based on any error.
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        tone_instructions = {
            "Supportive Coach": "Be warm, encouraging, and empathetic.",
            "Strict Advisor": "Be firm, direct, and no-nonsense.",
            "Sarcastic Friend": "Be witty, sarcastic, but ultimately helpful.",
        }

        prompt = (
            f"User overspent ₹{overspend_amount:.0f}. "
            f"Risk level: {risk_level} (score: {risk_score}). "
            f"Spending personality: {personality}. "
            f"Tone instruction: {tone_instructions.get(tone, '')} "
            f"Generate a short (max 20 words), humorous but motivating financial nudge."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a witty behavioral finance coach. Keep responses under 20 words.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=60,
            temperature=0.85,
        )
        return response.choices[0].message.content.strip()

    except Exception:
        # Graceful fallback to rule-based nudge
        return _rule_based_nudge(risk_level, tone)


def generate_nudge(
    risk_score: float,
    risk_level: str,
    personality: str,
    overspend_amount: float,
    tone: str = "Supportive Coach",
) -> tuple[str, bool]:
    """
    Generate a behavioral nudge message.

    Returns:
        (nudge_text, used_ai) — nudge string and whether AI was used
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key and api_key != "your_openai_api_key_here":
        nudge = _openai_nudge(risk_score, risk_level, personality, overspend_amount, tone)
        return nudge, True
    else:
        nudge = _rule_based_nudge(risk_level, tone)
        return nudge, False
