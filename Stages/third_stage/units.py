from primitives.components import Unit, Mux


class AddressMux(Mux):
    def __init__(self):
        super().__init__()


class AddAddress(Unit):
    def __init__(self, address_mux: AddressMux = None):
        super().__init__()
        self.perform_task = self.work
        self.val_one = None
        self.val_two = None
        self.result = None
        self.address_mux = address_mux

    def get_result(self):
        self.result = self.val_one + self.val_two

    def send_address_to_mux(self):
        self.address_mux.input_one = self.result

    def work(self):
        if self.val_two is not None:
            self.get_result()
            self.send_address_to_mux()

    def print_to_console(self):
        print("=====================ADD ADDRESS==========================")
        print(f"ADDRESS: {self.val_one}", end='  ')
        print(f"SHIFTED IMM: {self.val_two}", end='  ')
        print(f"RESULT: {self.result}")
        print("==========================================================")


class ShiftLeft(Unit):
    def __init__(self, add_address: AddAddress = None):
        super().__init__()
        self.perform_task = self.work
        self.val_one = None
        self.result = None
        self.add_address = add_address

    def get_result(self):
        if self.val_one is not None:
            self.result = self.val_one << 2

    def send_to_add_address(self):
        self.add_address.val_two = self.result

    def work(self):
        self.get_result()
        self.send_to_add_address()


class AndGate(Unit):
    def __init__(self, address_mux: AddressMux = None):
        super().__init__()
        self.perform_task = self.work
        self.val_one = None
        self.val_two = None
        self.result = None
        self.address_mux = address_mux

    def get_result(self):
        if self.val_one is not None and self.val_two is not None:
            self.result = self.val_one & self.val_two

    def send_result_to_mux(self):
        self.address_mux.in_signal = self.result

    def work(self):
        self.get_result()
        self.send_result_to_mux()

    def print_to_console(self):
        print("=====================AND GATE==========================")
        print(f"PC SRC: {self.val_one}", end='  ')
        print(f"ALU RESULT: {self.val_two}", end='  ')
        print(f"RESULT: {self.result}")
        print("==========================================================")


class ALU(Unit):
    from Stages.fourth_stage.units import ExToMem

    def __init__(self, and_gate: AndGate = None, ex_to_mem: ExToMem = None):
        super().__init__()
        self.perform_task = self.work
        self.val_one = None
        self.val_two = None
        self.result = None
        self.alu_ctrl = None
        self.and_gate = and_gate
        self.ex_mem = ex_to_mem

    def get_result(self):
        if self.alu_ctrl == 32 or self.alu_ctrl == 8 or self.alu_ctrl == 43 or self.alu_ctrl == 35:
            self.result = self.val_one + self.val_two
        elif self.alu_ctrl == 34:
            self.result = self.val_one - self.val_two
        elif self.alu_ctrl == 28:
            self.result = self.val_one * self.val_two
        elif self.alu_ctrl == 36:
            self.result = self.val_one & self.val_two
        elif self.alu_ctrl == 37:
            self.result = self.val_one | self.val_two
        elif self.alu_ctrl == 0:
            self.result = self.val_one << self.val_two
        elif self.alu_ctrl == 2:
            self.result = self.val_one >> self.val_two
        elif self.alu_ctrl == 4:
            if self.val_one is self.val_two:
                self.result = 1
            else:
                self.result = 0
        elif self.alu_ctrl == 77:
            self.result = 1
        else:
            pass

    def send_to_and_gate(self):
        self.and_gate.val_two = self.result

    def send_to_ex_mem(self):
        self.ex_mem.alu_result = self.result

    def work(self):
        self.get_result()
        self.send_to_and_gate()
        self.send_to_ex_mem()

    def print_to_console(self):
        print("========================ALU==============================")
        print(f"INPUT 1: {self.val_one}", end='  ')
        print(f"INPUT 2: {self.val_two}", end='  ')
        print(f"RESULT: {self.result}")
        print("==========================================================")

    def reset(self):
        self.val_one = None
        self.val_two = None
        self.result = None
        self.alu_ctrl = None


class ALUSrcMux(Mux):
    def __init__(self, alu: ALU = None):
        super().__init__()
        self.ALU = alu

    def send_input_zero(self):
        self.ALU.val_two = self.input_zero

    def send_input_one(self):
        self.ALU.val_two = self.input_one


class IDToEX(Unit):
    from Stages.fourth_stage.units import ExToMem

    def __init__(self, alu_src_mux: ALUSrcMux = None, alu: ALU = None, and_gate: AndGate = None,
                 add_address: AddAddress = None, shift_left: ShiftLeft = None, ex_to_mem: ExToMem = None):
        super().__init__()
        self.perform_task = self.work
        self.pc_address = None
        self.pc_src = None
        self.mem_read = None
        self.mem_write = None
        self.mem_to_reg = None
        self.alu_src = None
        self.alu_ctrl = None
        self.val_one = None
        self.val_two = None
        self.write_address = None
        self.reg_write = None
        self.val_imm = None

        self.alu_src_mux = alu_src_mux
        self.alu = alu
        self.and_gate = and_gate
        self.add_address = add_address
        self.shift_left = shift_left
        self.ex_mem = ex_to_mem

    def send_to_alu_src_mux(self):
        self.alu_src_mux.input_zero = self.val_two
        self.alu_src_mux.input_one = self.val_imm
        self.alu_src_mux.in_signal = self.alu_src

    def send_to_alu(self):
        self.alu.val_one = self.val_one
        self.alu.alu_ctrl = self.alu_ctrl

    def send_to_and_gate(self):
        self.and_gate.val_one = self.pc_src

    def send_to_add_address(self):
        self.add_address.val_one = self.pc_address

    def send_to_shift_left(self):
        self.shift_left.val_one = self.val_imm

    def send_to_ex_mem(self):
        self.ex_mem.mem_read = self.mem_read
        self.ex_mem.mem_write = self.mem_write
        self.ex_mem.mem_to_reg = self.mem_to_reg
        self.ex_mem.write_value = self.val_two
        self.ex_mem.reg_address = self.write_address
        self.ex_mem.reg_write = self.reg_write

    def work(self):
        self.send_to_alu_src_mux()
        self.send_to_alu()
        self.send_to_and_gate()
        self.send_to_add_address()
        self.send_to_shift_left()
        self.send_to_ex_mem()

    def print_info_to_console(self):
        print("=================ID-TO-EX=================================")
        print(f'PC ADDR:{self.pc_address}', end='|')
        print(f'PC SRC:{self.pc_src}', end='|')
        print(f'MEM READ:{self.mem_read}', end='|')
        print(f'MEM WRITE:{self.mem_write}', end='|')
        print(f'MEM TO REG:{self.mem_to_reg}')
        print(f'ALU SRC:{self.alu_src}', end='|')
        print(f'ALU CTRL:{self.alu_ctrl}', end='|')
        print(f'REG ONE VALUE:{self.val_one}', end='|')
        print(f'REG TWO VALUE:{self.val_two}')
        print(f'REG WRITE ADDR:{self.write_address}', end='|')
        print(f'REG WRITE:{self.reg_write}', end='|')
        print(f'IMM VALUE:{self.val_imm}')
        print("==========================================================")

    def reset(self):
        self.pc_address = None
        self.pc_src = None
        self.mem_read = None
        self.mem_write = None
        self.mem_to_reg = None
        self.alu_src = None
        self.alu_ctrl = None
        self.val_one = None
        self.val_two = None
        self.write_address = None
        self.reg_write = None
        self.val_imm = None


class ThirdStage(Unit):
    def __init__(self, address_mux: AddressMux, id_ex: IDToEX):
        from Stages.fourth_stage.units import ExToMem
        super().__init__()
        self.perform_task = self.work
        self.id_ex = id_ex
        self.alu_src_mux = ALUSrcMux()
        self.alu = ALU()
        self.and_gate = AndGate()
        self.shift_left = ShiftLeft()
        self.add_address = AddAddress()
        self.address_mux = address_mux
        self.ex_mem = ExToMem()
        self.Units = [self.id_ex, self.alu_src_mux, self.shift_left, self.alu, self.add_address, self.and_gate]

    def connect_parts(self):
        self.id_ex.add_address = self.add_address
        self.id_ex.and_gate = self.and_gate
        self.id_ex.ex_mem = self.ex_mem
        self.id_ex.alu = self.alu
        self.id_ex.alu_src_mux = self.alu_src_mux
        self.id_ex.shift_left = self.shift_left
        self.add_address.address_mux = self.address_mux
        self.shift_left.add_address = self.add_address
        self.and_gate.address_mux = self.address_mux
        self.alu_src_mux.ALU = self.alu
        self.alu.and_gate = self.and_gate
        self.alu.ex_mem = self.ex_mem

    def work(self):
        for unit in self.Units:
            unit.clock_update()

    def print_to_console(self):
        print("^^^^^^^^^^^^^^^^^^^^THIRD-STAGE^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.alu.print_to_console()
        self.add_address.print_to_console()
        self.and_gate.print_to_console()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("^^^^^^^^^^^^^^^^^^^^State-Register^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.ex_mem.print_info_to_console()

    def reset(self):
        self.alu.reset()
        self.id_ex.reset()
