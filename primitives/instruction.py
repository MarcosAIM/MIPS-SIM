from primitives.index import Index


def get_binary(number, size):
    return format(number, 'b').zfill(size)


def get_2_complement_for_imm(number, size):
    if number < 0:
        return bin(number & int('1' * size, 2))[2:]
    else:
        return get_binary(number, size)


class Instruction:
    index = None

    def __init__(self, instruction_string: str = None, index: Index = None):
        Instruction.index = index
        self.instruction_string = instruction_string.strip()
        self.i_type = None
        self.op_code = None
        self.register_d = None
        self.register_s = None
        self.register_t = None
        self.shift_value = None
        self.function_value = None
        self.immediate_value = None
        self.instruction_bits = None
        if instruction_string == "eop":
            pass
        else:
            self.initialize_fields()

    def initialize_fields(self):
        instruction_split = self.instruction_string.split()
        self.op_code = instruction_split[0]
        if self.op_code == 'nop':
            self.i_type = 0
            self.op_code = 0
            self.register_d = 0
            self.register_s = 0
            self.register_t = 0
            self.shift_value = 0
            self.function_value = 0
            self.immediate_value = 0
            self.instruction_bits = '000000000000000000000000000000000000'
            return
        op_code_num = int(Instruction.index["OpCode"][self.op_code])
        if op_code_num == 0 or op_code_num == 28:
            self.function_value = Instruction.index["Function"][self.op_code]
        self.op_code = op_code_num
        self.i_type = Instruction.get_i_type(self.op_code)

        if self.i_type == 'R':
            self.get_r_instruction_bits(instruction_split)
        elif self.i_type == 'I':
            self.get_i_instruction_bits(instruction_split)
        else:
            self.get_j_instruction_bits(instruction_split)

    @property
    def instruction_string(self):
        return self.__instruction_string

    @instruction_string.setter
    def instruction_string(self, instruction_string: str):
        if type(instruction_string) is not str:
            self.__instruction_string = None
        else:
            self.__instruction_string = instruction_string

    def get_r_instruction_bits(self, split):
        split_array = split
        self.register_d = split_array[1].replace(',', '')
        if self.op_code == 28:  # for multiply
            self.register_s = split_array[2].replace(',', '')
            self.register_t = split_array[3]
        elif self.function_value == 0 or self.function_value == 2:
            self.register_s = 0
            self.register_t = split_array[2].replace(',', '')
            self.immediate_value = int(split_array[3])
        else:
            self.register_s = split_array[2].replace(',', '')
            self.register_t = split_array[3]

        if self.register_d is None or self.register_s is None or self.register_t is None:
            raise TypeError

        rd_register_num = int(self.index["Registers"][self.register_d])
        rt_register_num = int(self.index["Registers"][self.register_t])
        if self.immediate_value is not None:
            rs_register_num = 0
            self.instruction_bits = get_binary(self.op_code, 6) + get_binary(rs_register_num, 5) + get_binary(
                rt_register_num, 5) + get_binary(rd_register_num, 5) + get_binary(self.immediate_value, 5) + get_binary(
                self.function_value, 6)
        else:
            rs_register_num = int(self.index["Registers"][self.register_s])
            self.instruction_bits = get_binary(self.op_code, 6) + get_binary(rs_register_num, 5) + get_binary(
                rt_register_num, 5) + get_binary(rd_register_num, 5) + get_binary(0, 5) + get_binary(
                self.function_value, 6)

    def get_i_instruction_bits(self, split):
        split_array = split
        if self.op_code == 4 or self.op_code == 8:
            self.register_t = split_array[1].replace(',', '')
            self.register_s = split_array[2].replace(',', '')
            self.immediate_value = int(split_array[3])
            rt_register_num = int(self.index["Registers"][self.register_t])
            rs_register_num = int(self.index["Registers"][self.register_s])

            self.instruction_bits = get_binary(self.op_code, 6) + get_binary(rs_register_num, 5) + get_binary(
                rt_register_num, 5) + get_2_complement_for_imm(self.immediate_value, 16)

        elif self.op_code == 43 or self.op_code == 35:
            self.register_t = split_array[1].replace(',', '')
            split_last = split_array[2].split('(')
            self.immediate_value = int(split_last[0])
            self.register_s = split_last[1].replace(')', '')
            rt_register_num = int(self.index["Registers"][self.register_t])
            rs_register_num = int(self.index["Registers"][self.register_s])
            self.instruction_bits = get_binary(self.op_code, 6) + get_binary(rs_register_num, 5) + get_binary(
                rt_register_num, 5) + get_2_complement_for_imm(self.immediate_value, 16)

    def get_j_instruction_bits(self, split):
        split_array = split
        self.immediate_value = int(int(split_array[1]))
        self.instruction_bits = get_binary(self.op_code, 6) + get_2_complement_for_imm(self.immediate_value, 26)

    @staticmethod
    def get_i_type(op_code=None):
        if op_code is None:
            return
        elif op_code == 0 or op_code == 28:
            return 'R'
        elif op_code == 2 or op_code == 3:
            return 'J'
        else:
            return 'I'
