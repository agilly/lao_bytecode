import xml.etree.ElementTree as ET

def get_coverage(coverage_elem):
    return [glyph.attrib["value"] for glyph in coverage_elem.findall("Glyph")]

def parse_ttx_gsub_rules(ttx_file):
    tree = ET.parse(ttx_file)
    root = tree.getroot()

    gsub = root.find("GSUB")
    if gsub is None:
        raise ValueError("No <GSUB> table found in the TTX file.")

    lookup_list = gsub.find("LookupList")
    if lookup_list is None:
        raise ValueError("No <LookupList> found in the GSUB table.")

    rules = []

    for lookup in lookup_list.findall("Lookup"):
        lookup_index = lookup.attrib.get("index")
        lookup_type_elem = lookup.find("LookupType")
        lookup_type = lookup_type_elem.attrib.get("value") if lookup_type_elem is not None else None

        # Iterate over all direct children of <Lookup>
        for child in lookup:
            tag = child.tag

            if tag == "SingleSubst":
                for sub in child.findall("Substitution"):
                    rules.append({
                        "lookup_index": lookup_index,
                        "type": "SingleSubst",
                        "in": sub.attrib["in"],
                        "out": sub.attrib["out"]
                    })

            elif tag == "MultipleSubst":
                for seq in child.findall("Sequence"):
                    input_glyph = seq.attrib["name"]
                    output = [s.attrib["value"] for s in seq.findall("Substitute")]
                    rules.append({
                        "lookup_index": lookup_index,
                        "type": "MultipleSubst",
                        "in": input_glyph,
                        "out": output
                    })

            elif tag == "AlternateSubst":
                for altset in child.findall("AlternateSet"):
                    input_glyph = altset.attrib["glyph"]
                    output = [alt.attrib["value"] for alt in altset.findall("Alternate")]
                    rules.append({
                        "lookup_index": lookup_index,
                        "type": "AlternateSubst",
                        "in": input_glyph,
                        "out": output
                    })

            elif tag == "LigatureSubst":
                for lig_set in child.findall("LigatureSet"):
                    first = lig_set.attrib["glyph"]
                    for lig in lig_set.findall("Ligature"):
                        components = [first] + lig.attrib["components"].split(",")
                        rules.append({
                            "lookup_index": lookup_index,
                            "type": "LigatureSubst",
                            "in": components,
                            "out": lig.attrib["glyph"]
                        })

            # elif tag == "ChainContextSubst" and child.attrib.get("Format") == "3":
            #     backtrack = []
            #     input_glyphs = []
            #     lookahead = []
            #     substs = []

            #     for coverage in child.findall("BacktrackCoverage"):
            #         backtrack.extend(get_coverage(coverage))

            #     for coverage in child.findall("InputCoverage"):
            #         input_glyphs.extend(get_coverage(coverage))

            #     for coverage in child.findall("LookAheadCoverage"):
            #         lookahead.extend(get_coverage(coverage))

            #     for record in child.findall("SubstLookupRecord"):
            #         substs.append({
            #             "SequenceIndex": record.attrib["SequenceIndex"],
            #             "LookupListIndex": record.attrib["LookupListIndex"]
            #         })

            #     rules.append({
            #         "lookup_index": lookup_index,
            #         "type": "ChainContextSubst_Format3",
            #         "backtrack": backtrack,
            #         "input": input_glyphs,
            #         "lookahead": lookahead,
            #         "substitutions": substs
            #     })

            # You may still want to check SubTable children if they exist
            elif tag == "SubTable":
                # fallback: parse subtables as before (optional)
                for subt in child:
                    subt_tag = subt.tag
                    # Similar parsing as above can be done here, or just warn unknown
                    rules.append({
                        "lookup_index": lookup_index,
                        "type": subt_tag,
                        "detail": "SubTable child substitution - parsing not implemented"
                    })

            else:
                rules.append({
                    "lookup_index": lookup_index,
                    "type": tag,
                    "detail": "Unhandled or unknown substitution type"
                })

    return rules

# Example usage
if __name__ == "__main__":
    rules = parse_ttx_gsub_rules("./output_files/Phetsarath-Regular-GSUB.ttx")
    for rule in rules:
        print(rule)
