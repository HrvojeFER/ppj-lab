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
        return "\tLOAD " + str(dest) + ", (" + str(adr) + ")" + "\n"

    @staticmethod
    def build_store_with_size(dest, adr, size):
        return "\tLOAD" + str(size) + " " + str(dest) + ", (" + str(adr) + ")" + "\n"
    
    @staticmethod
    def build_store_from_register(dest, adrreg, offset):
        return "\tLOAD " + str(dest) + ",  (" + str(adrreg) + "+" + str(offset) + ")" + "\n"
    
    @staticmethod
    def build_store_from_register_with_size(dest, size, adrreg, offset):
        return "\tLOAD" + str(size) + " " + str(dest) + ", (" + str(adrreg) + "+" + str(offset) + ")" + "\n"

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
        return "\t`DB " + str(value) + "\n"

    @staticmethod
    def build_dh(value):
        return "\t`DH " + str(value) + "\n"

    @staticmethod
    def build_dw(value):
        return "\t`DW " + str(value) + "\n"

    @staticmethod
    def build_dw_from_list(values):
        vals = ""
        for val in values:
            vals += str(val) + ", "

        return "\t`DW " + vals[:-2] + "\n"

    # initializer
    @staticmethod
    def build_initializer():
        return "\t`BASE D" \
               "\tMOVE %H 40000, R7\n" \
               "\tCALL F_MAIN\n" \
               "\tHALT\n"
