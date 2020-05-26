from primitives.components import Unit, Mux


class RegisterMemory(Unit):
    def __init__(self):
        super().__init__()
        self.Registers = []
        for _ in range(0, 32):
            self.Registers.append(_)
        self.readPort = '0'
        self.readPort2 = '0'
        self.outPort = 0
        self.outPort2 = 0
        self.writePort = '0'
        self.writeData = 0
        self.regWrite = 0

    def handle_write_to_register(self):
        if self.regWrite == 1:
            index = self.Registers[int(self.writePort, 2)]
            if index != 0:
                self.Registers[index] = self.writeData
                self.regWrite = 0


class RegValueMux(Mux):
    def __init__(self, rm: RegisterMemory = None):
        super().__init__()
        self.rm = rm

    def send_input_zero(self):
        self.rm.writeData = self.input_zero

    def send_input_one(self):
        self.rm.writeData = self.input_one

    def print_to_console(self):
        print("================REGISTER-VALUE-MUX========================")
        print(f"0.MEMORY VALUE: {self.input_zero}")
        print(f"1.ALU VALUE: {self.input_one}")
        print(f"DECIDING VALUE: {self.in_signal}")
        print("==========================================================")


class MemToReg(Unit):
    def __init__(self, reg_val_mux: RegValueMux = None, rm: RegisterMemory = None):
        super().__init__()
        self.perform_task = self.work
        self.mem_to_reg = None
        self.mem_value = None
        self.alu_result = None
        self.reg_address = None
        self.reg_write = None
        self.reg_val_mux = reg_val_mux
        self.rm = rm

    def send_reg_val_mux(self):
        self.reg_val_mux.input_zero = self.mem_value
        self.reg_val_mux.input_one = self.alu_result
        self.reg_val_mux.in_signal = self.mem_to_reg

    def send_to_rm(self):
        self.rm.writePort = self.reg_address
        self.rm.regWrite = self.reg_write

    def work(self):
        self.send_reg_val_mux()
        self.send_to_rm()

    def reset(self):
        self.mem_to_reg = None
        self.mem_value = None
        self.alu_result = None
        self.reg_address = None
        self.reg_write = None

    def print_info_to_console(self):
        print("=================EX-TO-MEM===============================")
        print(f'MEM TO REG:{self.mem_to_reg}', end='|')
        print(f'MEM VALUE:{self.mem_value}', end='|')
        print(f'ALU RESULT:{self.alu_result}')
        print(f'REG FILE WRITE:{self.reg_write}', end='|')
        print(f'REG WRITE ADDR:{self.reg_address}')
        print("==========================================================")


class FifthStage(Unit):
    def __init__(self, mem_reg: MemToReg, rm: RegisterMemory):
        super().__init__()
        self.perform_task = self.work
        self.reg_value_mux = RegValueMux()
        self.mem_reg = mem_reg
        self.rm = rm
        self.Units = [self.mem_reg, self.reg_value_mux]

    def connect_parts(self):
        self.mem_reg.reg_val_mux = self.reg_value_mux
        self.mem_reg.rm = self.rm
        self.reg_value_mux.rm = self.rm

    def work(self):
        for unit in self.Units:
            unit.clock_update()
        self.rm.handle_write_to_register()

    def print_to_console(self):
        print("^^^^^^^^^^^^^^^^^^^^FIFTH-STAGE^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.reg_value_mux.print_to_console()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    def reset(self):
        self.mem_reg.reset()
