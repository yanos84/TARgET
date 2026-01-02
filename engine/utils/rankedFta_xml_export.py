import xml.etree.ElementTree as ET
from xml.dom import minidom
from fta.rankedfta import ranked_Fta

def export_ranked_fta_to_xml(automaton: ranked_Fta, file_name: str) -> None:
    """
    Export a ranked finite tree automaton (RFTA) to an XML file.

    Args:
        automaton: The ranked finite tree automaton to export.
        file_path: The path to the output XML file.
    """

    root = ET.Element("RankedFta", {"name": automaton.name, "type": "Ranked"})

    # States
    states_elem = ET.SubElement(root, "States")
    for state in automaton.states_list:
        ET.SubElement(states_elem, "State", {
            "name": state.name,
            "final": str(state.is_Final).lower(),
        })

    # Ranked Symbols
    symbols_elem = ET.SubElement(root, "Symbols")
    for symbol in automaton.alphabet:
        ET.SubElement(symbols_elem, "Symbol", {
            "name": symbol.name,
            "arity": str(symbol.rank)
        })
    
    # Rules
    transitions_elem = ET.SubElement(root, "transitions")

    for rule in automaton.transitions:
        rule_elem = ET.SubElement(transitions_elem, "rule")

        ET.SubElement(rule_elem, "symbol", {
            "name": rule.func.name
        })

        input_elem = ET.SubElement(rule_elem, "input")
        for st in rule.input:
            ET.SubElement(input_elem, "state", {
                "name": st.name
            })

        ET.SubElement(rule_elem, "output", {
            "state": rule.output.name
        })

    # Pretty print the XML
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # ---------- Write to file ----------
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

# Example usage

if __name__ == "__main__":
    from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    random_fta = generator.generate()
    random_fta.print_Fta()
    export_ranked_fta_to_xml(random_fta, "random_rfta.xml")