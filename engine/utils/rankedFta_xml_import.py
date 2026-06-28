import xml.etree.ElementTree as ET
from TARgET.fta.state import State
from TARgET.fta.rankedfta import ranked_Fta
from TARgET.fta.rankedRule import ranked_Rule
from TARgET.core.symbol import Ranked_Symbol

def load_fta_from_xml(filename: str) -> ranked_Fta:
    """
    Load a ranked finite tree automaton from an XML file.
    """

    tree = ET.parse(filename)
    root = tree.getroot()

    if root.tag != "RankedFta":
        raise ValueError("Invalid XML format: root tag must be <RankedFta>")

    fta_name = root.attrib.get("name")

    # ------------------------------------------------------------------
    # STATES
    # ------------------------------------------------------------------
    states = []
    states_elem = root.find("States")

    if states_elem is None:
        raise ValueError("Missing <States> section")

    for st_elem in states_elem.findall("State"):
        name = st_elem.attrib["name"]
        final = st_elem.attrib.get("final", "false") == "true"
        initial = st_elem.attrib.get("initial", "false") == "true"

        state = State(name=name, is_Final=final, is_Initial=initial)
        states.append(state)

    # ------------------------------------------------------------------
    # ALPHABET
    # ------------------------------------------------------------------
    alphabet = []
    alphabet_elem = root.find("Symbols")

    if alphabet_elem is None:
        raise ValueError("Missing <alphabet> section")

    for sym_elem in alphabet_elem.findall("Symbol"):
        name = sym_elem.attrib["name"]
        rank = int(sym_elem.attrib["arity"])

        symbol = Ranked_Symbol(name=name, rank=rank)
        alphabet.append(symbol)

    state_by_name = {st.name: st for st in states} #build dictionary of states for lookup
    symbol_by_name = {sym.name: sym for sym in alphabet} #build dictionary of symbols for lookup

    # ------------------------------------------------------------------
    # TRANSITIONS
    # ------------------------------------------------------------------
    transitions = []
    _symbol = None
    trans_elem = root.find("transitions")

    if trans_elem is None:
        raise ValueError("Missing <transitions> section")

    for rule_elem in trans_elem.findall("rule"):

        # Symbol
        sym_elem = rule_elem.find("symbol")
        if sym_elem is None:
            raise ValueError("Rule without symbol")

        sym_name = sym_elem.attrib["name"]
        if sym_name not in symbol_by_name:
            raise ValueError(f"Unknown symbol '{sym_name}' in rule")

        _symbol = symbol_by_name[sym_name]

        # Input states
        input_states = []
        input_elem = rule_elem.find("input")

        if input_elem is None:
            raise ValueError("Rule without input")

        for st in input_elem.findall("state"):
            st_name = st.attrib["name"]
            if st_name not in state_by_name:
                raise ValueError(f"Unknown state '{st_name}' in rule input")
            input_states.append(state_by_name[st_name])

        # Output state
        output_elem = rule_elem.find("output")
        if output_elem is None:
            raise ValueError("Rule without output")

        out_name = output_elem.attrib["state"]
        if out_name not in state_by_name:
            raise ValueError(f"Unknown state '{out_name}' in rule output")

        out_state = state_by_name[out_name]

        # Build rule
        rule = ranked_Rule(
            func=_symbol,
            input_states=input_states,
            output_state=out_state
        )

        if not rule.is_valid():
            raise ValueError("Invalid ranked rule (arity mismatch)")

        transitions.append(rule)

    # ------------------------------------------------------------------
    # BUILD AUTOMATON
    # ------------------------------------------------------------------
    fta = ranked_Fta(
        fta_name=fta_name,
        alphabet=alphabet,
        fta_states=states,
        transitions=transitions
    )

    return fta

# Example usage
if __name__ == "__main__":
    fta = load_fta_from_xml("random_rfta.xml")
    fta.print_Fta()