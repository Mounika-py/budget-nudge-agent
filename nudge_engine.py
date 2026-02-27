"""
nudge_engine.py
---------------
Generates AI-powered (or rule-based fallback) behavioral nudges with multimedia assets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Multimedia Assets ─────────────────────────────────────────────────────────

# Default Remote Assets
DEFAULT_ASSETS = {
    "Low": {
        "meme": "https://api.memegen.link/images/stonks.png",
        "sound": "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
    },
    "Medium": {
        "meme": "https://api.memegen.link/images/fine.png",
        "sound": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    },
    "High": {
        "meme": "https://api.memegen.link/images/ds.png",
        "sound": "https://actions.google.com/sounds/v1/emergency/emergency_siren_short_burst.ogg",
    },
}

def get_assets(risk_level: str) -> dict:
    """
    Get meme and sound for a given risk level.
    Prioritizes local files in assets/memes and assets/sounds.
    """
    level_lower = risk_level.lower()

    # Potential local paths
    local_meme = None
    for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
        path = Path(f"assets/memes/{level_lower}.{ext}")
        if path.exists():
            local_meme = str(path)
            break

    local_sound = None
    for ext in ['mp3', 'wav', 'ogg']:
        path = Path(f"assets/sounds/{level_lower}.{ext}")
        if path.exists():
            local_sound = str(path)
            break

    defaults = DEFAULT_ASSETS.get(risk_level, DEFAULT_ASSETS["Low"])

    return {
        "meme": local_meme if local_meme else defaults["meme"],
        "sound": local_sound if local_sound else defaults["sound"]
    }

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
) -> dict:
    """
    Generate a behavioral nudge with multimedia assets.

    Returns:
        dict: {
            "text": str,
            "image": str (URL),
            "sound": str (URL),
            "used_ai": bool
        }
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    used_ai = False

    if api_key and api_key != "your_openai_api_key_here":
        nudge_text = _openai_nudge(risk_score, risk_level, personality, overspend_amount, tone)
        used_ai = True
    else:
        nudge_text = _rule_based_nudge(risk_level, tone)

    assets = get_assets(risk_level)

    return {
        "text": nudge_text,
        "image": assets["meme"],
        "sound": assets["sound"],
        "used_ai": used_ai,
    }
