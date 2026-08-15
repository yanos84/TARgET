import ijson
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA


class HedgeRejected(Exception):
    """Raised internally to abort parsing as soon as the file is known
    to be rejected — no point reading the rest of a 4GB file."""
    pass


class StreamingHedgeDfaAcceptorV2:
    """
    Same idea as StreamingHedgeDfaAcceptor, but memory is O(depth) instead
    of O(max width of any single container).

    The earlier version accumulated a Python list of child state names for
    the currently-open container and only ran the DFA once, over the whole
    word, when the container closed. That's fine for deep-and-narrow trees,
    but for a container with millions of DIRECT children (wide/shallow
    JSON), that list grows for as long as the container stays open --
    memory scales with file size again, just with a smaller constant than
    building a full tree.

    This version instead steps the DFA one symbol at a time as each child
    completes, and keeps only the DFA's *current state* per open frame
    (a small int/object, not a growing list). A frame closes successfully
    iff its current DFA state is one of the DFA's final states.

    Assumes the automaton is unambiguous: at most one transition per
    symbol. (Same assumption as the earlier streaming versions.)
    """

    def __init__(self, hedge_automaton):
        self.automaton = hedge_automaton
        self._final_state_names = hedge_automaton.get_final_states()

        # symbol name -> (dfa, target_hedge_state_name)
        self._symbol_dfa = {}
        dfa_cache = {}
        for t in hedge_automaton.transitions:
            regex = t.horizontal_language
            if regex not in dfa_cache:
                dfa_cache[regex] = DFA.from_nfa(NFA.from_regex(regex))
            self._symbol_dfa[t.symbol.name] = (dfa_cache[regex], t.target_state.name)

        # precompute: does the "value" leaf's DFA accept immediately (empty word)?
        # value() has no children, so this is checked once, not per-leaf.
        value_dfa, value_target = self._symbol_dfa["value"]
        if value_dfa.initial_state not in value_dfa.final_states:
            raise HedgeRejected("value() itself is not accepted by its own rule")
        self._value_target = value_target

    def _step(self, dfa, state, symbol_char):
        table = dfa.transitions.get(state)
        if table is None or symbol_char not in table:
            raise HedgeRejected(f"no DFA transition for {symbol_char!r} from state {state}")
        return table[symbol_char]

    def _feed_child(self, frame, child_state_name):
        # frame = [kind, dfa, current_dfa_state]
        dfa = frame[1]
        state = frame[2]
        for ch in child_state_name:
            state = self._step(dfa, state, ch)
        frame[2] = state

    def _close_frame(self, kind, dfa, state):
        if state not in dfa.final_states:
            raise HedgeRejected(f"{kind} closed in non-accepting DFA state {state}")
        return self._symbol_dfa[kind][1]

    def accepts_file(self, filename):
        stack = []               # list of [kind, dfa, current_dfa_state]
        final_state_name = None

        try:
            with open(filename, "rb") as f:
                for event, value in ijson.basic_parse(f):

                    if event in ("start_map", "start_array"):
                        kind = "document" if (event == "start_map" and not stack) \
                               else ("object" if event == "start_map" else "array")
                        dfa, _ = self._symbol_dfa[kind]
                        stack.append([kind, dfa, dfa.initial_state])

                    elif event in ("end_map", "end_array"):
                        kind, dfa, state = stack.pop()
                        state_name = self._close_frame(kind, dfa, state)
                        if stack:
                            self._feed_child(stack[-1], state_name)
                        else:
                            final_state_name = state_name

                    elif event in ("string", "number", "boolean", "null"):
                        if stack:
                            self._feed_child(stack[-1], self._value_target)
                        else:
                            final_state_name = self._value_target

        except HedgeRejected:
            return False

        return final_state_name in self._final_state_names


#Example of use

if __name__ == "__main__":
    import time
    import pandas as pd
    from pathlib import Path
    import os
    from TARgET.core.base.symbol import Symbol
    from TARgET.core.fta.state import State
    from TARgET.core.fta.hedge.hedge import HedgeAutomaton

    # Build automaton once (not part of the benchmark)
    qV = State("qV", is_Final=False)
    qO = State("qO", is_Final=False)
    qA = State("qA", is_Final=False)
    qDoc = State("qDoc", is_Final=True)

    ha = HedgeAutomaton(
        "json_hedge_automaton",
        [qV, qO, qA, qDoc],
        [Symbol("value"), Symbol("object"), Symbol("array"), Symbol("document")],
    )

    ha.add_transition(Symbol("value"),    r"", qV)
    ha.add_transition(Symbol("object"),   r"(qV|qO|qA)*", qO)
    ha.add_transition(Symbol("array"),    r"(qO|qV)*", qA)
    ha.add_transition(Symbol("document"), r"qO", qDoc)
    acceptor = StreamingHedgeDfaAcceptorV2(ha)  # StreamingHedgeAcceptor or StreamingHedgeDfaAcceptorV2
    #process = psutil.Process(os.getpid())

    dataset_path = Path("/home/yanos/Desktop/JSON_For_Hedge_automata/JSON_general")

    results = []

    for json_file in sorted(dataset_path.glob("*.json")):

        print(f"Processing {json_file.name}")

        # Load input (not measured)
        #tree = load_json_as_tree(json_file)

        # Memory measurement starts here
        #tracemalloc.start()

        # CPU time measurement
        #mem_before = process.memory_info().rss
        #before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        start = time.thread_time()

        accepted = acceptor.accepts_file(json_file)

        end = time.thread_time()
        #after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        #memory_mb = after / 1024
        # Memory after
        # mem_after = process.memory_info().rss

        # Get peak memory
        #current, peak = tracemalloc.get_traced_memory()
        #tracemalloc.stop()

        results.append({
            "file": json_file.name,
            "size_bytes": json_file.stat().st_size,
            "accepted": accepted,
            "time_ms": (end - start) * 1000,
            #"memory_usage" : memory_mb+"KB",
            #"memory_kb": f"Peak: {peak/1024:.1f} KB"
        })


    df = pd.DataFrame(results)

    df.to_csv("hedge_dfa_acceptor_benchmark.csv", index=False)

    print(df)