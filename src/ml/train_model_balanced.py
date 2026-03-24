import pickle
import random
from collections import Counter

from src.detection.detect import detect_stix_version
from src.normalization.normalize import normalize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# -------- PREPARE DATA (BALANCED) --------
def prepare_data(file_path):

    version_info = detect_stix_version(file_path)
    data = normalize(file_path, version_info)

    texts = []
    labels = []

    for obj in data:

        text = obj.get("description", "")

        # -------- LABELING --------
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

    print("Original distribution:", Counter(labels))

    # -------- BALANCING --------
    data_pairs = list(zip(texts, labels))

    class_0 = [x for x in data_pairs if x[1] == 0]
    class_1 = [x for x in data_pairs if x[1] == 1]

    min_size = min(len(class_0), len(class_1))

    class_0 = random.sample(class_0, min_size)
    class_1 = random.sample(class_1, min_size)

    balanced = class_0 + class_1
    random.shuffle(balanced)

    texts, labels = zip(*balanced)

    print("Balanced distribution:", Counter(labels))

    return list(texts), list(labels)


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

    # Save separate files (IMPORTANT)
    with open("model_balanced.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("vectorizer_balanced.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("Balanced model trained & saved successfully!")
