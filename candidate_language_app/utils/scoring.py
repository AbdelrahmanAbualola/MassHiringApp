def get_cefr_level(score):
    """
    Returns the Common European Framework of Reference for Languages (CEFR) level
    based on a given proficiency score (0-100).
    """
    if score >= 90:
        return "C2 (Mastery)"
    elif score >= 80:
        return "C1 (Effective Operational Proficiency)"
    elif score >= 70:
        return "B2 (Vantage)"
    elif score >= 55:
        return "B1 (Threshold)"
    elif score >= 40:
        return "A2 (Waystage)"
    else:
        return "A1 (Breakthrough)"

def calculate_proficiency_score(confidence, duration):
    """
    Calculates a language proficiency score (0-100) based on model confidence
    and recording duration.
    """
    # A base score using model confidence
    # (Confidence is between 0 and 1, mapping to 0-100)
    base_score = confidence * 100

    # Simple bonus/penalty based on duration (longer clips are often better but can also have more errors)
    # This is a simplified logic. In a real app, it would be much more complex.
    if duration < 5: # Too short
        score = base_score * 0.7
    elif duration < 10:
        score = base_score * 0.9
    elif duration > 60: # Too long for a quick test
        score = base_score * 0.95
    else:
        score = base_score

    return round(min(100, max(0, score)), 2)
