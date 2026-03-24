from src.detection.detect import detect_stix_version

# STIX 2.1
print(detect_stix_version(
    "data/stix2_1_json/attack-stix-data/enterprise-attack/enterprise-attack.json"
))

# STIX 2.0
print(detect_stix_version(
    "data/stix2_0_json/cti/enterprise-attack/enterprise-attack.json"
))

# STIX 1.x
print(detect_stix_version(
    "data/stix1_xml/apt1.xml"
))
