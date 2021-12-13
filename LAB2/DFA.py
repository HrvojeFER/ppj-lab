ERROR_STATE_STRING = "<err>"


class DFA:
    def __init__(self, dfa=None):
        if dfa is None:
            self.starting_state = ""
            self.transitions = dict()
            self.acceptables = set()
        else:
            self.starting_state = dfa.starting_state
            self.transitions = dfa.transitions
            self.acceptables = dfa.acceptables

    @staticmethod
    def from_transitions(transition_set, starting_state=None, acceptables_set=None):
        dfa = DFA()

        if starting_state is None:
            dfa.starting_state = "0"

        for transition in transition_set:
            if not transition[0] in dfa.transitions:
                dfa.transitions[transition[0]] = dict()

            dfa.transitions[transition[0]][transition[1]] = transition[2]

        all_states = set(dfa.transitions)
        all_signs = set()

        for starting_state in dfa.transitions:
            for sign in dfa.transitions[starting_state]:
                all_signs.add(sign)
                all_states.add(dfa.transitions[starting_state][sign])

        if acceptables_set is None or len(acceptables_set) == 0:
            dfa.acceptables = set(all_states)

        for state in dfa.transitions:
            for sign in all_signs:
                if sign not in dfa.transitions[state]:
                    dfa.transitions[state][sign] = ERROR_STATE_STRING

        return dfa

    def add_transition(self, transition_tuple):
        if transition_tuple[0] not in self.transitions:
            self.transitions[transition_tuple[0]] = dict()

        self.transitions[transition_tuple[0]][transition_tuple[1]] = transition_tuple[2]

    def extract_into_groups(self):
        state_set = self.reachable_states()

    def reachable_states(self):
        return DFA.reachable_states_s(self.starting_state, self.transitions)

    # For a given state and input as sign, returns the next state.
    def transition(self, state, sign):
        if state in self.transitions:
            if sign in self.transitions[state]:
                new_state = self.transitions[state][sign]
                if new_state != ERROR_STATE_STRING:
                    return new_state

        return None

    # Simulates the DFA for a given input, returning the last state the DFA finds itself in.
    def simulate(self, source):
        current_state = self.starting_state

        for x in source:
            current_state = self.transition(current_state, x)

        return current_state

    # Returns true if for input source the DFA ends in an acceptable state, false otherwise.
    def calculate(self, source):
        return self.simulate(source) in self.acceptables

    @staticmethod
    def reachable_states_s(starting_state, transition_classes):
        # to_ret contains the list of reachable states.
        to_ret = [starting_state]

        # add contains the set of states that were added to to_ret. This exists only because search is easier on a set.
        added = set(to_ret)

        # checked contains the set of states already checked for transitions.
        checked = set()

        # Using i as an iterator
        i = 0
        while i < len(transition_classes):
            checking_next = to_ret[i]
            i += 1

            # If we checked the state we're currently checking, we don't need to check it again.
            if checked.__contains__(checking_next):
                continue

            # To check will give us a list of transitions for the checking_next state.
            to_check = list(filter(lambda x: x.state == checking_next, transition_classes))[0].transition_dict

            # We check every transition for new possible states.
            for c in to_check:
                # If the state we're currently looking at is not added yet, we'll add it.
                if not added.__contains__(to_check[c]):
                    to_ret.append(to_check[c])
                    added.add(to_check[c])

            # Finally, mark checking_next as checked.
            checked.add(checking_next)

            # If the length of the states we're returning is equal to the length of checked states, that means that we're done checking.
            if len(to_ret) == len(checked):
                break

        # We return the states as a set.
        return set(to_ret)

"""
DFA.from_transitions([("A", "c", "F"),
                      ("A", "d", "C"),
                      ("B", "c", "G"),
                      ("B", "d", "C"),
                      ("C", "c", "A"),
                      ("C", "d", "E"),
                      ("D", "c", "D"),
                      ("D", "d", "F"),
                      ("E", "c", "G"),
                      ("E", "d", "C"),
                      ("F", "c", "D"),
                      ("F", "d", "A"),
                      ("G", "c", "D"),
                      ("G", "d", "B")])
"""
