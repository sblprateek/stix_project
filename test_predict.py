from src.ml.predict import predict

path = "data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json"

result = predict(path)

print(result[:50])
