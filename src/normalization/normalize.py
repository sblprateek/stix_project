import json
import xml.etree.ElementTree as ET
import re


# -------- FEATURE EXTRACTION --------
def extract_features(text):
    if not text:
        return {"ip": [], "domain": [], "hash": [], "url": []}

    ip = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
    url = re.findall(r'https?://\S+', text)
    domain = re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)
    hash_val = re.findall(r'\b[a-fA-F0-9]{32,64}\b', text)

    return {
        "ip": ip,
        "domain": domain,
        "hash": hash_val,
        "url": url
    }


# -------- STIX 2.x NORMALIZATION --------
def normalize_stix2(file_path):
    with open(file_path) as f:
        data = json.load(f)

    objects = data.get("objects", [])
    normalized = []

    important_types = [
        "attack-pattern",
        "malware",
        "indicator",
        "tool",
        "intrusion-set"
    ]

    for obj in objects:

        if obj.get("type") not in important_types:
            continue

        description = obj.get("description", "")

        normalized.append({
            "id": obj.get("id"),
            "type": obj.get("type"),
            "name": obj.get("name", ""),
            "description": description,
            "confidence": obj.get("confidence", 50),
            "created": obj.get("created", ""),
            "source": "MITRE",

            "features": extract_features(description)
        })

    return normalized


# -------- STIX 1.x NORMALIZATION --------
def normalize_stix1(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    normalized = []

    title = ""
    description = ""

    for elem in root.iter():
        if "Title" in elem.tag:
            title = elem.text
        if "Description" in elem.tag:
            description = elem.text

            normalized.append({
                "id": "stix1",
                "type": "indicator",
                "name": title,
                "description": description,
                "confidence": 50,
                "created": "",
                "source": "STIX1",

                "features": extract_features(description)
            })

    return normalized


# -------- MAIN NORMALIZATION --------
def normalize(file_path, version_info):

    if version_info["version"] in ["2.0", "2.1"]:
        return normalize_stix2(file_path)

    elif version_info["version"] == "1.x":
        return normalize_stix1(file_path)

    return []
