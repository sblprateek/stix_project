# 🛡️ STIX Threat Intelligence Analyzer

An end-to-end AI system to analyze Cyber Threat Intelligence (CTI) across **STIX 1.x (XML), STIX 2.0, and STIX 2.1 (JSON)**, classify threats using Machine Learning, and compute a **trust score** for each object.

---

## 🚀 What This Project Does

Given any STIX file, the system will:

1. **Detect** the STIX version (1.x / 2.0 / 2.1).
2. **Parse and normalize** data into a common CTI format.
3. **Extract** useful features (IP, domain, URL, hash).
4. **Predict** using an ML model if it's a threat or non-threat.
5. **Compute** a trust score.
6. **Output** results in a clean, readable format.

---

## 🧠 Pipeline

`STIX Input` ➡️ `Detection` ➡️ `Normalization` ➡️ `CTI` ➡️ `ML Model` ➡️ `Trust Score` ➡️ `Output`

---

## 📂 Project Structure

```text
stix_project/
├── data/
│   ├── stix1_xml/
│   │   ├── apt1.xml
│   │   ├── malware.xml
│   │   └── phishing.xml
│   ├── stix2_0_json/
│   │   └── cti/
│   └── stix2_1_json/
│       └── attack-stix-data/
├── src/
│   ├── detection/
│   │   └── detect.py
│   ├── ml/
│   │   ├── predict.py
│   │   ├── predict_balanced.py
│   │   ├── train_model.py
│   │   └── train_model_balanced.py
│   ├── normalization/
│   │   └── normalize.py
│   └── credibility/
│       └── trust.py
├── main.py
├── run.sh
├── model.pkl
├── model_balanced.pkl
├── test_detect.py
├── test_normalize.py
├── test_predict.py
├── test_predict_balanced.py
├── vectorizer.pkl
└── vectorizer_balanced.pkl
```

---

## ⚙️ Setup Instructions (IMPORTANT)

### 1️⃣ Clone the repo
```bash
git clone --recursive https://github.com/sblprateek/stix_project
cd stix_project
```

### 2️⃣ Install dependencies
```bash
pip install scikit-learn
```
*(That’s enough to run everything)*

### 3️⃣ Make script executable (IMPORTANT)
Before using the command-line runner, you need to grant it execution permissions:
```bash
chmod +x run.sh
```

### 4️⃣ Verify structure
Make sure your root directory has:
* The `data/` folder containing the datasets.
* The pre-trained models: `model_balanced.pkl` and `vectorizer_balanced.pkl`.

---

## 🚀 How to Run

Run the full pipeline with a single command by passing the file path as an argument.

▶️ **Balanced Model (Recommended)**
```bash
./run.sh --balanced data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json
```

▶️ **Baseline Model**
```bash
./run.sh --baseline data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json
```

### 📥 Example Inputs to Test
* **STIX 2.1:** `data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json`
* **STIX 2.0:** `data/stix2_0_json/cti/enterprise-attack/enterprise-attack.json`
* **STIX 1.x:** `data/stix1_xml/apt1.xml`

### 📤 Output Example
```text
Name: TrickBot
Type: malware
Threat: 1
Trust Score: 0.75
----------------------------------------
```

---

## 🤖 Models Used

🔹 **Balanced Model (USED IN MAIN & run.sh)**
* Trained on a balanced dataset.
* Reduces bias toward the "threat" class.
* Uses TF-IDF + Logistic Regression.

🔹 **Baseline Model**
* Trained on an imbalanced dataset.
* Kept primarily for baseline testing and comparison.
* Uses TF-IDF + Logistic Regression.

---

## 📊 Key Design Choices

* **Common CTI format:** Unifies all STIX versions into a single representation, simplifying the ML pipeline.
* **TF-IDF + Logistic Regression:** Fast, highly interpretable, and effective for text-based feature classification.
* **Balanced training:** Prevents the model from blindly guessing the majority class.
* **Trust score:** Adds a crucial layer of interpretability using confidence intervals, source tracking, and metadata completeness.

---

## 🧪 Testing (Optional)

You can verify individual modules by running the test scripts:

```bash
python3 test_detect.py
python3 test_normalize.py
python3 test_predict.py
python3 test_predict_balanced.py
```

---

## ⚠️ Notes

* Some malware may occasionally be predicted as a non-threat depending on the quality and depth of the description inside the STIX file (this is normal NLP ML behavior).
* The STIX 1.x dataset is limited and used mainly for backward compatibility testing.
* Trust scores may appear similar across different objects if their underlying metadata completeness and source context are similar.

---

### ✅ Summary
This project builds a complete intelligent CTI analysis pipeline:
* Multi-STIX support ✅
* AI-based threat classification ✅
* Trust scoring system ✅
* CLI execution via `run.sh` ✅
* Fully working end-to-end system ✅
