import sys
import os

from LAB2 import LRDefinition
from LAB2 import EquivalentStates
from LAB2 import Tables

# What separates classes of input.
CLASS_SEPARATOR = "\n"

# The prefix of the line which holds non-ending signs.
NON_ENDING_SIGN_PREFIX = "%V"

# The delimiter for every non-ending sign.
NON_ENDING_SIGN_DELIMITER = " "

# The prefix of the line which holds ending signs.
ENDING_SIGN_PREFIX = "%T"

# The delimiter for every ending sign.
ENDING_SIGN_DELIMITER = " "

# The prefix of the line which holds synchronization sings.
SYNCHRONIZING_SIGN_PREFIX = "%Syn"

# The delimiter for every synchronization sign.
SYNCHRONIZING_SIGN_DELIMITER = " "

# The delimiter for every specific production set.
GRAMMAR_DELIMITER = "\n<"

# The sign we unintentionally remove from each production set.
GRAMMAR_REMOVED_SIGN = "<"

# The delimiter for every production.
PRODUCTION_DELIMITER = "\n"

# The delimiter for the right side of each production.
RIGHT_SIDE_DELIMITER = " "

# The starting state of every LR grammar.
LR_STARTING_STATE = "<%>"

DOT = '*'
ITEM_RIGHT_SIDE_DELIMITER = ' '
ITEM_DELIMITER = '->'
STARTING_STATE = '<%>'
EPSILON = '$'
INIT_FILE_NAME = 'generator.ini'
ANALYZER_FILE_NAME = 'SA.py'
ANALYZER_FOLDER = 'analizator'
GENERATOR_FILE_NAME = 'Generator.py'

MOVE_ACTION = 'MOVE'
REDUCE_ACTION = 'REDUCE'
ACCEPT_ACTION = 'ACCEPT'
REJECT_ACTION = 'REJECT'

TEST_STRING = """%V <A> <B> <C> <D> <E>
%T a b c d e f
%Syn a
<A>
 <B> <C> c
<B>
 $
 b <C> <D> <E>
<A>
 e <D> <B>
<C>
 <D> a <B>
 c a
<D>
 $
 d <D>
<E>
 e <A> f
 c"""


# Returns all lines as a string.
def get_all_lines():
    to_ret = ''

    for line in sys.stdin:
        # debug
        if line == 'END\n':
            break

        to_ret += line

    return to_ret


# The syntax analyzer generator class.
class GSA:
    def __init__(self, non_ending_signs, ending_signs, sync_signs, productions):
        self.non_ending_signs = non_ending_signs
        self.first_non_ending = self.non_ending_signs[0]
        self.ending_signs = ending_signs
        self.sync_signs = sync_signs
        self.productions = productions

    # Class for productions.
    class Production:

        def __init__(self, non_ending_sign, righ_side):

            self.non_ending_sign = non_ending_sign
            self.right_side = righ_side

        def __str__(self):
            return self.non_ending_sign + ' -> ' + self.right_side.__str__()

        def __eq__(self, other):
            if type(other) == GSA.Production:
                return self.non_ending_sign == other.non_ending_sign and \
                       self.right_side == other.right_side
            else:
                return False

    # Parses the specifically formatted input into a GSA class object.
    @staticmethod
    def parse(source):
        lines = list(filter(None, source.split(CLASS_SEPARATOR, 3)))

        non_ending_signs = lines[0]\
            .replace(NON_ENDING_SIGN_PREFIX, "")\
            .strip()\
            .split(NON_ENDING_SIGN_DELIMITER)

        non_ending_signs.append(LR_STARTING_STATE)

        ending_signs = lines[1]\
            .replace(ENDING_SIGN_PREFIX, "")\
            .strip()\
            .split(ENDING_SIGN_DELIMITER)

        sync_signs = lines[2]\
            .replace(SYNCHRONIZING_SIGN_PREFIX, "")\
            .strip()\
            .split(SYNCHRONIZING_SIGN_DELIMITER)

        entries = lines[3]\
            .strip()\
            .split(GRAMMAR_DELIMITER)

        productions = list()

        for entry in entries:
            production_lines = entry.split(PRODUCTION_DELIMITER)

            if not production_lines[0].startswith(GRAMMAR_REMOVED_SIGN):
                current_non_ending_sign = GRAMMAR_REMOVED_SIGN + production_lines[0]
            else:
                current_non_ending_sign = production_lines[0]

            for right_side in production_lines[1:]:
                productions.append(GSA.Production(
                    current_non_ending_sign, right_side[1:].split(RIGHT_SIDE_DELIMITER)))

        return GSA(non_ending_signs, ending_signs, sync_signs, productions)

    # To-strings everything, no need to look.
    def __str__(self):
        to_ret = "Non-ending signs:\n"

        for non_ending_sign in self.non_ending_signs:
            to_ret += non_ending_sign + NON_ENDING_SIGN_DELIMITER

        to_ret = to_ret[0:-len(NON_ENDING_SIGN_DELIMITER)] + "\nEnding signs:\n"

        for ending_sign in self.ending_signs:
            to_ret += ending_sign + ENDING_SIGN_DELIMITER

        to_ret = to_ret[0:-len(ENDING_SIGN_DELIMITER)] + "\nSynchronizing signs:\n"

        for sync_sign in self.sync_signs:
            to_ret += sync_sign + SYNCHRONIZING_SIGN_DELIMITER

        to_ret = to_ret[0:-len(SYNCHRONIZING_SIGN_DELIMITER)] + "\nProductions:\n"

        for production in self.productions:
            to_ret += production.__str__() + PRODUCTION_DELIMITER

        to_ret = to_ret[:-1]

        return to_ret


class Item:
    def __init__(self, non_ending_sign, right_side, ending_signs, state):
        self.non_ending_sign = non_ending_sign
        self.right_side = right_side
        self.ending_signs = ending_signs
        self.state = state

    def __str__(self):
        return self.non_ending_sign + ' -> ' + \
               self.right_side.__str__() + ' ' + \
               self.ending_signs.__str__() + ' ' + \
               self.state


def get_item_production(item_str):
    tmp_item = (item_str[:item_str.index(DOT)] + item_str[item_str.index(DOT) + 1:]).split(ITEM_DELIMITER)

    non_ending_sign = tmp_item[0].strip()
    right_side = tmp_item[1].strip().split(ITEM_RIGHT_SIDE_DELIMITER)

    if len(right_side) == 1:
        if right_side[0] == '':
            right_side = [EPSILON]

    if right_side.__contains__(''):
        right_side.remove('')

    return GSA.Production(non_ending_sign, right_side)


def get_ordered_items(productions, states):
    ordered_items = list()

    for production in productions:
        items = set()

        for state in states.keys():
            for item in states[state]:
                if get_item_production(item[0]) == production:
                    items.add(Item(item[0].split(ITEM_DELIMITER)[0].strip(),
                                   item[0].split(ITEM_DELIMITER)[1].strip().split(ITEM_RIGHT_SIDE_DELIMITER),
                                   item[1],
                                   state))
                # debug
                else:
                    pass

        ordered_items.extend(sorted(items, key=lambda item: (item.right_side.index(DOT), item.state)))

    starting_items = set()

    for state in states:
        for item in states[state]:
            if item[0].split(ITEM_DELIMITER)[0].strip() == STARTING_STATE:
                starting_items.add(Item(item[0].split(ITEM_DELIMITER)[0].strip(),
                                        item[0].split(ITEM_DELIMITER)[1].strip().split(ITEM_RIGHT_SIDE_DELIMITER),
                                        item[1],
                                        state))

    ordered_items.extend(sorted(starting_items, key=lambda item: (item.right_side.index(DOT), item.state)))

    return ordered_items


def get_dfa_states(items):
    states = set()

    for item in items:
        states.add(item.state)

    return states


def print_init_file(action_list, new_state_list, sync_signs):
    init_file_path = os.path.join(ANALYZER_FOLDER, INIT_FILE_NAME)
    if os.path.exists(init_file_path):
        os.remove(init_file_path)

    if not os.path.exists(ANALYZER_FOLDER):
        os.mkdir(ANALYZER_FOLDER)

    init_file = open(init_file_path, 'a')

    for action in action_list:
        if action[1][0] == MOVE_ACTION:
            init_file.write(action[0][0] + ' ' + action[0][1] + ':' +
                            action[1][0] + ' ' + action[1][1] + ' ' + action[1][2])

        elif action[1][0] == REDUCE_ACTION:
            to_write = action[0][0] + ' ' + action[0][1] + ':' + \
                       action[1][0] + ' ' + action[1][1]

            for reduction_sign in action[1][2]:
                to_write += ' ' + reduction_sign

            init_file.write(to_write)

        else:
            init_file.write(action[0][0] + ' ' + action[0][1] + ':' + action[1][0])

        init_file.write('\n')

    init_file.write('\n')

    for new_state in new_state_list:
        if new_state[1] is not None:
            init_file.write(new_state[0][0] + ' ' + new_state[0][1] + ':' + new_state[1])
            init_file.write('\n')

    init_file.write('\n')

    to_write = ''
    for sign in sync_signs:
        to_write += sign + ' '
    init_file.write(to_write + '\n')


def print_analyzer():
    generator_file = open(GENERATOR_FILE_NAME, 'r')

    analyzer_file_path = os.path.join(ANALYZER_FOLDER, ANALYZER_FILE_NAME)
    if os.path.exists(analyzer_file_path):
        os.remove(analyzer_file_path)
    analyzer_file = open(analyzer_file_path, 'w')

    analyzer_file.writelines(generator_file.readlines())


gsa = GSA.parse(TEST_STRING)

dfa, states = EquivalentStates.EquivalentStates.build_dfa_with_dict(LRDefinition.LRDefinition(gsa))

ordered_items = get_ordered_items(gsa.productions, states)

dfa_states = get_dfa_states(ordered_items)

action_table = Tables.get_action_table(ordered_items, gsa.ending_signs, dfa, dfa_states)
action_list = list()
for key in action_table.keys():
    action_list.append([key, action_table[key]])
action_list = sorted(action_list, key=lambda action: (int(action[0][0]), action[0][1]))

new_state_table = Tables.get_new_state_table(gsa.non_ending_signs, dfa, dfa_states)
new_state_list = list()
for key in new_state_table.keys():
    new_state_list.append([key, new_state_table[key]])
new_state_list = sorted(new_state_list, key=lambda new_state: (int(new_state[0][0]), new_state[0][1]))

print_init_file(action_list, new_state_list, gsa.sync_signs)
print_analyzer()

# todo remove print

print(gsa.__str__() + '\n')

for state in states.keys():
    for item in states[state]:
        print(item[0], item[1].__str__(), state)

print()

for state in dfa.transitions.keys():
    for transitional_sign in dfa.transitions[state]:
        for new_state in dfa.transitions[state][transitional_sign]:
            if new_state.isnumeric():
                print(state, transitional_sign, new_state)

print()

for item in ordered_items:
    print(item.__str__())

print()

for state in dfa_states:
    print(state)

print()

for action in action_list:
    print(action[0], action[1])

print()

for new_state in new_state_list:
    if new_state[1] is not None:
        print(new_state[0], new_state[1])
