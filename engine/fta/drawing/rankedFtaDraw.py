from graphviz import Digraph
from fta.rankedfta import ranked_Fta
from fta.rankedRule import ranked_Rule
from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator

def draw_ranked_fta(fta: ranked_Fta):

    '''
    Docstring for draw_ranked_fta
    
    :param fta: The ranked finite tree automaton to be drawn
    :type fta: ranked_Fta
    :return: A Graphviz Digraph representing the ranked FTA
    :rtype: Digraph
    Draws a ranked finite tree automaton using Graphviz.
    '''

    dot = Digraph(name=fta.name, engine="dot")
    dot.attr(rankdir="TB")

    # --- States ---
    for q in fta.states_list:
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
        for q in rule.input:
            dot.edge(q.name, rule_node)

        # symbol → output state
        dot.edge(rule_node, rule.output.name)

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