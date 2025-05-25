import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_gsub(ttx_path):
    tree = ET.parse(ttx_path)
    root = tree.getroot()

    # GSUB elements
    gsub = root.find(".//GSUB")
    if gsub is None:
        raise ValueError("No GSUB table found in this TTX file.")

    # Feature tag -> lookup index list
    feature_to_lookups = defaultdict(list)
    for feature in gsub.findall(".//FeatureRecord"):
        tag = feature.find("FeatureTag").attrib["value"]
        lookup_indices = [int(idx.attrib["value"]) for idx in feature.findall(".//LookupListIndex")]
        feature_to_lookups[tag].extend(lookup_indices)

    # Lookup index -> list of substitution rules
    lookup_rules = defaultdict(list)
    lookups = gsub.find("LookupList")
    for lookup in lookups.findall("Lookup"):
        index = int(lookup.attrib["index"])
        lookup_type = int(lookup.attrib["LookupType"])

        if lookup_type == 1:
            # Single substitutions
            for subst in lookup.findall(".//SubstFormat1/Substitution"):
                lookup_rules[index].append(("single", subst.attrib["in"], subst.attrib["out"]))
        elif lookup_type == 4:
            # Ligature substitutions
            for ligset in lookup.findall(".//LigatureSet"):
                first = ligset.attrib["glyph"]
                for lig in ligset.findall("Ligature"):
                    components = [first] + [comp.attrib["glyph"] for comp in lig.findall("Component")]
                    ligature = lig.attrib["glyph"]
                    lookup_rules[index].append(("ligature", components, ligature))
        elif lookup_type == 6:
            # Contextual substitutions (basic example)
            lookup_rules[index].append(("contextual", "See LookupType=6"))  # Simplified
        else:
            lookup_rules[index].append(("other", f"LookupType={lookup_type} not parsed"))

    # Final mapping: feature -> list of readable rules
    result = {}
    for feature, indices in feature_to_lookups.items():
        result[feature] = []
        for idx in indices:
            result[feature].extend(lookup_rules[idx])

    return result

# Example usage:
if __name__ == "__main__":
    gsub_info = parse_gsub("./output_files/Phetsarath-Regular.G_S_U_B_.ttx")
    for feature, rules in gsub_info.items():
        print(f"\nFeature: {feature}")
        for rule in rules:
            print("  ", rule)
