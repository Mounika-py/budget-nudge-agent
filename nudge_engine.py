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

# Sound assets
PERSONALITY_SOUNDS = {
    "Financial Firestarter": "https://www.myinstants.com/media/sounds/emotional-damage-meme.mp3",
    "Average Enjoyer": "https://www.myinstants.com/media/sounds/bruh.mp3",
    "Ascetic Legend": "https://www.myinstants.com/media/sounds/gta-san-andreas-mission-passed.mp3",
}
CLAP_SOUND = "https://www.myinstants.com/media/sounds/clapping.mp3"

# Savage Gen-Z Nudges (Categorized by Personality)
SAVAGE_NUDGES = {
    "Financial Firestarter": [
        {
            "text": "Your salary had dreams. You had cravings. Swiggy has entered the chat. 💸",
            "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKDkDbIDJieKbVm/giphy.gif",
            "overlay": "SALARY CREDITED... AND IT'S GONE."
        },
        {
            "text": "Me watching my budget burn after ordering extra cheese. 🔥",
            "meme": "assets/memes/english_funny.jpg",
            "overlay": "BUDGET ON FIRE"
        },
        {
            "text": "Congratulations! You've officially funded Swiggy's next IPO personally. 🏆",
            "meme": "assets/memes/telugu_troll.jpg",
            "overlay": "INVESTOR OF THE YEAR"
        },
        {
            "text": "Cause of death: Midnight biryani with 'no minimum order' confidence. ⚰️",
            "meme": "https://i.imgflip.com/2/4t0m5.jpg",
            "overlay": "BANK BALANCE FUNERAL"
        }
    ],
    "Average Enjoyer": [
        {
            "text": "This relationship with Swiggy is one-sided. You pay. They deliver. Regret arrives free. 💔",
            "meme": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpueXpuJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif",
            "overlay": "SWIGGY: I CHANGED 🥺"
        },
        {
            "text": "Me looking at my bank statement like... why am I like this? 🤡",
            "meme": "assets/memes/monkey_facepalm.webp",
            "overlay": "FINANCIAL REGRET"
        },
        {
            "text": "You don't have a spending problem. You have a 'treat yourself' addiction. 🧐",
            "meme": "assets/memes/english_roast.jpeg",
            "overlay": "POINTING OUT THE TRUTH"
        },
        {
            "text": "When the delivery guy knows your WiFi password better than you. 📶",
            "meme": "assets/memes/monkey_angry.jpeg",
            "overlay": "STOP ORDERING ALREADY"
        }
    ],
    "Ascetic Legend": [
        {
            "text": "She didn't raise you for ₹320 garlic bread. Imagine the disappointment. 🎭",
            "meme": "assets/memes/telugu_brahmi_troll.jpeg",
            "overlay": "MOM'S DISAPPOINTMENT"
        },
        {
            "text": "Be that damn penguin. Run away from the delivery apps. 🐧",
            "meme": "assets/memes/penguin_sarcastic.jpeg",
            "overlay": "FINANCIAL FREEDOM"
        },
        {
            "text": "Running away from my responsibilities and my empty savings account. 🏔️",
            "meme": "assets/memes/penguin_disappointed.jpeg",
            "overlay": "RUNNING TO THE MOUNTAINS"
        },
        {
            "text": "Your money works hard. You send it to butter chicken. 🍗",
            "meme": "assets/memes/telugu_funny.jpeg",
            "overlay": "WHY ARE YOU LIKE THIS"
        }
    ]
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
            "personality_sound": str (URL),
            "clap_sound": str (URL),
            "overlay_text": str,
            "used_ai": bool
        }
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    used_ai = False

    # Selection for savage library
    savage_options = SAVAGE_NUDGES.get(personality, SAVAGE_NUDGES["Average Enjoyer"])
    savage_nudge = random.choice(savage_options)

    if tone == "Savage Roaster":
        if api_key and api_key != "your_openai_api_key_here":
            nudge_text = _openai_nudge(risk_score, risk_level, personality, overspend_amount, tone)
            used_ai = True
        else:
            nudge_text = savage_nudge["text"]
        assets = get_assets(risk_level)
    else:
        if api_key and api_key != "your_openai_api_key_here":
            nudge_text = _openai_nudge(risk_score, risk_level, personality, overspend_amount, tone)
            used_ai = True
        else:
            nudge_text = _rule_based_nudge(risk_level, tone)
        assets = get_assets(risk_level)

    return {
        "text": nudge_text,
        "image": savage_nudge["meme"] if tone == "Savage Roaster" else assets["meme"],
        "sound": assets["sound"],
        "personality_sound": PERSONALITY_SOUNDS.get(personality, PERSONALITY_SOUNDS["Average Enjoyer"]),
        "clap_sound": CLAP_SOUND,
        "overlay_text": savage_nudge["overlay"],
        "used_ai": used_ai,
    }
