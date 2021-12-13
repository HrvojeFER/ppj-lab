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
        # return RegularExpression.__check(self, toCheck, 0, len(toCheck), 0) == 1

    # Checks if the toCheck can fulfill the regex in the future
    def possible(self, toCheck):
        return len(self.possibleStates(toCheck)) > 0

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

    # Returns all states that the automata can end up in starting in state for the transitional sign sign
    def transition(self, state, sign, withh=True):
        toRet = list()

        if withh:
            state = self.getPreSignStates(state)

        if type(state) is list:
            for s in state:
                toRet.extend(self.transition(s, sign, False))
        else:
            if self.automata.states.__contains__((state, sign)):
                toRet.extend(self.automata.states[(state, sign)])

            if len(toRet) > 0:
                toRet2 = self.getAllEpsilonExcept(toRet, set())

                if toRet2 is not None:
                    toRet.extend(toRet2)

        t = list(set(toRet))
        return t

    # Gets the epsilon environment of the state.
    def getAllEpsilon(self, state):
        toRet = list()

        if type(state) is list:
            for s in state:
                toRet.extend(self.getAllEpsilon(s))
        else:
            if self.automata.states.__contains__((state, EPSILON)):
                toRet.extend(self.automata.states[(state, EPSILON)])
                res = self.getAllEpsilon(self.automata.states[(state, EPSILON)])

                if res is None:
                    return toRet
                else:
                    res.extend(toRet)
                    return res

            return []
        return toRet

    def getAllEpsilonExcept(self, state, exc):
        toRet = list()

        if type(state) is list:
            for s in state:
                if not exc.__contains__(s):
                    toRet.extend(self.getAllEpsilon(s))
        else:
            if self.automata.states.__contains__((state, EPSILON)):
                exc.add(state)
                toRet.extend(self.automata.states[(state, EPSILON)])
                res = self.getAllEpsilonExcept(self.automata.states[(state, EPSILON)], exc)

                if res is None:
                    return toRet
                else:
                    res.extend(toRet)
                    return res

            return []
        return toRet

    # Merges the epsilon environment with the state
    def getPreSignStates(self, state):
        toRet = list()

        if type(state) is list:
            for s in state:
                toRet.extend(self.getAllEpsilonExcept(s, set()))
            toRet.extend(state)
        else:
            toRet.extend(self.getAllEpsilonExcept(state, set()))
            toRet.append(state)

        return list(set(toRet))

    # Returns the last viable state of the contained automata auto for input toCheck from index index,
    # with the last index being maxIndex, with the current state of state, or -1 if there is no viable state to go into.
    def __check(self, toCheck, index, maxIndex, state):
        if type(state) is list:
            tt = -1
            t = 0
            for x in state:
                t = self.__check(toCheck, index, maxIndex, x)
                if t == 1:
                    return 1
            return -1

        if index < maxIndex and self.automata.states.__contains__((state, toCheck[index])):
            state = self.automata.states[(state, toCheck[index])]
            index += 1
        elif self.automata.states.__contains__((state, EPSILON)):
            state = self.automata.states[(state, EPSILON)]
        elif index < maxIndex:
            return state
        elif index == maxIndex:
            return -1

        print("toCheck:-", toCheck, "-\nindex:", index, "\nmaxTndex:", maxIndex, "\ncurrentState:", state, "\n\n")

        return RegularExpression.__check(self, toCheck, index, maxIndex, state)

    def getPossibleTransitions(self, state, sign):
        return filter(lambda x: x[0] == state and x[1] == sign, self.auto.states)


class Automata:
    def __init__(self):
        self.states = {}
        self.stateAmount = 0

    def __init__(self, expr):
        self.states = {}
        self.stateAmount = 0
        self.convert(expr)

        #for i in self.states:
        #     print(i, "->", self.states[i])


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


def main():
    str = "''"
    expr = "\'(\(|\)|\{|\}|\||\*|\\|\$|\|!|\"|#|%|&|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^||`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)'\'"

    r = RegularExpression(expr)
    print(r.possible(str))


main()
