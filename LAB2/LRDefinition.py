import copy
import LAB2.HashableSet as HashableSet

# The sign that depicts an epsilon state with.
EPSILON_SIGN = "$"

# The sign that depicts an LR separator.
LR_DOT_SIGN = "*"

# The starting state of every LR grammar.
LR_STARTING_STATE = "<%>"

# The delimiter for each ending or non-ending sign in a production.
GRAMMAR_SIGN_DELIMITER = " "

# The sign representing the end of input (not actually read, simply symbolic).
END_SIGN = '#'


class LRDefinition:

    def __init__(self, gsa):
        # The syntax analyzer generator instance.
        self.gsa = gsa

        # We assume the starting state looks like the one below. It doesn't belong to the original SAG definition.
        self.starting_state = LR_STARTING_STATE + ' -> ' + LR_DOT_SIGN + " " + self.gsa.first_non_ending

        # The set of empty signs.
        self.empty_signs = self.calculate_empty_signs()

        # A dictionary containing signs a certain non-ending sign can start with.
        self.starts_dict = self.starts()

        # A dictionary in the format dict[lr_item_and_starts][sign] = resulting_lr_item_and_starts
        self.lr_productions = self.get_lr_productions()

        # A set of all LR item and starts signs combos.
        self.all_lr_items_with_starts = self.get_all_lr_with_starts()

        # List of all signs present in the LR definition.
        self.all_signs = gsa.non_ending_signs + gsa.ending_signs

        # Minus the starting sign.
        self.all_signs.remove(LR_STARTING_STATE)

    # Calculates empty signs
    def calculate_empty_signs(self):

        empty_signs = list()
        temp_productions = copy.deepcopy(self.gsa.productions)

        # Puts a non-ending sign into list empty_signs if it has an $-production
        for production in self.gsa.productions:
            if production.right_side == [EPSILON_SIGN]:
                empty_signs.append(production.non_ending_sign)

        # Puts a non-ending sign into list empty_signs if it has at least one production with only empty signs
        # on the right side
        for emtpy_sign in empty_signs:
            for production in temp_productions:
                if production.non_ending_sign in empty_signs:
                    continue

                if production.right_side.__contains__(emtpy_sign):
                    production.right_side.remove(emtpy_sign)

                if not production.right_side:
                    empty_signs.append(production.non_ending_sign)
                    continue

        # Returns empty signs in a list
        return set(empty_signs)

    # Returns a dictionary for the given syntax analyzer generator with StartsWith() values.
    def calculate_starts_with_sign(self):

        all_signs = self.gsa.non_ending_signs + self.gsa.ending_signs
        starts_with = dict()

        for sign in all_signs:
            starts_with[sign] = {}

            for value in all_signs:
                if self.check(sign, value):
                    starts_with[sign].update({value: 1})
                else:
                    starts_with[sign].update({value: 0})

        for key in starts_with.keys():
            LRDefinition.check_again(starts_with, key)

        return starts_with

    def get_all_states(self):
        to_ret = list()

        for production in self.gsa.productions:
            if production.right_side == [EPSILON_SIGN]:
                to_ret.append(production.non_ending_sign + ' -> ' + LR_DOT_SIGN)
            else:
                for i in range(len(production.right_side) + 1):
                    state = copy.deepcopy(production.right_side)
                    state.insert(i, LR_DOT_SIGN)
                    to_ret.append(production.non_ending_sign + ' -> ' + " ".join(state))

        return to_ret

        # Prints a dictionary that represents the functions Starts()
        # TODO starts_with is a dictonary, for a given key(sign) gives a value(all ending signs a given sign starts)

    def starts(self):

        starts_with = self.calculate_starts_with_sign()
        starts_dict = dict()
        ending_signs = self.gsa.ending_signs

        for key in starts_with:
            starts_dict[key] = set()
            for _key in starts_with[key]:
                if starts_with[key][_key] == 1 and _key in ending_signs:
                    starts_dict[key].add(_key)

        return starts_dict

        # TODO added new function which calculates starts for a given string, returns start signs as a list

    def starts_for_string(self, list_of_strings_after_dot):
        starts_signs = []

        if len(list_of_strings_after_dot) != 0:
            for s in list_of_strings_after_dot:
                starts_signs.extend(self.starts_dict[s])

                if s not in self.empty_signs:
                    break
        return starts_signs

        # TODO Checks if a string can become epsilon(empty string) ,returns True if possible, otherwise False

    def epsilon_string(self, string):

        if len(string) == 0:
            return True
        else:
            for s in string:
                if s not in self.empty_signs:
                    return False
            return True

    # Finds all epsilon productions for a given state
    def epsilon_productions(self, tuple):
        # TODO
        # Removed left_side, returns list of new LR items (new_state)
        # for a given tuple which consists of (state, starts_signs),
        # state represents current LR item

        all_states = self.get_all_states()
        non_ending = copy.deepcopy(self.gsa.non_ending_signs)
        if non_ending.__contains__(LR_STARTING_STATE):
            non_ending.remove(LR_STARTING_STATE)

        state = tuple[0]
        state = state.split(" ")

        if state[-1] is not LR_DOT_SIGN:
            i = state.index(LR_DOT_SIGN)

            if state[i + 1] in non_ending:
                sign = state[i + 1]
                new_state = []

                for s in all_states:
                    if s.startswith(sign) and s.split("-> ")[1].startswith(LR_DOT_SIGN):
                        new_state.append(s)

                return new_state
            else:
                return False

        return False

    # Finds all states that a given state can go with transition sign (which is after '*' in the current state's name)
    @staticmethod
    def productions(item_starts_pair):

        lr_item = item_starts_pair[0]
        lr_item = lr_item.split(GRAMMAR_SIGN_DELIMITER)
        i = lr_item.index(LR_DOT_SIGN)

        if lr_item[-1] is not LR_DOT_SIGN:

            sign = lr_item[i + 1]

            temp = lr_item[i]
            lr_item[i] = lr_item[i + 1]
            lr_item[i + 1] = temp

            new_state = [GRAMMAR_SIGN_DELIMITER.join(lr_item)]

            return sign, new_state

        return False

    # Returns LR productions based on the syntax analyzer generator and the starting state
    def get_lr_productions(self):
        # starting_tuple represents the combination of the starting state and it's Starts() result; the end sign.
        starting_tuple = (self.starting_state, HashableSet.HashableSet(END_SIGN))

        # nfa_productions is a dictionary that will hold all transitions in the form of lr_productions[lr_item_and_starts][sign] = result
        lr_productions = dict()
        to_do_list = [starting_tuple]

        while True:
            for item in to_do_list:
                result = self.epsilon_productions(item)

                if result is not False:
                    new_state = result

                    if item not in lr_productions:
                        # If the item is not already present in LR productions, we'll create a dictionary for its first key
                        # and an empty set for all the possible (LR item, Starts()) values.
                        lr_productions[item] = dict()
                        lr_productions[item][EPSILON_SIGN] = HashableSet.HashableSet()

                        # We check every epsilon state.
                        for state in new_state:
                            # Since sets are not hashable by default, we have to use a custom collection which enables us to hash sets.
                            starts_signs = HashableSet.HashableSet()

                            # Since we don't have a class for LR items, we have to parse the string. This will separate signs for us.
                            try:
                                string = item[0].split('* ')[1].split(' ')[1:]
                            except IndexError:
                                string = ""

                            # We'll check if we're missing any signs in starts_sign and add them.
                            for sign in self.starts_for_string(string):
                                if sign not in starts_signs:
                                    starts_signs.add(sign)

                            # If a string can become an epsilon string, that means that we need its starts signs as well.
                            if self.epsilon_string(string):
                                for sign in item[1]:
                                    if sign not in starts_signs:
                                        starts_signs.add(sign)

                            # We need to make sure that the new states are checked as well, if they're not already in the productions.
                            temp_tuple = (state, starts_signs)
                            if temp_tuple not in to_do_list and temp_tuple not in lr_productions:
                                to_do_list.append(temp_tuple)

                            lr_productions[item][EPSILON_SIGN].add(temp_tuple)

                s_productions = LRDefinition.productions(item)

                if s_productions is not False:
                    sign, new_state = s_productions

                    if item not in lr_productions:
                        lr_productions[item] = dict()

                    lr_productions[item][sign] = HashableSet.HashableSet()

                    temp_tuple = False

                    for state in new_state:
                        temp_tuple = (state, item[1])

                        if temp_tuple not in to_do_list:
                            to_do_list.append(temp_tuple)

                    if temp_tuple is not False:
                        lr_productions[item][sign].add(temp_tuple)

                if result is False and s_productions is False:
                    lr_productions[item] = None

                to_do_list.remove(item)

            if len(to_do_list) == 0:
                break

        return lr_productions

    # Returns a set of all combinations of (lr_item, starts)
    def get_all_lr_with_starts(self):
        all_lr_with_starts = set()

        for production in self.lr_productions:
            all_lr_with_starts.add(production)

        return all_lr_with_starts

    # Returns a sorted list of all LR items contained in the LR production dictionary of this entity.
    def get_lr_items(self):
        return list(LRDefinition.get_all_lr_items(self.lr_productions))

    @staticmethod
    def get_lr_productions_with(lr_item, lr_productions):
        return lr_productions[lr_item]

    @staticmethod
    def get_lr_production_list(lr_productions):
        to_ret = list()

        for lr_production in lr_productions:
            to_ret.append({lr_production: lr_productions[lr_production]})

        return to_ret

    # Checks if the production for a given key whose right side starts with 'sign' exists
    # (key -> alpha sign beta),     alpha ->* $
    def check(self, key, sign):
        if key == sign:
            return True

        for production in [prd for prd in self.gsa.productions if prd.non_ending_sign == key]:
            for prd_sign in production.right_side:
                if prd_sign == sign:
                    return True
                if prd_sign not in self.empty_signs:
                    break

        return False

    @staticmethod
    def check_again(starts_with, key):
        for _key in starts_with[key]:
            if starts_with[key][_key] == 1:
                for j in starts_with[_key]:
                    if starts_with[_key][j] == 1:
                        if starts_with[key][j] != 1:
                            starts_with[key][j] = 1
                            LRDefinition.check_again(starts_with, key)

    @staticmethod
    def print_lr_production(lr_production):
        for sign in lr_production:
            print("\t" + str(sign) + ":")

            for result in lr_production[sign]:
                print("\t\t" + str(result[0]) + "    " + str(result[1]))

    @staticmethod
    def print_lr_productions(lr_productions):
        for combo in lr_productions:
            print(str(combo[0]) + "    " + str(combo[1]) + ":")

            if lr_productions[combo] is not None:
                for sign in lr_productions[combo]:
                    print("\t" + str(sign) + ":")

                    for result in lr_productions[combo][sign]:
                        print("\t\t" + str(result[0]) + "    " + str(result[1]))
            else:
                print("\t" + str(lr_productions[combo]))

            print("\n")

    @staticmethod
    def get_all_lr_items(lr_productions):
        to_ret = list()

        for production in lr_productions:
            to_ret.append(production)

            if lr_productions[production] is not None:
                for sign in lr_productions[production]:
                    for lr_item in lr_productions[production][sign]:
                        to_ret.append(lr_item)

        return to_ret
