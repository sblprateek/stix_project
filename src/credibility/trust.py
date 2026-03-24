def calculate_trust(obj):

    confidence = obj.get("confidence", 50)

    trust_score = (
        0.5 * (confidence / 100) +
        0.3 * (1 if obj.get("source") == "MITRE" else 0.5) +
        0.2 * (1 if obj.get("description") else 0)
    )

    return round(trust_score, 2)
