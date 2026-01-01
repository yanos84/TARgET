class Determinism:
    @staticmethod
    def check(rules, semantics) -> bool:
        """
        Generic determinism check.
        `semantics` defines how rules are interpreted.
        """

        transition_map = {}

        for rule in rules:

            key, output = semantics.transition_signature(rule)

            if key in transition_map:
                if transition_map[key] != output:
                    return False
            else:
                transition_map[key] = output

        return True

