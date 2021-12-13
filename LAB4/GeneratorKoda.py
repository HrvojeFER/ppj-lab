from enum import Enum
import sys
import copy

CHAR_RANGE = (0, 255)
REDUCED_CHAR_RANGE = (32, 255)
INT_RANGE = (-2147483648, 2147483647)
ALLOWED_DOUBLE_SIGNS = ['\t', '\n', '\0', '\'', '\"', '\\']

LEVEL_DELIMITER = " "

KEYWORDS = {"IDN", "BROJ", "ZNAK", "NIZ_ZNAKOVA", "KR_BREAK", "KR_CHAR", "KR_CONST", "KR_CONTINUE", "KR_ELSE",
            "KR_FOR", "KR_IF", "KR_INT", "KR_RETURN", "KR_VOID", "KR_WHILE", "PLUS", "OP_INC", "MINUS", "OP_DEC",
            "OP_PUTA", "OP_DIJELI", "OP_MOD", "OP_PRIDRUZI", "OP_LT", "OP_LTE", "OP_GT", "OP_GTE", "OP_EQ", "OP_NEQ",
            "OP_NEG", "OP_TILDA", "OP_I", "OP_ILI", "OP_BIN_I", "OP_BIN_ILI", "OP_BIN_XILI", "ZAREZ", "TOCKAZAREZ",
            "L_ZAGRADA", "D_ZAGRADA", "L_UGL_ZAGRADA", "D_UGL_ZAGRADA", "L_VIT_ZAGRADA", "D_VIT_ZAGRADA"}

test = """<prijevodna_jedinica>
 <prijevodna_jedinica>
  <prijevodna_jedinica>
   <prijevodna_jedinica>
    <vanjska_deklaracija>
     <deklaracija>
      <ime_tipa>
       <specifikator_tipa>
        KR_INT 1 int
      <lista_init_deklaratora>
       <init_deklarator>
        <izravni_deklarator>
         IDN 1 a
         L_ZAGRADA 1 (
         <lista_parametara>
          <deklaracija_parametra>
           <ime_tipa>
            <specifikator_tipa>
             KR_INT 1 int
           IDN 1 c
         D_ZAGRADA 1 )
      TOCKAZAREZ 1 ;
   <vanjska_deklaracija>
    <definicija_funkcije>
     <ime_tipa>
      <specifikator_tipa>
       KR_INT 3 int
     IDN 3 main
     L_ZAGRADA 3 (
     KR_VOID 3 void
     D_ZAGRADA 3 )
     <slozena_naredba>
      L_VIT_ZAGRADA 3 {
      <lista_deklaracija>
       <deklaracija>
        <ime_tipa>
         <specifikator_tipa>
          KR_INT 4 int
        <lista_init_deklaratora>
         <init_deklarator>
          <izravni_deklarator>
           IDN 4 a
           L_ZAGRADA 4 (
           <lista_parametara>
            <deklaracija_parametra>
             <ime_tipa>
              <specifikator_tipa>
               KR_INT 4 int
             IDN 4 c
           D_ZAGRADA 4 )
        TOCKAZAREZ 4 ;
      <lista_naredbi>
       <lista_naredbi>
        <naredba>
         <izraz_naredba>
          <izraz>
           <izraz_pridruzivanja>
            <log_ili_izraz>
             <log_i_izraz>
              <bin_ili_izraz>
               <bin_xili_izraz>
                <bin_i_izraz>
                 <jednakosni_izraz>
                  <odnosni_izraz>
                   <aditivni_izraz>
                    <multiplikativni_izraz>
                     <cast_izraz>
                      <unarni_izraz>
                       <postfiks_izraz>
                        <postfiks_izraz>
                         <primarni_izraz>
                          IDN 5 a
                        L_ZAGRADA 5 (
                        <lista_argumenata>
                         <izraz_pridruzivanja>
                          <log_ili_izraz>
                           <log_i_izraz>
                            <bin_ili_izraz>
                             <bin_xili_izraz>
                              <bin_i_izraz>
                               <jednakosni_izraz>
                                <odnosni_izraz>
                                 <aditivni_izraz>
                                  <multiplikativni_izraz>
                                   <cast_izraz>
                                    <unarni_izraz>
                                     <postfiks_izraz>
                                      <primarni_izraz>
                                       BROJ 5 5
                        D_ZAGRADA 5 )
          TOCKAZAREZ 5 ;
       <naredba>
        <naredba_skoka>
         KR_RETURN 6 return
         <izraz>
          <izraz_pridruzivanja>
           <log_ili_izraz>
            <log_i_izraz>
             <bin_ili_izraz>
              <bin_xili_izraz>
               <bin_i_izraz>
                <jednakosni_izraz>
                 <odnosni_izraz>
                  <aditivni_izraz>
                   <multiplikativni_izraz>
                    <cast_izraz>
                     <unarni_izraz>
                      <postfiks_izraz>
                       <primarni_izraz>
                        BROJ 6 5
         TOCKAZAREZ 6 ;
      D_VIT_ZAGRADA 7 }
  <vanjska_deklaracija>
   <definicija_funkcije>
    <ime_tipa>
     <specifikator_tipa>
      KR_INT 9 int
    IDN 9 a
    L_ZAGRADA 9 (
    <lista_parametara>
     <deklaracija_parametra>
      <ime_tipa>
       <specifikator_tipa>
        KR_INT 9 int
      IDN 9 c
    D_ZAGRADA 9 )
    <slozena_naredba>
     L_VIT_ZAGRADA 9 {
     <lista_naredbi>
      <naredba>
       <naredba_skoka>
        KR_RETURN 10 return
        <izraz>
         <izraz_pridruzivanja>
          <log_ili_izraz>
           <log_i_izraz>
            <bin_ili_izraz>
             <bin_xili_izraz>
              <bin_i_izraz>
               <jednakosni_izraz>
                <odnosni_izraz>
                 <aditivni_izraz>
                  <multiplikativni_izraz>
                   <cast_izraz>
                    <unarni_izraz>
                     <postfiks_izraz>
                      <primarni_izraz>
                       BROJ 10 0
        TOCKAZAREZ 10 ;
     D_VIT_ZAGRADA 11 }
 <vanjska_deklaracija>
  <deklaracija>
   <ime_tipa>
    <specifikator_tipa>
     KR_INT 13 int
   <lista_init_deklaratora>
    <init_deklarator>
     <izravni_deklarator>
      IDN 13 a
      L_ZAGRADA 13 (
      <lista_parametara>
       <deklaracija_parametra>
        <ime_tipa>
         <specifikator_tipa>
          KR_INT 13 int
        IDN 13 f
      D_ZAGRADA 13 )
   TOCKAZAREZ 13 ;"""


def tree_level(string: str) -> int:
    counter = 0

    for character in string:
        if character == LEVEL_DELIMITER:
            counter += 1
        else:
            break

    return counter


def special_split(string: str):
    to_return = list()
    buffer = ""
    is_in_quote = False

    for character in string:
        if not is_in_quote and character is "\n":
            to_return.append(buffer)
            buffer = ""
            continue

        if character is '"':
            is_in_quote = not is_in_quote

        buffer += character

    if len(buffer) is not 0:
        to_return.append(buffer)

    return to_return


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


def castable(cast, original):
    if mutable(original.get_type(), cast.get_type()):
        return True

    if cast.get_type() in [PrimitiveType.INT, PrimitiveType.CONST_INT]:
        return original.get_type() in [PrimitiveType.INT, PrimitiveType.CONST_INT,
                                       PrimitiveType.CHAR, PrimitiveType.CONST_CHAR]

    if cast.get_type() in [PrimitiveType.CHAR, PrimitiveType.CONST_CHAR]:
        if original.get_type() in [PrimitiveType.INT, PrimitiveType.CONST_INT]:
            if CHAR_RANGE[0] <= original.get_value() <= CHAR_RANGE[1]:
                return True

            return False

        if original.get_type() in [PrimitiveType.CONST_CHAR, PrimitiveType.CONST_CHAR]:
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


def unarray(array_type):
    if array_type is ArrayType.ARRAY_INT:
        return PrimitiveType.INT

    if array_type is ArrayType.ARRAY_CHAR:
        return PrimitiveType.CHAR

    if array_type is ArrayType.ARRAY_CONST_INT:
        return PrimitiveType.CONST_INT

    if array_type is ArrayType.ARRAY_CONST_CHAR:
        return PrimitiveType.CONST_CHAR

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
    if char.startswith("'"):
        char = char[1:]

    if char.endswith("'"):
        char = char[:-1]

    if len(char) is 1:
        return CHAR_RANGE[0] <= ord(char) <= CHAR_RANGE[1]
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

    @staticmethod
    def to_base_type(_type):
        if _type is ArrayType.ARRAY_INT:
            return PrimitiveType.INT

        if _type is ArrayType.ARRAY_CONST_INT:
            return PrimitiveType.CONST_INT

        if _type is ArrayType.ARRAY_CHAR:
            return PrimitiveType.CHAR

        if _type is ArrayType.ARRAY_CONST_CHAR:
            return PrimitiveType.CONST_CHAR

        return None


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

    IZRAZ_PRIDRUZIVANJA_IZ_LISTE = 100,
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

    def __len__(self):
        return len(self.__types)

    def __eq__(self, other):
        if isinstance(other, Params):
            if len(other) is len(self):
                for i in range(0, len(self)):
                    if self.__types[i] != other[i]:
                        return False

                return True

        return False


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
    def __init__(self, value_type: KeywordEnumeration, line: int, value: int or str, parent=None):
        self.__type = value_type
        self.__line = line
        self.__parent = parent

        if self.__type is KeywordEnumeration.BROJ and isinstance(value, str):
            self.__value = int(value)
        else:
            self.__value = value

        self.__passing = None

    @staticmethod
    def from_strings(keyword_type: str, line: int, literal: str, parent=None):
        for name, member in KeywordEnumeration.__members__.items():
            if name == keyword_type:
                return Keyword(member, line, literal, parent)

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

    @staticmethod
    def get_idn_value():
        return 0

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
        return True

    def __str__(self):
        return self.__type.name + "(" + str(self.__line) + "," + str(self.__value) + ")"


class TableEntry:
    def __init__(self, entry_type, l_flag: bool, is_defined: bool = False):
        self.__type = entry_type
        self.__l_flag = l_flag
        self.__is_defined = is_defined

    def get_type(self):
        return self.__type

    def get_l_flag(self):
        return self.__l_flag

    def is_defined(self):
        return self.__is_defined

    def define(self):
        self.__is_defined = True

    def __str__(self):
        return "type: " + str(self.__type) + ", l-flag: " + str(self.__l_flag) + ", defined: " + str(self.__is_defined)


class SemanticException(Exception):
    pass


class Command:
    # arithmetic commands
    @staticmethod
    def build_add(src1, src2, dest):
        return "\tADD " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_adc(src1, src2, dest):
        return "\tADC " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_sub(src1, src2, dest):
        return "\tSUB " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_sbc(src1, src2, dest):
        return "\tSBC " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_cmp(src1, src2):
        return "\tCMP " + str(src1) + ", " + str(src2) + "\n"

    @staticmethod
    def build_and(src1, src2, dest):
        return "\tAND " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_or(src1, src2, dest):
        return "\tOR " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_xor(src1, src2, dest):
        return "\tXOR " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_shl(src1, src2, dest):
        return "\tSHL " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_shr(src1, src2, dest):
        return "\tSHR " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_ashr(src1, src2, dest):
        return "\tASHR " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_rotl(src1, src2, dest):
        return "\tROTL " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    @staticmethod
    def build_rotr(src1, src2, dest):
        return "\tROTR " + str(src1) + ", " + str(src2) + ", " + str(dest) + "\n"

    # register commands
    @staticmethod
    def build_move(src, dest):
        return "\tMOVE " + str(src) + ", " + str(dest) + "\n"

    # memory commands
    @staticmethod
    def build_load(dest, adr):
        return "\tLOAD " + str(dest) + ", (" + str(adr) + ")" + "\n"

    @staticmethod
    def build_load_with_size(dest, adr, size):
        return "\tLOAD" + str(size) + " " + str(dest) + ", (" + str(adr) + ")" + "\n"

    @staticmethod
    def build_load_from_register(dest, adrreg, offset):
        return "\tLOAD " + str(dest) + ",  (" + str(adrreg) + "+" + str(offset) + ")" + "\n"

    @staticmethod
    def build_load_from_register_with_size(dest, size, adrreg, offset):
        return "\tLOAD" + str(size) + " " + str(dest) + ", (" + str(adrreg) + "+" + str(offset) + ")" + "\n"

    @staticmethod
    def build_store(dest, adr):
        return "\tSTORE " + str(dest) + ", (" + str(adr) + ")" + "\n"

    @staticmethod
    def build_store_with_size(dest, adr, size):
        return "\tSTORE " + str(size) + " " + str(dest) + ", (" + str(adr) + ")" + "\n"

    @staticmethod
    def build_store_from_register(dest, adrreg, offset):
        return "\tSTORE " + str(dest) + ",  (" + str(adrreg) + "+" + str(offset) + ")" + "\n"

    @staticmethod
    def build_store_from_register_with_size(dest, size, adrreg, offset):
        return "\tSTORE " + str(size) + " " + str(dest) + ", (" + str(adrreg) + "+" + str(offset) + ")" + "\n"

    @staticmethod
    def build_push(src):
        return "\tPUSH " + str(src) + "\n"

    @staticmethod
    def build_pop(dest):
        return "\tPOP " + str(dest) + "\n"

    # control commands
    @staticmethod
    def build_jp(dest):
        return "\tJP " + str(dest) + "\n"

    @staticmethod
    def build_jp_with_condition(condition, dest):
        return "\tJP_" + str(condition) + " " + str(dest) + "\n"

    @staticmethod
    def build_jp_from_register(adrreg):
        return "\tJP (" + str(adrreg) + ")" + "\n"

    @staticmethod
    def build_jp_from_register_with_condition(condition, adrreg):
        return "\tJP_" + str(condition) + " (" + str(adrreg) + ")" + "\n"

    @staticmethod
    def build_jr(offset):
        return "\tJR " + str(offset) + "\n"

    @staticmethod
    def build_jr_with_condition(condition, offset):
        return "\tJR_" + str(condition) + " " + str(offset) + "\n"

    @staticmethod
    def build_call(func):
        return "\tCALL " + str(func) + "\n"

    @staticmethod
    def build_call_with_condition(condition, func):
        return "\tCALL_" + str(condition) + " " + str(func) + "\n"

    @staticmethod
    def build_call_from_register(adrreg):
        return "\tJP (" + str(adrreg) + ")" + "\n"

    @staticmethod
    def build_call_from_register_with_condition(condition, adrreg):
        return "\tJP_" + str(condition) + " (" + str(adrreg) + ")" + "\n"

    @staticmethod
    def build_ret():
        return "\tRET" + "\n"

    @staticmethod
    def build_ret_with_condition(condition):
        return "\tRET_" + str(condition) + "\n"

    @staticmethod
    def build_halt():
        return "\tHALT" + "\n"

    @staticmethod
    def build_halt_with_contition(condition):
        return "\tHALT_" + str(condition) + "\n"

    # pseudo commands
    @staticmethod
    def build_db(value):
        return "\tDB " + str(value) + "\n"

    @staticmethod
    def build_dh(value):
        return "\tDH " + str(value) + "\n"

    @staticmethod
    def build_dw(value):
        return "\tDW " + str(value) + "\n"

    @staticmethod
    def build_dw_from_list(values):
        vals = ""
        for val in values:
            vals += str(val) + ", "

        return "\tDW " + vals[:-2] + "\n"

    # initializer
    @staticmethod
    def build_initializer():
        return "\t`BASE D\n" \
               "\tMOVE %H 40000, R7\n" \
               "\tCALL F_MAIN\n" \
               "\tHALT\n"


class ConstantResolver:
    @staticmethod
    def resolve(member):
        current_member = copy.deepcopy(member)

        while not isinstance(current_member, Keyword) and len(current_member.get_content()) is not 0:
            current_member = current_member.get_content()[0]

        if current_member.get_type() == KeywordEnumeration.NIZ_ZNAKOVA:
            string = current_member.get_value()

            to_return = list()

            for character in string:
                to_return.append(ord(character))

            to_return.append(0)

            return to_return

        if member.get_content_type() is OtherType.LISTA_PRIDRUZIVANJA:
            expression_list = member.get_content()[1]
            head = copy.deepcopy(expression_list)

            to_return = list()
            value_stack = list()

            while head.get_content_type() is OtherType.IZRAZ_LISTE_PRIDRUZVANJA:
                value_stack.append(head.get_content()[2])
                head = head.get_content()[0]

            value_stack.append(head.get_content()[0])

            while len(value_stack) is not 0:
                to_return.append(ConstantResolver.resolve_assign(value_stack.pop()))

            return to_return

        result = ConstantResolver.resolve_assign(member.get_content()[0])

        if isinstance(result, str):
            result = ord(result[0])

        return [result]

    @staticmethod
    def resolve_assign(member):
        if member.get_content_type() is OtherType.OP_PRIDRUZI_IZRAZ:
            return ConstantResolver.resolve_assign(member.get_content_type()[2])

        return ConstantResolver.resolve_log_or(member.get_content()[0])

    @staticmethod
    def resolve_log_or(member):
        if member.get_content_type() is OtherType.LOG_I_IZRAZ:
            return ConstantResolver.resolve_log_and(member.get_content()[0])

        if ConstantResolver.resolve_log_or(member.get_content()[0]) is not 0 or \
                ConstantResolver.resolve_log_and(member.get_content()[2]) is not 0:
            return 1

        return 0

    @staticmethod
    def resolve_log_and(member):
        if member.get_content_type() is OtherType.BIN_ILI_IZRAZ:
            return ConstantResolver.resolve_bin_or(member.get_content()[0])

        if ConstantResolver.resolve_log_and(member.get_content()[0]) is not 0 and \
                ConstantResolver.resolve_bin_or(member.get_content()[2]) is not 0:
            return 1

        return 0

    @staticmethod
    def resolve_bin_or(member):
        if member.get_content_type() is OtherType.BIN_XILI_IZRAZ:
            return ConstantResolver.resolve_bin_xor(member.get_content()[0])

        return ConstantResolver.resolve_bin_or(member.get_content()[0]) | \
               ConstantResolver.resolve_bin_xor(member.get_content()[2])

    @staticmethod
    def resolve_bin_xor(member):
        if member.get_content_type() is OtherType.BIN_I_IZRAZ:
            return ConstantResolver.resolve_bin_and(member.get_content()[0])

        return ConstantResolver.resolve_bin_xor(member.get_content()[0]) ^ \
               ConstantResolver.resolve_bin_and(member.get_content()[2])

    @staticmethod
    def resolve_bin_and(member):
        if member.get_content_type() is OtherType.JEDNAKOSNI_IZRAZ:
            return ConstantResolver.resolve_eq(member.get_content()[0])

        return ConstantResolver.resolve_bin_and(member.get_content()[0]) & \
               ConstantResolver.resolve_eq(member.get_content()[2])

    @staticmethod
    def resolve_eq(member):
        content_type = member.get_content_type()

        if content_type is OtherType.ODNOSNI_IZRAZ:
            return ConstantResolver.resolve_relation(member.get_content()[0])

        first = ConstantResolver.resolve_eq(member.get_content()[0])
        second = ConstantResolver.resolve_relation(member.get_content()[2])

        if content_type is OtherType.EQ_IZRAZ:
            if first == second:
                return 1

            return 0

        if content_type is OtherType.NEQ_IZRAZ:
            if first != second:
                return 1

            return 0

    @staticmethod
    def resolve_relation(member):
        content_type = member.get_content_type()

        if content_type is OtherType.ADITIVNI_IZRAZ:
            return ConstantResolver.resolve_add(member.get_content()[0])

        first = ConstantResolver.resolve_relation(member.get_content()[0])
        second = ConstantResolver.resolve_add(member.get_content()[2])

        if content_type is OtherType.LT_IZRAZ:
            if first < second:
                return 1

            return 0

        if content_type is OtherType.GT_IZRAZ:
            if first > second:
                return 1

            return 0

        if content_type is OtherType.LTE_IZRAZ:
            if first <= second:
                return 1

            return 0

        if content_type is OtherType.GTE_IZRAZ:
            if first >= second:
                return 1

            return 0

    @staticmethod
    def resolve_add(member):
        content_type = member.get_content_type()

        if content_type is OtherType.MULTIPLIKATIVNI_IZRAZ:
            return ConstantResolver.resolve_mul(member.get_content()[0])

        first = ConstantResolver.resolve_add(member.get_content()[0])
        second = ConstantResolver.resolve_mul(member.get_content()[2])

        if content_type is OtherType.PLUS_IZRAZ:
            return first + second

        if content_type is OtherType.MINUS_IZRAZ:
            return first - second

    @staticmethod
    def resolve_mul(member):
        content_type = member.get_content_type()

        if content_type is OtherType.CAST_IZRAZ:
            return ConstantResolver.resolve_cast(member.get_content()[0])

        first = ConstantResolver.resolve_mul(member.get_content()[0])
        second = ConstantResolver.resolve_cast(member.get_constant()[2])

        if content_type is OtherType.PUTA_IZRAZ:
            return first * second

        if content_type is OtherType.DIJELI_IZRAZ:
            return first / second

        if content_type is OtherType.MOD_IZRAZ:
            return first % second

    @staticmethod
    def resolve_cast(member):
        if member.get_content_type() is OtherType.UNARNI_IZRAZ:
            return ConstantResolver.resolve_unary(member.get_content()[0])

        value = ConstantResolver.resolve_cast(member.get_content()[3])
        _type = member.get_content()[1].get_type()

        if _type in [PrimitiveType.CHAR, PrimitiveType.CONST_CHAR]:
            return chr(value)

        return value

    @staticmethod
    def resolve_unary(member):
        content_type = member.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            return ConstantResolver.resolve_postfix(member.get_content()[0])

        value = ConstantResolver.resolve_unary(member.get_content()[1])

        if content_type is OtherType.INC_UNARNI_IZRAZ:
            return value + 1

        if content_type is OtherType.DEC_UNARNI_IZRAZ:
            return value - 1

        if content_type is OtherType.UNARNI_OPERATOR_UZ_CAST:
            content_type = member.get_content()[0].get_content_type()

            if content_type is OtherType.UNARNI_PLUS:
                return value

            if content_type is OtherType.UNARNI_MINUS:
                return -value

            if content_type is OtherType.UNARNI_TILDA:
                return ~value

            if content_type is OtherType.UNARNI_NEG:
                if value is 0:
                    return 1

                return 0

    @staticmethod
    def resolve_postfix(member):
        content_type = member.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return ConstantResolver.resolve_primary(member.get_content()[0])

        # Ne inkrementira vrijednosti thou haha
        if content_type in [OtherType.POSTFIKS_INC, OtherType.POSTFIKS_DEC]:
            return ConstantResolver.resolve_postfix(member.get_content()[0])

        return 0

    @staticmethod
    def resolve_primary(member):
        content_type = member.get_content_type()

        if content_type in [OtherType.BROJ, OtherType.ZNAK]:
            return member.get_content()[0].get_value()

        # Ne da mi se implementirati sve ovo lul
        return 0


class Stack:
    stack = list()
    start = False

    @staticmethod
    def set_start():
        Stack.start = True

    @staticmethod
    def is_local(name: str):
        for element in Stack.stack:
            if name == element[0]:
                return True

        return False

    @staticmethod
    def clear_current_scope():
        presumed_scope = False

        for element in Stack.stack:
            if element[2]:
                presumed_scope = True
                break

        i = len(Stack.stack) - 1
        end_it = False
        while i >= 0 and presumed_scope:
            if Stack.stack[i][2]:
                end_it = True

            Stack.stack.pop()
            FRISC.push_command(Command.build_pop("R0"))

            if end_it:
                break
            else:
                i -= 1

    @staticmethod
    def push(name: str or None = None, _type=None):
        if name is not None and _type is not None:
            Stack.stack.append((name, _type, Stack.start))

            Stack.start = False
        else:
            Stack.stack.append((None, None, False))

    @staticmethod
    def pop():
        return Stack.stack.pop()

    @staticmethod
    def get_type_of(name: str):
        i = len(Stack.stack) - 1

        while i >= 0:
            if name == Stack.stack[i][0]:
                return Stack.stack[i][1]

            i -= 1

        return None

    @staticmethod
    def offset(name: str):
        to_return = 0

        i = len(Stack.stack) - 1
        while i >= 0:
            if name == Stack.stack[i][0]:
                break

            to_return += 1

            i -= 1

        return to_return * 4


class FRISC:
    program = list()
    globals = list()

    loop_num = 0
    loops = list()

    if_num = 0
    ifs = list()

    @staticmethod
    def push_command(command: str):
        FRISC.program.append(command)

    @staticmethod
    def push_command_with_label(label: str, command: str):
        FRISC.program.append(label + "\t" + command)

    @staticmethod
    def generate_broj(num):
        FRISC.program.append(Command.build_move(num, "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_znak(char):
        FRISC.program.append(Command.build_move(ord(char), "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_niz_znakova(string):
        to_write = list()

        for char in string:
            to_write.append(Command.build_move(ord(char), "R0"))
            to_write.append(Command.build_push("R0"))

        FRISC.program.append(Command.build_move(0, "R0"))
        FRISC.program.append(Command.build_push("R0"))

        FRISC.program.extend(to_write)

    @staticmethod
    def generate_idn_get(adr):
        FRISC.program.append(Command.build_load("R0", adr))
        FRISC.program.append(Command.build_push("R0"))

    # todo nakon mul
    @staticmethod
    def generate_niz_get(adr):
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_move(adr, "R1"))
        FRISC.program.append(Command.build_add("R0", "R1", "R0"))
        FRISC.program.append(Command.build_load_from_register("R0", "R0", 0))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def save_context():
        FRISC.program.append(Command.build_push("R5"))
        FRISC.program.append(Command.build_push("R4"))
        FRISC.program.append(Command.build_push("R3"))
        FRISC.program.append(Command.build_push("R2"))
        FRISC.program.append(Command.build_push("R1"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def load_context():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_pop("R2"))
        FRISC.program.append(Command.build_pop("R3"))
        FRISC.program.append(Command.build_pop("R4"))
        FRISC.program.append(Command.build_pop("R5"))

    @staticmethod
    def generate_post_inc_adr(adr):
        FRISC.program.append(Command.build_load("R0", adr))
        FRISC.program.append(Command.build_push("R0"))
        FRISC.program.append(Command.build_add("R0", 1, "R0"))
        FRISC.program.append(Command.build_store("R0", adr))

    @staticmethod
    def generate_post_dec_adr(adr):
        FRISC.program.append(Command.build_load("R0", adr))
        FRISC.program.append(Command.build_push("R0"))
        FRISC.program.append(Command.build_sub("R0", 1, "R0"))
        FRISC.program.append(Command.build_store("R0", adr))

    @staticmethod
    def generate_pre_inc_adr(adr):
        FRISC.program.append(Command.build_load("R0", adr))
        FRISC.program.append(Command.build_add("R0", 1, "R0"))
        FRISC.program.append(Command.build_push("R0"))
        FRISC.program.append(Command.build_store("R0", adr))

    @staticmethod
    def generate_pre_dec_adr(adr):
        FRISC.program.append(Command.build_load("R0", adr))
        FRISC.program.append(Command.build_sub("R0", 1, "R0"))
        FRISC.program.append(Command.build_push("R0"))
        FRISC.program.append(Command.build_store("R0", adr))

    @staticmethod
    def generate_post_inc():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_load("R1", "R0"))
        FRISC.program.append(Command.build_push("R1"))
        FRISC.program.append(Command.build_add("R1", 1, "R1"))
        FRISC.program.append(Command.build_store("R1", "R0"))

    @staticmethod
    def generate_post_dec():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_load("R1", "R0"))
        FRISC.program.append(Command.build_push("R1"))
        FRISC.program.append(Command.build_sub("R1", 1, "R1"))
        FRISC.program.append(Command.build_store("R1", "R0"))

    @staticmethod
    def generate_pre_inc():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_load("R1", "R0"))
        FRISC.program.append(Command.build_add("R1", 1, "R1"))
        FRISC.program.append(Command.build_store("R1", "R0"))
        FRISC.program.append(Command.build_push("R1"))

    @staticmethod
    def generate_pre_dec():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_load("R1", "R0"))
        FRISC.program.append(Command.build_sub("R1", 1, "R1"))
        FRISC.program.append(Command.build_store("R1", "R0"))
        FRISC.program.append(Command.build_push("R1"))

    @staticmethod
    def generate_u_minus():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_move(0, "R1"))
        FRISC.program.append(Command.build_sub("R1", "R0", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_u_tilda():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_move(0, "R1"))
        FRISC.program.append(Command.build_sub("R1", 1, "R1"))
        FRISC.program.append(Command.build_xor("R0", "R1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_u_neg():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_cmp("R0", 0))
        FRISC.program.append(Command.build_jr_with_condition("Z", 8))
        FRISC.program.append(Command.build_move(0, "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move(1, "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_add():
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_add("R0", "R1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_sub():
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_sub("R0", "R1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_gt():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_cmp("R0", "R1"))
        FRISC.program.append(Command.build_jr_with_condition("SGT", 8))
        FRISC.program.append(Command.build_move("0", "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move("1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_lt():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_cmp("R0", "R1"))
        FRISC.program.append(Command.build_jr_with_condition("SLT", 8))
        FRISC.program.append(Command.build_move("0", "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move("1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_gte():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_cmp("R0", "R1"))
        FRISC.program.append(Command.build_jr_with_condition("SGE", 8))
        FRISC.program.append(Command.build_move("0", "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move("1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_lte():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_cmp("R0", "R1"))
        FRISC.program.append(Command.build_jr_with_condition("SLE", 8))
        FRISC.program.append(Command.build_move("0", "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move("1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_eq():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_cmp("R0", "R1"))
        FRISC.program.append(Command.build_jr_with_condition("EQ", 8))
        FRISC.program.append(Command.build_move("0", "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move("1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_neq():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_cmp("R0", "R1"))
        FRISC.program.append(Command.build_jr_with_condition("NE", 8))
        FRISC.program.append(Command.build_move("0", "R0"))
        FRISC.program.append(Command.build_jr(4))
        FRISC.program.append(Command.build_move("1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_bin_and():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_and("R0", "R1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_bin_xor():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_xor("R0", "R1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_bin_or():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_or("R0", "R1", "R0"))
        FRISC.program.append(Command.build_push("R0"))

    @staticmethod
    def generate_bin_eq():
        FRISC.push_command(Command.build_cmp("R0", "R1"))
        FRISC.set_eq_flag()

    @staticmethod
    def generate_bin_ne():
        FRISC.push_command(Command.build_cmp("R0", "R1"))
        FRISC.set_eq_flag()
        FRISC.push_command(Command.build_xor("R0", 1, "R0"))

    @staticmethod
    def generate_log_and():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_move("R2", "0"))
        FRISC.program.append(Command.build_cmp("R0", "0"))
        FRISC.program.append(Command.build_jr_with_condition("Z", 16))
        FRISC.program.append(Command.build_move("R2", "1"))
        FRISC.program.append(Command.build_cmp("R1", "0"))
        FRISC.program.append(Command.build_jr_with_condition("Z", 4))
        FRISC.program.append(Command.build_move("R2", "1"))
        FRISC.program.append(Command.build_push("R2"))

    @staticmethod
    def generate_log_or():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))
        FRISC.program.append(Command.build_move("R2", "1"))
        FRISC.program.append(Command.build_cmp("R0", "0"))
        FRISC.program.append(Command.build_jr_with_condition("NZ", 16))
        FRISC.program.append(Command.build_move("R2", "0"))
        FRISC.program.append(Command.build_cmp("R1", "0"))
        FRISC.program.append(Command.build_jr_with_condition("NZ", 4))
        FRISC.program.append(Command.build_move("R2", "0"))
        FRISC.program.append(Command.build_push("R2"))

    @staticmethod
    def generate_log_not():
        FRISC.push_command(Command.build_pop("R0"))
        FRISC.push_command(Command.build_and("R0", "R0", "R0"))
        FRISC.set_eq_flag()
        FRISC.push_command(Command.build_xor("R0", 1, "R0"))
        FRISC.push_command(Command.build_push("R0"))

    @staticmethod
    def generate_bit_not():
        FRISC.push_command(Command.build_pop("R0"))
        FRISC.push_command(Command.build_xor("R0", -1, "R0"))

    @staticmethod
    def generate_return():
        FRISC.program.append(Command.build_pop("R6"))

    @staticmethod
    def generate_helpers():
        FRISC.generate_mul()
        FRISC.generate_div()
        FRISC.generate_mod()

    @staticmethod
    def generate_mul():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_pop("R1"))

        FRISC.program.append(Command.build_rotl("R0", 1, "R0"))
        FRISC.program.append(Command.build_rotr("R0", 1, "R0"))
        FRISC.program.append(Command.build_jp_with_condition("NC", "MUL_N_FIRST"))

        FRISC.program.append(Command.build_rotl("R1", 1, "R1"))
        FRISC.program.append(Command.build_rotr("R1", 1, "R1"))
        FRISC.program.append(Command.build_jp_with_condition("C", "MUL_SECOND_T"))

        FRISC.program.append(Command.build_move(0, "R2"))
        FRISC.program.append("MUL_1\t" + Command.build_add("R0", "R2", "R2"))
        FRISC.program.append(Command.build_sub("R1", 1, "R1"))
        FRISC.program.append(Command.build_jp_with_condition("NZ", "MUL_1"))
        FRISC.program.append(Command.build_jp("MUL_DONE"))

        FRISC.program.append("MUL_N_FIRST\t" + Command.build_rotl("R1", 1, "R1"))
        FRISC.program.append(Command.build_rotr("R1", 1, "R1"))
        FRISC.program.append(Command.build_jp_with_condition("NC", "MUL_NONE"))

        FRISC.program.append(Command.build_move(0, "R2"))
        FRISC.program.append("MUL_2\t" + Command.build_add("R1", "R2", "R2"))
        FRISC.program.append(Command.build_sub("R0", 1, "R0"))
        FRISC.program.append(Command.build_jp_with_condition("NZ", "MUL_2"))
        FRISC.program.append(Command.build_jp("MUL_DONE"))

        FRISC.program.append("MUL_SECOND_T\t" + Command.build_xor("R0", -1, "R0"))
        FRISC.program.append(Command.build_xor("R1", -1, "R1"))
        FRISC.program.append(Command.build_add("R0", 1, "R0"))
        FRISC.program.append(Command.build_add("R1", 1, "R1"))

        FRISC.program.append("MUL_NONE\t" + Command.build_move(0, "R2"))
        FRISC.program.append("MUL_3\t" + Command.build_add("R0", "R2", "R2"))
        FRISC.program.append(Command.build_sub("R1", 1, "R1"))
        FRISC.program.append(Command.build_jp_with_condition("NZ", "MUL_3"))

        FRISC.program.append("MUL_DONE\t" + Command.build_push("R2"))

    @staticmethod
    def generate_div():
        FRISC.push_command(Command.build_pop("R1"))
        FRISC.push_command(Command.build_pop("R0"))

        FRISC.program.append(Command.build_rotl("R0", 1, "R0"))
        FRISC.program.append(Command.build_rotr("R0", 1, "R0"))
        FRISC.program.append(Command.build_jp_with_condition("NC", "DIV_N_FIRST"))

        FRISC.program.append(Command.build_rotl("R1", 1, "R1"))
        FRISC.program.append(Command.build_rotr("R1", 1, "R1"))
        FRISC.program.append(Command.build_jp_with_condition("C", "DIV_SECOND_T"))

        FRISC.program.append(Command.build_move(0, "R2"))
        FRISC.program.append("DIV_1\t" + Command.build_add("R2", "1", "R2"))
        FRISC.program.append(Command.build_add("R0", "R1", "R2"))
        FRISC.program.append(Command.build_jp_with_condition("N", "DIV_1"))
        FRISC.program.append(Command.build_jp_with_condition("NZ", "DIV_DONE"))
        FRISC.program.append(Command.build_jp("ADJUST_DIV"))

        FRISC.program.append("DIV_N_FIRST\t" + Command.build_rotl("R1", 1, "R1"))
        FRISC.program.append(Command.build_rotr("R1", 1, "R1"))
        FRISC.program.append(Command.build_jp_with_condition("NC", "DIV_NONE"))

        FRISC.program.append("DIV_SECOND_T\t" + Command.build_xor("R0", -1, "R0"))
        FRISC.program.append(Command.build_xor("R1", -1, "R1"))
        FRISC.program.append(Command.build_add("R0", 1, "R0"))
        FRISC.program.append(Command.build_add("R1", 1, "R1"))

        FRISC.program.append(Command.build_move(0, "R2"))
        FRISC.program.append("DIV_2\t" + Command.build_add("R2", 1, "R2"))
        FRISC.program.append(Command.build_add("R0", "R1", "R0"))
        FRISC.program.append(Command.build_jp_with_condition("N", "DIV_2"))
        FRISC.program.append(Command.build_jp_with_condition("Z", "DIV_DONE"))
        FRISC.program.append(Command.build_jp("ADJUST_DIV"))

        FRISC.program.append("MUL_SECOND_T\t" + Command.build_xor("R0", -1, "R0"))
        FRISC.program.append(Command.build_xor("R1", -1, "R1"))
        FRISC.program.append(Command.build_add("R0", 1, "R0"))
        FRISC.program.append(Command.build_add("R1", 1, "R1"))

        FRISC.program.append("DIV_NONE\t" + Command.build_move(0, "R2"))
        FRISC.program.append("DIV_3\t" + Command.build_add("R2", 1, "R2"))
        FRISC.program.append("DIV_3\t" + Command.build_sub("R0", "R1", "R0"))
        FRISC.program.append(Command.build_jp_with_condition("P", "DIV_3"))
        FRISC.program.append(Command.build_jp_with_condition("Z", "DONE"))

        FRISC.program.append("ADJUST_DIV\t" + Command.build_sub("R2", 1, "R2"))
        FRISC.program.append("DIV_DONE\t" + Command.build_push("R2"))

    # TODO
    @staticmethod
    def generate_mod():
        pass

    @staticmethod
    def generate_global_label(name: str):
        return "G_" + name.upper()

    @staticmethod
    def generate_function_label(name: str):
        return "F_" + name.upper()

    @staticmethod
    def generate_function_call(name: str, _type):
        FRISC.push_command(Command.build_call(FRISC.generate_function_label(name)))

        if _type is not PrimitiveType.VOID:
            FRISC.push_command(Command.build_push("R6"))
            Stack.push()

    @staticmethod
    def generate_identifier(name: str):
        if Stack.is_local(name):
            _type = Stack.get_type_of(name)

            if _type is None:
                FRISC.push_command(Command.build_move(FRISC.generate_function_label(name), "R0"))
            else:
                FRISC.push_command(Command.build_load_from_register("R0", "SP", Stack.offset(name)))
        else:
            FRISC.push_command(Command.build_load("R0", FRISC.generate_global_label(name)))

        FRISC.push_command(Command.build_push("R0"))

    @staticmethod
    def define_global(name: str, command: str):
        FRISC.globals.append((FRISC.generate_global_label(name), command))

    @staticmethod
    def enter_loop():
        FRISC.loop_num = FRISC.loop_num + 1
        FRISC.loops.append(FRISC.loop_num)

        return FRISC.loop_num

    @staticmethod
    def leave_loop():
        loop = FRISC.loops[-1]
        FRISC.loops = FRISC.loops[:-1]

        return loop

    @staticmethod
    def current_loop():
        return FRISC.loops[-1]

    @staticmethod
    def enter_if():
        FRISC.if_num += 1
        FRISC.ifs.append(FRISC.if_num)

        return FRISC.if_num

    @staticmethod
    def leave_if():
        iff = FRISC.ifs[-1]
        FRISC.loops = FRISC.ifs[:-1]

        return iff

    @staticmethod
    def current_if():
        return FRISC.ifs[-1]

    @staticmethod
    def generate_continue():
        FRISC.program.append(Command.build_jp("LOOP_START_" + str(FRISC.current_loop())))

    @staticmethod
    def generate_break():
        FRISC.program.append(Command.build_jp("LOOP_END_" + str(FRISC.current_loop())))

    @staticmethod
    def generate_ret():
        FRISC.program.append(Command.build_ret())

    @staticmethod
    def generate_ret_with_value():
        FRISC.program.append(Command.build_pop("R6"))
        FRISC.generate_ret()

    @staticmethod
    def generate_loop_start():
        FRISC.program.append("LOOP_START_" + str(FRISC.enter_loop()))

    @staticmethod
    def generate_loop_end():
        FRISC.program.append("LOOP_END_" + str(FRISC.leave_loop()) + "\n")

    @staticmethod
    def generate_if_end():
        FRISC.program.append("IF_END_" + str(FRISC.leave_if()) + "\n")

    @staticmethod
    def generate_else_end():
        FRISC.program.append("ELSE_END_" + str(FRISC.leave_if()) + "\n")

    @staticmethod
    def generate_if_condition():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_cmp("R0", 0))
        FRISC.program.append(Command.build_jp_with_condition("Z", "IF_END_" + str(FRISC.enter_if())))

    @staticmethod
    def generate_loop_condition():
        FRISC.program.append(Command.build_pop("R0"))
        FRISC.program.append(Command.build_cmp("R0", 0))
        FRISC.program.append(Command.build_jp_with_condition("Z", "LOOP_END_" + str(FRISC.current_loop())))

    @staticmethod
    def set_eq_flag():
        FRISC.push_command(Command.build_move("SR", "R0"))
        FRISC.push_command(Command.build_shr("R0", 3, "R0"))
        FRISC.push_command(Command.build_and("R0", 1, "R0"))

    # -----------------------------------


# Gotovo
class PrimarniIzraz:
    def __init__(self, content=None, parent=None):
        self.__content = list()
        self.__parent = parent

        if content is not None:
            for item in content:
                self.__content.append(item)

        self.__passing = None

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

    def get_value(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IDN:
            return self.__content[0].get_idn_value()

        if content_type in [OtherType.BROJ, OtherType.ZNAK, OtherType.NIZ_ZNAKOVA]:
            return self.__content[0].get_value()

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            return 0

        return None

    def get_name(self):
        if self.get_content_type() is OtherType.IDN:
            return self.__content[0].get_value()

        return None

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

        if content_type in [OtherType.BROJ, OtherType.ZNAK, OtherType.NIZ_ZNAKOVA]:
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
            return self.__content[0].get_count()

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
            raise SemanticException("Pitoni gang did an oopsie!")

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            self.__content[1].is_valid()

        if content_type in [OtherType.BROJ, OtherType.ZNAK, OtherType.NIZ_ZNAKOVA]:
            self.__content[0].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IDN:
            name = self.__content[0].get_value()
            _type = self.get_entry(name).get_type()

            if isinstance(_type, FunctionType):
                FRISC.generate_function_call(name, _type)
            else:
                FRISC.generate_identifier(name)

        # ISPOD DODAO
        if content_type is OtherType.BROJ:
            value = int(self.__content[0].get_value())
            if value > 1<<20:
                label = "BIG_INT_" + str(len(FRISC.globals))
                FRISC.globals.append((label, Command.build_dw(value)))

                FRISC.push_command(Command.build_load("R0", label))
                FRISC.push_command(Command.build_push("R0"))
                Stack.push(str(value), PrimitiveType.INT)
            else:
                FRISC.generate_broj(value)
                Stack.push(str(value), PrimitiveType.INT)

        if content_type is OtherType.ZNAK:
            value = str(self.__content[0].get_value())[0]
            FRISC.generate_znak(value)
            Stack.push(str(value), PrimitiveType.CHAR)

        if content_type is OtherType.NIZ_ZNAKOVA:
            value = self.__content[0].get_value()
            FRISC.generate_niz_znakova(self.__content[0].get_value())
            Stack.push(value, KeywordEnumeration.NIZ_ZNAKOVA)

        if content_type is OtherType.IZRAZ_U_ZAGRADAMA:
            self.__content[1].generate()

    def __str__(self):
        return "<primarni_izraz>"


# Gotovo, eventualno get name u generate može zezat.
class PostfiksIzraz:
    def __init__(self, content, parent=None):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

    def get_value(self):
        content_type = self.get_content_type()

        if content_type is not None:
            return self.__content[0].get_value()

        return None

    def get_name(self):
        content_type = self.get_content_type()
        name = None

        if content_type is OtherType.PRIMARNI_IZRAZ:
            name = self.__content[0].get_name()

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            name = self.__content[0].get_name()

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE:
            name = self.__content[0].get_name()

        if content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            name = self.__content[0].get_name()

        if content_type in [OtherType.POSTFIKS_INC, OtherType.POSTFIKS_DEC]:
            name = self.__content[0].get_name()

        return name

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].get_type()

        if content_type is OtherType.POSTFIKS_INC or content_type is OtherType.POSTFIKS_DEC:
            return PrimitiveType.INT

        if content_type in [OtherType.POSTFIKS_PRAZNE_ZAGRADE, OtherType.POSTFIKS_PUNE_ZAGRADE]:
            return self.__content[0].get_type().get_destination_type()

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            return unarray(self.__content[0].get_type())

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type in [OtherType.POSTFIKS_INC, OtherType.POSTFIKS_DEC,
                            OtherType.POSTFIKS_PRAZNE_ZAGRADE, OtherType.POSTFIKS_PUNE_ZAGRADE]:
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
                self.__content[2].get_type() is KeywordEnumeration.D_ZAGRADA:
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
            self.__content[0].is_valid()

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE:
            self.__content[0].is_valid()

        if content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        if content_type in [OtherType.POSTFIKS_INC, OtherType.POSTFIKS_DEC]:
            self.__content[0].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.PRIMARNI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
            # vidi jel oke
            name = self.__content[0].get_name()
            self.__content[2].generate()

            FRISC.push_command(Command.build_pop("R1"))
            FRISC.push_command(Command.build_add("R1", "R1", "R1"))
            FRISC.push_command(Command.build_add("R1", "R1", "R1"))

            if Stack.is_local(name):
                offset = Stack.offset(name)
                FRISC.push_command(Command.build_add("R1", offset, "R1"))
                FRISC.push_command(Command.build_add("R1", "SP", "R1"))
                FRISC.push_command(Command.build_load("R0", "R1"))
            else:
                FRISC.push_command(Command.build_move(FRISC.generate_global_label(name), "R2"))
                FRISC.push_command(Command.build_add("R1", "R2", "R1"))
                FRISC.push_command(Command.build_load("R0", "R1"))

            FRISC.push_command(Command.build_push("R0"))

            pass

        if content_type is OtherType.POSTFIKS_PRAZNE_ZAGRADE:
            self.__content[0].generate()

        if content_type is OtherType.POSTFIKS_PUNE_ZAGRADE:
            self.__content[2].generate()
            self.__content[0].generate()
            # Dodano
            Stack.clear_current_scope()

        if content_type is OtherType.POSTFIKS_INC:
            self.__content[0].generate()
            FRISC.generate_post_inc()

        if content_type is OtherType.POSTFIKS_DEC:
            self.__content[0].generate()
            FRISC.generate_post_dec()

    def __str__(self):
        return "<postfiks_izraz>"


# Gotovo
class ListaArgumenata:
    def __init__(self, content, parent=None):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type == OtherType.LISTA_ARGUMENATA_UZ_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type == OtherType.IZRAZ_PRIDRUZIVANJA:
            self.__content[0].generate()

        if content_type == OtherType.LISTA_ARGUMENATA_UZ_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()

    def __str__(self):
        return "<lista_argumenata>"


# Gotovo
class UnarniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

    def get_value(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            return self.__content[0].get_value()

        if content_type in [OtherType.INC_UNARNI_IZRAZ, OtherType.DEC_UNARNI_IZRAZ]:
            return self.__content[1].get_value()

        if content_type is OtherType.UNARNI_OPERATOR_UZ_CAST:
            return self.__content[1].get_value()

        return None

    def get_type(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            return self.__content[0].get_type()

        if content_type in [OtherType.INC_UNARNI_IZRAZ, OtherType.DEC_UNARNI_IZRAZ, OtherType.UNARNI_OPERATOR_UZ_CAST]:
            return PrimitiveType.INT

        return None

    def get_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type in [OtherType.INC_UNARNI_IZRAZ, OtherType.DEC_UNARNI_IZRAZ, OtherType.UNARNI_OPERATOR_UZ_CAST]:
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
            self.__content[0].is_valid()

        if content_type in [OtherType.DEC_UNARNI_IZRAZ, OtherType.INC_UNARNI_IZRAZ]:
            self.__content[1].is_valid()

        if content_type is OtherType.UNARNI_OPERATOR_UZ_CAST:
            self.__content[1].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.POSTFIKS_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.INC_UNARNI_IZRAZ:
            self.__content[1].generate()
            FRISC.generate_pre_inc()

        if content_type is OtherType.DEC_UNARNI_IZRAZ:
            self.__content[1].generate()
            FRISC.generate_pre_dec()

        if content_type is OtherType.UNARNI_OPERATOR_UZ_CAST:
            self.__content[1].generate()
            self.__content[0].generate()

    def __str__(self):
        return "<unarni_izraz>"


# Gotovo
class UnarniOperator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
        if len(self.__content) is 1 and isinstance(self.__content[0], Keyword):
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

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.UNARNI_MINUS:
            FRISC.generate_u_neg()

        if content_type is OtherType.UNARNI_TILDA:
            FRISC.generate_bit_not()

        if content_type is OtherType.UNARNI_NEG:
            FRISC.generate_log_not()

    def __str__(self):
        return "<unarni_operator>"


# Gotovo
class CastIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

    def get_value(self):
        content_type = self.get_content_type()

        if content_type is OtherType.UNARNI_IZRAZ:
            return self.__content[0].get_value()

        if content_type is OtherType.VISESTRUKI_CAST:
            return self.__content[3].get_value()

        return None

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
            self.__content[0].is_valid()

        if content_type is OtherType.VISESTRUKI_CAST:
            self.__content[1].is_valid()
            self.__content[3].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.UNARNI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.VISESTRUKI_CAST:
            self.__content[1].generate()
            self.__content[3].generate()

    def __str__(self):
        return "<cast_izraz>"


# Gotovo
class ImeTipa:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
                isinstance(self.__content[1], SpecifikatorTipa):
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
            self.__content[0].is_valid()

        if content_type is OtherType.KONSTANTAN_TIP:
            self.__content[1].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.OBICAN_TIP:
            self.__content[0].generate()

        if content_type is OtherType.KONSTANTAN_TIP:
            self.__content[1].generate()

    def __str__(self):
        return "<ime_tipa>"


# Gotovo
class SpecifikatorTipa:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

    @staticmethod
    def get_l_flag():
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

        self.__content[0].is_valid()

        return True

    def generate(self):
        pass

    def __str__(self):
        return "<specifikator_tipa>"


# Gotovo
class MultiplikativniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        if content_type in [OtherType.PUTA_IZRAZ, OtherType.DIJELI_IZRAZ, OtherType.MOD_IZRAZ]:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CAST_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type in [OtherType.PUTA_IZRAZ, OtherType.DIJELI_IZRAZ, OtherType.MOD_IZRAZ]:
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
            self.__content[0].is_valid()

        if content_type in [OtherType.PUTA_IZRAZ, OtherType.DIJELI_IZRAZ, OtherType.MOD_IZRAZ]:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CAST_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.PUTA_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_mul()

        if content_type is OtherType.DIJELI_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_div()

        if content_type is OtherType.MOD_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_mod()

    def __str__(self):
        return "<multiplikativni_izraz>"


# Gotovo
class AditivniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        if content_type in [OtherType.PLUS_IZRAZ, OtherType.MINUS_IZRAZ]:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.MULTIPLIKATIVNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type in [OtherType.PLUS_IZRAZ, OtherType.MINUS_IZRAZ]:
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
            self.__content[0].is_valid()

        if content_type in [OtherType.PLUS_IZRAZ, OtherType.MINUS_IZRAZ]:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.MULTIPLIKATIVNI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.PLUS_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_add()

        if content_type is OtherType.MINUS_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_sub()

    def __str__(self):
        return "<aditivni_izraz>"


# Gotovo
class OdnosniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        if content_type in [OtherType.GT_IZRAZ, OtherType.LT_IZRAZ, OtherType.GTE_IZRAZ, OtherType.LTE_IZRAZ]:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ADITIVNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type in [OtherType.GT_IZRAZ, OtherType.LT_IZRAZ, OtherType.GTE_IZRAZ, OtherType.LTE_IZRAZ]:
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
            self.__content[0].is_valid()

        if content_type in [OtherType.GT_IZRAZ, OtherType.LT_IZRAZ, OtherType.GTE_IZRAZ, OtherType.LTE_IZRAZ]:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ADITIVNI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.GT_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_gt()

        if content_type is OtherType.LT_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_lt()

        if content_type is OtherType.GTE_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_gte()

        if content_type is OtherType.LTE_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_lte()

    def __str__(self):
        return "<odnosni_izraz>"


# Gotovo
class JednakosniIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        if content_type in [OtherType.EQ_IZRAZ, OtherType.NEQ_IZRAZ]:
            return PrimitiveType.INT

        return None

    def get_l_flag(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ODNOSNI_IZRAZ:
            return self.__content[0].get_l_flag()

        if content_type in [OtherType.EQ_IZRAZ, OtherType.NEQ_IZRAZ]:
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
            self.__content[0].is_valid()

        if content_type in [OtherType.EQ_IZRAZ, OtherType.NEQ_IZRAZ]:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.ODNOSNI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.EQ_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_bin_eq()

        if content_type is OtherType.NEQ_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_bin_ne()

    def __str__(self):
        return "<jednakosni_izraz>"


# Gotovo
class BinIIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.OP_BIN_I_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.JEDNAKOSNI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.OP_BIN_I_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_bin_and()

    def __str__(self):
        return "<bin_i_izraz>"


# Gotovo
class BinXiliIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.OP_BIN_XILI_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_I_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.OP_BIN_XILI_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_bin_xor()

    def __str__(self):
        return "<bin_xili_izraz>"


# Gotovo
class BinIliIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.OP_BIN_ILI_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_XILI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.OP_BIN_ILI_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_bin_or()

    def __str__(self):
        return "<bin_ili_izraz>"


# Gotovo
class LogIIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.OP_LOG_I_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.BIN_ILI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.OP_LOG_I_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_log_and()

    def __str__(self):
        return "<log_i_izraz>"


# Gotovo
class LogIliIzraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.OP_LOG_ILI_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_I_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.OP_LOG_ILI_IZRAZ:
            self.__content[0].generate()
            self.__content[2].generate()
            FRISC.generate_log_or()

    def __str__(self):
        return "<log_ili_izraz>"


# Gotovo
class IzrazPridruzivanja:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        if content_type in [OtherType.LOG_ILI_IZRAZ, OtherType.OP_PRIDRUZI_IZRAZ]:
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
                if isinstance(item, PrimarniIzraz) and \
                        isinstance(item.get_content()[0], Keyword) and \
                        item.get_content()[0].get_count() is not None:
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
            new_try_list = list()

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
            self.__content[0].is_valid()

        if content_type is OtherType.OP_PRIDRUZI_IZRAZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LOG_ILI_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.OP_PRIDRUZI_IZRAZ:
            self.__content[2].generate()

            postfix_content_type = self.__content[0].get_content_type()

            if postfix_content_type is OtherType.PRIMARNI_IZRAZ:
                name = self.__content[0].get_name()

                if Stack.is_local(name):
                    FRISC.push_command(Command.build_pop("R0"))
                    FRISC.push_command(Command.build_store_from_register("R0", "SP", Stack.offset(name)))
                else:
                    FRISC.push_command(Command.build_move(FRISC.generate_global_label(name), "R1"))
                    FRISC.push_command(Command.build_pop("R0"))
                    FRISC.push_command(Command.build_store("R0", "R1"))

            if postfix_content_type is OtherType.POSTFIKS_UGLATE_ZAGRADE:
                postexpr = copy.deepcopy(self.__content[0])
                name = postexpr.get_value()

                while not isinstance(name, str):
                    postexpr = postexpr.get_content()[0]
                    name = postexpr.get_value()

                self.__content[0].get_content()[2].generate()
                FRISC.push_command(Command.build_pop("R1"))
                FRISC.push_command(Command.build_pop("R0"))
                # Zamijeni sa mul 4 ?
                FRISC.push_command(Command.build_add("R1", "R1", "R1"))
                FRISC.push_command(Command.build_add("R1", "R1", "R1"))

                if Stack.is_local(name):
                    FRISC.push_command(Command.build_add("R1", Stack.offset(name), "R1"))
                    FRISC.push_command(Command.build_add("R1", "SP", "R1"))
                    FRISC.push_command(Command.build_store("R0", "R1"))
                else:
                    FRISC.push_command(Command.build_move(FRISC.generate_global_label(name), "R2"))
                    FRISC.push_command(Command.build_add("R1", "R2", "R1"))
                    FRISC.push_command(Command.build_store("R0", "R1"))

    def __str__(self):
        return "<izraz_pridruzivanja>"


# Gotovo
class Izraz:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_IZRAZ:
            self.__content[0].generate()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_UZ_ZAREZ:
            self.__content[0].generate()
            self.__content[2].generate()

    def __str__(self):
        return "<izraz>"


# Gotovo
class SlozenaNaredba:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        self.__entries = dict()

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        if content_type is OtherType.SLOZ_NAREDBA_LISTA_NAREDBI:
            self.__content[1].is_valid()

        if content_type is OtherType.SLOZ_NARED_S_LISTOM_DEKL_I_NAREDBI:
            self.__content[1].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.SLOZ_NAREDBA_LISTA_NAREDBI:
            self.__content[1].generate()

        if content_type is OtherType.SLOZ_NARED_S_LISTOM_DEKL_I_NAREDBI:
            Stack.set_start()
            self.__content[1].generate()
            self.__content[2].generate()
            Stack.clear_current_scope()

    def __str__(self):
        return "<slozena_naredba>"


# Gotovo
class ListaNaredbi:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[0].is_valid()

        if content_type is OtherType.LISTA_NAREDBI:
            self.__content[0].is_valid()
            self.__content[1].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.NAREDBA:
            self.__content[0].generate()

        if content_type is OtherType.LISTA_NAREDBI:
            self.__content[0].generate()
            self.__content[1].generate()

    def __str__(self):
        return "<lista_naredbi>"


# Gotovo
class Naredba:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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

        self.__content[0].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is not None:
            self.__content[0].generate()

    def __str__(self):
        return "<naredba>"


# Gotovo
class IzrazNaredba:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
                and isinstance(self.__content[1], Keyword)\
                and self.__content[1].get_type() is KeywordEnumeration.TOCKAZAREZ:
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
            self.__content[0].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_I_TOCKAZAREZ:
            self.__content[0].generate()

    def __str__(self):
        return "<izraz_naredba>"


# Gotovo*
class NaredbaGrananja:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[2].is_valid()
            self.__content[4].is_valid()

        if content_type is OtherType.IF_S_ELSEOM:
            self.__content[2].is_valid()
            self.__content[4].is_valid()
            self.__content[6].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IF:
            self.__content[2].generate()
            FRISC.generate_if_condition()
            self.__content[4].generate()
            FRISC.generate_if_end()

        if content_type is OtherType.IF_S_ELSEOM:
            self.__content[2].generate()
            FRISC.generate_if_condition()
            self.__content[4].generate()
            FRISC.push_command(Command.build_jp("ELSE_END_" + str(FRISC.current_if())))
            FRISC.generate_if_end()
            self.__content[6].generate()
            FRISC.generate_else_end()

    def __str__(self):
        return "<naredba_grananja>"


# Gotovo*
class NaredbaPetlje:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            self.__content[2].is_valid()
            self.__content[4].is_valid()

        if content_type is OtherType.FOR_BEZ_INDEKSIRANJA:
            self.__content[2].is_valid()
            self.__content[3].is_valid()
            self.__content[5].is_valid()

        if content_type is OtherType.FOR_SA_INDEKSIRANJEM:
            self.__content[2].is_valid()
            self.__content[3].is_valid()
            self.__content[4].is_valid()
            self.__content[6].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.WHILE:
            FRISC.generate_loop_start()
            self.__content[2].generate()
            FRISC.generate_loop_condition()
            self.__content[4].generate()
            FRISC.push_command(Command.build_jp("LOOP_START_" + str(FRISC.current_loop())))
            FRISC.generate_loop_end()

        if content_type is OtherType.FOR_BEZ_INDEKSIRANJA:
            self.__content[2].generate()
            FRISC.generate_loop_start()
            self.__content[3].generate()
            FRISC.generate_loop_condition()
            self.__content[5].generate()
            FRISC.push_command(Command.build_jp("LOOP_START_" + str(FRISC.current_loop())))
            FRISC.generate_loop_end()

        if content_type is OtherType.FOR_SA_INDEKSIRANJEM:
            self.__content[2].generate()
            FRISC.generate_loop_start()
            self.__content[3].generate()
            FRISC.generate_loop_condition()
            self.__content[6].generate()
            self.__content[4].generate()
            FRISC.push_command(Command.build_jp("LOOP_START_" + str(FRISC.current_loop())))
            FRISC.generate_loop_end()

    def __str__(self):
        return "<naredba_petlje>"


# Trebalo bi bit gotovo*
class NaredbaSkoka:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

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
            if self.__content[0].get_type() in [KeywordEnumeration.KR_CONTINUE, KeywordEnumeration.KR_BREAK]:
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
        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.CONTINUE_OR_BREAK:
            if self.__content[0].get_type() is KeywordEnumeration.KR_CONTINUE:
                FRISC.generate_continue()
                pass

            if self.__content[0].get_type() is KeywordEnumeration.KR_BREAK:
                FRISC.generate_break()
                pass

        if content_type is OtherType.RETURN_BEZ_POV_VRIJEDNOSTI:
            Stack.clear_current_scope()
            FRISC.load_context()
            FRISC.push_command(Command.build_ret())
            pass

        if content_type is OtherType.RETURN_SA_POV_VRIJEDNOSTI:
            self.__content[1].generate()
            FRISC.push_command(Command.build_pop("R6"))
            Stack.clear_current_scope()
            FRISC.load_context()
            FRISC.push_command(Command.build_ret())

    def __str__(self):
        return "<naredba_skoka>"


# Gotovo
class PrijevodnaJedinica:
    def __init__(self, content, parent, with_table=False):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__entries = dict()
        self.__has_table = with_table
        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_table(self):
        return self.__entries

    def get_entry(self, name: str):
        if self.__has_table and name in self.__entries:
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

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
            self.__content[0].is_valid()

        if content_type is OtherType.PRIJEVODNA_JED_I_VANJSKA_DEKL:
            self.__content[0].is_valid()
            self.__content[1].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.VANJSKA_DEKL:
            self.__content[0].generate()

        if content_type is OtherType.PRIJEVODNA_JED_I_VANJSKA_DEKL:
            self.__content[0].generate()
            self.__content[1].generate()

    def __str__(self):
        return "<prijevodna_jedinica>"


# Gotovo
class VanjskaDeklaracija:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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

        self.__content[0].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.DEFINICIJA_FUNKCIJE:
            self.__content[0].generate()

        if content_type is OtherType.DEKLARACIJA:
            declaration = self.__content[0]
            init_declarator = declaration.get_content()[1]

            init_declarator_stack = list()

            while len(init_declarator.get_content()) == 3:
                init_declarator_stack.append(init_declarator.get_content()[2])
                init_declarator = init_declarator.get_content()[0]

            init_declarator_stack.append(init_declarator.get_content()[0])

            while len(init_declarator_stack) is not 0:
                current_init_declarator = init_declarator_stack.pop()

                name = current_init_declarator.get_content()[0].get_content()[0].get_value()
                declarator_type = self.get_entry_global(name).get_type()

                if isinstance(declarator_type, FunctionType):
                    continue

                if len(current_init_declarator.get_content()) is 1:
                    if isinstance(declarator_type, ArrayType):
                        size = current_init_declarator.get_content()[0].get_content()[2].get_value()
                        command = Command.build_db(size * 4)
                    else:
                        command = Command.build_db(4)
                else:
                    values = ConstantResolver.resolve(current_init_declarator.get_content()[2])
                    values_string = ""

                    for value in values:
                        values_string += str(value) + ", "

                    command = Command.build_dw(values_string[:-2])

                FRISC.define_global(name, command)

    def __str__(self):
        return "<vanjska_deklaracija>"


# Gotovo
class DefinicijaFunkcije:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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

                if isinstance(self.__content[3], Keyword) and \
                        self.__content[3].get_type() is KeywordEnumeration.KR_VOID:
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
            self.__content[0].is_valid()

            self.add_to_table()

            self.__content[5].is_valid()

        if content_type is OtherType.FUNKCIJA_S_PARAMETRIMA:
            self.__content[0].is_valid()

            hypothetical_function = self.get_entry(self.__content[1].get_value())

            self.__content[3].is_valid()

            if hypothetical_function is not None:
                hypothetical_function.define()
            else:
                self.add_to_table()

            names_and_types = self.__content[3].get_parameter_names_and_types()

            for name_and_type in names_and_types:
                self.__content[5].add_entry(name_and_type[0], TableEntry(name_and_type[1], True))

            self.__content[5].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.FUNKCIJA_BEZ_PARAMETARA:
            self.__content[0].generate()
            label = FRISC.generate_function_label(self.__content[1].get_value())
            FRISC.push_command_with_label(label, "")
            FRISC.save_context()
            self.__content[5].generate()

        if content_type is OtherType.FUNKCIJA_S_PARAMETRIMA:
            self.__content[0].generate()
            label = FRISC.generate_function_label(self.__content[1].get_value())
            FRISC.push_command_with_label(label, "")
            FRISC.save_context()
            self.__content[3].generate()
            self.__content[5].generate()

    def __str__(self):
        return "<definicija_funkcije>"


# Gotovo
class ListaParametara:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
            self.__content[0].is_valid()

        if content_type is OtherType.LISTA_S_VISE_PARAMETARA:
            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.LISTA_S_JEDNIM_PARAMETROM:
            self.__content[0].generate()

        if content_type is OtherType.LISTA_S_VISE_PARAMETARA:
            self.__content[0].generate()
            self.__content[2].generate()

    def __str__(self):
        return "<lista_parametara>"


# Gotovo
class DeklaracijaParametra:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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

        if content_type in [OtherType.DEKLARACIJA_OBICNOG_PARAMETRA, OtherType.DEKLARACIJA_PARAMETRA_POLJA]:
            self.__content[0].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is not None:
            self.__content[0].generate()

    def __str__(self):
        return "<deklaracija_parametra>"


# Gotovo
class ListaDeklaracija:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
            self.__content[0].is_valid()

        if content_type is OtherType.LISTA_DEKL_I_DEKL:
            self.__content[0].is_valid()
            self.__content[1].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.DEKL:
            self.__content[0].generate()

        if content_type is OtherType.LISTA_DEKL_I_DEKL:
            declaration_stack = list()
            current_declaration = self

            while current_declaration.get_content_type() is OtherType.LISTA_DEKL_I_DEKL:
                declaration_stack.append(current_declaration.get_content()[1])
                current_declaration = current_declaration.get_content()[0]

            declaration_stack.append(current_declaration.get_content()[0])

            while len(declaration_stack) is not 0:
                declaration_stack.pop().generate()

    def __str__(self):
        return "<lista_deklaracija>"


# Nešto mi je sumnjiv get_content_type(), ali trebali bi biti gotovo
class Deklaracija:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
            self.__content[0].is_valid()
            self.__content[1].is_valid(self.__content[0].get_type())

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.NAREDBA_DEKLARACIJE:
            self.__content[1].generate()

    def __str__(self):
        return "<deklaracija>"


# Gotovo
class ListaInitDeklaratora:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
            self.__content[0].is_valid(type_to_check)

        if content_type is OtherType.LISTA_INIT_DEKLARATORA:
            self.__content[0].is_valid(type_to_check)
            self.__content[2].is_valid(type_to_check)

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.INIT_DEKLARATOR:
            self.__content[0].generate()

        if content_type is OtherType.LISTA_INIT_DEKLARATORA:
            init_declarator_stack = list()
            current_declarator_list = self

            while current_declarator_list.get_content_type() is OtherType.LISTA_DEKL_I_DEKL:
                init_declarator_stack.append(current_declarator_list.get_content()[2])
                current_declarator_list = current_declarator_list.get_content()[0]

            init_declarator_stack.append(current_declarator_list.get_content()[0])

            while len(init_declarator_stack) is not 0:
                init_declarator_stack.pop().generate()

    def __str__(self):
        return "<lista_init_deklaratora>"


# Gotovo, malo sumnjivo da nisam sjebo is valid
class InitDeklarator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
            self.__content[0].is_valid(type_to_check)

        if content_type is OtherType.IZRAVNI_DEKLARATOR_UZ_INICIJALIZATOR:
            self.__content[0].is_valid(type_to_check)
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        name = self.__content[0].get_content()[0].get_value()
        _type = self.get_entry_local(name).get_type()

        if content_type is OtherType.IZRAVNI_DEKLARATOR:
            FRISC.push_command(Command.build_move(0, "R5"))
            FRISC.push_command(Command.build_push("R5"))
            Stack.push(name, _type)

            if isinstance(_type, ArrayType):
                size = self.__content[0].get_content()[2].get_value()

                for i in range(1, size):
                    FRISC.push_command(Command.build_push("R5"))
                    Stack.push(None, ArrayType.to_base_type(_type))

        if content_type is OtherType.IZRAVNI_DEKLARATOR_UZ_INICIJALIZATOR:
            self.__content[2].generate()
            Stack.push(name, _type)

            if isinstance(_type, ArrayType):
                size = self.__content[0].get_content()[2].get_value()

                for i in range(1, size):
                    Stack.push(None, ArrayType.to_base_type(_type))

    def __str__(self):
        return "<init_deklarator>"


# Gotovo
class IzravniDeklarator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__type = None
        self.__count = 1
        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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

            if type_to_check is not PrimitiveType.VOID and self.get_entry_local(self.__content[0].get_value()) is None:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, True))

        if content_type is OtherType.ARRAY_DEKLARATOR:
            self.__type = array(type_to_check)
            self.__count = self.__content[2].get_value()

            if type_to_check is not PrimitiveType.VOID and \
                    self.get_entry_local(self.__content[0].get_value()) is None and \
                    0 < self.__content[2].get_value() <= 1024:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, True))

        if content_type is OtherType.DEKLARATOR_FUNKCIJE_BEZ_PARAMETARA:
            self.__type = FunctionType(PrimitiveType.VOID, type_to_check)

            hypothetical_function = self.get_entry_local(self.__content[0].get_value())

            if hypothetical_function is None:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, False))

        if content_type is OtherType.DEKLARATOR_FUNKCIJE:
            self.__type = FunctionType(Params(self.__content[2].get_parameter_types()), type_to_check)
            self.__content[2].is_valid()

            hypothetical_function = self.get_entry_local(self.__content[0].get_value())

            if hypothetical_function is None:
                self.add_entry(self.__content[0].get_value(), TableEntry(self.__type, False))

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is not None:
            return
        else:
            raise ValueError("Izravni deklarator nas trolla")

    def __str__(self):
        return "<izravni_deklarator>"


# Gotovo
class Inicijalizator:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__count = None
        self.__types = None
        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

        if name in parent.get_table():
            return parent.get_table()[name]

        return None

    def add_entry(self, name: str, entry: TableEntry):
        if self.__parent is None:
            return None

        return self.__parent.add_entry(name, entry)

    def get_type(self):
        return self.get_types()

    def get_count(self):
        if self.__count is None:
            content_type = self.get_content_type()

            if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_INICIJALIZATOR:
                count = self.__content[0].get_count()

                if count is not None:
                    self.__count = count + 1
                    return self.__count

            if content_type is OtherType.LISTA_PRIDRUZIVANJA:
                self.__count = self.__content[1].get_count()
                return self.__count
        else:
            return self.__count

        return None

    def get_types(self):
        if self.__types is None:
            content_type = self.get_content_type()

            if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_INICIJALIZATOR:
                count = self.__content[0].get_count()

                if count is not None:
                    self.__types = list()

                    for i in range(0, self.__count):
                        self.__types.append(PrimitiveType.CHAR)

                    return self.__types
                else:
                    self.__types = self.__content[0].get_type()
                    return self.__types

            if content_type is OtherType.LISTA_PRIDRUZIVANJA:
                self.__types = self.__content[1].get_types()
                return self.__types
        else:
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
            self.__content[0].is_valid()

        if content_type is OtherType.LISTA_PRIDRUZIVANJA:
            self.__content[1].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_INICIJALIZATOR:
            self.__content[0].generate()

        if content_type is OtherType.LISTA_PRIDRUZIVANJA:
            self.__content[1].generate()

    def __str__(self):
        return "<inicijalizator>"


# Gotovo
class ListaIzrazaPridruzivanja:
    def __init__(self, content, parent):
        self.__content = list()
        self.__parent = parent

        for item in content:
            self.__content.append(item)

        self.__count = None
        self.__types = None
        self.__passing = None

    def get_content(self):
        return self.__content

    def add_content(self, content):
        self.__content.append(content)

    def get_parent(self):
        return self.__parent

    def get_entry(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry(name)

    def get_entry_local(self, name: str):
        if self.__parent is None:
            return None

        return self.__parent.get_entry_local(name)

    def get_entry_global(self, name: str):
        parent = self

        while parent.get_parent() is not None:
            parent = parent.get_parent()

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
        if self.__types is None:
            content_type = self.get_content_type()

            if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_LISTE:
                self.__types = [self.__content[0].get_type()]
                return self.__types

            if content_type is OtherType.IZRAZ_LISTE_PRIDRUZVANJA:
                to_return = self.__content[0].get_types()
                to_return.append(self.__content[2].get_type())

                self.__types = to_return
                return self.__types
        else:
            return self.__types

        return None

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

        return None

    def is_valid(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_LISTE:
            self.__types = [self.__content[0].get_type()]
            self.__count = 1

            self.__content[0].is_valid()

        if content_type is OtherType.IZRAZ_LISTE_PRIDRUZVANJA:
            t_types = self.__content[0].get_types()
            t_types.append(self.__content[2].get_type())

            self.__types = t_types
            self.__count = len(self.__types)

            self.__content[0].is_valid()
            self.__content[2].is_valid()

        return True

    def generate(self):
        content_type = self.get_content_type()

        if content_type is OtherType.IZRAZ_PRIDRUZIVANJA_IZ_LISTE:
            self.__content[0].generate()

        if content_type is OtherType.IZRAZ_LISTE_PRIDRUZVANJA:
            self.__content[0].generate()
            self.__content[2].generate()

    def __str__(self):
        return "<lista_izraza_pridruzivanja>"


class GenerativeTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def set_root(self, root):
        self.__root = root

    def get_content(self):
        return self.__root.get_content()

    def add_content(self, content):
        self.__root.add_content(content)

    def get_entry(self, name: str):
        self.__root.get_entry(name)

    def add_entry(self, name: str, entry: TableEntry):
        self.__root.add_entry(name, entry)

    def has_main(self):
        tables = self.get_all_tables()

        if "main" in tables and tables["main"].get_type() == FunctionType(PrimitiveType.VOID, PrimitiveType.INT):
            return True

        return False

    def has_all_functions_defined(self):
        tables = self.get_all_tables()

        for entry in tables:
            if isinstance(tables[entry].get_type(), FunctionType) and not tables[entry].is_defined():
                return False

        return True

    def get_all_tables(self):
        full_table = dict()

        to_check = [self.__root]
        new_to_check = []

        while len(to_check) > 0:
            for item in to_check:
                table = GenerativeTree.fetch_table(item)

                if table is not None and len(table) is not 0:
                    for key in table:
                        if key in full_table:
                            if full_table[key].is_defined is False:
                                full_table[key] = table[key]
                        else:
                            full_table[key] = table[key]

                for n_item in item.get_content():
                    if not isinstance(n_item, Keyword):
                        new_to_check.append(n_item)

            to_check = new_to_check
            new_to_check = []

        return full_table

    @staticmethod
    def fetch_table(node):
        if isinstance(node, SlozenaNaredba):
            return node.get_table()

        if isinstance(node, PrijevodnaJedinica):
            return node.get_table()

        return dict()

    def check(self):
        to_print = None
        if self.__root is not None:
            self.__root.is_valid()

    def generate(self):
        to_write = Command.build_initializer()

        if self.__root is not None:
            self.__root.generate()

            # FRISC.generate_helpers()

            for line in FRISC.program:
                to_write += line
            for var in FRISC.globals:
                to_write += str(var[0]) + "\t" + str(var[1])

        open("a.frisc", "w+").write(to_write)

    @staticmethod
    def print_all_tables(node):
        if isinstance(node, PrijevodnaJedinica) or isinstance(node, SlozenaNaredba):
            for item in node.get_table():
                print("[" + str(item) + "] " + str(node.get_table()[item]))

            print()

        if not isinstance(node, Keyword):
            for item in node.get_content():
                GenerativeTree.print_all_tables(item)

    # Prototype for check function.
    @staticmethod
    def build_from_string(string: str):
        to_return = GenerativeTree.parse(string)

        try:
            GenerativeTree.refresh_tables(to_return.get_root())
        except Exception as message:
            print(message)

    @staticmethod
    def refresh_tables(node):
        currently_visiting = node

        if isinstance(node, DefinicijaFunkcije):
            node.add_to_table()

        if not isinstance(currently_visiting, Keyword):
            for item in currently_visiting.get_content():
                GenerativeTree.refresh_tables(item)

    # Other methods
    # Parsira string u stablo, tj. vraća Node.
    @staticmethod
    def parse(string: str):
        string = string.strip()

        # Prvo ručno postavljamo korijen stabla za prvu liniju.
        to_return = GenerativeTree()
        lines = special_split(string)
        starting_level = tree_level(lines[0])
        to_return.set_root(GenerativeTree.create_class(lines[0].strip()))

        # Ideja je za svaku liniju naći roditelja čvora i dodati mu ga
        for i in range(1, len(lines)):

            # Prvo se nađe nivo čvora, te mu se oduzme jedan jer to treba biti nivo roditelja.
            parent_node_level = tree_level(lines[i]) - starting_level - 1

            # Počne se tako da je roditelj korijen stabla
            parent = to_return.__root

            # U svakoj iteraciji se za roditelja postavlja posljednje dijete proteklog roditelja.
            for j in range(0, parent_node_level):
                parent = (parent.get_content())[-1]

            # Roditelju se dodaje dijete te se sa svake strane uklanja višak razmaka.
            parent.add_content(GenerativeTree.create_class(lines[i].strip(), parent=parent))

        # Vraćamo korijen stabla.
        return to_return

    @staticmethod
    def create_class(string: str, parent=None):
        if string == "<primarni_izraz>":
            return PrimarniIzraz(list(), parent=parent)

        if string == "<postfiks_izraz>":
            return PostfiksIzraz(list(), parent=parent)

        if string == "<lista_argumenata>":
            return ListaArgumenata(list(), parent=parent)

        if string == "<unarni_izraz>":
            return UnarniIzraz(list(), parent=parent)

        if string == "<unarni_operator>":
            return UnarniOperator(list(), parent=parent)

        if string == "<cast_izraz>":
            return CastIzraz(list(), parent=parent)

        if string == "<ime_tipa>":
            return ImeTipa(list(), parent=parent)

        if string == "<specifikator_tipa>":
            return SpecifikatorTipa(list(), parent=parent)

        if string == "<multiplikativni_izraz>":
            return MultiplikativniIzraz(list(), parent=parent)

        if string == "<aditivni_izraz>":
            return AditivniIzraz(list(), parent=parent)

        if string == "<odnosni_izraz>":
            return OdnosniIzraz(list(), parent=parent)

        if string == "<jednakosni_izraz>":
            return JednakosniIzraz(list(), parent=parent)

        if string == "<bin_i_izraz>":
            return BinIIzraz(list(), parent=parent)

        if string == "<bin_xili_izraz>":
            return BinXiliIzraz(list(), parent=parent)

        if string == "<bin_ili_izraz>":
            return BinIliIzraz(list(), parent=parent)

        if string == "<log_i_izraz>":
            return LogIIzraz(list(), parent=parent)

        if string == "<log_ili_izraz>":
            return LogIliIzraz(list(), parent=parent)

        if string == "<izraz_pridruzivanja>":
            return IzrazPridruzivanja(list(), parent=parent)

        if string == "<izraz>":
            return Izraz(list(), parent=parent)

        if string == "<slozena_naredba>":
            return SlozenaNaredba(list(), parent=parent)

        if string == "<lista_naredbi>":
            return ListaNaredbi(list(), parent=parent)

        if string == "<naredba>":
            return Naredba(list(), parent=parent)

        if string == "<izraz_naredba>":
            return IzrazNaredba(list(), parent=parent)

        if string == "<naredba_grananja>":
            return NaredbaGrananja(list(), parent=parent)

        if string == "<naredba_petlje>":
            return NaredbaPetlje(list(), parent=parent)

        if string == "<naredba_skoka>":
            return NaredbaSkoka(list(), parent=parent)

        if string == "<prijevodna_jedinica>":
            if parent is None:
                return PrijevodnaJedinica(list(), parent=None, with_table=True)

            return PrijevodnaJedinica(list(), parent=parent)

        if string == "<vanjska_deklaracija>":
            return VanjskaDeklaracija(list(), parent=parent)

        if string == "<definicija_funkcije>":
            return DefinicijaFunkcije(list(), parent=parent)

        if string == "<lista_parametara>":
            return ListaParametara(list(), parent=parent)

        if string == "<deklaracija_parametra>":
            return DeklaracijaParametra(list(), parent=parent)

        if string == "<lista_deklaracija>":
            return ListaDeklaracija(list(), parent=parent)

        if string == "<deklaracija>":
            return Deklaracija(list(), parent=parent)

        if string == "<lista_init_deklaratora>":
            return ListaInitDeklaratora(list(), parent=parent)

        if string == "<init_deklarator>":
            return InitDeklarator(list(), parent=parent)

        if string == "<izravni_deklarator>":
            return IzravniDeklarator(list(), parent=parent)

        if string == "<inicijalizator>":
            return Inicijalizator(list(), parent=parent)

        if string == "<lista_izraza_pridruzivanja>":
            return ListaIzrazaPridruzivanja(list(), parent=parent)

        split_string = string.split(" ", 2)

        if split_string is not None and split_string[0] in KEYWORDS:
            return Keyword.from_strings(split_string[0], int(split_string[1]), split_string[2], parent=parent)

        return None

    def __str__(self):
        return GenerativeTree.__to_str(self.__root)

    @staticmethod
    def __to_str(node, level: int = 0):
        to_return = ""

        for i in range(0, level):
            to_return += LEVEL_DELIMITER

        to_return += str(node)

        if isinstance(node, Keyword):
            return to_return

        for item in node.get_content():
            to_return += "\n" + GenerativeTree.__to_str(item, level + 1)

        return to_return


some_tree = GenerativeTree.parse(sys.stdin.read())
# some_tree = GenerativeTree.parse(test)
some_tree.check()
some_tree.generate()
