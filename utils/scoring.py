import pandas as pd

def calculate_health_score(detections):
    """
    Calculates a 0-100 score based on detections.
    Expected input: list of dicts [{'class': 'Pothole', 'confidence': 0.85}, ...]
    """
    if not detections:
        return 100 # Perfect score if no damage
    
    weights = {
        'Pothole': 10,
        'Alligator': 8,
        'Transverse': 5,
        'Longitudinal': 4
    }
    
    penalty = 0
    for d in detections:
        base_penalty = weights.get(d['class'], 2)
        # Higher confidence = more certain penalty
        penalty += (base_penalty * d['confidence']) 
        
    score = max(0, 100 - (penalty * 2)) # Arbitrary multiplier for scale
    return round(score)

def get_urgency_badge(score):
    if score < 40:
        return "🔴 Urgent"
    elif score < 70:
        return "🟡 Monitor"
    else:
        return "🟢 OK"