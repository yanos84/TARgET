import re
import ijson


class HedgeRejected(Exception):
    pass


class StreamingHedgeAcceptor:
    """
    Runs the hedge automaton directly against ijson's event stream instead
    of building a JSON object graph + UnrankedTree first. Memory is
    O(depth x branching factor), not O(file size).
    """

    def __init__(self, hedge_automaton):
        self.automaton = hedge_automaton
        self._final_state_names = hedge_automaton.get_final_states()
        self._rules = {}
        for t in hedge_automaton.transitions:
            self._rules.setdefault(t.symbol.name, []).append(
                (re.compile(t.horizontal_language), t.target_state.name)
            )

    def _resolve(self, symbol_name, word):
        for regex, target_name in self._rules.get(symbol_name, []):
            if regex.fullmatch(word):
                return target_name
        raise HedgeRejected(f"no rule matches {symbol_name}({word!r})")

    def accepts_file(self, filename):
        stack = []
        final_state_name = None

        try:
            with open(filename, "rb") as f:
                for prefix, event, value in ijson.parse(f):

                    if event in ("start_map", "start_array"):
                        if event == "start_map" and not stack:
                            kind = "document"
                        else:
                            kind = "object" if event == "start_map" else "array"
                        stack.append([kind, []])

                    elif event in ("end_map", "end_array"):
                        kind, children = stack.pop()
                        state_name = self._resolve(kind, "".join(children))
                        if stack:
                            stack[-1][1].append(state_name)
                        else:
                            final_state_name = state_name

                    elif event in ("string", "number", "boolean", "null"):
                        stack[-1][1].append(self._resolve("value", ""))

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
    acceptor = StreamingHedgeAcceptor(ha)  # StreamingHedgeAcceptor or StreamingHedgeDfaAcceptorV2
    #process = psutil.Process(os.getpid())

    dataset_path = Path("/home/yanos/Desktop/JSON_For_Hedge_automata/JSON_by_arrays")

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

    df.to_csv("regex_by_array.csv", index=False)

    print(df)