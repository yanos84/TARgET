
classDiagram

%% =======================
%% Core automata hierarchy
%% =======================

class Fta {
    +fta_name: str
    +fta_states: List[State]
}

class ranked_Fta {
    +alphabet: List[Ranked_Symbol]
    +transitions: List[ranked_Rule]
    +chech_weighted(): bool
    +get_semiring()
}

Fta <|-- ranked_Fta


%% =======================
%% States and symbols
%% =======================

class State {
    +name: str
    +is_Final: bool
    +is_Initial: bool
}

class Ranked_Symbol {
    +name: str
    +rank: int
}

ranked_Fta --> State
ranked_Fta --> Ranked_Symbol


%% =======================
%% Transition rules
%% =======================

class ranked_Rule {
    +func: Ranked_Symbol
    +input_states: List[State]
    +output_state: State
    +is_weighted: bool
    +weight
}

ranked_Fta --> ranked_Rule
ranked_Rule --> State
ranked_Rule --> Ranked_Symbol


%% =======================
%% Rational tree expressions
%% =======================

class Rte {
    <<abstract>>
}

class Zero
class One
class Atom
class function
class Plus
class CProduct
class CStar
class Weight

Rte <|-- Zero
Rte <|-- One
Rte <|-- Atom
Rte <|-- function
Rte <|-- Plus
Rte <|-- CProduct
Rte <|-- CStar
Rte <|-- Weight

Atom --> Ranked_Symbol
function --> Ranked_Symbol

Plus --> Rte
CProduct --> Rte
CStar --> Rte
Weight --> Rte


%% =======================
%% Semiring hierarchy
%% =======================

class Semiring {
    <<interface>>
    +__add__()
    +__mul__()
    +zero()
    +one()
}

class ProbabilitySemiring

Semiring <|-- ProbabilitySemiring

ranked_Rule --> Semiring
Weight --> Semiring