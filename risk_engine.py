"""
risk_engine.py
--------------
Calculates spending analytics and behavioral risk scores.
"""

import pandas as pd


# Fixed monthly budget (in INR)
MONTHLY_BUDGET = 4000


def load_transactions(csv_path: str) -> pd.DataFrame:
    """Load and parse the transaction CSV file."""
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def calculate_analytics(df: pd.DataFrame, extra_food: float = 0.0) -> dict:
    """
    Compute key spending metrics.

    Args:
        df: Transaction dataframe
        extra_food: Additional food spend added via simulation

    Returns:
        Dictionary of analytics values
    """
    total_spend = df["amount"].sum() + extra_food
    food_spend = df[df["category"] == "Food"]["amount"].sum() + extra_food

    # Ratios
    food_ratio = food_spend / total_spend if total_spend > 0 else 0
    overspend_amount = max(0, total_spend - MONTHLY_BUDGET)
    overspend_ratio = overspend_amount / MONTHLY_BUDGET

    # Risk Score Formula: (food_ratio * 50) + (overspend_ratio * 50), capped at 100
    risk_score = (food_ratio * 50) + (overspend_ratio * 50)
    risk_score = min(round(risk_score, 1), 100.0)

    # Classify risk level
    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # Category breakdown for pie chart
    category_totals = df.groupby("category")["amount"].sum().to_dict()
    if extra_food > 0:
        category_totals["Food"] = category_totals.get("Food", 0) + extra_food

    return {
        "total_spend": round(total_spend, 2),
        "food_spend": round(food_spend, 2),
        "budget": MONTHLY_BUDGET,
        "overspend_amount": round(overspend_amount, 2),
        "overspend_ratio": round(overspend_ratio, 4),
        "food_ratio": round(food_ratio, 4),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "category_totals": category_totals,
    }


def get_gamification_level(risk_score: float) -> dict:
    """
    Map risk score to gamification badge and next-level progress.

    Returns:
        Dict with level name, emoji, progress %, and next threshold
    """
    if risk_score < 15:
        return {
            "level": "Gold Saver",
            "emoji": "🥇",
            "color": "#FFD700",
            "progress": 100,
            "next_level": None,
            "points_to_next": 0,
        }
    elif risk_score < 25:
        progress = int(((25 - risk_score) / 10) * 100)
        return {
            "level": "Silver Saver",
            "emoji": "🥈",
            "color": "#C0C0C0",
            "progress": progress,
            "next_level": "Gold Saver",
            "points_to_next": round(risk_score - 15, 1),
        }
    elif risk_score < 40:
        progress = int(((40 - risk_score) / 15) * 100)
        return {
            "level": "Bronze Saver",
            "emoji": "🥉",
            "color": "#CD7F32",
            "progress": progress,
            "next_level": "Silver Saver",
            "points_to_next": round(risk_score - 25, 1),
        }
    else:
        return {
            "level": "Beginner",
            "emoji": "🌱",
            "color": "#78C850",
            "progress": max(0, int(((100 - risk_score) / 60) * 100)),
            "next_level": "Bronze Saver",
            "points_to_next": round(risk_score - 40, 1),
        }
