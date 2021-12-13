import LAB3.Global as Global
from enum import Enum


class TableEntry:
    def __init__(self, entry_type, l_flag: bool, is_defined: bool=False):
        self.__type = entry_type
        self.__l_flag = l_flag
        self.__is_defined = is_defined

    def get_type(self):
        return self.__type

    def get_l_flag(self):
        return self.__l_flag

    def is_defined(self):
        return self.__is_defined

    def __str__(self):
        return "type: " + str(self.__type) + ", l-flag: " + str(self.__l_flag) + ", defined: " + str(self.__is_defined)


def mutable(source, destination):
    if source in [PrimitiveType.CHAR, PrimitiveType.CONST_CHAR]:
        return True

    if source in [PrimitiveType.INT, PrimitiveType.CONST_INT] and \
            destination in [PrimitiveType.INT, PrimitiveType.CONST_INT]:
        return True

    array_types = [ArrayType.ARRAY_INT, ArrayType.ARRAY_CONST_INT, ArrayType.ARRAY_CHAR, ArrayType.ARRAY_CONST_CHAR]
    if source in array_types and destination in array_types:
        return True

    return False


# Prima "nešto -> nešto" za funkcijske tipove, "nešto, nešto, nešto" za parametere,
# (const)0..1nešto za primitivne tipove, ili (const)0..1nešto[] za polja.
def get_type_from_string(string: str):
    # Check if the type is a function.
    f_params = string.split(" -> ")

    if len(f_params) is 1:
        # Check if the type is a params.
        params = string.split(", ")

        if len(params) is 1:
            # Check if the type is an array.
            if "[]" in string:
                new_string = string.replace("[]", "")

                # Check if the type is a constant.
                if new_string.startswith("const"):
                    other_word = string.split(" ")[1]

                    if other_word == "int":
                        return ArrayType.ARRAY_CONST_INT

                    if other_word == "char":
                        return ArrayType.ARRAY_CONST_CHAR
                else:
                    if string == "int":
                        return ArrayType.ARRAY_INT

                    if string == "char":
                        return ArrayType.ARRAY_CHAR
            else:
                # Check if the type is a constant.
                if string.startswith("const"):
                    other_word = string.split(" ")[1]

                    if other_word == "int":
                        return PrimitiveType.CONST_INT

                    if other_word == "char":
                        return PrimitiveType.CONST_CHAR
                else:
                    if string == "int":
                        return PrimitiveType.INT

                    if string == "char":
                        return PrimitiveType.CHAR

                    if string == "void":
                        return PrimitiveType.VOID
        else:
            type_list = list()

            for param in params:
                type_list.append(get_type_from_string(param))

            return Params(type_list)
    else:
        return FunctionType(get_type_from_string(f_params[0]), get_type_from_string(f_params[1]))


def array(primitive_type):
    if primitive_type is PrimitiveType.INT:
        return ArrayType.ARRAY_INT

    if primitive_type is PrimitiveType.CONST_INT:
        return ArrayType.ARRAY_CONST_INT

    if primitive_type is PrimitiveType.CHAR:
        return ArrayType.ARRAY_CHAR

    if primitive_type is PrimitiveType.CONST_CHAR:
        return ArrayType.ARRAY_CONST_CHAR

    return None


def split_signs(string: str):
    if string.startswith('"'):
        string = string[1:]

    if string.endswith('"'):
        string = string[:-1]

    new_string = list()

    i = 0
    i_max = len(string)

    while i < i_max:
        if i + 1 < i_max and string[i] == '\\':
            new_string.append(str(string[i] + string[i + 1]))
            i += 2
            continue
        else:
            new_string.append(str(string[i]))
            i += 1

    return new_string


def znak_valid(char: str) -> bool:
    if len(char) is 1:
        return Global.CHAR_RANGE[0] <= ord(char) <= Global.CHAR_RANGE[1]
    else:
        return char[1] in ['n', 't', '0', "'", '"', "\\"]


def niz_znakova_valid(string: str):
    split = split_signs(string)

    for character in split:
        if not znak_valid(character):
            return False

    return True


def count_signs(string: str):
    split = split_signs(string)

    return len(split)


# -------------------------------


class PrimitiveType(Enum):
    NONE = 0,
    INT = 1,
    CONST_INT = 2,
    CHAR = 3,
    CONST_CHAR = 4,
    POV = 5,
    VOID = 6,
    PARAMS = 7,
    FUNCTION = 8


class ArrayType(Enum):
    NONE = 0,
    ARRAY_INT = 1,
    ARRAY_CONST_INT = 2
    ARRAY_CHAR = 3
    ARRAY_CONST_CHAR = 4


class OtherType(Enum):
    NONE = 0,

    IDN = 1,
    BROJ = 2,
    ZNAK = 3,
    NIZ_ZNAKOVA = 4,
    IZRAZ_U_ZAGRADAMA = 5

    PRIMARNI_IZRAZ = 6,
    POSTFIKS_INC = 7,
    POSTFIKS_DEC = 8,
    POSTFIKS_PRAZNE_ZAGRADE = 9,
    POSTFIKS_UGLATE_ZAGRADE = 10,
    POSTFIKS_PUNE_ZAGRADE = 11,

    IZRAZ_PRIDRUZIVANJA = 12,
    LISTA_ARGUMENATA_UZ_IZRAZ = 13,

    POSTFIKS_IZRAZ = 14,
    INC_UNARNI_IZRAZ = 15,
    DEC_UNARNI_IZRAZ = 16,
    UNARNI_OPERATOR_UZ_CAST = 17,

    UNARNI_PLUS = 18,
    UNARNI_MINUS = 19,
    UNARNI_TILDA = 20,
    UNARNI_NEG = 21,

    UNARNI_IZRAZ = 22,
    VISESTRUKI_CAST = 23,

    OBICAN_TIP = 24,
    KONSTANTAN_TIP = 25,

    VOID_TIP = 26,
    CHAR_TIP = 27,
    INT_TIP = 28,

    CAST_IZRAZ = 29,
    PUTA_IZRAZ = 30,
    DIJELI_IZRAZ = 31,
    MOD_IZRAZ = 32,

    MULTIPLIKATIVNI_IZRAZ = 33,
    PLUS_IZRAZ = 34,
    MINUS_IZRAZ = 35,

    ADITIVNI_IZRAZ = 36,
    LT_IZRAZ = 37,
    GT_IZRAZ = 38,
    LTE_IZRAZ = 39,
    GTE_IZRAZ = 40,

    ODNOSNI_IZRAZ = 41,
    EQ_IZRAZ = 42,
    NEQ_IZRAZ = 43,

    JEDNAKOSNI_IZRAZ = 44,
    OP_BIN_I_IZRAZ = 45,

    BIN_I_IZRAZ = 46,
    OP_BIN_XILI_IZRAZ = 47,

    BIN_XILI_IZRAZ = 48,
    OP_BIN_ILI_IZRAZ = 49,

    BIN_ILI_IZRAZ = 50,
    OP_LOG_I_IZRAZ = 51,

    LOG_I_IZRAZ = 52,
    OP_LOG_ILI_IZRAZ = 53,

    LOG_ILI_IZRAZ = 54,
    OP_PRIDRUZI_IZRAZ = 55,

    IZRAZ_PRIDRUZIVANJA_IZ_IZRAZ = 56,
    IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ = 57,

    SLOZ_NAREDBA_LISTA_NAREDBI = 58,
    SLOZ_NARED_S_LISTOM_DEKL_I_NAREDBI = 59,

    NAREDBA = 60,
    LISTA_NAREDBI = 61,

    SLOZENA_NAREDBA = 62,
    IZRAZ_NAREDBA = 63,
    NAREDBA_GRANANJA = 64,
    NAREDBA_PETLJE = 65,
    NAREDBA_SKOKA = 66,

    TOCKAZAREZ = 67,
    IZRAZ_I_TOCKAZAREZ = 68,

    IF = 69,
    IF_S_ELSEOM = 70,

    WHILE = 71,
    FOR_BEZ_INDEKSIRANJA = 72,
    FOR_SA_INDEKSIRANJEM = 73,

    CONTINUE_OR_BREAK = 74,
    RETURN_BEZ_POV_VRIJEDNOSTI = 75,
    RETURN_SA_POV_VRIJEDNOSTI = 76,

    VANJSKA_DEKL = 77,
    PRIJEVODNA_JED_I_VANJSKA_DEKL = 78,

    DEFINICIJA_FUNKCIJE = 79,
    DEKLARACIJA = 80,

    FUNKCIJA_BEZ_PARAMETARA = 81,
    FUNKCIJA_S_PARAMETRIMA = 82,

    LISTA_S_JEDNIM_PARAMETROM = 83,
    LISTA_S_VISE_PARAMETARA = 84,

    DEKLARACIJA_OBICNOG_PARAMETRA = 85,
    DEKLARACIJA_PARAMETRA_POLJA = 86,

    DEKL = 87,
    LISTA_DEKL_I_DEKL = 88,

    NAREDBA_DEKLARACIJE = 89,

    INIT_DEKLARATOR = 90,
    LISTA_INIT_DEKLARATORA = 91,

    IZRAVNI_DEKLARATOR = 92,
    IZRAVNI_DEKLARATOR_UZ_INICIJALIZATOR = 93,

    IDN_DEKLARATOR = 94,
    ARRAY_DEKLARATOR = 95,
    DEKLARATOR_FUNKCIJE_BEZ_PARAMETARA = 96,
    DEKLARATOR_FUNKCIJE = 97,

    IZRAZ_PRIDRUZIVANJA_IZ_INICIJALIZATOR = 98,
    LISTA_PRIDRUZIVANJA = 99,

    IZRAZ_PRIDRUZIVANJA_IZ_LISTE = 10,
    IZRAZ_LISTE_PRIDRUZVANJA = 101


class FunctionType:
    def __init__(self, source_type, destination_type):
        self.__source_type = source_type
        self.__destination_type = destination_type

    def get_source_type(self):
        return self.__source_type

    def get_destination_type(self):
        return self.__destination_type

    def __eq__(self, other):
        if isinstance(other, FunctionType):
            return self.__source_type == other.__source_type and self.__destination_type == other.__destination_type

        return False

    def __str__(self):
        if self.__source_type in [PrimitiveType, ArrayType, KeywordEnumeration]:
            source_string = str(self.__source_type.name)
        else:
            source_string = str(self.__source_type)

        if self.__destination_type in [PrimitiveType, ArrayType]:
            destination_string = str(self.__destination_type.name)
        else:
            destination_string = str(self.__destination_type)

        return "Function: " + source_string + " -> " + destination_string


class Params:
    def __init__(self, types):
        self.__types = list()

        for item in types:
            self.__types.append(item)

    def get_types(self):
        return self.__types

    def __iter__(self):
        return self.__types.__iter__()

    def __getitem__(self, item):
        return self.__types.__getitem__(item)

    def __str__(self):
        to_return = "["

        for item in self.__types:
            if item in [PrimitiveType, ArrayType, KeywordEnumeration]:
                to_return += str(item.name) + ", "
            else:
                to_return += str(item) + ", "

        if len(to_return) is not 0:
            to_return = to_return[:-2]

        return to_return + "]"


class KeywordEnumeration(Enum):
    IDN = 0,
    BROJ = 1,
    ZNAK = 2,
    NIZ_ZNAKOVA = 3,
    KR_BREAK = 4,
    KR_CHAR = 5,
    KR_CONST = 6,
    KR_CONTINUE = 7,
    KR_ELSE = 8,
    KR_FOR = 9,
    KR_IF = 10,
    KR_INT = 11,
    KR_RETURN = 12,
    KR_VOID = 13,
    KR_WHILE = 14,
    PLUS = 15,
    OP_INC = 16,
    MINUS = 17,
    OP_DEC = 18,
    OP_PUTA = 19,
    OP_DIJELI = 20,
    OP_MOD = 21,
    OP_PRIDRUZI = 22,
    OP_LT = 23,
    OP_LTE = 24,
    OP_GT = 25,
    OP_GTE = 26,
    OP_EQ = 27,
    OP_NEQ = 28,
    OP_NEG = 29,
    OP_TILDA = 30,
    OP_I = 31,
    OP_ILI = 32,
    OP_BIN_I = 33,
    OP_BIN_ILI = 34,
    OP_BIN_XILI = 35,
    ZAREZ = 36,
    TOCKAZAREZ = 37,
    L_ZAGRADA = 38,
    D_ZAGRADA = 39,
    L_UGL_ZAGRADA = 40,
    D_UGL_ZAGRADA = 41,
    L_VIT_ZAGRADA = 42,
    D_VIT_ZAGRADA = 43

    # --------------------------------


# Gotobvo, provjereno
class Keyword:
    def __init__(self, value_type: KeywordEnumeration, line: int, value: int or str, parent=None):
        self.__type = value_type
        self.__line = line
        self.__parent = parent

        if self.__type is KeywordEnumeration.BROJ and isinstance(value, str):
            self.__value = int(value)
        else:
            self.__value = value

    @staticmethod
    def from_strings(keyword_type: str, line: int, literal: str):
        for name, member in KeywordEnumeration.__members__.items():
            if name == keyword_type:
                return Keyword(member, line, literal)

        return None

    # Getters
    def get_type(self):
        return self.__type

    def get_type_name(self):
        return self.__type.name

    def get_line(self):
        return self.__line

    def get_value(self):
        return self.__value

    def get_parent(self):
        return self.__parent

    def get_count(self):
        if self.__type is KeywordEnumeration.NIZ_ZNAKOVA:
            return count_signs(self.__value)

    def get_info(self):
        return self.__type.name, self.__line, self.__value

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_idn_type(self):
        if self.__type is KeywordEnumeration.IDN:
            hypothetical_entry = self.get_entry(self.__value)

            if hypothetical_entry is not None:
                return hypothetical_entry.get_type()

        return None

    def get_idn_l_flag(self):
        if self.__type is KeywordEnumeration.IDN:
            hypothetical_entry = self.get_entry(self.__value)

            if hypothetical_entry is not None:
                return hypothetical_entry.get_l_flag()

        return None

    def get_error(self):
        return self.__str__()

    # Checking
    def is_valid(self):
        if self.__type is KeywordEnumeration.BROJ:
            if not Global.INT_RANGE[0] <= self.__value <= Global.INT_RANGE[1]:
                raise SemanticException(self.get_error())

        if self.__type is KeywordEnumeration.ZNAK:
            if not znak_valid(self.__value):
                raise SemanticException(self.get_error())

        if self.__type is KeywordEnumeration.IDN:
            if self.__value is None or len(self.__value) is 0:
                raise SemanticException(self.get_error())

        if self.__type is KeywordEnumeration.NIZ_ZNAKOVA:
            if not niz_znakova_valid(self.__value):
                raise SemanticException(self.get_error())

        return True

    def __str__(self):
        return self.__type.name + "(" + str(self.__line) + "," + str(self.__value) + ")"


class SemanticException(Exception):
    pass


# -----------------------------------


# Gotovo, provjereno
class PrimarniIzraz:
    def __init__(self, content=list(), parent=None):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return False

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IDN:
            return self.__content[0].get_idn_type()

        if content_type is OtherType.BROJ:
            return PrimitiveType.INT

        if content_type is OtherType.ZNAK:
            return PrimitiveType.CHAR

        if content_type is OtherType.NIZ_ZNAKOVA:
            return ArrayType.ARRAY_CONST_CHAR

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            return self.__content[1].get_type()

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IDN:
            return self.__content[0].get_idn_l_flag()

        if content_type is (OtherType.BROJ or OtherType.ZNAK or OtherType.NIZ_ZNAKOVA):
            return False

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            return self.__content[1].get_l_flag()

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def get_count(self):
        content_type = self.get_content_type()

        if content_type is OtherType.NIZ_ZNAKOVA:
            return self.__content[0].count()

        return None

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1:
            to_check = self.__content[0]

            if isinstance(to_check, Keyword):
                if to_check.get_type() is KeywordEnumeration.IDN:
                    return OtherType.IDN

                if to_check.get_type() is KeywordEnumeration.BROJ:
                    return OtherType.BROJ

                if to_check.get_type() is KeywordEnumeration.ZNAK:
                    return OtherType.ZNAK

                if to_check.get_type() is KeywordEnumeration.NIZ_ZNAKOVA:
                    return OtherType.NIZ_ZNAKOVA

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.L_ZAGRADA and \
                isinstance(self.__content[1], Izraz) and \
                isinstance(self.__content[2], Keyword) and \
                self.__content[2].get_type() is KeywordEnumeration.D_ZAGRADA:
            return OtherType.IZRAZ_U_ZAGRADAMA

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            raise SemanticException(self.get_error())

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            if not self.__content[1].is_valid():
                raise SemanticException(self.get_error())

        if self.get_entry(self.__content[0].get_value()) is None:
            raise SemanticException(self.get_error())

        return True

    def __str__(self):
        return "<primarni_izraz>"


# Gotovo, provjereno
class PostfiksIzraz:
    def __init__(self, content, parent=None):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.POSTFIKS_INC or content_type is OtherType.POSTFIKS_DEC:
            return PrimitiveType.INT

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE or content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            return self.__content[0].get_type().get_destination_type()

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            return self.__content[0].get_type()

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is (OtherType.POSTFIKS_INC or OtherType.POSTFIKS_DEC or
                            OtherType.POSTFIKS_PRAZNE_ZAGRADE or OtherType.POSTFIKS_PUNE_ZAGRADE):
            return False

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            return self.__content[0].get_type() not in [PrimitiveType.CONST_INT, PrimitiveType.CONST_CHAR]

        return None

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], PrimarniIzraz):
            return OtherType.PRIMARNI_IZRAZ

        if len(self.__content) is 2 and \
                isinstance(self.__content[0], PostfiksIzraz) and \
                isinstance(self.__content[1], Keyword):
            if self.__content[1].get_type() is KeywordEnumeration.OP_INC:
                return OtherType.POSTFIKS_INC

            if self.__content[1].get_type() is KeywordEnumeration.OP_DEC:
                return OtherType.POSTFIKS_DEC

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], PostfiksIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                isinstance(self.__content[2], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.D_ZAGRADA:
            return OtherType.POSTFIKS_PRAZNE_ZAGRADE

        if len(self.__content) is 4 and \
                isinstance(self.__content[0], PostfiksIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[3], Keyword):
            if self.__content[1].get_type() is KeywordEnumeration.L_UGL_ZAGRADA and \
                    isinstance(self.__content[2], Izraz) and \
                    self.__content[3].get_type() is KeywordEnumeration.D_UGL_ZAGRADA:
                return OtherType.POSTFIKS_UGLATE_ZAGRADE

            if self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                    isinstance(self.__content[2], ListaArgumenata) and \
                    self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA:
                return OtherType.POSTFIKS_PUNE_ZAGRADE

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            if self.__content[0].is_valid() and \
                    self.__content[0].get_type is (ArrayType.ARRAY_INT or ArrayType.ARRAY_CHAR or
                                                   ArrayType.ARRAY_CONST_INT or ArrayType.ARRAY_CONST_CHAR) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE:
            if self.__content[0].is_valid() and \
                    self.__content[0].get_type() == FunctionType(PrimitiveType.VOID, self.get_type()):
                return True

        if content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            if not (self.__content[0].is_valid() and self.__content[2].is_valid()):
                raise SemanticException(self.get_error())

            postfix_type = self.__content[0].get_type()

            if not (isinstance(postfix_type, FunctionType) and
                    isinstance(postfix_type.get_source_type(), Params) and
                    postfix_type.get_destination_type() == self.get_type()):
                raise SemanticException(self.get_error())

            param_types = postfix_type.get_source_type().get_types()
            argument_types = self.__content[2].get_types()

            if not len(param_types) == len(argument_types):
                raise SemanticException(self.get_error())

            for i in range(0, len(param_types)):
                if not mutable(argument_types[i], param_types[i]):
                    raise SemanticException(self.get_error())

            return True

        if content_type in [OtherType.POSTFIKS_INC, OtherType.POSTFIKS_DEC]:
            if self.__content[0].is_valid() and \
                    self.__content[0].get_l_flag is True and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<postfiks_izraz>"


# Gotovo, provjereno
class ListaArgumenata:
    def __init__(self, content, parent=None):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_types(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA:
            return [self.__content[0].get_type()]

        if content_type is OtherType.LISTA_ARGUMENATA_UZ_IZRAZ:
            to_return = self.__content[0].get_types()
            to_return.append(self.__content[2].get_type())

            return to_return

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], IzrazPridruzivanja):
            return OtherType.IZRAZ_PRIDRUZIVANJA

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], ListaArgumenata) and \
                isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.ZAREZ and \
                isinstance(self.__content[2], IzrazPridruzivanja):
            return OtherType.LISTA_ARGUMENATA_UZ_IZRAZ

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type == OtherType.IZRAZ_PRIDRUZIVANJA:
            if self.__content[0].is_valid():
                return True

        if content_type == OtherType.LISTA_ARGUMENATA_UZ_IZRAZ:
            if self.__content[0].is_valid() and self.__content[2].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<lista_argumenata>"


# Gotovo, provjereno
class UnarniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            return self.__content[0].get_type()

        if content_type is (OtherType.INC_UNARNI_IZRAZ or OtherType.DEC_UNARNI_IZRAZ or
                            OtherType.UNARNI_OPERATOR_UZ_CAST):
            return PrimitiveType.INT

        return None

    def get_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is (OtherType.INC_UNARNI_IZRAZ or OtherType.DEC_UNARNI_IZRAZ or
                            OtherType.UNARNI_OPERATOR_UZ_CAST):
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 \
                and isinstance(self.__content[0], PostfiksIzraz):
            return OtherType.POSTFIKS_IZRAZ

        if len(self.__content) is 2:
            if isinstance(self.__content[0], Keyword) and isinstance(self.__content[1], UnarniIzraz):
                if self.__content[0].get_type() is KeywordEnumeration.OP_INC:
                    return OtherType.INC_UNARNI_IZRAZ

                if self.__content[0].get_type() is KeywordEnumeration.OP_DEC:
                    return OtherType.DEC_UNARNI_IZRAZ

            if isinstance(self.__content[0], UnarniOperator) and isinstance(self.__content[1], CastIzraz):
                return OtherType.UNARNI_OPERATOR_UZ_CAST

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is (OtherType.DEC_UNARNI_IZRAZ or OtherType.INC_UNARNI_IZRAZ):
            if self.__content[1].is_valid() and \
                    self.__content[1].get_l_flag() is True and \
                    mutable(self.__content[1].get_type(), PrimitiveType.INT):
                return True

        if content_type is OtherType.UNARNI_OPERATOR_UZ_CAST:
            if self.__content[1].is_valid() and mutable(self.__content[1].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<unarni_izraz>"


# Gotovo, provjereno
class UnarniOperator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content[0]) is 1 and isinstance(self.__content[0], Keyword):
            if self.__content[0].get_type() is KeywordEnumeration.PLUS:
                return OtherType.UNARNI_PLUS

            if self.__content[0].get_type() is KeywordEnumeration.MINUS:
                return OtherType.UNARNI_MINUS

            if self.__content[0].get_type() is KeywordEnumeration.OP_TILDA:
                return OtherType.UNARNI_TILDA

            if self.__content[0].get_type() is KeywordEnumeration.OP_NEG:
                return OtherType.UNARNI_NEG

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        if self.get_content_type() is None:
            raise SemanticException(self.get_error())

        return True

    def __str__(self):
        return "<unarni_operator>"


# Gotovo, provjereno
class CastIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.UNARNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.VISESTRUKI_CAST:
            return self.__content[1].get_type()

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.UNARNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.VISESTRUKI_CAST:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], UnarniIzraz):
            return OtherType.UNARNI_IZRAZ

        if len(self.__content) is 4 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.L_ZAGRADA and \
                isinstance(self.__content[1], ImeTipa) and \
                isinstance(self.__content[2], Keyword) and \
                self.__content[2].get_type() is KeywordEnumeration.D_ZAGRADA and \
                isinstance(self.__content[3], CastIzraz):
            return OtherType.VISESTRUKI_CAST

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.UNARNI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.VISESTRUKI_CAST:
            # Dodaj metodu za 3. - ??
            if self.__content[1].is_valid() and \
                    self.__content[3].is_valid() and \
                    mutable(self.__content[3].get_type(), self.__content[1].get_type()):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<cast_izraz>"


# Gotovo, provjereno
class ImeTipa:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type_name(self) -> str or None:
        content_type = self.get_content_type()

        if content_type is OtherType.OBICAN_TIP:
            return self.__content[0].get_content()[0].get_value()

        if content_type is OtherType.KONSTANTAN_TIP:
            return self.__content[0].get_value() + " " + self.__content[1].get_content()[0].get_value()

        return None

    def get_type(self):
        return get_type_from_string(self.get_type_name())

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], SpecifikatorTipa):
                return OtherType.OBICAN_TIP

        if len(self.__content) is 2 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.KR_CONST and \
                isinstance(self.__content, SpecifikatorTipa):
            return OtherType.KONSTANTAN_TIP

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.OBICAN_TIP:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.KONSTANTAN_TIP:
            if self.__content[1].is_valid() and \
                    get_type_from_string(self.__content[1].get_content()[0].get_value()) is not PrimitiveType.VOID:
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<ime_tipa>"


# Gotovo, provjereno
class SpecifikatorTipa:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.VOID_TIP:
            return PrimitiveType.VOID

        if content_type is OtherType.CHAR_TIP:
            return PrimitiveType.CHAR

        if content_type is OtherType.INT_TIP:
            return PrimitiveType.INT

    def get_l_flag(self):
        return False

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], Keyword):
            if self.__content[0].get_type() is KeywordEnumeration.KR_VOID:
                return OtherType.VOID_TIP

            if self.__content[0].get_type() is KeywordEnumeration.KR_CHAR:
                return OtherType.CHAR_TIP

            if self.__content[0].get_type() is KeywordEnumeration.KR_INT:
                return OtherType.INT_TIP

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        if self.get_content_type() is None:
            raise SemanticException(self.get_error())

        if self.__content[0].is_valid():
            return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<specifikator_tipa>"


# Gotovo, provjereno
class MultiplikativniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CAST_IZRAZ:
            return self.__content[0].get_type()

        if content_type is (OtherType.PUTA_IZRAZ or OtherType.DIJELI_IZRAZ or OtherType.MOD_IZRAZ):
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CAST_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is (OtherType.PUTA_IZRAZ or OtherType.DIJELI_IZRAZ or OtherType.MOD_IZRAZ):
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], CastIzraz):
            return OtherType.CAST_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], MultiplikativniIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], CastIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_PUTA:
                return OtherType.PUTA_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.OP_DIJELI:
                return OtherType.DIJELI_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.OP_MOD:
                return OtherType.MOD_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CAST_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is (OtherType.PUTA_IZRAZ or OtherType.DIJELI_IZRAZ or OtherType.MOD_IZRAZ):
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<multiplikativni_izraz>"


# Gotovo, provjereno
class AditivniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.MULTIPLIKATIVNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is (OtherType.PLUS_IZRAZ or OtherType.MINUS_IZRAZ):
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.MULTIPLIKATIVNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is (OtherType.PLUS_IZRAZ or OtherType.MINUS_IZRAZ):
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], MultiplikativniIzraz):
            return OtherType.MULTIPLIKATIVNI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], AditivniIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], MultiplikativniIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.PLUS:
                return OtherType.PLUS_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.MINUS:
                return OtherType.MINUS_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.MULTIPLIKATIVNI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is (OtherType.PLUS_IZRAZ or OtherType.MINUS_IZRAZ):
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<aditivni_izraz>"


# Gotovo, provjereno
class OdnosniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ADITIVNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is (OtherType.GT_IZRAZ or OtherType.LT_IZRAZ or OtherType.GTE_IZRAZ or OtherType.LTE_IZRAZ):
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ADITIVNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is (OtherType.GT_IZRAZ or OtherType.LT_IZRAZ or OtherType.GTE_IZRAZ or OtherType.LTE_IZRAZ):
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], AditivniIzraz):
            return OtherType.ADITIVNI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], OdnosniIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], AditivniIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_GT:
                return OtherType.GT_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.OP_LT:
                return OtherType.LT_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.OP_GTE:
                return OtherType.GTE_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.OP_LTE:
                return OtherType.LTE_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ADITIVNI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is (OtherType.GT_IZRAZ or OtherType.LT_IZRAZ or OtherType.GTE_IZRAZ or OtherType.LTE_IZRAZ):
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<odnosni_izraz>"


# Gotovo, provjereno
class JednakosniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ODNOSNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is (OtherType.EQ_IZRAZ or OtherType.NEQ_IZRAZ):
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ODNOSNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is (OtherType.EQ_IZRAZ or OtherType.NEQ_IZRAZ):
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], OdnosniIzraz):
            return OtherType.ODNOSNI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], JednakosniIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], OdnosniIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_EQ:
                return OtherType.EQ_IZRAZ

            if self.__content[1].get_type() is KeywordEnumeration.OP_NEQ:
                return OtherType.NEQ_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ODNOSNI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is (OtherType.EQ_IZRAZ or OtherType.NEQ_IZRAZ):
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<jednakosni_izraz>"


# Gotovo, provjereno
class BinIIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.JEDNAKOSNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.OP_BIN_I_IZRAZ:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.JEDNAKOSNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.OP_BIN_I_IZRAZ:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], JednakosniIzraz):
            return OtherType.JEDNAKOSNI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], BinIIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], JednakosniIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_BIN_I:
                return OtherType.OP_BIN_I_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.JEDNAKOSNI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.OP_BIN_I_IZRAZ:
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<bin_i_izraz>"


# Gotovo, provjereno
class BinXiliIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_I_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.OP_BIN_XILI_IZRAZ:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_I_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.OP_BIN_XILI_IZRAZ:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], BinIIzraz):
            return OtherType.BIN_I_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], BinXiliIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], BinIIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_BIN_XILI:
                return OtherType.OP_BIN_XILI_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_I_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.OP_BIN_XILI_IZRAZ:
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<bin_xili_izraz>"


# Gotovo, provjereno
class BinIliIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_XILI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.OP_BIN_ILI_IZRAZ:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_XILI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.OP_BIN_ILI_IZRAZ:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], BinXiliIzraz):
            return OtherType.BIN_XILI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], BinIliIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], BinXiliIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_BIN_ILI:
                return OtherType.OP_BIN_ILI_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_XILI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.OP_BIN_ILI_IZRAZ:
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<bin_ili_izraz>"


# Gotovo, provjereno
class LogIIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_ILI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.OP_LOG_I_IZRAZ:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_ILI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.OP_LOG_I_IZRAZ:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], BinIliIzraz):
            return OtherType.BIN_ILI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], LogIIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], BinIliIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_I:
                return OtherType.OP_LOG_I_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_ILI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.OP_LOG_I_IZRAZ:
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<log_i_izraz>"


# Gotovo, provjereno
class LogIliIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_I_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.OP_LOG_ILI_IZRAZ:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_I_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.OP_LOG_ILI_IZRAZ:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], LogIIzraz):
            return OtherType.LOG_I_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], LogIliIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], LogIIzraz):
            if self.__content[1].get_type() is KeywordEnumeration.OP_ILI:
                return OtherType.OP_LOG_ILI_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_I_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.OP_LOG_ILI_IZRAZZ:
            if self.__content[0].is_valid() and \
                    mutable(self.__content[0].get_type(), PrimitiveType.INT) and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<log_ili_izraz>"


# Gotovo, provjereno
class IzrazPridruzivanja:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is (OtherType.LOG_ILI_IZRAZ or OtherType.OP_PRIDRUZI_IZRAZ):
            return self.__content[0].get_type()

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_ILI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.OP_PRIDRUZI_IZRAZ:
            return False

        return None

    def get_niz_znakova(self):
        try_list = self.__content
        new_try_list = list()

        while len(try_list) is not 0:
            for item in try_list:
                if isinstance(item, PrimarniIzraz) and isinstance(item.get_content()[0], Keyword) and item.get_content()[0].count() is not None:
                    return item.get_content()[0]
                else:
                    if isinstance(item, Keyword):
                        if item.get_type() is KeywordEnumeration.NIZ_ZNAKOVA:
                            return item
                        else:
                            continue
                    else:
                        new_try_list.extend(item.get_content())

            try_list = new_try_list

        return None

    def get_count(self):
        niz_znakova = self.get_niz_znakova()

        if niz_znakova is not None:
            return niz_znakova.get_count()

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], LogIliIzraz):
            return OtherType.LOG_ILI_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], PostfiksIzraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], IzrazPridruzivanja):
            if self.__content[1].get_type() is KeywordEnumeration.OP_PRIDRUZI:
                return OtherType.OP_PRIDRUZI_IZRAZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_ILI_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.OP_PRIDRUZI_IZRAZ:
            if self.__content[0].is_valid() and \
                    self.__content[0].get_l_flag() is True and \
                    self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), self.__content[0].get_type()):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<izraz_pridruzivanja>"


# Gotovo, provjereno
class Izraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ:
            return self.__content[2].get_type()

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ:
            return False

        return None

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], IzrazPridruzivanja):
            return OtherType.IZRAZ_PRIDRUZIVANJA_IZ_IZRAZ

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], Izraz) and \
                isinstance(self.__content[1], Keyword) and \
                isinstance(self.__content[2], IzrazPridruzivanja):
            if self.__content[1].get_type() is KeywordEnumeration.ZAREZ:
                return OtherType.IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_IZRAZ:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ:
            if self.__content[0].is_valid() and self.__content[2].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<izraz>"


# Gotovo, provjereno
class SlozenaNaredba:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        self.__entries = dict()

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_table(self):
        return self.__entries

    def get_entry(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        return None

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if name in self.__entries:
            return False

        self.__entries[name] = entry
        return True

    def is_in_loop(self):
        if self.__parent is None:
            return None

        if isinstance(self.__parent, NaredbaPetlje):
            return True

        if isinstance(self.__parent, SlozenaNaredba) or \
                isinstance(self.__parent, ListaNaredbi) or \
                isinstance(self.__parent, Naredba) or \
                isinstance(self.__parent, NaredbaGrananja):
            return self.__parent.is_in_loop()

        return False

    def get_function_type(self):
        if self.__parent is not None:
            if isinstance(self.__parent, SlozenaNaredba) or \
                    isinstance(self.__parent, ListaNaredbi) or \
                    isinstance(self.__parent, Naredba) or \
                    isinstance(self.__parent, NaredbaGrananja) or \
                    isinstance(self.__parent, DefinicijaFunkcije):
                return self.__parent.get_function_type()

        return None

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.L_VIT_ZAGRADA and \
                isinstance(self.__content[1], ListaNaredbi) and \
                isinstance(self.__content[2], Keyword) and \
                self.__content[2].get_type() is KeywordEnumeration.D_VIT_ZAGRADA:
            return OtherType.SLOZ_NAREDBA_LISTA_NAREDBI

        if len(self.__content) is 4 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.L_VIT_ZAGRADA and \
                isinstance(self.__content[1], ListaDeklaracija) and \
                isinstance(self.__content[2], ListaNaredbi) and \
                isinstance(self.__content[3], Keyword) and \
                self.__content[3].get_type() is KeywordEnumeration.D_VIT_ZAGRADA:
            return OtherType.SLOZ_NARED_S_LISTOM_DEKL_I_NAREDBI

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.SLOZ_NAREDBA_S_LISTOM_NAREDBI:
            if self.__content[1].is_valid():
                return True

        if content_type is OtherType.SLOZ_NAREDBA_S_LISTOM_DEKL_I_NAREDBI:
            if self.__content[1].is_valid() and self.__content[2].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<slozena_naredba>"


# Gotovo, provjereno
class ListaNaredbi:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def is_in_loop(self):
        if self.__parent is None:
            return None

        if isinstance(self.__parent, NaredbaPetlje):
            return True

        if isinstance(self.__parent, SlozenaNaredba) or \
                isinstance(self.__parent, ListaNaredbi) or \
                isinstance(self.__parent, Naredba) or \
                isinstance(self.__parent, NaredbaGrananja):
            return self.__parent.is_in_loop()

        return False

    def get_function_type(self):
        if self.__parent is not None:
            if isinstance(self.__parent, SlozenaNaredba) or \
                    isinstance(self.__parent, ListaNaredbi) or \
                    isinstance(self.__parent, Naredba) or \
                    isinstance(self.__parent, NaredbaGrananja) or \
                    isinstance(self.__parent, DefinicijaFunkcije):
                return self.__parent.get_function_type()

        return None

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 and isinstance(self.__content[0], Naredba):
            return OtherType.NAREDBA

        if len(self.__content) is 2 and \
                isinstance(self.__content[0], ListaNaredbi) and \
                isinstance(self.__content[1], Naredba):
            return OtherType.LISTA_NAREDBI

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.NAREDBA:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.LISTA_NAREDBI:
            if self.__content[0].is_valid() and self.__content[1].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<lista_naredbi>"


# Gotovo, provjereno.
class Naredba:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def is_in_loop(self):
        if self.__parent is None:
            return None

        if isinstance(self.__parent, NaredbaPetlje):
            return True

        if isinstance(self.__parent, SlozenaNaredba) or \
                isinstance(self.__parent, ListaNaredbi) or \
                isinstance(self.__parent, Naredba) or \
                isinstance(self.__parent, NaredbaGrananja):
            return self.__parent.is_in_loop()

        return False

    def get_function_type(self):
        if self.__parent is not None:
            if isinstance(self.__parent, SlozenaNaredba) or \
                    isinstance(self.__parent, ListaNaredbi) or \
                    isinstance(self.__parent, Naredba) or \
                    isinstance(self.__parent, NaredbaGrananja) or \
                    isinstance(self.__parent, DefinicijaFunkcije):
                return self.__parent.get_function_type()

        return None

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1:
            if isinstance(self.__content[0], SlozenaNaredba):
                return OtherType.SLOZENA_NAREDBA

            if isinstance(self.__content[0], IzrazNaredba):
                return OtherType.IZRAZ_NAREDBA

            if isinstance(self.__content[0], NaredbaGrananja):
                return OtherType.NAREDBA_GRANANJA

            if isinstance(self.__content[0], NaredbaPetlje):
                return OtherType.NAREDBA_PETLJE

            if isinstance(self.__content[0], NaredbaSkoka):
                return OtherType.NAREDBA_SKOKA

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            raise SemanticException(self.get_error())

        if self.__content[0].is_valid():
            return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<naredba>"


# Gotovo, provjereno
class IzrazNaredba:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.TOCKAZAREZ:
            return PrimitiveType.INT

        if content_type is OtherType.IZRAZ_I_TOCKAZAREZ:
            return self.__content[0].get_type()

        return None

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.TOCKAZAREZ

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], Izraz) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.IZRAZ_I_TOCKAZAREZ

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            raise SemanticException(self.get_error())

        if content_type is OtherType.IZRAZ_I_TOCKAZAREZ:
            if not self.__content[0].is_valid():
                raise SemanticException(self.get_error())

        return True

    def __str__(self):
        return "<izraz_naredba>"


# Gotovo, provjereno
class NaredbaGrananja:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def is_in_loop(self):
        if self.__parent is None:
            return None

        if isinstance(self.__parent, NaredbaPetlje):
            return True

        if isinstance(self.__parent, SlozenaNaredba) or \
                isinstance(self.__parent, ListaNaredbi) or \
                isinstance(self.__parent, Naredba) or \
                isinstance(self.__parent, NaredbaGrananja):
            return self.__parent.is_in_loop()

        return False

    def get_function_type(self):
        if self.__parent is not None:
            if isinstance(self.__parent, SlozenaNaredba) or \
                    isinstance(self.__parent, ListaNaredbi) or \
                    isinstance(self.__parent, Naredba) or \
                    isinstance(self.__parent, NaredbaGrananja) or \
                    isinstance(self.__parent, DefinicijaFunkcije):
                return self.__parent.get_function_type()

        return None

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) > 4:
            if isinstance(self.__content[0], Keyword) and \
                    self.__content[0].get_type() is KeywordEnumeration.KR_IF and \
                    isinstance(self.__content[1], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                    isinstance(self.__content[2], Izraz) and \
                    isinstance(self.__content[3], Keyword) and \
                    self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA and \
                    isinstance(self.__content[4], Naredba):
                if len(self.__content) is 5:
                    return OtherType.IF

                if len(self.__content) is 7 and \
                        isinstance(self.__content[5], Keyword) and \
                        self.__content[5].get_type() is KeywordEnumeration.KR_ELSE and \
                        isinstance(self.__content[6], Naredba):
                    return OtherType.IF_S_ELSEOM

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IF:
            if self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT) and \
                    self.__content[4].is_valid():
                return True

        if content_type is OtherType.IF_S_ELSEOM:
            if self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT) and \
                    self.__content[4].is_valid() and \
                    self.__content[6].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<naredba_grananja>"


# Gotovo, provjereno
class NaredbaPetlje:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 5 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.KR_WHILE and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                isinstance(self.__content[2], Izraz) and \
                isinstance(self.__content[3], Keyword) and \
                self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA and \
                isinstance(self.__content[4], Naredba):
            return OtherType.WHILE

        if len(self.__content) is 6 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.KR_FOR and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                isinstance(self.__content[2], IzrazNaredba) and \
                isinstance(self.__content[3], IzrazNaredba) and \
                isinstance(self.__content[4], Keyword) and \
                self.__content[4].get_type() is KeywordEnumeration.D_ZAGRADA and \
                isinstance(self.__content[5], Naredba):
            return OtherType.FOR_BEZ_INDEKSIRANJA

        if len(self.__content) is 7 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.KR_FOR and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                isinstance(self.__content[2], IzrazNaredba) and \
                isinstance(self.__content[3], IzrazNaredba) and \
                isinstance(self.__content[4], Izraz) and \
                isinstance(self.__content[5], Keyword) and \
                self.__content[5].get_type() is KeywordEnumeration.D_ZAGRADA and \
                isinstance(self.__content[6], Naredba):
            return OtherType.FOR_SA_INDEKSIRANJEM

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.WHILE:
            if self.__content[2].is_valid() and \
                    mutable(self.__content[2].get_type(), PrimitiveType.INT) and \
                    self.__content[4].is_valid():
                return True

        if content_type is OtherType.FOR_BEZ_INDEKSIRANJA:
            if self.__content[2].is_valid() and \
                    self.__content[3].is_valid() and \
                    mutable(self.__content[3].get_type(), PrimitiveType.INT) and \
                    self.__content[5].is_valid():
                return True

        if content_type is OtherType.FOR_SA_INDEKSIRANJEM:
            if self.__content[2].is_valid() and \
                    self.__content[3].is_valid() and \
                    mutable(self.__content[3].get_type(), PrimitiveType.INT) and \
                    self.__content[4].is_valid() and \
                    self.__content[6].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<naredba_petlje>"


# Gotovo, provjereno
class NaredbaSkoka:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def is_in_loop(self):
        if self.__parent is None:
            return None

        if isinstance(self.__parent, NaredbaPetlje):
            return True

        if isinstance(self.__parent, SlozenaNaredba) or \
                isinstance(self.__parent, ListaNaredbi) or \
                isinstance(self.__parent, Naredba) or \
                isinstance(self.__parent, NaredbaGrananja):
            return self.__parent.is_in_loop()

        return False

    def get_function_type(self):
        if self.__parent is not None:
            if isinstance(self.__parent, SlozenaNaredba) or \
                    isinstance(self.__parent, ListaNaredbi) or \
                    isinstance(self.__parent, Naredba) or \
                    isinstance(self.__parent, NaredbaGrananja) or \
                    isinstance(self.__parent, DefinicijaFunkcije):
                return self.__parent.get_function_type()

        return None

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 2 and \
                isinstance(self.__content[0], Keyword) and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.TOCKAZAREZ:
            if self.__content[0].get_type() is (KeywordEnumeration.KR_CONTINUE or KeywordEnumeration.KR_BREAK):
                return OtherType.CONTINUE_OR_BREAK

            if self.__content[0].get_type() is KeywordEnumeration.KR_RETURN:
                return OtherType.RETURN_BEZ_POV_VRIJEDNOSTI

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.KR_RETURN and \
                isinstance(self.__content[1], Izraz) and \
                isinstance(self.__content[2], Keyword) and \
                self.__content[2].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.RETURN_SA_POV_VRIJEDNOSTI

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CONTINUE_OR_BREAK:
            if self.is_in_loop():
                return True

        if content_type is OtherType.RETURN_BEZ_POV_VRIJEDNOSTI:
            in_function_type = self.get_function_type()

            # TODO Možda ipak treba biti params prvi argument???
            if isinstance(in_function_type, FunctionType) and \
                    isinstance(in_function_type.get_destination_type(), PrimitiveType) and \
                    in_function_type.get_destination_type().get_type() is PrimitiveType.VOID:
                return True

        if content_type is OtherType.RETURN_SA_POV_VRIJEDNOSTI:
            in_function_type = self.get_function_type()

            # TODO Možda ipak treba biti params prvi argument???
            if isinstance(in_function_type, FunctionType) and \
                    mutable(self.__content[1].get_type(), in_function_type.get_destination_type()):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<naredba_skoka>"


# Gotovo, provjereno
class PrijevodnaJedinica:
    def __init__(self, content, parent, with_table=False):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__entries = dict()
        self.__has_table = with_table

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_table(self):
        return self.__entries

    def get_entry(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        return None

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__has_table:
            if name in self.__entries:
                return False

            self.__entries[name] = entry
            return True

        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], VanjskaDeklaracija):
            return OtherType.VANJSKA_DEKL

        if len(self.__content) is 2 and \
                isinstance(self.__content[0], PrijevodnaJedinica) and \
                isinstance(self.__content[1], VanjskaDeklaracija):
            return OtherType.PRIJEVODNA_JED_I_VANJSKA_DEKL

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.VANJSKA_DEKL:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.PRIJEVODNA_JED_I_VANJSKA_DEKL:
            if self.__content[0].is_valid() and self.__content[1].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<prijevodna_jedinica>"


# Gotovo, provjereno
class VanjskaDeklaracija:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], DefinicijaFunkcije):
            return OtherType.DEFINICIJA_FUNKCIJE

        if len(self.__content) is 1 and isinstance(self.__content[0], Deklaracija):
            return OtherType.DEKLARACIJA

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            raise SemanticException(self.get_error())
        elif self.__content[0].is_valid():
            return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<vanjska_deklaracija>"


# Gotovo, provjereno
class DefinicijaFunkcije:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_function_type(self):
        content_type = self.get_content_type()

        source_type = None

        if content_type is OtherType.FUNKCIJA_BEZ_PARAMETARA:
            source_type = PrimitiveType.VOID

        if content_type is OtherType.FUNKCIJA_S_PARAMETRIMA:
            types = self.__content[3].get_parameter_types()

            if len(types) is not 1:
                source_type = Params(types)
            else:
                source_type = types[0]

        destination_type = get_type_from_string(self.__content[0].get_type_name())

        return FunctionType(source_type, destination_type)

    def add_to_table(self):
        content = self.__content

        if isinstance(content[0], ImeTipa) and isinstance(content[1], Keyword) and \
                content[1].get_type() is KeywordEnumeration.IDN:
            name = content[1].get_value()
            function_type = self.get_function_type()
            l_flag = False

            self.add_entry(name, TableEntry(function_type, l_flag, True))

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 6:
            if isinstance(self.__content[0], ImeTipa) and \
                    isinstance(self.__content[1], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.IDN and \
                    isinstance(self.__content[2], Keyword) and \
                    self.__content[2].get_type() is KeywordEnumeration.L_ZAGRADA and \
                    isinstance(self.__content[4], Keyword) and \
                    self.__content[4].get_type() is KeywordEnumeration.D_ZAGRADA and \
                    isinstance(self.__content[5], SlozenaNaredba):

                if isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.KR_VOID:
                    return OtherType.FUNKCIJA_BEZ_PARAMETARA

                if isinstance(self.__content[3], ListaParametara):
                    return OtherType.FUNKCIJA_S_PARAMETRIMA

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.FUNKCIJA_BEZ_PARAMETARA:
            if not self.__content[0].is_valid():
                raise SemanticException(self.get_error())

            defined_function_return_type = self.__content[0].get_type()

            if defined_function_return_type is (PrimitiveType.CONST_INT or PrimitiveType.CONST_CHAR):
                raise SemanticException(self.get_error())

            hypothetical_function = self.get_entry(self.__content[1].get_value())

            if hypothetical_function is not None and isinstance(hypothetical_function, TableEntry):
                if hypothetical_function.is_defined():
                    raise SemanticException(self.get_error())

                function_type = hypothetical_function.get_type()

                if not (isinstance(function_type, FunctionType) and
                        function_type == FunctionType(PrimitiveType.VOID, defined_function_return_type)):
                    raise SemanticException(self.get_error())

            self.add_to_table()

            if self.__content[5].is_valid():
                return True

        if content_type is OtherType.FUNKCIJA_S_PARAMETRIMA:
            if not self.__content[0].is_valid():
                raise SemanticException(self.get_error())

            defined_function_return_type = self.__content[0].get_type()

            if defined_function_return_type is (PrimitiveType.CONST_INT or PrimitiveType.CONST_CHAR):
                raise SemanticException(self.get_error())

            hypothetical_function = self.get_entry(self.__content[1].get_value())

            if hypothetical_function is not None and isinstance(hypothetical_function, TableEntry):
                if hypothetical_function.is_defined():
                    raise SemanticException(self.get_error())

                function_type = hypothetical_function.get_type()

                if not (isinstance(function_type, FunctionType) and
                        function_type == FunctionType(Params(self.__content[3].get_types()), defined_function_return_type)):
                        raise SemanticException(self.get_error())

            # TODO Provjera 4 prije provjere 5, mogući problemi!!!
            if not self.__content[3].is_valid():
                raise SemanticException(self.get_error())

            self.add_to_table()

            names_and_types = self.__content[3].get_parameter_names_and_types()

            for name_and_type in names_and_types:
                self.__content[5].add_entry(name_and_type[0], TableEntry(name_and_type[1], True))

            if self.__content[5].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<definicija_funkcije>"


# Gotovo, provjereno
class ListaParametara:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_parameter_names(self):
        to_return = list()

        if self.get_content_type() is OtherType.LISTA_S_VISE_PARAMETARA:
            to_return.extend(self.__content[0].get_parameter_names())
            to_return.append(self.__content[2].get_parameter_name())
        elif self.get_content_type() is OtherType.LISTA_S_JEDNIM_PARAMETROM:
            to_return.append(self.__content[0].get_parameter_name())

        return to_return

    def get_parameter_types(self):
        to_return = list()

        if self.get_content_type() is OtherType.LISTA_S_VISE_PARAMETARA:
            to_return.extend(self.__content[0].get_parameter_types())
            to_return.append(self.__content[2].get_parameter_type())
        elif self.get_content_type() is OtherType.LISTA_S_JEDNIM_PARAMETROM:
            to_return.append(self.__content[0].get_parameter_type())

        return to_return

    def get_parameter_names_and_types(self):
        names = self.get_parameter_names()
        types = self.get_parameter_types()

        to_return = list()

        for i in range(0, len(names)):
            to_return.append((names[i], types[i]))

        return to_return

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1:
            if isinstance(self.__content[0], DeklaracijaParametra):
                return OtherType.LISTA_S_JEDNIM_PARAMETROM

        if len(self.__content) is 3:
            if isinstance(self.__content[0], ListaParametara) and \
                    isinstance(self.__content[1], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.ZAREZ and \
                    isinstance(self.__content[2], DeklaracijaParametra):
                return OtherType.LISTA_S_VISE_PARAMETARA

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LISTA_S_JEDNIM_PARAMETROM:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.LISTA_S_VISE_PARAMETARA:
            if self.__content[0].is_valid() and \
                    self.__content[2].is_valid() and \
                    self.__content[2].get_parameter_name() not in self.__content[0].get_parameter_names():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<lista_parametara>"


# Gotovo, provjereno
class DeklaracijaParametra:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_parameter_name(self):
        if self.get_content_type() is not None:
            return self.__content[1].get_value()

    def get_parameter_type(self):
        if self.get_content_type() is not None:
            type_name = self.__content[0].get_type_name()

            if type_name is not None:
                return get_type_from_string(type_name)

            return None

    def get_parameter_name_and_type(self):
        return self.get_parameter_name(), self.get_parameter_type()

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) > 1 and \
                isinstance(self.__content[0], ImeTipa) and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.IDN:
            if len(self.__content) is 2:
                return OtherType.DEKLARACIJA_OBICNOG_PARAMETRA

            if len(self.__content) is 4:
                if isinstance(self.__content[2], Keyword) and \
                        self.__content[2].get_type() is KeywordEnumeration.L_UGL_ZAGRADA and \
                        isinstance(self.__content[3], Keyword) and \
                        self.__content[3].get_type() is KeywordEnumeration.D_UGL_ZAGRADA:
                    return OtherType.DEKLARACIJA_PARAMETRA_POLJA

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is (OtherType.DEKLARACIJA_CJELOBROJNI_TIP or OtherType.DEKLARACIJA_NIZ):
            if self.__content[0].is_valid() and self.__content[0].get_type() is not PrimitiveType.VOID:
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<deklaracija_parametra>"


# Gotovo, provjereno
class ListaDeklaracija:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], Deklaracija):
            return OtherType.DEKL

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], ListaDeklaracija) \
                and isinstance(self.__content[1], Deklaracija):
            return OtherType.LISTA_DEKL_I_DEKL

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.DEKL:
            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.LISTA_DEKL_I_DEKL:
            if self.__content[0].is_valid() and self.__content[1].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<lista_deklaracija>"


# Gotovo, provjereno
class Deklaracija:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 3 \
                and isinstance(self.__content[0], ImeTipa) \
                and isinstance(self.__content[1], ListaInitDeklaratora) \
                and isinstance(self.__content[2], Keyword) and \
                self.__content[2].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.NAREDBA_DEKLARACIJE

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.NAREDBA_DEKLARACIJE:
            if self.__content[0].is_valid() and self.__content[1].is_valid(self.__content[0].get_type()):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<deklaracija>"


# Gotovo, provjereno
class ListaInitDeklaratora:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], InitDeklarator):
            return OtherType.INIT_DEKLARATOR

        if len(self.__content) is 3 \
                and isinstance(self.__content[0], ListaInitDeklaratora) \
                and isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.ZAREZ \
                and isinstance(self.__content[2], InitDeklarator):
            return OtherType.LISTA_INIT_DEKLARATORA

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self, type_to_check):
        content_type = self.get_content_type()

        if content_type is OtherType.INIT_DEKLARATOR:
            if self.__content[0].is_valid(type_to_check):
                return True

        if content_type is OtherType.LISTA_INIT_DEKLARATORA:
            if self.__content[0].is_valid(type_to_check) and self.__content[2].is_valid(type_to_check):
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<lista_init_deklaratora>"


# Gotovo, provjereno
class InitDeklarator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], IzravniDeklarator):
            return OtherType.IZRAVNI_DEKLARATOR

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], IzravniDeklarator) and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.OP_PRIDRUZI and \
                isinstance(self.__content[2], Inicijalizator):
            return OtherType.IZRAVNI_DEKLARATOR_UZ_INICIJALIZATOR

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self, type_to_check):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAVNI_DEKLARATOR:
            if self.__content[0].is_valid(type_to_check) and \
                    self.__content[0].get_type() is not (PrimitiveType.CONST_INT or PrimitiveType.CONST_CHAR or
                                                         ArrayType.ARRAY_CONST_INT or ArrayType.ARRAY_CONST_CHAR):
                return True

        if content_type is OtherType.IZRAVNI_DEKLARATOR_UZ_INICIJALIZATOR:
            if self.__content[0].is_valid(type_to_check) and self.__content[2].is_valid():
                if self.__content[0].get_type() is (PrimitiveType.INT or PrimitiveType.CHAR or
                                                    PrimitiveType.CONST_INT or PrimitiveType.CONST_CHAR):
                    if self.__content[0].get_type() is PrimitiveType.CONST_INT:
                        if mutable(self.__content[2].get_type(), PrimitiveType.INT):
                            return True

                    if self.__content[0].get_type() is PrimitiveType.CONST_CHAR:
                        if mutable(self.__content[2].get_type(), PrimitiveType.CHAR):
                            return True

                    if mutable(self.__content[2].get_type(), self.__content[0].get_type()):
                        return True
                elif self.__content[0].get_type() is (ArrayType.ARRAY_INT or ArrayType.ARRAY_CHAR or
                                                      ArrayType.ARRAY_CONST_INT or ArrayType.ARRAY_CONST_CHAR):
                    if self.__content[2].get_count() <= self.__content[0].get_count():
                        for init_type in self.__content[2].get_types():
                            if not (mutable(init_type, PrimitiveType.INT) or mutable(init_type, PrimitiveType.CHAR)):
                                raise SemanticException(self.get_error())
                    else:
                        raise SemanticException(self.get_error())
                else:
                    raise SemanticException(self.get_error())

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<init_deklarator>"


# Gotovo, provjereno
class IzravniDeklarator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__type = None
        self.__count = 1

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        return self.__type

    def get_count(self):
        return self.__count

    def get_content_type(self):
        if len(self.__content) is 1 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.IDN:
            return OtherType.IDN_DEKLARATOR

        if len(self.__content) is 4:
            if isinstance(self.__content[0], Keyword) and \
                    self.__content[0].get_type() is KeywordEnumeration.IDN and \
                    isinstance(self.__content[1], Keyword) and \
                    isinstance(self.__content[3], Keyword):
                if self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                        self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA:
                    if isinstance(self.__content[2], Keyword) and \
                            self.__content[2].get_type() is KeywordEnumeration.KR_VOID:
                        return OtherType.DEKLARATOR_FUNKCIJE_BEZ_PARAMETARA

                    if isinstance(self.__content[2], ListaParametara):
                        return OtherType.DEKLARATOR_FUNKCIJE

                if self.__content[1].get_type() is KeywordEnumeration.L_UGL_ZAGRADA and \
                        self.__content[3].get_type() is KeywordEnumeration.D_UGL_ZAGRADA and \
                        isinstance(self.__content[2], Keyword) and \
                        self.__content[2].get_type() is KeywordEnumeration.BROJ:
                    return OtherType.ARRAY_DEKLARATOR

        return None

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def is_valid(self, type_to_check):
        content_type = self.get_content_type()

        if content_type is OtherType.IDN_DEKLARATOR:
            self.__type = type_to_check

            if type_to_check is not PrimitiveType.VOID and \
                    self.get_entry_local(self.__content[0].get_value()) is None:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, True))
                return True

        if content_type is OtherType.ARRAY_DEKLARATOR:
            self.__type = array(type_to_check)
            self.__count = self.__content[2].get_value()

            if type_to_check is not PrimitiveType.VOID and \
                    self.get_entry_local(self.__content[0].get_value()) is None and \
                    0 < self.__content[2].get_value() <= 1024:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, True))
                return True

        if content_type is OtherType.DEKLARATOR_FUNKCIJE_BEZ_PARAMETARA:
            self.__type = FunctionType(PrimitiveType.VOID, type_to_check)

            hypothetical_function = self.get_entry_local(self.__content[0].get_value())

            if hypothetical_function is not None:
                if hypothetical_function.get_type() == self.__type:
                    return True
            else:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, False))
                return True

        if content_type is OtherType.DEKLARATOR_FUNKCIJE:
            self.__type = FunctionType(Params(self.__content[2].get_parameter_types()), type_to_check)

            if self.__content[2].is_valid():
                hypothetical_function = self.get_entry_local(self.__content[0].get_value())

                if hypothetical_function is not None:
                    if hypothetical_function.get_type() == self.__type:
                        return True
                else:
                    self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, False))
                    return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<izravni_deklarator>"


# Gotovo, provjereno
class Inicijalizator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__count = 1
        self.__types = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        if self.__count is 1:
            return self.__types[0]
        else:
            return self.__types

    def get_count(self):
        return self.__count

    def get_types(self):
        return self.__types

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], IzrazPridruzivanja):
            return OtherType.IZRAZ_PRIDRUZIVANJA_IZ_INICIJALIZATOR

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], Keyword) and \
                self.__content[0].get_type() is KeywordEnumeration.L_VIT_ZAGRADA and \
                isinstance(self.__content[1], ListaIzrazaPridruzivanja) and \
                isinstance(self.__content[2], Keyword) and \
                self.__content[2].get_type() is KeywordEnumeration.D_VIT_ZAGRADA:
            return OtherType.LISTA_PRIDRUZIVANJA

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_INICIJALIZATOR:
            count = self.__content[0].get_count()

            if count is not None:
                self.__count = count + 1
                self.__types = list()

                for i in range(0, self.__count):
                    self.__types.append(PrimitiveType.CHAR)
            else:
                self.__types = [self.__content[0].get_type()]

            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.LISTA_PRIDRUZIVANJA:
            self.__count = self.__content[1].get_count()
            self.__types = self.__content[1].get_types()

            if self.__content[1].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<inicijalizator>"


# Gotovo, provjereno.
class ListaIzrazaPridruzivanja:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__count = None
        self.__types = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.__parent is not None:
            parent = parent.__parent

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_count(self):
        return self.__count

    def get_types(self):
        return self.__types

    def get_error(self):
        error = self.__str__() + ' ::= '

        for item in self.__content:
            error += item.__str__() + ' '

        return error[:-1]

    def get_content_type(self):
        if len(self.__content) is 1 and isinstance(self.__content[0], IzrazPridruzivanja):
            return OtherType.IZRAZ_PRIDRUZIVANJA_IZ_LISTE

        if len(self.__content) is 3 and \
                isinstance(self.__content[0], ListaIzrazaPridruzivanja) and \
                isinstance(self.__content[1], Keyword) and \
                self.__content[1].get_type() is KeywordEnumeration.ZAREZ and \
                isinstance(self.__content[2], IzrazPridruzivanja):
            return OtherType.IZRAZ_LISTE_PRIDRUZVANJA

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_LISTE:
            self.__types = [self.__content[0].get_type()]
            self.__count = 1

            if self.__content[0].is_valid():
                return True

        if content_type is OtherType.IZRAZ_LISTE_PRIDRUZVANJA:
            t_types = self.__content[0].get_types()
            t_types.append(self.__content[2].get_type())

            self.__types = t_types
            self.__count = len(self.__types)

            if self.__content[0].is_valid() and self.__content[2].is_valid():
                return True

        raise SemanticException(self.get_error())

    def __str__(self):
        return "<lista_izraza_pridruzivanja>"
