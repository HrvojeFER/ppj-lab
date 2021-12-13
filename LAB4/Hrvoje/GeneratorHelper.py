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


class GeneratorHelper:
    def __init__(self):
        self.program = list()

    # --------------------------------------------------------------------
    # grananje, petlje, skokovi
        self.loop_num = 0
        self.loops = list()

        self.if_num = 0
        self.ifs = list()

    def enter_loop(self):
        self.loop_num = self.loop_num + 1
        self.loops.append(self.loop_num)
        return self.loop_num

    def leave_loop(self):
        loop = self.loops[-1]
        self.loops = self.loops[:-1]
        return loop

    def current_loop(self):
        return self.loops[-1]

    def enter_if(self):
        self.if_num = self.if_num + 1
        self.ifs.append(self.if_num)
        return self.if_num

    def leave_if(self):
        iff = self.ifs[-1]
        self.loops = self.ifs[:-1]
        return iff

    def current_if(self):
        return self.ifs[-1]

    def generate_continue(self):
        self.program.append(Command.build_jp("LOOP_START_" + str(self.current_loop())))

    def generate_break(self):
        self.program.append(Command.build_jp("LOOP_END_" + str(self.leave_loop())))

    def generate_ret(self):
        self.program.append(Command.build_push("R5"))
        self.program.append(Command.build_ret())

    def generate_ret_with_value(self):
        self.program.append(Command.build_pop("R6"))
        self.generate_ret()

    def generate_loop_start(self):
        self.program.append("LOOP_START_" + str(self.enter_loop()))

    def generate_loop_end(self):
        self.program.append("LOOP_END_" + str(self.leave_loop()))

    def generate_if_end(self):
        self.program.append("IF_END" + str(self.leave_if()))

    def generate_else_end(self):
        self.program.append("ELSE_END_" + str(self.leave_if()))

    def generate_if_condition(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_cmp("R0", 0))
        self.program.append(Command.build_jp_with_condition(
            "Z", "IF_END_" + str(self.enter_if())))

    def generate_loop_condition(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_cmp("R0", 0))
        self.program.append(Command.build_jp_with_condition(
            "Z", "LOOP_END_" + str(self.current_loop())))

    # --------------------------------------------------------------------

    def generate_broj(self, num):
        self.program.append(Command.build_move(num, "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_znak(self, char):
        self.program.append(Command.build_move(ord(char), "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_niz_znakova(self, string):
        to_write = list()

        for char in string:
            to_write.append(Command.build_move(ord(char), "R0"))
            to_write.append(Command.build_push("R0"))

        self.program.extend(to_write)

    def generate_idn_get(self, adr):
        self.program.append(Command.build_load("R0", adr))
        self.program.append(Command.build_push("R0"))

    # todo nakon mul
    def generate_niz_get(self, adr):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_move(adr, "R1"))
        self.program.append(Command.build_add("R0", "R1", "R0"))
        self.program.append(Command.build_load_from_register("R0", "R0", 0))
        self.program.append(Command.build_push("R0"))

    def generate_ctx_save(self):
        self.program.append(Command.build_push("R0"))
        self.program.append(Command.build_push("R1"))
        self.program.append(Command.build_push("R2"))
        self.program.append(Command.build_push("R3"))
        self.program.append(Command.build_push("R4"))
        self.program.append(Command.build_push("R5"))

    def generate_ctx_load(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_pop("R2"))
        self.program.append(Command.build_pop("R3"))
        self.program.append(Command.build_pop("R4"))
        self.program.append(Command.build_pop("R5"))

    def generate_post_inc(self, adr):
        self.program.append(Command.build_load("R0", adr))
        self.program.append(Command.build_push("R0"))
        self.program.append(Command.build_add("R0", 1, "R0"))
        self.program.append(Command.build_store("R0", adr))

    def generate_post_dec(self, adr):
        self.program.append(Command.build_load("R0", adr))
        self.program.append(Command.build_push("R0"))
        self.program.append(Command.build_sub("R0", 1, "R0"))
        self.program.append(Command.build_store("R0", adr))

    def generate_pre_inc(self, adr):
        self.program.append(Command.build_load("R0", adr))
        self.program.append(Command.build_add("R0", 1, "R0"))
        self.program.append(Command.build_push("R0"))
        self.program.append(Command.build_store("R0", adr))

    def generate_pre_dec(self, adr):
        self.program.append(Command.build_load("R0", adr))
        self.program.append(Command.build_sub("R0", 1, "R0"))
        self.program.append(Command.build_push("R0"))
        self.program.append(Command.build_store("R0", adr))

    def generate_u_minus(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_move(0, "R1"))
        self.program.append(Command.build_sub("R1", "R0", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_u_tilda(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_move(0, "R1"))
        self.program.append(Command.build_sub("R1", 1, "R1"))
        self.program.append(Command.build_xor("R0", "R1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_u_neg(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_cmp("R0", 0))
        self.program.append(Command.build_jr_with_condition("Z", 8))
        self.program.append(Command.build_move(0, "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move(1, "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_add(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_add("R0", "R1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_sub(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_sub("R0", "R1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_gt(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_cmp("R0", "R1"))
        self.program.append(Command.build_jr_with_condition("SGT", 8))
        self.program.append(Command.build_move("0", "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move("1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_lt(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_cmp("R0", "R1"))
        self.program.append(Command.build_jr_with_condition("SLT", 8))
        self.program.append(Command.build_move("0", "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move("1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_gte(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_cmp("R0", "R1"))
        self.program.append(Command.build_jr_with_condition("SGE", 8))
        self.program.append(Command.build_move("0", "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move("1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_lte(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_cmp("R0", "R1"))
        self.program.append(Command.build_jr_with_condition("SLE", 8))
        self.program.append(Command.build_move("0", "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move("1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_eq(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_cmp("R0", "R1"))
        self.program.append(Command.build_jr_with_condition("EQ", 8))
        self.program.append(Command.build_move("0", "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move("1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_neq(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_cmp("R0", "R1"))
        self.program.append(Command.build_jr_with_condition("NE", 8))
        self.program.append(Command.build_move("0", "R0"))
        self.program.append(Command.build_jr(4))
        self.program.append(Command.build_move("1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_bin_and(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_and("R0", "R1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_bin_xor(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_xor("R0", "R1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_bin_or(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_or("R0", "R1", "R0"))
        self.program.append(Command.build_push("R0"))

    def generate_log_and(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_move("R2", "0"))
        self.program.append(Command.build_cmp("R0", "0"))
        self.program.append(Command.build_jr_with_condition("Z", 16))
        self.program.append(Command.build_move("R2", "1"))
        self.program.append(Command.build_cmp("R1", "0"))
        self.program.append(Command.build_jr_with_condition("Z", 4))
        self.program.append(Command.build_move("R2", "1"))
        self.program.append(Command.build_push("R2"))

    def generate_log_or(self):
        self.program.append(Command.build_pop("R0"))
        self.program.append(Command.build_pop("R1"))
        self.program.append(Command.build_move("R2", "1"))
        self.program.append(Command.build_cmp("R0", "0"))
        self.program.append(Command.build_jr_with_condition("NZ", 16))
        self.program.append(Command.build_move("R2", "0"))
        self.program.append(Command.build_cmp("R1", "0"))
        self.program.append(Command.build_jr_with_condition("NZ", 4))
        self.program.append(Command.build_move("R2", "0"))
        self.program.append(Command.build_push("R2"))
