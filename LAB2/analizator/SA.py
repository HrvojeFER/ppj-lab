# Contains all the classes and methods needed by the Generator to make the generative tree.
# The init file location has to be specified.

from enum import Enum
import sys

STARTING_SIGN = '<%>'
END_OF_PROGRAM = '#'
DOT = '*'
STARTING_STATE = 0
EPSILON = '$'
INIT_FILE_NAME = 'generator.ini'


class UniformSign:
    UNIFORM_SIGN_DELIMITER = ' '

    def __init__(self, sign, line_index, program_str):
        self.sign = sign
        self.line_index = line_index
        self.program_str = program_str

    # The reverse parse method.
    # Returns the string that the parse method would parse to get the object.
    def __str__(self):
        return self.sign + UniformSign.UNIFORM_SIGN_DELIMITER + \
               self.line_index + UniformSign.UNIFORM_SIGN_DELIMITER + \
               self.program_str

    # Returns a UniformSign parsed from the input string.
    @staticmethod
    def parse(uniform_sign_str):
        # The uniform sign string always has three elements.
        split = uniform_sign_str.split(UniformSign.UNIFORM_SIGN_DELIMITER, 2)
        sign = split[0]
        line_index = split[1]
        program_str = split[2]
        return UniformSign(sign, line_index, program_str)


class Action:
    ARGUMENT_DELIMITER = ' '
    REDUCTION_DELIMITER = ' '

    # Action type enum.
    class ActionType(Enum):
        MOVE = 'MOVE'
        REDUCE = 'REDUCE'
        ACCEPT = 'ACCEPT'
        REJECT = 'REJECT'

    # Initializes the appropriate action for the given action type (type) and
    # arguments (arg1, arg2).
    def __init__(self, action_type, arg1=None, arg2=None):
        self.action_type = action_type
        if self.action_type == Action.ActionType.MOVE:
            self.ending_sign = arg1
            self.new_state = arg2
        elif self.action_type == Action.ActionType.REDUCE:
            self.non_ending_sign = arg1
            self.to_reduce = arg2

    # The reverse parse method.
    # Returns the string that the parse method would parse to get the object.
    def __str__(self):
        to_ret = self.action_type.__str__()

        if self.action_type == Action.ActionType.MOVE:
            to_ret += ' ' + self.ending_sign + ' ' + self.new_state.__str__()

        elif self.action_type == Action.ActionType.REDUCE:
            to_ret += ' ' + self.non_ending_sign + ' ' + self.to_reduce.__str__()

        return to_ret

    # Parses the given string into an Action object.
    @staticmethod
    def parse(action_str):
        # Split the string with the argument delimiter.
        arg_list = action_str.split(Action.ARGUMENT_DELIMITER, 2)

        action_type = Action.ActionType(arg_list[0])

        # If the argument list has only one element
        # it means that there are no other arguments to be added.
        if len(arg_list) == 1:
            return Action(action_type)

        # If there are more arguments - there will always be three arguments.
        arg1 = arg_list[1]

        # Split the second argument with the reduction delimiter
        arg2 = arg_list[2].split(Action.REDUCTION_DELIMITER)

        # If the first element of the last argument is numeric or is epsilon then
        # the action type is a move action type.
        # arg2 in a move action type is a new state which should be an integer or epsilon.
        if arg2[0].isnumeric():
            arg2 = int(arg2[0])

        elif arg2[0] == EPSILON:
            arg2 = EPSILON

        return Action(action_type, arg1, arg2)


class Generator:
    KEY_VALUE_DELIMITER = ':'
    KEY_DELIMITER = ' '
    SYNC_DELIMITER = ' '

    def __init__(self, init_file_path):
        # Opens the init file.
        init_file = open(init_file_path, 'r')

        # Creates an action table and iterates over lines while there are new actions to be added.
        # Splits the line into the key and action string, parses the action string and
        # adds it to the table with the key.
        # The first half of the key is the current state so it converts it to an integer.
        self.action_table = dict()
        while True:
            line = init_file.readline()
            if line == '\n':
                break

            key_value = line[:-1].split(Generator.KEY_VALUE_DELIMITER)
            key = key_value[0].split(Generator.KEY_DELIMITER)
            self.action_table[int(key[0]), key[1]] = Action.parse(key_value[1])

        # Creates a new state stable and iterates over lines until there are no new states to be added.
        # Splits the line into the key and the new state string, converts the new state string into an integer
        # and adds those to the table.
        # The first half of the key is the current state so it converts it to an integer.
        self.new_state_table = dict()
        while True:
            line = init_file.readline()
            if line == '\n':
                break

            key_value = line[:-1].split(Generator.KEY_VALUE_DELIMITER)
            key = key_value[0].split(Generator.KEY_DELIMITER)
            self.new_state_table[int(key[0]), key[1]] = int(key_value[1])

        # Get the synchronization signs list by splitting the last line
        # with the synchronization signs delimiter.
        self.sync_signs = init_file.readline()[:-1].split(Generator.SYNC_DELIMITER)

    # Returns the string representation of the object.
    def __str__(self):
        to_ret = ''

        for key in self.action_table.keys():
            to_ret += key.__str__() + ' ' + self.action_table[key].__str__() + '\n'
        to_ret += '\n'

        for key in self.new_state_table.keys():
            to_ret += key.__str__() + ' ' + self.new_state_table[key].__str__() + '\n'
        to_ret += '\n'

        to_ret += self.sync_signs.__str__()

        return to_ret

    # Class used by the class TreeStack to manage leaves on the generator stack.
    class Leaf:
        # Sign (sign) and state (state) have to be specified in the leaf constructor.
        # Raises a ValueError if the sign provided is not a uniform sign.
        def __init__(self, sign, state):
            if type(sign) != UniformSign:
                raise ValueError('This is not a uniform sign.')
            self.sign = sign
            self.state = state

        # Returns the string representation of itself.
        # The string representation of a leaf is the string representation of its sign.
        def __str__(self):
            return self.sign.__str__()

    # Class for trees used by the TreeStack class. Used for tree manipulation and their string representation.
    class Tree:
        TREE_LEVEL_INDICATOR = ' '
        BASE_TREE_LEVEL = 0

        # Sign (root) has to be specified in the tree constructor.
        # The constructor makes a list of branches.
        def __init__(self, sign, state=None):
            self.sign = sign
            self.state = state
            self.branches = list()

        # __str__ can't take arguments so the best option is to make a separate DFS function for printing.
        def __str__(self):
            return self.print(Generator.Tree.BASE_TREE_LEVEL)

        # DFS algorithm that returns the string representation of the tree.
        def print(self, tree_level):
            to_ret = self.sign

            # If there are any branches or leaves on the tree - goes over them and
            # adds a newline, a tree level indicator and their string representation
            # to the return value (to_ret).
            if self.branches:
                for branch in self.branches:
                    if type(branch) == Generator.Tree:
                        to_ret += '\n' + Generator.Tree.TREE_LEVEL_INDICATOR * \
                                  (tree_level + 1) + branch.print(tree_level + 1)
                    else:
                        to_ret += '\n' + Generator.Tree.TREE_LEVEL_INDICATOR * \
                                  (tree_level + 1) + branch.__str__()
            else:
                to_ret += '\n' + Generator.Tree.TREE_LEVEL_INDICATOR * (tree_level + 1) + EPSILON

            return to_ret

        # Adds a branch to the tree.
        def add_branch(self, branch):
            self.branches.append(branch)

        # Sets the state if the state is None, otherwise raises a ValueError.
        def set_state(self, state):
            if self.state is not None:
                raise ValueError('State already set.')

            self.state = state

    # Class for managing states of the generator.
    class TreeStack:
        # Main constructor makes a list of trees.
        # List is used because there doesn't exist a stack class in Python.
        def __init__(self):
            self.trees = list()

        # Returns the length of the stack
        def __len__(self):
            return len(self.trees)

        # Returns the string representation of the stack.
        def __str__(self):
            to_ret = ''
            # Reverse the tree order so that the result is top-down.
            self.trees.reverse()

            # Goes over all of the trees in the stack and adds
            # their string representation and a newline in the return variable to_ret.
            for tree in self.trees:
                to_ret += tree.__str__() + '\n'

            # Revert changes.
            self.trees.reverse()

            # The last newline is redundant.
            return to_ret[:-1]

        # Makes the class boolean-able.
        def __bool__(self):
            return self.__len__() > 0

        # Returns the current stack state.
        def get_state(self):
            # If the stack is empty returns the starting state.
            if not self:
                return STARTING_STATE

            return self.peek().state

        # Pushes a tree on the stack
        def push(self, tree):
            # If the tree is not of type Tree or Leaf raises a ValueError.
            if not (type(tree) == Generator.Tree or type(tree) == Generator.Leaf):
                raise ValueError('This is not a good tree.')

            # The tree has to have a state to be put on the stack.
            if type(tree) is Generator.Tree and tree.state is None:
                raise ValueError('This tree has no state.')

            self.trees.append(tree)

        # Returns the tree on the stack. If there are no trees on the stack, returns None
        def peek(self):
            if not self:
                return None

            return self.trees[-1]

        # Same as peek, but it removes the tree if there is one.
        def pop(self):
            to_ret = self.peek()

            if to_ret is None:
                return None

            self.trees = self.trees[:-1]

            return to_ret

        # Reduces the trees on the stack with the corresponding tree signs (tree_signs)
        # to a new tree (new_tree).
        def reduce(self, tree_signs, non_ending_sign):
            reduced_tree = Generator.Tree(non_ending_sign)
            branches = list()

            # Goes over the tree signs (tree_signs) and checks if there is a tree on the stack
            # with the corresponding sign. If there is, it adds that tree to the branches of the new tree (new_tree)
            # If there isn't, it raises a ValueError.
            # Reverses the order of the branches so its in the order of the production.
            if tree_signs != EPSILON:
                tree_signs.reverse()
                for sign in tree_signs:
                    if type(self.peek()) == Generator.Leaf:
                        if self.peek().sign.sign != sign:
                            raise ValueError('You got a bad tree.')
                    elif type(self.peek()) == Generator.Tree:
                        if self.peek().sign != sign:
                            raise ValueError('You got a bad tree')
                    else:
                        raise ValueError('You got a bad tree')

                    branches.append(self.pop())

                branches.reverse()
                for branch in branches:
                    reduced_tree.add_branch(branch)
                tree_signs.reverse()

            return reduced_tree

        # Resets the stack.
        def reset(self):
            self.trees = list()

    # Class used for parsing a list of uniform signs (uniform_signs).
    class Parser:
        # Initializes the stack and the the accepted variable.
        # Adds the end of program sign to the uniform signs list.
        def __init__(self, uniform_signs):
            self.uniform_signs = uniform_signs
            uniform_signs.append(END_OF_PROGRAM)
            self.is_accepted = None
            self.index = 0

        # Returns the current sign on the parser head.
        def get_sign(self):
            if self.there_are_more():
                return self.uniform_signs[self.index]
            else:
                return None

        # Moves the parser head by one spot.
        def move(self):
            if self.there_are_more():
                self.index += 1

        # Returns true if there are more uniform signs to be parsed, otherwise false.
        def there_are_more(self):
            return self.index < len(self.uniform_signs)

        # Accept action method. Sets the given set of uniform signs as accepted.
        def accept(self):
            self.is_accepted = True

        # Reject action method. Sets the given set of uniform signs as rejected.
        def reject(self):
            self.is_accepted = False

        # Finds the next synchronizing sign and skips all the signs before it.
        # Returns the fitting sign if there is one, otherwise returns None.
        def skip_signs(self, fitting_sign_list):
            fitting_sign = None

            self.move()
            while self.there_are_more():
                current_sign = self.get_sign()
                if type(current_sign) == UniformSign:
                    if fitting_sign_list.__contains__(current_sign.sign):
                        fitting_sign = current_sign
                        break
                else:
                    if fitting_sign_list.__contains__(current_sign):
                        fitting_sign = current_sign
                        break
                self.move()

            return fitting_sign

    # Returns the action for the given state and sign from the action table.
    def get_action(self, state, uniform_sign):
        if type(uniform_sign) == UniformSign:
            return self.action_table[state, uniform_sign.sign]
        elif uniform_sign == END_OF_PROGRAM:
            return self.action_table[state, uniform_sign]
        else:
            raise ValueError('Wrong sign my dude.')

    # Returns the new state for the given state and sign from the action table.
    def get_new_state(self, state, sign):
        return self.new_state_table[state, sign]

    # Parses a list of uniform signs (uniform_signs)
    def parse(self, uniform_signs):
        # Initializes a new parser for the list of uniform signs and a new stack.
        parser = Generator.Parser(uniform_signs)
        stack = Generator.TreeStack()

        # Iterates over the uniform signs list while there are uniform signs to iterate over.
        while parser.there_are_more():
            # Determines which action to do.
            uniform_sign = parser.get_sign()
            action = self.get_action(stack.get_state(), parser.get_sign())

            # If the action determined is a move action - pushes a leaf on the stack and
            # moves the parser head.
            if action.action_type == Action.ActionType.MOVE:
                stack.push(Generator.Leaf(uniform_sign, action.new_state))
                parser.move()

            # If the action determined is a reduce action - reduces the stack trees with
            # roots action.to_reduce to a new reduced tree with the sign action.non_ending_sign,
            # sets the new state of the reduced tree and pushes it on the stack.
            elif action.action_type == Action.ActionType.REDUCE:
                reduced_tree = stack.reduce(action.to_reduce, action.non_ending_sign)
                reduced_tree.set_state(self.get_new_state(stack.get_state(), action.non_ending_sign))

                stack.push(reduced_tree)

            # If the action is an accept action - does the parser accept action and moves the parser head.
            # Only happens at the end of the program.
            elif action.action_type == Action.ActionType.ACCEPT:
                parser.accept()
                parser.move()

            # If the action is a reject action - does the parser reject action.
            # Skips uniform signs until it finds the next synchronizing sign.
            # Removes trees from the stack until there is an action which is not a reject action or
            # until the stack is empty.
            elif action.action_type == Action.ActionType.REJECT:
                parser.reject()
                self.print_error()

                sync_sign = parser.skip_signs(self.sync_signs)

                if sync_sign is None:
                    break

                while True:
                    if self.get_action(stack.get_state(), sync_sign).action_type != Action.ActionType.REJECT:
                        break

                    if stack.pop() is None:
                        break

        # Prints the generative tree.
        return stack.__str__()

    # todo error print
    def print_error(self):
        pass

    # Method for getting the uniform signs list from the standard input
    @staticmethod
    def get_uniform_signs():
        uniform_signs = list()

        # Goes over all of the lines from the standard input and
        # appends the uniform sign in the current line to the uniform signs list.
        for line in sys.stdin:
            # debug
            if line == 'END\n':
                break

            uniform_signs.append(UniformSign.parse(line[:-1]))

        return uniform_signs


generator = Generator(INIT_FILE_NAME)
print(generator.parse(Generator.get_uniform_signs()))
