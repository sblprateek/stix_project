#!/bin/bash

# -----------------------------
# STIX Analyzer Runner Script
# -----------------------------

# Usage:
# ./run.sh --balanced <file_path>
# ./run.sh --baseline <file_path>

if [ "$#" -ne 2 ]; then
    echo "Usage: ./run.sh --balanced|--baseline <file_path>"
    exit 1
fi

MODE=$1
FILE=$2

# Check file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File not found -> $FILE"
    exit 1
fi

echo "----------------------------------------"
echo "STIX Threat Intelligence Analyzer"
echo "Mode: $MODE"
echo "File: $FILE"
echo "----------------------------------------"

# Run based on mode
if [ "$MODE" == "--balanced" ]; then

    python3 - <<EOF
from src.ml.predict_balanced import predict

results = predict("$FILE")

print("\n--- RESULTS (BALANCED MODEL) ---\n")

for r in results[:10]:
    print(f"Name: {r['name']}")
    print(f"Type: {r['type']}")
    print(f"Threat: {r['threat']}")
    print(f"Trust Score: {r['trust_score']}")
    print("-" * 40)
EOF

elif [ "$MODE" == "--baseline" ]; then

    python3 - <<EOF
from src.ml.predict import predict

results = predict("$FILE")

print("\n--- RESULTS (BASELINE MODEL) ---\n")

for r in results[:10]:
    print(f"Name: {r['name']}")
    print(f"Type: {r['type']}")
    print(f"Threat: {r['threat']}")
    print(f"Trust Score: {r['trust_score']}")
    print("-" * 40)
EOF

else
    echo "Invalid mode. Use --balanced or --baseline"
    exit 1
fi
