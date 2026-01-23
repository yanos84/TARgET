from tests.contracts.engine.fta.acceptor_contracts import (
    ContractedRankedBottomUpAcceptor,
)
from tests.contracts.engine.fta.complement_contracts import (
    ContractedComplement,
)

CONTRACT_OVERRIDES = {
    "RankedBottomUpAcceptor": ContractedRankedBottomUpAcceptor,
    "Complement": ContractedComplement,
}
