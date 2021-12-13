FLUSH = "-"
NEW_LINE = "NOVI_REDAK"
ENTER_STATE = "UDJI_U_STANJE"
RETURN = "VRATI_SE"


class LA:
    def __init__(self, generator):
        self.states = generator.states
        self.signs = generator.signs
        self.rules = generator.rules
        self.startingState = self.states[0]

    def analyze(self, text):
        inst = LAInstance(self, text)

        while inst.currentIndex < inst.lastIndex:
            inst.checkNext()

        for x in inst.generation:
            print(x[0] + " " + str(x[1]) + " " + x[2])


class LAInstance:
    def __init__(self, la, text):
        self.la = la
        self.text = text
        self.currentIndex = 0
        self.lastIndex = len(text)
        self.currentLine = 1
        self.currentRead = ""
        self.currentState = la.startingState
        self.possibleRules = self.getPossibleRules()
        self.generation = []

    # Only shows rules you can transition to from the current state.
    def getPossibleRules(self):
        return list(filter(lambda x: x[0] == self.currentState, self.la.rules))

    # Changes the currentState to state
    def enterState(self, state):
        self.currentState = state
        self.possibleRules = self.getPossibleRules()

    # Flushes the currentRead variable
    def flushRead(self):
        self.currentRead = ""

    # Returns a tuple containing the uniform sign name, the line it was read in and what it read
    def uniformSign(self, usName, read):
        return usName, self.currentLine, read

    # Increments currentLine
    def newLine(self):
        self.currentLine += 1

    # Changes the current index to the difference of the read expression and the value
    # and flushes whatever has been read
    def returnTo(self, value):
        self.currentIndex -= (len(self.currentRead) - value)
        self.flushRead()
        return self.text[self.currentIndex - value:self.currentIndex]

    # Adds the currently pointed to character to the currentRead queue and increments currentIndex
    def next(self):
        self.currentRead = self.currentRead + self.text[self.currentIndex]
        self.currentIndex += 1

    # Adds the next character to read queue and checks if any events should trigger
    def checkNext(self):
        self.next()
        self.checkForHit()

    # Checks if the currentRead has triggered any event
    def checkForHit(self):
        rules = self.getPossibles()
        lastRules = rules
        didIt = False

        lastMatchingRule = (int, list())

        while len(rules) > 0 and self.currentIndex < self.lastIndex:
            didIt = True
            lastRules = rules

            for r in lastRules:
                if r[1].match(self.currentRead):
                    lastMatchingRule = (self.currentIndex, r)
                    break

            self.next()
            rules = self.getPossibles()

        if didIt:
            diff = self.currentIndex - lastMatchingRule[0]
            self.currentIndex = lastMatchingRule[0]
            self.currentRead = self.currentRead[:-diff]

        theRule = lastMatchingRule[1]

        if len(theRule) < 0:
            if len(lastRules) > 0:
                theRule = lastRules[0]
            else:
                theRule = []
        if len(theRule) > 0:
            self.doCommand(theRule[2])
        else:
            self.flushRead()

    def getPossibles(self):
        toRet = list()

        for r in self.getPossibleRules():
            if r[1].possible(self.currentRead):
                toRet.append(r)

        return toRet


    # Does a command
    def doCommand(self, commands):
        queueInsertion = False
        commandQueue = ""
        returnOverwrite = ""

        for command in commands:
            if command in self.la.signs:
                queueInsertion = True
                commandQueue = command
            elif command == FLUSH:
                self.flushRead()
            elif command == NEW_LINE:
                self.newLine()
            elif command.startswith(ENTER_STATE):
                temp = command.split(" ")
                self.enterState(temp[1])
            elif command.startswith(RETURN):
                temp = command.split(" ")
                returnOverwrite = self.returnTo(int(temp[1]))

        if queueInsertion:
            if returnOverwrite == "":
                returnOverwrite = self.currentRead

            operatorValue = returnOverwrite.split(' ')
            operatorValue = operatorValue[0].split('\n')
            operatorValue = operatorValue[0].split('\t')
            self.generation.append(self.uniformSign(commandQueue, operatorValue[0]))
            self.flushRead()

def main():
