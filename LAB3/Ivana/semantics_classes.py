import LAB3.Global as Global
from enum import Enum


class TableEntry:
    def __init__(self, entry_type, line: int, literal: str):
        if isinstance(entry_type, FunctionType):
            self.__type = PrimitiveType.FUNCTION
            self.__real_type = entry_type
        elif isinstance(entry_type, Params):
            self.__type = PrimitiveType.PARAMS
            self.__real_type = entry_type
        else:
            self.__type = entry_type

        self.__line = line
        self.__literal = literal

    def get_type(self):
        return self.__type

    def get_real_type(self):
        if self.__type is PrimitiveType.FUNCTION or self.__type is PrimitiveType.PARAMS:
            return self.__real_type

        return self.__type

    def get_line(self):
        return self.__line

    def get_literal(self):
        return self.__literal

    def get_info(self):
        return self.__type, self.__line, self.__literal


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

    SLOZ_NAREDBA_LISTA_NAREDBI = 54,
    SLOZ_NARED_S_LISTOM_DEKL_I_NAREDBI = 55,
    NAREDBA = 56,
    LISTA_NAREDBI = 57,
    IZRAZ_NAREDBA = 58,
    NAREDBA_GRANANJA = 59,
    NAREDBA_PETLJE = 60,
    NAREDBA_SKOKA = 61,
    TOCKAZAREZ = 62,
    IZRAZ_I_TOCKAZAREZ = 63,
    IF = 64,
    IF_S_ELSEOM = 65,
    WHILE = 66,
    FOR_BEZ_INDEKSIRANJA = 67,
    FOR_SA_INDEKSIRANJEM = 68,
    CONTINUE_OR_BREAK = 69,
    RETURN_BEZ_POV_VRIJEDNOSTI = 70,
    RETURN_SA_POV_VRIJEDNOSTI = 71,
    VANJSKA_DEKL = 72,
    PRIJEVODNA_JED_I_VANJSKA_DEKL = 73,

    DEFINICIJA_FUNKCIJE = 74,
    DEKLARACIJA = 75,
    DEF_FUNKCIJE_BEZ_PARAM = 76,
    DEF_FUNKCIJE_SA_PARAM = 77,
    DEKLARACIJA_PARAM = 78,
    LISTA_PARAM_I_DEKLARACIJA = 79,
    DEKLARACIJA_CJELOBROJNI_TIP = 80,
    DEKLARACIJA_NIZ = 81,
    DEKL = 82,
    LISTA_DEKL_I_DEKL = 83,
    NAREDBA_DEKLARACIJE = 84,
    INIT_DEKLARATOR = 85,
    LISTA_INIT_DEKLARATORA = 86

class FunctionType:
    def __init__(self, source_type, destination_type):
        self.__source_type = source_type
        self.__destination_type = destination_type

    def __eq__(self, other):
        if isinstance(other, FunctionType):
            return self.__source_type == other.__source_type and self.__destination_type == other.__destination_type

        return False


class Params:
    def __init__(self, content):
        self.__content = list()

        for item in content:
            self.__content.append(item)

    def get_types(self):
        types = list()

        for item in self.__content:
            types.append(item.get_type_and_l_flag()[0])

    def get_l_flags(self):
        l_flags = list()

        for item in self.__content:
            l_flags.append(item.get_type_and_l_flag()[1])

    def __iter__(self):
        return self.__content.__iter__()

    def __getitem__(self, item):
        return self.__content.__getitem__(item)


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


class Keyword:
    def __init__(self, value_type: KeywordEnumeration, line: int, value: int or str):
        self.__type = value_type
        self.__line = line

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

    def get_line(self):
        return self.__line

    def get_value(self):
        return self.__value

    def get_info(self):
        return self.__type.name, self.__line, self.__value

    def get_error(self):
        return self.__type.name + "(" + str(self.__line) + "," + str(self.__value) + ")"

    # Checking
    def is_valid(self):
        if self.__type is KeywordEnumeration.BROJ:
            return Global.INT_RANGE[0] <= self.__value <= Global.INT_RANGE[1]

        if self.__type is KeywordEnumeration.ZNAK:
            return Global.REDUCED_CHAR_RANGE[0] <= self.__value <= Global.REDUCED_CHAR_RANGE[1] or \
                   self.__value in Global.ALLOWED_DOUBLE_SIGNS

        if self.__type is KeywordEnumeration.IDN:
            return self.__value is not None and len(self.__value) is not 0

        if self.__type is KeywordEnumeration.NIZ_ZNAKOVA:
            for char in self.__value:
                if not (Global.REDUCED_CHAR_RANGE[0] <= char <= Global.REDUCED_CHAR_RANGE[1] or
                        char in Global.ALLOWED_DOUBLE_SIGNS):
                    return False

            return True

        return True

    def __str__(self):
        return self.__type.name + " " + str(self.__line) + " " + str(self.__value)


# -----------------------------------


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return False

        return self.__parent.add_entry(name, entry)

    def get_type_and_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].get_type(), self.__content[0].get_l_expression_flag()

        if content_type is OtherType.BROJ:
            return PrimitiveType.INT, False

        if content_type is OtherType.ZNAK:
            return PrimitiveType.CHAR, False

        if content_type is OtherType.NIZ_ZNAKOVA:
            return ArrayType.ARRAY_CONST_CHAR, False

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            return self.__content[1].get_type(), self.__content[1].get_l_expression_flag()

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
            return False

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            return self.__content[1].is_valid()

        return self.__content[0].is_valid()

    def __str__(self):
        return "<primarni_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type_and_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].get_type(), self.__content[0].get_l_expression_flag()

        if content_type is OtherType.POSTFIKS_INC or content_type is OtherType.POSTFIKS_DEC:
            return PrimitiveType.INT, False

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE or content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            return PrimitiveType.POV, False

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            new_type = self.__content[0].get_type_and_l_flag[0]
            return new_type, new_type not in [PrimitiveType.CONST_INT, PrimitiveType.CONST_CHAR]

        return None

    def get_content_type(self) -> OtherType or None:
        if len(self.__content) is 1 and isinstance(self.__content[0], PrimarniIzraz):
            return OtherType.PRIMARNI_IZRAZ

        if len(self.__content) is 2 and isinstance(self.__content[0], PostfiksIzraz):
            if isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.OP_INC:
                return OtherType.POSTFIKS_INC

            if isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.OP_DEC:
                return OtherType.POSTFIKS_DEC

        if len(self.__content) is 3 and isinstance(self.__content[0], PostfiksIzraz):
            if isinstance(self.__content[1], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                    isinstance(self.__content[2], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.D_ZAGRADA:
                return OtherType.POSTFIKS_PRAZNE_ZAGRADE

        if len(self.__content) is 4 and isinstance(self.__content[0], PostfiksIzraz):
            if isinstance(self.__content[1], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.L_UGL_ZAGRADA and \
                    isinstance(self.__content[2], Izraz) and \
                    isinstance(self.__content[3], Keyword) and \
                    self.__content[3].get_type() is KeywordEnumeration.D_UGL_ZAGRADA:
                return OtherType.POSTFIKS_UGLATE_ZAGRADE

            if isinstance(self.__content[1], Keyword) and \
                    self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA and \
                    isinstance(self.__content[2], ListaArgumenata) and \
                    isinstance(self.__content[3], Keyword) and \
                    self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA:
                return OtherType.POSTFIKS_PUNE_ZAGRADE

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].is_valid()

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            if not self.__content[0].is_valid():
                return False

            if self.__content[0].get_type_and_l_flag()[0] not in \
                    [ArrayType.ARRAY_INT, ArrayType.ARRAY_CONST_INT, ArrayType.ARRAY_CHAR, ArrayType.ARRAY_CONST_CHAR]:
                return False

            if not self.__content[2].is_valid():
                return False

            return mutable(self.__content[2].get_type_and_l_flag()[0], PrimitiveType.INT)

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE:
            if not self.__content[0].is_valid():
                return False

            if self.__content[0].get_type_and_l_flag()[0] is not FunctionType(PrimitiveType.VOID, PrimitiveType.POV):
                return False

            return True

        if content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            if not self.__content[0].is_valid():
                return False

            if not self.__content[2].is_valid():
                return False

            postfix_type = self.__content[0].get_type_and_l_flag()[0]
            if postfix_type is not FunctionType(PrimitiveType.PARAMS, PrimitiveType.POV):
                # Trebamo dodati kod s funkcijama
                return False

        if content_type in [OtherType.POSTFIKS_INC, OtherType.POSTFIKS_DEC]:
            if not self.__content[0].is_valid():
                return False

            type_and_l_flag = self.__content[0].get_type_and_l_flag()
            if type_and_l_flag[1] is False or not mutable(type_and_l_flag[0], PrimitiveType.INT):
                return False

        return False

    def __str__(self):
        return "<postfiks_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_types(self):
        types = list()

        for item in self.__content:
            types.append(item.get_type_and_l_flag()[0])

    def __iter__(self):
        return self.__content.__iter__()

    def __getitem__(self, item):
        return self.__content.__getitem__(item)

    def __str__(self):
        return "<lista_argumenata>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<unarni_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<unarni_operator>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<cast_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<ime_tipa>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<specifikator_tipa>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<multiplikativni_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<aditivni_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<odnosni_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<jednakosni_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<bin_i_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<bin_xili_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<bin_ili_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<log_i_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<log_ili_izraz>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<izraz_pridruzivanja>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<izraz>"


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

    def get_entry(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def add_entry(self, name: str, entry: TableEntry):
        if name in self.__entries:
            return False

        self.__entries[name] = entry
        return True


    def get_entry_with_name(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        return None

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 3 \
                    and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.L_VIT_ZAGRADA \
                    and isinstance(self.__content[1], ListaNaredbi) \
                    and isinstance(self.__content[2], Keyword) and self.__content[2].get_type() is KeywordEnumeration.D_VIT_ZAGRADA:
                return OtherType.SLOZ_NAREDBA_LISTA_NAREDBI

        if len(self.__content) is 4 \
                    and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.L_VIT_ZAGRADA \
                    and isinstance(self.__content[1], ListaDeklaracija) \
                    and isinstance(self.__content[2], ListaNaredbi) \
                    and isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.D_VIT_ZAGRADA:
                return OtherType.SLOZ_NARED_S_LISTOM_DEKL_I_NAREDBI

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.SLOZ_NAREDBA_S_LISTOM_NAREDBI:
            return self.__content[1].is_valid()

        if content_type is OtherType.SLOZ_NAREDBA_S_LISTOM_DEKL_I_NAREDBI:
            return self.__content[1].is_valid() and self.__content[2].is_valid()

    def __str__(self):
        return "<slozena_naredba>"





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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], Naredba):
            return OtherType.NAREDBA

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], ListaNaredbi) \
                and isinstance(self.__content[1], Naredba):
            return OtherType.LISTA_NAREDBI

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.NAREDBA:
            return self.__content[0].is_valid()

        if content_type is OtherType.LISTA_NAREDBI:
            return self.__content[0].is_valid() and self.__content[1].is_valid()

    def __str__(self):
        return "<lista_naredbi>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    #TODO (Nezavrsni znak <naredba> generira blokove (<slozena_naredba>))
    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], SlozenaNaredba):
            return OtherType.SLOZENA_NAREDBA

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], IzrazNaredba):
            return OtherType.IZRAZ_NAREDBA

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], NaredbaGrananja):
            return OtherType.NAREDBA_GRANANJA

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], NaredbaPetlje):
            return OtherType.NAREDBA_PETLJE

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], NaredbaSkoka):
            return OtherType.NAREDBA_SKOKA

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        return self.__content[0].is_valid()

    def __str__(self):
        return "<naredba>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.TOCKAZAREZ

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], Izraz) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.IZRAZ_I_TOCKAZAREZ

        return None

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.TOCKAZAREZ:
            return PrimitiveType.INT

        if content_type is OtherType.IZRAZ_I_TOCKAZAREZ:
            return self.__content[0].get_type()

        return  None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.IZRAZ_I_TOCKAZAREZ:
            return self.__content[0].is_valid()

    def __str__(self):
        return "<izraz_naredba>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 5 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_IF \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[2], Izraz) \
                and isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[4], Naredba):
            return OtherType.IF

        if len(self.__content) is 7 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_IF \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[2], Izraz) \
                and isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[4], Naredba) \
                and isinstance(self.__content[5], Keyword) and self.__content[5].get_type() is KeywordEnumeration.KR_ELSE \
                and isinstance(self.__content[6], Naredba):
            return OtherType.IF_S_ELSEOM

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.IF:
            return self.__content[2].is_valid() \
                and mutable(self.__content[2].get_typle_and_l_flag[0], PrimitiveType.INT) \
                and self.__content[4].is_valid()

        if content_type is OtherType.IF_S_ELSEOM:
            return self.__content[2].is_valid() \
                   and mutable(self.__content[2].get_typle_and_l_flag[0], PrimitiveType.INT) \
                   and self.__content[4].is_valid() \
                   and self.__content[6].is_valid()


    def __str__(self):
        return "<naredba_grananja>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 5 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_WHILE \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[2], Izraz) \
                and isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[4], Naredba):
            return OtherType.WHILE

        if len(self.__content) is 6 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_FOR \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[2], IzrazNaredba) \
                and isinstance(self.__content[3], IzrazNaredba) \
                and isinstance(self.__content[4], Keyword) and self.__content[4].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[5], Naredba):
            return OtherType.FOR_BEZ_INDEKSIRANJA

        if len(self.__content) is 7 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_FOR \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[2], IzrazNaredba) \
                and isinstance(self.__content[3], IzrazNaredba) \
                and isinstance(self.__content[4], Izraz) \
                and isinstance(self.__content[5], Keyword)and self.__content[5].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[6], Naredba):
            return OtherType.FOR_SA_INDEKSIRANJEM

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.WHILE:
            return self.__content[2].is_valid() \
                and mutable(self.__content[2].get_type_and_l_flag[0], PrimitiveType.INT) \
                and self.__content[4].is_valid()

        if content_type is OtherType.FOR_BEZ_INDEKSIRANJA:
            return self.__content[2].is_valid() \
                   and self.__content[3].is_valid() \
                   and mutable(self.__content[3].get_type_and_l_flag[0], PrimitiveType.INT) \
                   and self.__content[5].is_valid()

        if content_type is OtherType.FOR_SA_INDEKSIRANJEM:
            return self.__content[2].is_valid() \
                   and self.__content[3].is_valid() \
                   and mutable(self.__content[3].get_type_and_l_flag[0], PrimitiveType.INT) \
                   and self.__content[4].is_valid() \
                   and self.__content[6].is_valid()

    def __str__(self):
        return "<naredba_petlje>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 2 \
                and ((isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_CONTINUE) \
                or   (isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_BREAK)) \
                and   isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.CONTINUE_OR_BREAK

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_RETURN \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.RETURN_BEZ_POV_VRIJEDNOSTI

        if len(self.__content) is 3 \
                and isinstance(self.__content[0], Keyword) and self.__content[0].get_type() is KeywordEnumeration.KR_RETURN \
                and isinstance(self.__content[1], Izraz) \
                and isinstance(self.__content[2], Keyword) and self.__content[2].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.RETURN_SA_POV_VRIJEDNOSTI

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False


    def __str__(self):
        return "<naredba_skoka>"


class PrijevodnaJedinica:
    def __init__(self, content, parent, with_table=False):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__entries = dict()

        if with_table:
            self.__has_table = True

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_entry(self, name: str):
        if name in self.__entries:
            return self.__entries[name]

        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

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

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], VanjskaDeklaracija):
            return OtherType.VANJSKA_DEKL

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], PrijevodnaJedinica) \
                and isinstance(self.__content[1], VanjskaDeklaracija):
            return OtherType.PRIJEVODNA_JED_I_VANJSKA_DEKL

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.VANJSKA_DEKL:
            return self.__content[0].is_valid()

        if content_type is OtherType.PRIJEVODNA_JED_I_VANJSKA_DEKL:
            return self.__content[0].is_valid() \
                   and self.__content[1].is_valid()

    def __str__(self):
        return "<prijevodna_jedinica>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], DefinicijaFunkcije):
            return OtherType.DEFINICIJA_FUNKCIJE

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], Deklaracija):
            return OtherType.DEKLARACIJA

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        return self.__content[0].is_valid()

    def __str__(self):
        return "<vanjska_deklaracija>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 6 \
                and isinstance(self.__content[0], ImeTipa) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.IDN \
                and isinstance(self.__content[2], Keyword) and self.__content[2].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.KR_VOID \
                and isinstance(self.__content[4], Keyword) and self.__content[4].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[5], SlozenaNaredba):
            return OtherType.DEF_FUNKCIJE_BEZ_PARAM

        if len(self.__content) is 6 \
                and isinstance(self.__content[0], ImeTipa) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.IDN \
                and isinstance(self.__content[2], Keyword) and self.__content[2].get_type() is KeywordEnumeration.L_ZAGRADA \
                and isinstance(self.__content[3], ListaParametara) \
                and isinstance(self.__content[4], Keyword) and self.__content[4].get_type() is KeywordEnumeration.D_ZAGRADA \
                and isinstance(self.__content[5], SlozenaNaredba):
            return OtherType.DEF_FUNKCIJE_SA_PARAM

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

    def __str__(self):
        return "<definicija_funkcije>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], DeklaracijaParametra):
            return OtherType.DEKLARACIJA_PARAM

        if len(self.__content) is 3 \
                and isinstance(self.__content[0], ListaParametara) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.ZAREZ \
                and isinstance(self.__content[2], DeklaracijaParametra):
            return OtherType.LISTA_PARAM_I_DEKLARACIJA

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

    def __str__(self):
        return "<lista_parametara>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 2 \
                and  isinstance(self.__content[0], ImeTipa) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.IDN:
            return OtherType.DEKLARACIJA_CJELOBROJNI_TIP

        if len(self.__content) is 4 \
                and isinstance(self.__content[0], ImeTipa) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.IDN \
                and isinstance(self.__content[2], Keyword) and self.__content[2].get_type() is KeywordEnumeration.L_UGL_ZAGRADA \
                and isinstance(self.__content[3], Keyword) and self.__content[3].get_type() is KeywordEnumeration.D_UGL_ZAGRADA:
            return OtherType.DEKLARACIJA_NIZ

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.DEKLARACIJA_CJELOBROJNI_TIP:
            return self.__content[0].is_valid() \
                    and self.__content[0].get_type() is not PrimitiveType.VOID

        if content_type is OtherType.DEKLARACIJA_NIZ:
            return self.__content[0].is_valid() \
                    and self.__content[0].get_type() is not PrimitiveType.VOID

    def __str__(self):
        return "<deklaracija_parametra>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], Deklaracija):
            return OtherType.DEKL

        if len(self.__content) is 2 \
                and isinstance(self.__content[0], ListaDeklaracija) \
                and isinstance(self.__content[1], Deklaracija):
            return OtherType.LISTA_DEKL_I_DEKL

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

        if content_type is OtherType.DEKL:
            return self.__content[0].is_valid()

        if content_type is OtherType.LISTA_DEKL_I_DEKL:
            return self.__content[0].is_valid() \
                   and self.__content[1].is_valid()

    def __str__(self):
        return "<lista_deklaracija>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 3 \
                and isinstance(self.__content[0], ImeTipa) \
                and isinstance(self.__content[1], ListaInitDeklaratora) \
                and isinstance(self.__content[2], Keyword) and self.__content[2].get_type() is KeywordEnumeration.TOCKAZAREZ:
            return OtherType.NAREDBA_DEKLARACIJE

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

    def __str__(self):
        return "<deklaracija>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_content_type(self) -> OtherType or None:

        if len(self.__content) is 1 \
                and isinstance(self.__content[0], InitDeklarator):
            return OtherType.INIT_DEKLARATOR

        if len(self.__content) is 3 \
                and isinstance(self.__content[0], ListaInitDeklaratora) \
                and isinstance(self.__content[1], Keyword) and self.__content[1].get_type() is KeywordEnumeration.ZAREZ \
                and isinstance(self.__content[2], InitDeklarator):
            return OtherType.LISTA_INIT_DEKLARATORA

        return None

    # TODO
    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is None:
            return False

    def __str__(self):
        return "<lista_init_deklaratora>"


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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<init_deklarator>"


class IzravniDeklarator:
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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<izravni_deklarator>"


class Inicijalizator:
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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<inicijalizator>"


class ListaIzrazaPridruzivanja:
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

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def __str__(self):
        return "<lista_izraza_pridruzivanja>"
