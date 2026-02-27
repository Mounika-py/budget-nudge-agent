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
            "name": "Impulsive Spender",
            "emoji": "🔥",
            "description": "You live for food and order without thinking twice!",
            "confidence": min(99, int(food_ratio * 150)),
            "color": "#FF4B4B",
        }
    elif food_ratio > 0.25:
        return {
            "name": "Balanced Spender",
            "emoji": "⚖️",
            "description": "You enjoy food but keep other expenses in check.",
            "confidence": min(99, int(70 + food_ratio * 50)),
            "color": "#F0A500",
        }
    else:
        return {
            "name": "Disciplined Saver",
            "emoji": "🧘",
            "description": "You treat your wallet like a sacred temple. Impressive!",
            "confidence": min(99, int((0.25 - food_ratio) * 300 + 60)),
            "color": "#21C55D",
        }


# Available advisor tones for nudge generation
ADVISOR_TONES = {
    "Supportive Coach": "supportive",
    "Strict Advisor": "strict",
    "Sarcastic Friend": "sarcastic",
}
