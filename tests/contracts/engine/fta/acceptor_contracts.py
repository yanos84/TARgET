import icontract
from icontract import ViolationError
from TARgET.core.rankedTree import RankedTree
from TARgET.engine.fta.acceptors.rankedAcceptor import RankedBottomUpAcceptor


# ======================================================
# Helper predicates
# ======================================================

def tree_is_not_none(automaton, tree):
    return tree is not None


def tree_is_ranked_tree(automaton, tree):
    return isinstance(tree, RankedTree)


def result_is_bool(result):
    return isinstance(result, bool)


def has_compute_states(self):
    return callable(getattr(self, "_compute_states", None))


# ======================================================
# Contracted test-only subclass
# ======================================================

@icontract.invariant(
    lambda self: has_compute_states(self),
    error=lambda self: ViolationError(
        "RankedBottomUpAcceptor must define a callable _compute_states method"
    ),
)
class ContractedRankedBottomUpAcceptor(RankedBottomUpAcceptor):

    @icontract.require(
        tree_is_not_none,
        error=lambda automaton, tree: ViolationError(
            "Tree must not be None"
        ),
    )
    @icontract.require(
        tree_is_ranked_tree,
        error=lambda automaton, tree: ViolationError(
            f"Tree must be a RankedTree, got {type(tree)}"
        ),
    )
    @icontract.ensure(
        result_is_bool,
        error=lambda result: ViolationError(
            f"accepts must return bool, got {type(result)}"
        ),
    )
    @icontract.snapshot(lambda tree: tree.structure(), name="tree_before")
    @icontract.ensure(
        lambda tree, OLD: tree.structure() == OLD.tree_before,
        "accepts must not mutate the input tree"
    )
    def accepts(self, automaton, tree):
        return super().accepts(automaton, tree)
