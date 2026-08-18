import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.algebraic.semiring import Semiring

from TARgET.engine.fta.acceptors.weight_rank_acceptor import (
    WeightedRankedBottomUpAcceptor,
)


# ======================================================
# Helper predicates
# ======================================================

def automaton_is_ranked_fta(automaton):
    return isinstance(automaton, ranked_Fta)


def tree_is_ranked_tree(tree):
    return isinstance(tree, RankedTree)


def result_is_semiring(result):
    return isinstance(result, Semiring)


# ======================================================
# Contracted test-only subclass
# ======================================================

class ContractedWeightedRankedBottomUpAcceptor(
    WeightedRankedBottomUpAcceptor
):

    @icontract.require(
        automaton_is_ranked_fta,
        error=lambda automaton: ViolationError(
            f"Automaton must be a ranked_Fta, got {type(automaton)}"
        ),
    )
    @icontract.require(
        tree_is_ranked_tree,
        error=lambda tree: ViolationError(
            f"Tree must be a RankedTree, got {type(tree)}"
        ),
    )
    @icontract.ensure(
        result_is_semiring,
        error=lambda result: ViolationError(
            f"accepts must return a Semiring, got {type(result)}"
        ),
    )
    def accepts(self, automaton, tree):
        return super().accepts(automaton, tree)