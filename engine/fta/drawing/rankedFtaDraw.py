from graphviz import Digraph
from fta.rankedfta import ranked_Fta
from fta.rankedRule import ranked_Rule
from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator

def draw_ranked_fta(fta: ranked_Fta):

    """Draws a ranked finite tree automaton (RFTA) using Graphviz.
    The function takes a ranked finite tree automaton (RFTA) as input and generates a visual representation of the automaton using Graphviz. The states of the automaton are represented as nodes, with final states depicted as double circles. The transitions between states are represented as directed edges, with the transition rules labeled on the edges. The resulting graph can be rendered and saved as an image file   for visualization and analysis purposes.
    Args:
        fta: a ranked finite tree automaton (RFTA) to be drawn
    Returns:
        A Graphviz Digraph object representing the visual structure of the RFTA.
    """

    dot = Digraph(name=fta.name, engine="dot")
    dot.attr(rankdir="TB")

    # --- States ---
    for q in fta.fta_states:
        if q.is_Final:
            dot.node(q.name, shape="doublecircle")
        else:
            dot.node(q.name, shape="circle")

    # --- Transitions ---
    for idx, rule in enumerate(fta.transitions):

        if not isinstance(rule, ranked_Rule):
            raise TypeError(
                f"Expected ranked_Rule, got {type(rule)}: {rule}"
            )

        # unique node per rule (important if rules repeat)
        rule_node = f"{rule.func.name}_{idx}"
        idx += 1

        dot.node(
            rule_node,
            label=rule.func.name,
            shape="box",
            style="filled",
            fillcolor="lightgray"
        )

        # input states → symbol
        for q in rule.input_states:
            dot.edge(q.name, rule_node)

        # symbol → output state
        dot.edge(rule_node, rule.output_state.name)

    return dot


## Example usage
if __name__ == "__main__":
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    automaton = generator.generate()
    automaton.print_Fta()

    dot = draw_ranked_fta(automaton)
    dot.render("fta1", format="png", cleanup=True) 