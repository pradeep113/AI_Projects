# backend/parser.py
import xml.etree.ElementTree as ET

def parse_project_xml(xml_content):
    try:
        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()
        actions = []
        for module in root.findall("module"):
            mod_name = module.get("name", "Unnamed")
            for elem in module:
                tag = elem.tag.lower()
                label = elem.get("label", "No Label")
                details = {k: v for k, v in elem.attrib.items()}
                actions.append({
                    "Module": mod_name,
                    "Action": tag,
                    "Label": label,
                    "Details": details
                })
        return actions
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {e}")

