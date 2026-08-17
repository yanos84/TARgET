from .acceptor import Acceptor
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.fta.state import State
from typing import Set

class RankedBottomUpAcceptor(Acceptor):
    """
    Bottom-up acceptance algorithm for ranked finite tree automata.
    Implements a bottom-up traversal of the tree, computing possible
    states for each subtree based on the automaton's transition rules.

    Args:
        automaton: a ranked finite tree automaton
        tree: a ranked tree structure  
    Returns:
        bool: True if the automaton accepts the tree, False otherwise
    """

    def accepts(self, automaton: ranked_Fta, tree: RankedTree) -> bool:
        """
        Check whether the automaton accepts the given tree.
        """
        root_states = self._compute_states(automaton, tree)
        return any(state.is_Final for state in root_states)

    def _compute_states(
        self,
        automaton: ranked_Fta,
        tree: RankedTree
    ) -> Set[State]:
        """
        Compute the set of states that can be assigned to the root
        of the given subtree.
        """

        # 1️⃣ Compute states for children
        children_states = [
            self._compute_states(automaton, child)
            for child in tree.children
        ]

        # 2️⃣ Match ranked rules
        possible_states = set()

        for rule in automaton.transitions:

            if rule.func != tree.ranked_symbol:
                continue

            if len(rule.input_states) != len(children_states):
                continue

            # Check if rule is compatible with children
            compatible = True
            for expected_state, child_set in zip(rule.input_states, children_states):
                if expected_state not in child_set:
                    compatible = False
                    break

            if compatible:
                possible_states.add(rule.output_state)

        return possible_states

#___defining example functions for testing the RankedBottomUpAcceptor class___


def nullary_tree_example():
    """
    Create a simple nullary tree (a single node).
    """
    a = Ranked_Symbol(name="a", rank=0)
    null_tree =  RankedTree(symbol=a)
    s1 = State(name="q1", is_Final=True)
    rule1 = ranked_Rule(func=a, input_states=[], output_state=s1   )
    rule1 = [rule1]
    alpha = [a]
    st = [s1]
    fta = ranked_Fta(fta_name="nullary_test", alphabet=alpha, fta_states=st, transitions=rule1)
    acceptor = RankedBottomUpAcceptor()
    if acceptor.accepts(fta, null_tree):
        print("Nullary Tree accepted")
    else:
        print("Nullary Tree rejected")

def nullary_tree_no_transition():
    """
    The tree contains symbol a, but the automaton has no
    transition for a.
    Expected result: rejected.
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    null_tree = RankedTree(symbol=a)

    s1 = State(name="q1", is_Final=True)

    rule1 = ranked_Rule(
        func=b,
        input_states=[],
        output_state=s1
    )

    fta = ranked_Fta(
        fta_name="nullary_no_transition",
        alphabet=[a, b],
        fta_states=[s1],
        transitions=[rule1]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, null_tree):
        print("ERROR: Tree was accepted without a matching transition")
    else:
        print("Nullary tree correctly rejected")

def random_automaton_tree_acceptance():
    """
    Generate a random ranked finite tree automaton and a random tree,
    then check if the automaton accepts the tree.
    """
# Create a simple ranked tree: f(a, b)
    f = Ranked_Symbol(name="f0", rank=2)
    a = Ranked_Symbol(name="f1", rank=0)

    root = RankedTree(symbol=f)
    child1 = RankedTree(symbol=a)
    child2 = RankedTree(symbol=a)

    root.add_child(child1)
    root.add_child(child2)

    print(root)  # Output: f(a,a)
    print("Is well formed:", root.is_well_formed())  # Output: True
    generator = RandomRankedFtaGenerator(
    n_states=3,
    n_symbols=2,
    max_rank=2,
    n_rules=8,
    seed=4512
)
    automaton = generator.generate()
    automaton.print_Fta()
    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(automaton, root):
        print("Tree accepted")
    else:
        print("Tree rejected")


def nullary_multiple_transitions():
    """
    A nullary symbol has two possible output states.
    Only one of them is final.

    a() -> q1
    a() -> q2

    q2 is final.

    Expected result: accepted.
    """
    a = Ranked_Symbol(name="a", rank=0)

    null_tree = RankedTree(symbol=a)

    s1 = State(name="q1", is_Final=False)
    s2 = State(name="q2", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=s1
    )

    rule2 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=s2
    )

    fta = ranked_Fta(
        fta_name="nullary_multiple_transitions",
        alphabet=[a],
        fta_states=[s1, s2],
        transitions=[rule1, rule2]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, null_tree):
        print("Nullary tree correctly accepted")
    else:
        print("ERROR: Nullary tree was rejected")

def unary_tree_example():
    """
    Test a simple unary tree:

        f(a)

    with:

        a()   -> q0
        f(q0) -> qf

    qf is final.

    Expected result: accepted.
    """
    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    tree = RankedTree(symbol=f)
    child = RankedTree(symbol=a)
    tree.add_child(child)

    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=f,
        input_states=[q0],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_name="unary_test",
        alphabet=[a, f],
        fta_states=[q0, qf],
        transitions=[rule1, rule2]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, tree):
        print("Unary tree correctly accepted")
    else:
        print("ERROR: Unary tree was rejected")

def unary_tree_wrong_child_state():
    """
    Test:

        f(a)

    Automaton:

        a()   -> q0
        f(q1) -> qf

    Since a produces q0 rather than q1, the tree must be rejected.
    """
    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    tree = RankedTree(symbol=f)
    child = RankedTree(symbol=a)
    tree.add_child(child)

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=f,
        input_states=[q1],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_name="unary_wrong_child",
        alphabet=[a, f],
        fta_states=[q0, q1, qf],
        transitions=[rule1, rule2]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, tree):
        print("ERROR: Unary tree was incorrectly accepted")
    else:
        print("Unary tree correctly rejected")


def binary_tree_example():
    """
    Test:

        f(a,b)

    Automaton:

        a()        -> q0
        b()        -> q1
        f(q0,q1)   -> qf

    qf is final.

    Expected result: accepted.
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    child1 = RankedTree(symbol=a)
    child2 = RankedTree(symbol=b)

    tree.add_child(child1)
    tree.add_child(child2)

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=b,
        input_states=[],
        output_state=q1
    )

    rule3 = ranked_Rule(
        func=f,
        input_states=[q0, q1],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_name="binary_test",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=[rule1, rule2, rule3]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, tree):
        print("Binary tree correctly accepted")
    else:
        print("ERROR: Binary tree was rejected")

def binary_tree_reversed_children():
    """
    Test:

        f(b,a)

    Automaton expects:

        f(q0,q1)

    where:

        a() -> q0
        b() -> q1

    Therefore f(b,a) must be rejected.
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    child1 = RankedTree(symbol=b)
    child2 = RankedTree(symbol=a)

    tree.add_child(child1)
    tree.add_child(child2)

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=b,
        input_states=[],
        output_state=q1
    )

    rule3 = ranked_Rule(
        func=f,
        input_states=[q0, q1],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_name="binary_reversed",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=[rule1, rule2, rule3]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, tree):
        print("ERROR: Reversed binary tree was incorrectly accepted")
    else:
        print("Reversed binary tree correctly rejected")

def binary_tree_wrong_arity():
    """
    Test:

        f(a,b)

    The automaton only has:

        f(q0) -> qf

    Therefore the transition has the wrong arity and must not match.
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))
    tree.add_child(RankedTree(symbol=b))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=b,
        input_states=[],
        output_state=q1
    )

    # Wrong arity: f has rank 2, but this rule expects only one state.
    rule3 = ranked_Rule(
        func=f,
        input_states=[q0],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_name="binary_wrong_arity",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=[rule1, rule2, rule3]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, tree):
        print("ERROR: Wrong-arity transition was incorrectly used")
    else:
        print("Wrong-arity transition correctly rejected")

def nondeterministic_internal_subtree():
    """
    Test nondeterminism below the root.

        a() -> q0
        a() -> q1

        f(q0) -> q2
        f(q1) -> qf

    qf is final.

    Tree:

        f(a)

    The subtree a can produce both q0 and q1.
    Therefore f(a) can produce q2 and qf.
    The tree must be accepted.
    """
    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q1
    )

    rule3 = ranked_Rule(
        func=f,
        input_states=[q0],
        output_state=q2
    )

    rule4 = ranked_Rule(
        func=f,
        input_states=[q1],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_name="nondeterministic_internal",
        alphabet=[a, f],
        fta_states=[q0, q1, q2, qf],
        transitions=[rule1, rule2, rule3, rule4]
    )

    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(fta, tree):
        print("Nondeterministic internal tree correctly accepted")
    else:
        print("ERROR: Nondeterministic internal tree was rejected")
    

# Example usage:

if __name__ == "__main__":
    from TARgET.core.base.symbol import Ranked_Symbol
    from TARgET.core.fta.rankedRule import ranked_Rule
    from TARgET.engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator

    
    random_automaton_tree_acceptance()
    nullary_tree_example()
    nullary_tree_no_transition()
    nullary_multiple_transitions()
    unary_tree_example()
    unary_tree_wrong_child_state()
    binary_tree_example()
    binary_tree_reversed_children()
    binary_tree_wrong_arity()
    nondeterministic_internal_subtree()