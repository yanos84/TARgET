# TARgET
## OVERVIEW

"TARgET: <ins>T</ins>ree <ins>A</ins>utomata and <ins>Reg</ins>ular <ins>E</ins>xpression <ins>T</ins>oolkit is an open-source Python library for the modeling, manipulation, transformation, and analysis of tree automata and related formal models. It provides a unified framework for implementing algorithms from formal language theory, term rewriting, and automata-based verification, while remaining extensible for research and educational purposes.

The toolkit offers a comprehensive collection of data structures and algorithms for constructing and manipulating finite tree automata, regular tree expressions, and term rewriting systems. It includes operations such as automata transformations, language-preserving constructions, reachability analysis, tree transformations, and visualization through Graphviz. These components are designed to facilitate the implementation, experimentation, and evaluation of algorithms commonly encountered in formal methods and program verification.

TARgET emphasizes modularity and extensibility. Its object-oriented architecture enables users to integrate new algorithms, define custom transformations, and extend existing components without modifying the core library. This design makes the toolkit suitable both as a reusable software library for research projects and as a foundation for developing new methods in automata theory and formal verification.

To further assist users, TARgET provides an optional AI-assisted module capable of supporting exploration of the library and generating guidance for available operations. This functionality complements the core toolkit while remaining independent of its primary analysis capabilities.

The project is implemented in Python and is accompanied by comprehensive API documentation, examples, and reproducible Conda environments, making it suitable for research, teaching, and rapid prototyping in areas including tree formal language theory, tree automata, term rewriting, model checking, and software verification.

## FEATURES

## Features

TARgET provides a comprehensive framework for working with tree automata and related formal models, including:

- **Comprehensive Framework**
  - Unified Python library for tree automata, term rewriting systems, and related formal models.

- **Extensible Architecture**
  - Modular object-oriented design.
  - Easily implement new automata operations, transformations, analysis algorithms, and data structures.
  - Designed to support research, experimentation, and rapid prototyping.

- **Tree Automata**
  - Construction and manipulation of finite tree automata.
  - Language analysis and automata operations.

- **Term Rewriting**
  - Representation of terms and rewrite rules.
  - Rewriting and reachability analysis.

- **Tree Transformations**
  - Support for implementing and applying transformation algorithms.

- **Visualization**
  - Graphviz-based visualization of automata, trees, and related structures.

- **Documentation and Examples**
  - Comprehensive API documentation and example workflows.

- **AI-Assisted Extensibility**
  - An optional AI assistant designed to facilitate the development of new TARgET modules.
  - Assists contributors in implementing new operations while adhering to the toolkit's architecture and software specifications.
  - Promotes consistency, maintainability, and faster integration of new functionalities into the framework.

## INSTALLATION


TARgET supports multiple installation methods to accommodate different user requirements. The recommended approach is to use one of the provided Conda environments, which ensure that all required dependencies are installed with compatible versions. A standard environment is available for the core toolkit, while an extended environment includes the optional AI assistant and its additional dependencies. Alternatively, TARgET can be installed via `pip`, with optional extras available to enable AI-assisted functionality.

### Conda (Core Toolkit)

Create and activate the Conda environment for the core TARgET toolkit:

```bash
conda env create -f environment.yml
conda activate target
```

### Conda (Toolkit + AI Assistant)

Create and activate the Conda environment including the optional AI assistant:

```bash
conda env create -f environment_ai.yml
conda activate target_ai
```

### pip

Install the latest release of the core toolkit from PyPI:

```bash
pip install target
```

To install TARgET together with the optional AI assistant and its required dependencies:

```bash
pip install "target[ai]"
```

> **Note**
>
> The AI assistant is an optional component intended to assist contributors and advanced users in extending TARgET. It provides guidance for developing new modules and operations while adhering to the toolkit's architecture, design principles, and implementation specifications. The core functionality of TARgET is fully available without the AI assistant.


## Quick Start

TARgET is organized into independent packages, each implementing a specific family of formal models, algorithms, or transformations. Every package includes illustrative examples demonstrating its typical usage, allowing users to quickly explore the available functionality and adopt the components most relevant to their applications.

The general workflow when using TARgET consists of:

1. Import the required package(s) and classes.
2. Construct the desired formal objects (e.g., tree automata, regular tree expressions, terms, or rewrite rules).
3. Apply the desired operations or analysis algorithms.
4. Inspect, export, or visualize the resulting structures.

The following template illustrates this workflow:

```python
from TARgET.<package> import ...

# Construct the required formal objects

# Apply one or more TARgET operations

# Process or visualize the results
```

Detailed, executable examples are provided within each package of the toolkit and serve as practical references for their respective APIs and functionalities. Users are encouraged to consult the documentation of the relevant package for complete usage examples and implementation details.



The following examples illustrate some of the core capabilities of TARgET. Additional examples are provided within each package of the toolkit.

### Example 1: Constructing and Visualizing a bottom up Finite Ranked Tree Automaton

We can create a bottom up finite ranked tree automaton mannually using

```
from TARgET.fta.state import State
from TARgET.core.symbol import Ranked_Symbol
from TARgET.fta.rankedRule import ranked_Rule
from TARgET.fta.rankedfta import ranked_Fta

from typing import List

s= State(name="q1", is_Final=False, is_Initial=False)
t=State(name="q2", is_Final=False, is_Initial=False)
u=State(name="q3", is_Final=False, is_Initial=False)
st = []
st.append(s)
st.append(t)
symb = Ranked_Symbol(name="f", rank=2)
rule = ranked_Rule(func = symb)
rule.input_states = st
rule.output_state = u
rules = []
rules.append(rule)
rules.append(rule)
alpha = []
alpha.append(symb)
automaton = ranked_Fta(fta_name="fta1", alphabet=alpha, fta_states=st, transitions=rules)
automaton.print_Fta()
```

or by using random generator:

```

from TARgET.fta.rankedfta import ranked_Fta
from TARgET.engine.random.ranked_fta_generator import RandomRankedFtaGenerator

generator = RandomRankedFtaGenerator(
n_states=6,
n_symbols=4,
max_rank=2,
n_rules=15,
seed=42
)
random_fta = generator.generate()
random_fta.print_Fta()
```


## DEVELOPING NEW FUNCTIONALITIES

TO DO

## API REFERENCE

TO DO

## TROUBLESHOOTING AND FAQs

TO DO

## CONTRIBUTION

TO DO

## ADITIONAL RESOURCES

TO DO