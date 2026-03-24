def detect_stix_version(file_path):

    import json
    import xml.etree.ElementTree as ET

    # Try JSON (STIX 2.x)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

            if data.get("type") == "bundle":

                version = data.get("spec_version")

                if not version and "objects" in data and len(data["objects"]) > 0:
                    version = data["objects"][0].get("spec_version", "unknown")

                return {
                    "format": "STIX",
                    "version": version,
                    "type": "JSON"
                }

    except:
        pass

    # Try XML (STIX 1.x)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        if "STIX_Package" in root.tag:
            return {
                "format": "STIX",
                "version": "1.x",
                "type": "XML"
            }

    except:
        pass

    return {
        "format": "Unknown",
        "version": "Unknown",
        "type": "Unknown"
    }
