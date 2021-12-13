import LAB2.DFA as DFA

# The sign that depicts an epsilon state with.
EPSILON_SIGN = "$"

# The starting state of every LR grammar.
LR_STARTING_STATE = "<%>"


class EquivalentStates:
    def __init__(self, lr_item=None, lr_productions=None):

        if lr_item is not None and lr_productions is not None:
            self.equivalent_lr_items = EquivalentStates.get_epsilon_lr_items(lr_item, lr_productions)
            self.equivalent_lr_transitions = EquivalentStates.get_epsilon_lr_transitions(lr_item, lr_productions)
            self.signs = EquivalentStates.get_possible_signs(self.equivalent_lr_transitions)
        else:
            self.equivalent_lr_items = set()
            self.equivalent_lr_transitions = list()
            self.signs = set()

    # Returns true if the starting LR state is contained in this instance of EquivalentStates
    def has_starting_state(self):
        return EquivalentStates.contains_starting_state(self.equivalent_lr_items)

    # By definition, equivalent states contain an item if it is in self.equivalent_lr_items.
    def __contains__(self, item):
        return item in self.equivalent_lr_items

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return len(set(self.equivalent_lr_items).difference(set(other.equivalent_lr_items))) == 0

    def __hash__(self):
        to_ret = 0

        for lr_item in self.equivalent_lr_items:
            to_ret ^= hash(lr_item)

        return to_ret

    def __str__(self):
        to_ret = ""

        for lr_item in sorted(self.equivalent_lr_items):
            to_ret += str(lr_item) + "\n"

        return to_ret[:-1]

    # Pseudo-constructor that uses a list of LR items and LR productions to create an equivalent state which it returns.
    @staticmethod
    def from_items(lr_items, lr_productions):
        equivalent_states = EquivalentStates()

        equivalent_states.equivalent_lr_items = EquivalentStates.\
            get_epsilon_lr_items_multiple(lr_items, lr_productions)

        equivalent_states.equivalent_lr_transitions = EquivalentStates.\
            get_epsilon_lr_transitions_mul(equivalent_states.equivalent_lr_items, lr_productions)

        equivalent_states.signs = EquivalentStates.\
            get_possible_signs(equivalent_states.equivalent_lr_transitions)

        return equivalent_states

    @staticmethod
    def contains_starting_state(lr_items):
        # First, reduce the number of possibilities to only those which start with the starting state.
        possibilities = set(filter(lambda x: x[0].startswith(LR_STARTING_STATE), lr_items))

        # We expect that the starting state is in the form below
        expected_form = LR_STARTING_STATE + " -> *"

        # Finally, we check if any of the possibilities starts with the expected form.
        for possibility in possibilities:
            if possibility[0].startswith(expected_form):
                return True

    # Return a set of LR items in the epsilon surrounding of lr_item
    @staticmethod
    def get_epsilon_lr_items(lr_item, lr_productions):
        # Initialize a list of epsilon items with the starting LR item, and a set named checked which is empty at the start.
        epsilon_items = {lr_item}
        checked = set()

        # When the length of epsilon_items is not equal to the length of checked, that means we have unchecked LR items.
        while len(epsilon_items) != len(checked):

            # So we define that the LR items we need to check are those in epsilon_items which are not found in checked.
            items_to_check = epsilon_items.difference(checked)
            epsilon_produced_items = set()

            # We check every item to check, and we add the result of every epsilon transition to the epsilon_produced_items.
            for item_to_check in items_to_check:
                if item_to_check in lr_productions and lr_productions[item_to_check] is not None and \
                        EPSILON_SIGN in lr_productions[item_to_check]:
                    for result in lr_productions[item_to_check][EPSILON_SIGN]:
                            epsilon_produced_items.add(result)

                # When we're done checking a specific LR item, we add it to the set of checked LR items.
                checked.add(item_to_check)

            # Finally, we add all the LR items we found which were not already in epsilon_produced_items.
            epsilon_items.update(epsilon_produced_items)

        return epsilon_items

    # Returns a set of LR items in the epsilon surrounding of all of the LR items in lr_item_list
    @staticmethod
    def get_epsilon_lr_items_multiple(lr_item_list, lr_productions):
        lr_items = set()

        for lr_item in lr_item_list:
            lr_items.update(EquivalentStates.get_epsilon_lr_items(lr_item, lr_productions))

        return lr_items

    # Returns a list of LR transitions equivalent to lr_item's transitions.
    @staticmethod
    def get_epsilon_lr_transitions(lr_item, lr_productions):
        return EquivalentStates.\
            get_epsilon_lr_transitions_mul(EquivalentStates.
                                           get_epsilon_lr_items(lr_item, lr_productions), lr_productions)

    @staticmethod
    def get_epsilon_lr_transitions_mul(lr_items, lr_productions):
        # Just making the search O(1)
        lr_items = set(lr_items)
        epsilon_transitions = list()

        # We check every production in lr_productions and if we find a production in our items, we append a dictionary
        # dictionary entry to our epsilon_transitions
        for production in lr_productions:
            if production in lr_items:
                epsilon_transitions.append({production: lr_productions[production]})

        return epsilon_transitions

    # Returns a set of possible signs for equivalent LR productions, except epsilon.
    @staticmethod
    def get_possible_signs(epsilon_lr_productions):
        to_ret = set()

        # We just iterate through the epsilon_lr_productions and add every sign we find.
        for lr_production in epsilon_lr_productions:
            for production in lr_production:
                if lr_production[production] is not None:
                    for sign in lr_production[production]:
                        to_ret.add(sign)

        # Returning every sign besides epsilon, because our DKA won't have any states we're reaching with epsilon, they're equivalent.
        return to_ret.difference(EPSILON_SIGN)

    # Builds a DFA for a specific LRDefinition instance, returns a tuple of (dfa, dfa_state_to_lr_items dictionary)
    @staticmethod
    def build_dfa_with_dict(lr_definition):
        # First we'll get all the LR items contained in the LR definition. We'll also initialize and empty list of
        # equivalent states, and we don't need to make it a set because we'll make sure they aren't duplicates anyways.
        lr_item_list = lr_definition.get_lr_items()
        equivalent_state_list = list()

        # We need to first create equivalent states for every LR item.
        for lr_item in lr_item_list:
            item_already_checked = False

            # We need to check if there are already equivalent states in which the current LR item is. If they are, then
            # the current LR_item already has its equivalent states calculated.
            for es in equivalent_state_list:
                if lr_item in es:
                    item_already_checked = True
                    break

            # If the current item is not in any equivalent state, then it is a new state which we need to add to equivalent_state_list
            if not item_already_checked:
                equivalent_state_list.append(EquivalentStates(lr_item, lr_definition.lr_productions))

        # state_dict will hold equivalent states as keys which create a dictionary of signs which have LR items as their values.
        # Put simply, it is state_dict[equivalent_state][sign] = lr_items
        state_dict = dict()

        for equivalent_state in equivalent_state_list:
            state_dict[equivalent_state] = dict()

            for sign in equivalent_state.signs:
                possible_lr_items = set()

                for production in lr_definition.lr_productions:
                    if lr_definition.lr_productions[production] is not None and \
                            production in equivalent_state.equivalent_lr_items and \
                            sign in lr_definition.lr_productions[production]:
                        possible_lr_items.add(production)

                if len(possible_lr_items) != 0:
                    state_dict[equivalent_state][sign] = possible_lr_items

        # transition dict is similar to state_dict, except it's transition_dict[equivalent_states][sign] = resulting_equivalent_states
        transition_dict = dict()

        for equivalent_state in state_dict:
            transition_dict[equivalent_state] = dict()

            for sign in state_dict[equivalent_state]:
                new_equivalent_lr_items = set()

                for lr_item in state_dict[equivalent_state][sign]:
                    new_lr_items = lr_definition.lr_productions[lr_item][sign]

                    new_equivalent_lr_items = EquivalentStates.\
                        from_items(new_lr_items, lr_definition.lr_productions).equivalent_lr_items

                if len(new_equivalent_lr_items) != 0:
                    transition_dict[equivalent_state][sign] = EquivalentStates.\
                        from_items(new_equivalent_lr_items, lr_definition.lr_productions)

        # equivalent_state_to_state maps equivalent states to DFA states.
        equivalent_state_to_state = dict()

        possible_starting_equivalent_states = list(filter(lambda x: x.has_starting_state(), transition_dict))

        if len(possible_starting_equivalent_states) == 0:
            return "No starting state!!!"

        i = 0
        equivalent_state_to_state[possible_starting_equivalent_states[0]] = str(i)

        for equivalent_state in transition_dict:
            if equivalent_state not in equivalent_state_to_state:
                i += 1
                equivalent_state_to_state[equivalent_state] = str(i)

        # state_to_lr_items maps each state to a list of LR items it represents.
        state_to_lr_items = dict()

        for equivalent_state in equivalent_state_to_state:
            state_to_lr_items[equivalent_state_to_state[equivalent_state]] = equivalent_state.equivalent_lr_items

        # transitions holds the set of all transitions based on the equivalent_state_to_state mapping.
        transitions = set()

        for equivalent_state in transition_dict:
            for sign in transition_dict[equivalent_state]:
                transitions.add((equivalent_state_to_state[equivalent_state], sign,
                                 equivalent_state_to_state[transition_dict[equivalent_state][sign]]))

        dfa = DFA.DFA.from_transitions(transitions)

        return dfa, state_to_lr_items
