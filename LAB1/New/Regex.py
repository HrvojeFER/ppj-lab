OP_SEPARATE = '|'
OP_KLEEN = '*'
LBRACKET = '('
RBRACKET = ')'
NAME_START = '{'
NAME_END = '}'
ESCAPE_CHAR = '\\'
EPSILON = '$'
STARTING_STATE = [0]


class RegularExpression:
    def __init__(self, expr):
        self.expression = expr
        self.automata = Automata(expr)

    # Returns true if toCheck matches the current instance of the regular expression, false otherwise.
    def match(self, toCheck):
        return self.automata.possible_states(toCheck).__contains__(1)

    # Checks if the toCheck can fulfill the regex in the future
    def possible(self, toCheck):
        return len(self.automata.possible_states(toCheck)) > 0


class Automata:
    def __init__(self):
        self.states = {}
        self.stateAmount = 0

    def __init__(self, expr):
        self.states = {}
        self.stateAmount = 0
        self.__convert(expr)

    # Increments the state count and returns the serial number of the last state available.
    def add_state(self):
        self.stateAmount += 1
        return self.stateAmount - 1

    # Adds a transition d(startingState, transitionalSign) -> endingState
    def add_transition(self, startingState, endingState, transitionalSign):
        if not self.states.__contains__((startingState, transitionalSign)):
            self.states[(startingState, transitionalSign)] = list()

        self.states[(startingState, transitionalSign)].append(endingState)

    # Adds a transition d(startingState, EPSILON) -> endingState
    def add_epsilon_transition(self, startingState, endingState):
        self.add_transition(startingState, endingState, EPSILON)

    # Gets all states in the epsilon environment of state
    def get_all_epsilon(self, state):
        states = {state}

        while True:
            newStates = set(states)

            for s in states:
                newStates.update(self.transition(s, EPSILON))

            if states == newStates:
                break

            states.update(newStates)

        return states

    def transition(self, state, sign):
        if self.states.__contains__((state, sign)):
            return set(self.states[(state, sign)])
        return set()

    def reachable_states(self, state, sign):
        states = set(state)
        newStates = set(states)

        for s in states:
            newStates.update(self.get_all_epsilon(s))

        states.update(newStates)
        newStates = set()

        for s in states:
            newStates.update(self.transition(s, sign))

        states = newStates
        newStates = set()

        for s in states:
            newStates.update(self.get_all_epsilon(s))

        states.update(newStates)

        return states

    def possible_states(self, toCheck):
        index = 0
        maxIndex = len(toCheck)
        states = set(STARTING_STATE)

        while index < maxIndex and len(states) > 0:
            states = self.reachable_states(states, toCheck[index])
            index += 1

        return states

    # Converts a given expression expr into a e-NFA auto
    def __convert(self, expr):
        choices = list()
        pCount = 0
        iCount = len(expr) - 1
        iLast = 0

        # Separates groups
        for i, x in enumerate(expr):
            if is_operator(expr, i):
                if x == LBRACKET:
                    pCount += 1
                elif x == RBRACKET:
                    pCount -= 1
                elif pCount == 0 and x == OP_SEPARATE and is_operator(expr, i):
                    choices.append(expr[iLast: i])
                    iLast = i + 1

            if i == iCount:
                choices.append(expr[iLast:i + 1])

        leftState = Automata.add_state(self)
        rightState = Automata.add_state(self)

        if len(choices) > 1:
            for I, x in enumerate(choices):
                temp = self.__convert(choices[I])
                self.add_epsilon_transition(leftState, temp[0])
                self.add_epsilon_transition(temp[1], rightState)
        else:
            prefixed = False
            lastState = leftState

            i = 0
            j = len(expr)
            while i < j:
                if prefixed:
                    prefixed = False
                    sign = ''

                    if expr[i] == 't':
                        sign = '\t'
                    elif expr[i] == 'n':
                        sign = '\n'
                    elif expr[i] == '_':
                        sign = ' '
                    else:
                        sign = expr[i]

                    a = Automata.add_state(self)
                    b = Automata.add_state(self)

                    self.add_transition(a, b, sign)
                else:
                    if expr[i] == ESCAPE_CHAR:
                        prefixed = True
                        i += 1
                        continue

                    if expr[i] != LBRACKET:
                        a = Automata.add_state(self)
                        b = Automata.add_state(self)
                        self.add_transition(a, b, expr[i])
                    else:
                        k = end_parenthesis_index(expr, i)
                        temp = self.__convert(expr[i + 1:k])
                        a = temp[0]
                        b = temp[1]
                        i = k

                if i + 1 < j and expr[i + 1] == OP_KLEEN:
                    x = a
                    y = b
                    a = Automata.add_state(self)
                    b = Automata.add_state(self)
                    self.add_epsilon_transition(a, x)
                    self.add_epsilon_transition(y, b)
                    self.add_epsilon_transition(a, b)
                    self.add_epsilon_transition(y, x)
                    i += 1

                self.add_epsilon_transition(lastState, a)
                lastState = b
                i += 1

            self.add_epsilon_transition(lastState, rightState)

        return leftState, rightState


# Checks if expr[i] is an operator
def is_operator(expr, i):
    x = 0

    while i > 0 and expr[i - 1] == ESCAPE_CHAR:
        x += 1
        i -= 1

    return x % 2 == 0


# Finds the index of the RBRACKET corresponding to the LBRACKET found at expr[startingIndex]
def end_parenthesis_index(expr, startingIndex):
    i = startingIndex + 1
    j = len(expr)
    pCount = 1

    while (i < j):
        if expr[i] == LBRACKET:
            pCount += 1
        elif expr[i] == RBRACKET:
            pCount -= 1

        if pCount == 0:
            return i

        i += 1

    return startingIndex


def main():
    str = "''"
    expr = "\'(\(|\)|\{|\}|\||\*|\\|\$|\|!|\"|#|%|&|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^||`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\'"
    expp = "\'\(|\)|\{|\}|\||\*|\\|\$|\_|!|\"|#|%|&|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~\'"

    r = RegularExpression(expp)
    print("Possible states:", r.automata.possible_states(str))
    print("Possible:", r.possible(str))
    print("Match:", r.match(str))


main()
