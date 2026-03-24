import pickle

from src.detection.detect import detect_stix_version
from src.normalization.normalize import normalize
from src.credibility.trust import calculate_trust   # ✅ NEW


# -------- LOAD BALANCED MODEL --------
with open("model_balanced.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer_balanced.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# -------- PREDICTION FUNCTION --------
def predict(file_path):

    version_info = detect_stix_version(file_path)
    data = normalize(file_path, version_info)

    results = []

    for obj in data:

        text = obj.get("description", "")

        X = vectorizer.transform([text])
        pred = model.predict(X)[0]

        # ✅ ADD TRUST SCORE
        trust = calculate_trust(obj)

        results.append({
            "name": obj.get("name", ""),
            "type": obj.get("type", ""),
            "threat": int(pred),
            "trust_score": trust   # ✅ NEW FIELD
        })

    return results