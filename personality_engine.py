"""
personality_engine.py
---------------------
Detects spending personality based on behavioral analytics.
"""


def detect_personality(food_ratio: float) -> dict:
    """
    Classify user's spending personality from food spending ratio.

    Args:
        food_ratio: Proportion of total spend going to food (0.0 – 1.0)

    Returns:
        Dict with personality name, description, emoji, and confidence
    """
    if food_ratio > 0.40:
        return {
            "name": "Financial Firestarter",
            "emoji": "🔥",
            "description": "You're literally burning your future for butter chicken. Swiggy's favorite victim.",
            "confidence": min(99, int(food_ratio * 150)),
            "color": "#FF4B4B",
        }
    elif food_ratio > 0.25:
        return {
            "name": "Average Enjoyer",
            "emoji": "⚖️",
            "description": "Basic. You spend enough to feel regret, but not enough to be legendary.",
            "confidence": min(99, int(70 + food_ratio * 50)),
            "color": "#F0A500",
        }
    else:
        return {
            "name": "Ascetic Legend",
            "emoji": "🧘",
            "description": "Your self-control is scary. Are you even human or just a savings bot?",
            "confidence": min(99, int((0.25 - food_ratio) * 300 + 60)),
            "color": "#21C55D",
        }


# Available advisor tones for nudge generation
ADVISOR_TONES = {
    "Supportive Coach": "supportive",
    "Strict Advisor": "strict",
    "Savage Roaster": "savage",
}
