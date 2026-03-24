from src.ml.predict_balanced import predict

path = "data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json"

result = predict(path)

# print few malware
print("---- MALWARE ----")
for r in result:
    if r["type"] == "malware":
        print(r)
        break

# print few tools
print("\n---- TOOLS ----")
count = 0
for r in result:
    if r["type"] == "tool":
        print(r)
        count += 1
    if count == 5:
        break
