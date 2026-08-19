from ..difference.ranked_diff import Ranked_Diff
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.emptiness.ranked_emptiness import RankedEmptiness



def is_equivalent(self, fta1: ranked_Fta, fta2: ranked_Fta) -> bool:
    """
    Check whether two ranked finite tree automata (RFTAs) are equivalent.

    Two RFTAs are equivalent if neither language contains a tree that is
    absent from the other language. This is checked by computing both
    differences and verifying that both resulting languages are empty.

    :param fta1: The first ranked finite tree automaton.
    :param fta2: The second ranked finite tree automaton.

    :returns: ``True`` if the automata are equivalent; otherwise, ``False``.
    :rtype: bool
    """
    emptiness_checker = RankedEmptiness()

    difference_1 = Ranked_Diff().diff(fta1, fta2)
    difference_2 = Ranked_Diff().diff(fta2, fta1)

    return (
        emptiness_checker.is_empty(difference_1)
        and emptiness_checker.is_empty(difference_2)
    )