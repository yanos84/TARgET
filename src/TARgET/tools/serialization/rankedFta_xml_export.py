import xml.etree.ElementTree as ET
from xml.dom import minidom
from TARgET.core.fta.rankedfta import ranked_Fta

def export_ranked_fta_to_xml(automaton: ranked_Fta, file_name: str) -> None:
    """
    Export a ranked finite tree automaton (RFTA) to an XML file.

    :param automaton: The ranked finite tree automaton to export.
    :param file_path: The path to the output XML file.
    """

    root = ET.Element("RankedFta", {"name": automaton.name, "type": "Ranked"})

    # States
    states_elem = ET.SubElement(root, "States")
    for state in automaton.fta_states:
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
        for st in rule.input_states:
            ET.SubElement(input_elem, "state", {
                "name": st.name
            })

        ET.SubElement(rule_elem, "output", {
            "state": rule.output_state.name
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
    from TARgET.engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    random_fta = generator.generate()
    random_fta.print_Fta()
    #export_ranked_fta_to_xml(random_fta, "random_rfta.xml")


    from TARgET.core.base.symbol import Ranked_Symbol
    from TARgET.core.fta.state import State
    from TARgET.core.fta.rankedfta import ranked_Fta
    from TARgET.core.fta.rankedRule import ranked_Rule

    # Define states
    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=True)
    q3 = State("q3", is_Final=True)
    #q4 = State("q4", final=True)

    # Define symbols
    f = Ranked_Symbol("f", rank=2)
    g = Ranked_Symbol("g", rank=1)
    a = Ranked_Symbol("a", rank=0)
    b = Ranked_Symbol("b", rank=0)

    # Define transitions
    r1 = ranked_Rule(f, [q0, q2], q3)
    r2 = ranked_Rule(f, [q0, q3], q3)
    r3 = ranked_Rule(g, [q0], q2)
    r4 = ranked_Rule(f, [q1, q2], q3)
    r5 = ranked_Rule(f, [q1, q3], q3)
    r6 = ranked_Rule(g, [q1], q3)
    r8 = ranked_Rule(a, [], q0)
    r9 = ranked_Rule(b, [], q1)

    # Create FTA
    fta = ranked_Fta(
        fta_name="example_fta",
        alphabet=[f, a, g, b],
        fta_states=[q0, q1, q2, q3],
        transitions=[r1, r2, r3, r4, r5, r6,  r8, r9]
    )
    #export_ranked_fta_to_xml(fta, "dfta_for_minim.xml")
    #third fta for minimization
    qa = State("qa", is_Final=False)
    qb = State("qb", is_Final=True)
    qc = State("qc", is_Final=True)

    r11 = ranked_Rule(a, [], qa)
    r12 = ranked_Rule(b, [], qb)
    r13 = ranked_Rule(f, [qa, qa], qa)
    r14 = ranked_Rule(f, [qb, qb], qb)
    r15 = ranked_Rule(f, [qa, qb], qc)
    r16 = ranked_Rule(f, [qb, qa], qc)
    r17 = ranked_Rule(f, [qc, qa], qc)
    r18 = ranked_Rule(f, [qc,qb], qc)
    r19 = ranked_Rule(f, [qa, qc], qc)
    r20 = ranked_Rule(f, [qb,qc], qc)
    fta2 = ranked_Fta(
        fta_name="example_fta_2",
        alphabet=[f, a, b],
        fta_states=[qa, qb, qc],
        transitions=[r11, r12, r13, r14, r15, r16, r17, r18, r19, r20]
    )
    export_ranked_fta_to_xml(fta2, "dfta_for_minim_3.xml")

