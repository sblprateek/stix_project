import pickle
from collections import Counter

from src.detection.detect import detect_stix_version
from src.normalization.normalize import normalize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# -------- PREPARE DATA --------
def prepare_data(file_path):

    version_info = detect_stix_version(file_path)
    data = normalize(file_path, version_info)

    texts = []
    labels = []

    for obj in data:

        text = obj.get("description", "")

        # -------- IMPROVED LABELING --------
        if obj["type"] in [
            "malware",
            "attack-pattern",
            "indicator",
            "intrusion-set"
        ]:
            label = 1  # threat

        elif obj["type"] in [
            "tool",
            "course-of-action",
            "x-mitre-mitigation"
        ]:
            label = 0  # non-threat

        else:
            continue  # skip irrelevant types

        texts.append(text)
        labels.append(label)

    # Debug: check balance
    print("Label distribution:", Counter(labels))

    return texts, labels


# -------- TRAIN MODEL --------
def train_model(file_path):

    texts, labels = prepare_data(file_path)

    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=200)
    model.fit(X, labels)

    return model, vectorizer


# -------- MAIN --------
if __name__ == "__main__":

    path = "data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json"

    model, vectorizer = train_model(path)

    # Save model
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model trained & saved successfully!")