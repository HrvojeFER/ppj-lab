# Contains all the functions needed to create the action table and the new state table.
# Returns them as dictionaries.
#
# List of requirements:
# dfa               - an object of the DFA class
# items             - List of objects of the Item class
# non_ending_signs  - List of non ending signs
# ending_signs      - List of ending signs
#
#   DFA class:
#       DFA functions:
# transition        - returns the next state of the DFA for the given current state and transitional sign
#                   - returns None if the next state does not exist
#
#       DFA attributes:
# states            - a list of DFA states
#
#   Item class:
#       Item attributes:
# non_ending_sign   - the non ending sign on the right side of the item,
#
# right_side        - a list of all the signs on the right side of the item
#                   - it has to contain the dot
#                   - the length has to be bigger than two
#
# ending_signs      - the ending signs list of the item
#
# state             - the state in which it is located in the dfa

STARTING_SIGN = '<%>'
DOT = '*'
END_OF_PROGRAM = '#'
EPSILON = '$'
MOVE_ACTION = 'MOVE'
REDUCE_ACTION = 'REDUCE'
ACCEPT_ACTION = 'ACCEPT'
REJECT_ACTION = 'REJECT'


# Returns true if actions a1 and a2 are the same.
def same_action(a1, a2):
    if a1[0] != a2[0]:
        return False

    if a1[0] == MOVE_ACTION:
        if a1[1] != a2[1]:
            return False
        if a1[2] != a2[2]:
            return False

    elif a1[0] == REDUCE_ACTION:
        if a1[1] != a2[1]:
            return False
        index = 0
        while len(a1) > index and len(a2) > index:
            if a1[2][index] != a2[2][index]:
                return False

    return True


# Returns the action table as a dictionary for the given items list (items), DFA (dfa) and
# ending signs list (ending_signs).
def get_action_table(items, ending_signs, dfa, dfa_states):
    action_table = dict()

    # Goes through the list of items provided and adds or puts the appropriate actions.
    for item in items:
        dot_index = item.right_side.index(DOT)

        # Checks if there is a sign behind the dot.
        sign_behind_dot = None
        if not dot_index + 1 >= len(item.right_side):
            sign_behind_dot = item.right_side[dot_index + 1]

        # If there is a sign behind the dot and its in the list of ending signs
        # puts or adds the move action to the action table.
        if sign_behind_dot is not None and sign_behind_dot in ending_signs + [END_OF_PROGRAM]:
            # Takes the new state from the dfa and puts or adds the move action.
            new_state = dfa.transition(item.state, sign_behind_dot)

            if new_state is not None:
                if (item.state, sign_behind_dot) not in action_table:
                    action_table[item.state, sign_behind_dot] = \
                        [[MOVE_ACTION, sign_behind_dot, dfa.transition(item.state, sign_behind_dot)]]
                else:
                    action_table[item.state, sign_behind_dot].\
                        append([MOVE_ACTION, sign_behind_dot, dfa.transition(item.state, sign_behind_dot)])

        # If there is no sign behind the dot that must mean that the dot is in the last place.
        elif sign_behind_dot is None:
            # If the sign on the left side of the item is not the starting sign puts or adds the reduce actions.
            if item.non_ending_sign != STARTING_SIGN:
                # Puts or adds the reduce action for every sign in the ending signs of the item.
                for sign in item.ending_signs:
                    right_side = item.right_side[:item.right_side.index(DOT)] + \
                                 item.right_side[item.right_side.index(DOT) + 1:]
                    if not right_side:
                        right_side = EPSILON
                    if (item.state, sign) not in action_table:
                        action_table[item.state, sign] = [[REDUCE_ACTION, item.non_ending_sign, right_side]]
                    else:
                        action_table[item.state, sign].append([REDUCE_ACTION, item.non_ending_sign, right_side])

            # If the sign on the left is the starting sign puts the accept action.
            else:
                action_table[item.state, END_OF_PROGRAM] = [[ACCEPT_ACTION]]

    # Goes through all of the action table entries, fixes contradiction and adds reject actions.
    for state in dfa_states:
        for sign in ending_signs + [END_OF_PROGRAM]:
            # If there is no action table entry puts the reject action in the entry.
            if (state, sign) not in action_table:
                action_table[state, sign] = [REJECT_ACTION]

            else:
                # If there is just one action in the entry, keeps it.
                if len(action_table[state, sign]) == 1:
                    action_table[state, sign] = action_table[state, sign][0]

                else:
                    # If there are multiple actions checks what types of actions are there.
                    has_move_action = False
                    has_reduce_action = False
                    has_other_action = False
                    all_actions_same = True

                    for index, action in enumerate(action_table[state, sign]):
                        action_type = action[0]

                        if action_type == MOVE_ACTION:
                            has_move_action = True
                        elif action_type == REDUCE_ACTION:
                            has_reduce_action = True
                        else:
                            has_other_action = True

                        if not same_action(action_table[state, sign][0], action):
                            all_actions_same = False

                    # If there are only move and reduce actions it means that there is a move/reduce contradiction.
                    if has_move_action and has_reduce_action and not has_other_action:
                        # Takes the first move action.
                        preferred_action = None

                        for action in action_table[state, sign]:
                            action_type = action[0]

                            if action_type == MOVE_ACTION:
                                preferred_action = action
                                break

                        action_table[state, sign] = preferred_action

                    # If there are only reduce actions it means that there is a reduce/reduce contradiction.
                    elif has_reduce_action and not has_move_action and not has_other_action:
                        # Takes the first action.
                        action_table[state, sign] = action_table[state, sign][0]

                    # If all actions are the same take the first one.
                    elif all_actions_same:
                        action_table[state, sign] = action_table[state, sign][0]

                    # If there are more than one actions in the entry and it can't detect a specific contradiction
                    # it means that there is a bug.
                    else:
                        raise ValueError('Action table has some wild actions')

    return action_table


# Returns the new state table as a dictionary for the given
# non ending signs list (non_ending_signs) and DFA (dfa).
def get_new_state_table(non_ending_signs, dfa, dfa_states):
    new_state_table = dict()

    # Goes through all of the dfa states and all of the non ending signs and
    # adds the new states in the new state table
    for state in dfa_states:
        for sign in non_ending_signs:
            new_state_table[state, sign] = dfa.transition(state, sign)

    return new_state_table
