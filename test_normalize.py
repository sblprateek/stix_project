from src.detection.detect import detect_stix_version
from src.normalization.normalize import normalize

# STIX 2.1
path = "data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json"
info = detect_stix_version(path)
data = normalize(path, info)

print("STIX 2.1 sample:", data[:2])


# STIX 1.x
path = "data/stix1_xml/apt1.xml"
info = detect_stix_version(path)
data = normalize(path, info)

print("STIX 1.x sample:", data)
