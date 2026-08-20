import icontract

from TARgET.core.rte.rte import Rte
from TARgET.engine.rte.properties.nullable import nullable


@icontract.ensure(
    lambda r, result: isinstance(result, bool)
)
def contracted_nullable(r: Rte) -> bool:
    """Contracted nullable predicate used for testing."""
    return nullable(r)