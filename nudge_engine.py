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

# Savage Gen-Z Nudge Library
SAVAGE_NUDGES = {
    "Impulsive Spender": [
        {"text": "Your salary had dreams. You had cravings.", "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKpxO7S5Y4gYF6U/giphy.gif", "overlay": "Salary credited 💰✨\nSwiggy has entered the chat."},
        {"text": "Cause of death: Midnight biryani with ‘no minimum order’ confidence.", "meme": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop", "overlay": "Bank balance funeral ceremony"},
        {"text": "This relationship is one-sided. You pay. They deliver. Regret arrives free.", "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0MYH8Q8S9P9mJ2Ww/giphy.gif", "overlay": "Swiggy: I changed 🥺"},
        {"text": "You don’t have a spending problem. You have a ‘treat yourself’ addiction.", "meme": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1000&auto=format&fit=crop", "overlay": "Financial advisor watching your Zomato history"},
        {"text": "At this point, the delivery guy knows your WiFi password.", "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26n6Gx9moCgs1pUuk/giphy.gif", "overlay": "Me saying ‘last order’ for the 8th time"},
        {"text": "Your money works hard. You send it to butter chicken.", "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7ZetGfIDzS7R9J0Q/giphy.gif", "overlay": "Bank balance trying to escape"},
        {"text": "You’re not a customer. You’re a venture capitalist.", "meme": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1000&auto=format&fit=crop", "overlay": "Investor pitch: How I funded Swiggy’s growth personally"}
    ],
    "Balanced Spender": [
        {"text": "You bought vegetables once. You ordered food 11 times.", "meme": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?q=80&w=1000&auto=format&fit=crop", "overlay": "I’ll cook at home this month 🤡"},
        {"text": "She didn’t raise you for ₹320 garlic bread.", "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKv6lK6L0P9M2Kk/giphy.gif", "overlay": "Mom opening your bank statement"},
        {"text": "You’re bulking. Financially.", "meme": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1000&auto=format&fit=crop", "overlay": "Gym membership: ₹1500 unused\nFood delivery: ₹7800 used"},
        {"text": "It all started with ‘free delivery above ₹199’.", "meme": "https://images.unsplash.com/photo-1470252646218-9e9760e8bb5a?q=80&w=1000&auto=format&fit=crop", "overlay": "My villain origin story"}
    ],
    "Disciplined Saver": [
        {"text": "You're so cheap even your wallet is bored.", "meme": "https://images.unsplash.com/photo-1594910413528-9430d8bb8965?q=80&w=1000&auto=format&fit=crop", "overlay": "Bank balance is too healthy 🧐"},
        {"text": "Did you forget Swiggy exists or did they block you?", "meme": "https://images.unsplash.com/photo-1512152272829-e3139592d56f?q=80&w=1000&auto=format&fit=crop", "overlay": "No food orders detected 🤡"}
    ]
}

PERSONALITY_SOUNDS = {
    "Impulsive Spender": "https://actions.google.com/sounds/v1/emergency/emergency_siren_short_burst.ogg",
    "Balanced Spender": "https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg",
    "Disciplined Saver": "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
}

CLAP_SOUND = "https://actions.google.com/sounds/v1/human/applause_clapping.ogg"

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
            "personality_sound": str (URL),
            "clap_sound": str (URL),
            "overlay_text": str,
            "used_ai": bool
        }
    """
    import random

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    used_ai = False

    # Get a savage nudge based on personality
    savage_options = SAVAGE_NUDGES.get(personality, SAVAGE_NUDGES["Balanced Spender"])
    savage_nudge = random.choice(savage_options)

    if api_key and api_key != "your_openai_api_key_here":
        nudge_text = _openai_nudge(risk_score, risk_level, personality, overspend_amount, tone)
        used_ai = True
    else:
        # For the "Emotional Damage Simulator", we prioritize the savage text
        nudge_text = savage_nudge["text"]

    assets = get_assets(risk_level)

    return {
        "text": nudge_text,
        "image": savage_nudge["meme"],
        "sound": assets["sound"],
        "personality_sound": PERSONALITY_SOUNDS.get(personality, PERSONALITY_SOUNDS["Balanced Spender"]),
        "clap_sound": CLAP_SOUND,
        "overlay_text": savage_nudge["overlay"],
        "used_ai": used_ai,
    }
