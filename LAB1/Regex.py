OP_SEPARATE = '|'
OP_KLEEN = '*'
LBRACKET = '('
RBRACKET = ')'
NAME_START = '{'
NAME_END = '}'
ESCAPE_CHAR = '\\'
EPSILON = '$'


class RegularExpression:
    def __init__(self, expr):
        self.expression = expr
        self.automata = Automata(expr)

    # Returns true if toCheck matches the current instance of the regular expression, false otherwise.
    def match(self, toCheck):
        return self.possibleStates(toCheck).__contains__(1)

    # Checks if the toCheck can fulfill the regex in the future
    def possible(self, toCheck):
        return len(self.possibleStates(toCheck)) > 0

    # Same as transition, but for a string.
    def possibleStates(self, toCheck):
        maxIndex = len(toCheck)

        if maxIndex < 1:
            return True
        else:
            t = self.transition(0, toCheck[0])
            index = 1

            while index < maxIndex and len(set(t)) > 0:
                t = self.transition(t, toCheck[index])
                index += 1

            return set(t)

    # Returns a complete list of possible states the automata could land in
    # from a given state and a transitional sign sign
    def transition(self, state, sign):
        new_states = self.epsilonTransition(state)

        tmp_states = set()
        for s in new_states:
            tmp_states.update(self.step(s, sign))

        new_states = self.epsilonTransition(tmp_states)

        return list(new_states)

    # Returns new states originating from state for a transitional sign sign
    def step(self, state, sign):
        if self.automata.states.__contains__((state, sign)):
            return self.automata.states[(state, sign)]
        return set()

    # Returns the epsilon transitions for a given state
    def epsilonTransition(self, state):
        state_checker_old = set(state)

        while True:
            state_checker_new = set(state_checker_old)

            for s in state_checker_old:
                state_checker_new.update(self.step(s, EPSILON))

            if state_checker_old != state_checker_new:
                state_checker_old.update(state_checker_new)
            else:
                break

        return state_checker_old

class Automata:
    def __init__(self, expr):
        self.states = {}
        self.stateAmount = 0
        self.convert(expr)

    # Increments the state count and returns the serial number of the last state available.
    def addState(self):
        self.stateAmount += 1
        return self.stateAmount - 1

    # Adds a transition d(startingState, transitionalSign) -> endingState
    def addTransition(self, startingState, endingState, transitionalSign):
        if not self.states.__contains__((startingState, transitionalSign)):
            self.states[(startingState, transitionalSign)] = list()

        self.states[(startingState, transitionalSign)].append(endingState)

    # Adds a transition d(startingState, EPSILON) -> endingState
    def addEpsilonTransition(self, startingState, endingState):
        self.addTransition(startingState, endingState, EPSILON)

    # Converts a given expression expr into a e-NFA auto
    def convert(self, expr):
        choices = list()
        pCount = 0
        iCount = len(expr) - 1
        iLast = 0

        # Separates groups
        for i, x in enumerate(expr):
            if isOperator(expr, i):
                if x == LBRACKET:
                    pCount += 1
                elif x == RBRACKET:
                    pCount -= 1
                elif pCount == 0 and x == OP_SEPARATE and isOperator(expr, i):
                    choices.append(expr[iLast: i])
                    iLast = i + 1

            if i == iCount:
                choices.append(expr[iLast:i + 1])

        leftState = Automata.addState(self)
        rightState = Automata.addState(self)

        if len(choices) > 1:
            for I, x in enumerate(choices):
                temp = self.convert(choices[I])
                self.addEpsilonTransition(leftState, temp[0])
                self.addEpsilonTransition(temp[1], rightState)
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

                    a = Automata.addState(self)
                    b = Automata.addState(self)

                    self.addTransition(a, b, sign)
                else:
                    if expr[i] == ESCAPE_CHAR:
                        prefixed = True
                        i += 1
                        continue

                    if expr[i] != LBRACKET:
                        a = Automata.addState(self)
                        b = Automata.addState(self)
                        self.addTransition(a, b, expr[i])
                    else:
                        k = endParenthesisIndex(expr, i)
                        temp = self.convert(expr[i + 1:k])
                        a = temp[0]
                        b = temp[1]
                        i = k

                if i + 1 < j and expr[i + 1] == OP_KLEEN:
                    x = a
                    y = b
                    a = Automata.addState(self)
                    b = Automata.addState(self)
                    self.addEpsilonTransition(a, x)
                    self.addEpsilonTransition(y, b)
                    self.addEpsilonTransition(a, b)
                    self.addEpsilonTransition(y, x)
                    i += 1

                self.addEpsilonTransition(lastState, a)
                lastState = b
                i += 1

            self.addEpsilonTransition(lastState, rightState)

        return leftState, rightState


# Checks if expr[i] is an operator
def isOperator(expr, i):
    x = 0

    while i > 0 and expr[i - 1] == ESCAPE_CHAR:
        x += 1
        i -= 1

    return x % 2 == 0


# Finds the index of the RBRACKET corresponding to the LBRACKET found at expr[startingIndex]
def endParenthesisIndex(expr, startingIndex):
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

