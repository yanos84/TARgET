import icontract
from icontract import ViolationError

from TARgET.engine.fta.determinism.determinism import Determinism


def rules_are_iterable(rules):
    try:
        iter(rules)
        return True
    except TypeError:
        return False


def semantics_has_transition_signature(semantics):
    return (
        semantics is not None
        and callable(getattr(semantics, "transition_signature", None))
    )


def result_is_bool(result):
    return isinstance(result, bool)


class ContractedDeterminism(Determinism):

    @staticmethod
    @icontract.require(
        rules_are_iterable,
        error=lambda rules: ViolationError(
            f"rules must be iterable, got {type(rules)}"
        ),
    )
    @icontract.require(
        semantics_has_transition_signature,
        error=lambda rules, semantics: ViolationError(
            "semantics must provide a callable transition_signature method"
        ),
    )
    @icontract.ensure(
        result_is_bool,
        error=lambda rules, semantics, result: ViolationError(
            f"check must return bool, got {type(result)}"
        ),
    )
    def check(rules, semantics):
        return Determinism.check(rules, semantics)