"""
nudge_engine.py
---------------
Generates AI-powered (or rule-based fallback) behavioral nudges with multimedia assets.
"""

import os
import random
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

# Savage Gen-Z Nudges
SAVAGE_NUDGES = [
    {
        "text": "Your salary had dreams. You had cravings. Swiggy has entered the chat. 💸",
        "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKDkDbIDJieKbVm/giphy.gif",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "Cause of death: Midnight biryani with 'no minimum order' confidence. ⚰️",
        "image": "https://i.imgflip.com/2/4t0m5.jpg", # Grim Reaper knocking on doors
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "You bought vegetables once. You ordered food 11 times. Delulu is not the solulu. 🤡",
        "image": "https://api.memegen.link/images/clown/I_will_cook_at_home/this_month.png",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "This relationship with Swiggy is one-sided. You pay. They deliver. Regret arrives free. 💔",
        "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "You don't have a spending problem. You have a 'treat yourself' addiction. 🧐",
        "image": "https://i.imgflip.com/4/3lmzyx.jpg",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "She didn't raise you for ₹320 garlic bread. Imagine the disappointment. 🎭",
        "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKDkDbIDJieKbVm/giphy.gif", # placeholder
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "You're bulking. Financially. Gym membership unused, Zomato history abused. 🏋️‍♂️",
        "image": "https://i.imgflip.com/1/305z6.jpg", # Drake hotline bling
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "At this point, the delivery guy knows your WiFi password. 'Last order' my foot. 🤡",
        "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/x0npYExCGOAP6/giphy.gif",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "It all started with 'free delivery above ₹199'. Now look at you. 📉",
        "image": "https://i.imgflip.com/4/3lmzyx.jpg",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    },
    {
        "text": "Your money works hard. You send it to butter chicken. Your bank balance is running away. 🏃‍♂️",
        "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7ZetIsj68qc0U6_C/giphy.gif",
        "sound": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
    }
]

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
    "savage": {
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
        "Savage Roaster": "savage",
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
            "Savage Roaster": "Be absolutely savage, use Gen-Z slang, and deliver 'emotional damage' about their spending habits. Mention Swiggy/Zomato.",
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

    if tone == "Savage Roaster":
        # Always pick from the savage library for maximum impact if not using AI
        # Or if AI is enabled, it will use the savage prompt.
        if api_key and api_key != "your_openai_api_key_here":
            nudge_text = _openai_nudge(risk_score, risk_level, personality, overspend_amount, tone)
            used_ai = True
            assets = get_assets(risk_level) # use standard assets for AI
            # Randomly mix in a savage sound if savage
            assets["sound"] = "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3"
        else:
            choice = random.choice(SAVAGE_NUDGES)
            return {
                "text": choice["text"],
                "image": choice["image"],
                "sound": choice["sound"],
                "used_ai": False
            }
    else:
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
