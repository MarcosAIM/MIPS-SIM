import os

from primitives.components import Unit

memory_file_name = "memory.dat"


class Memory(Unit):
    from Stages.fifth_stage.units import MemToReg

    def __init__(self, mem_reg: MemToReg = None):
        super().__init__()
        self.perform_task = self.work
        self.mem_read = None
        self.mem_write = None
        self.address = None
        self.write_value = None
        self.read_value = None
        self.mem_reg = mem_reg
        self.memory_list = []

    def write_to_memory(self):
        in_memory = False
        with open(memory_file_name, 'r') as r:
            memory = r.readlines()
            counter = 0
            for block in memory:
                if block is not None:
                    s_block = block.split()
                    if int(s_block[0]) is self.address:
                        in_memory = True
                        memory[counter] = str(self.address) + " " + str(self.write_value) + "\n"
                        break
                counter += 1
            if in_memory:
                with open(memory_file_name, 'w') as w:
                    w.writelines(memory)
            else:
                with open(memory_file_name, 'a') as a:
                    a.write(str(self.address) + " " + str(self.write_value) + "\n")

    def read_from_memory(self):
        in_memory = False
        with open(memory_file_name, 'r') as r:
            memory = r.readlines()
            for block in memory:
                if block is not None:
                    s_block = block.split()
                    if int(s_block[0]) is self.address:
                        in_memory = True
                        self.read_value = int(s_block[1])
                        break
        if not in_memory:
            self.read_value = 99999999999999999

    def load_memory_into_list(self):
        self.memory_list.clear()
        try:
            with open(memory_file_name, 'r') as r:
                memory = r.readlines()
                for block in memory:
                    if block is not None:
                        s_block = block.split()
                        self.memory_list.append(s_block[0])
                        self.memory_list.append(s_block[1])
        except FileNotFoundError:
            self.memory_list = []

    def send_to_mem_reg(self):
        self.mem_reg.mem_value = self.read_value

    def print_to_console(self):
        print("=====================MAIN-MEMORY==========================")
        print("Address :           VALUE")
        if len(self.memory_list) != 0:
            for x in range(0, len(self.memory_list), 2):
                print(f'{format(int(self.memory_list[x]), "#016x")}', end=':      ')
                print(self.memory_list[x + 1])
        else:
            print("EMPTY")
        print("==========================================================")

    def work(self):
        if self.mem_write == 1:
            self.write_to_memory()
        elif self.mem_read == 1:
            self.read_from_memory()
        self.send_to_mem_reg()

    def reset(self):
        self.memory_list = []
        self.mem_read = None
        self.mem_write = None
        self.address = None
        self.write_value = None
        self.read_value = None


class ExToMem(Unit):
    from Stages.fifth_stage.units import MemToReg

    def __init__(self, mem_reg: MemToReg = None, memory: Memory = None):
        super().__init__()
        self.perform_task = self.work
        self.mem_read = None
        self.mem_write = None
        self.mem_to_reg = None
        self.reg_write = None
        self.alu_result = None
        self.write_value = None
        self.reg_address = None
        self.mem_reg = mem_reg
        self.memory = memory

    def send_to_mem_reg(self):
        self.mem_reg.mem_to_reg = self.mem_to_reg
        self.mem_reg.alu_result = self.alu_result
        self.mem_reg.reg_address = self.reg_address
        self.mem_reg.reg_write = self.reg_write

    def send_to_mem(self):
        self.memory.mem_read = self.mem_read
        self.memory.write_value = self.write_value
        self.memory.mem_write = self.mem_write
        self.memory.address = self.alu_result

    def work(self):
        self.send_to_mem()
        self.send_to_mem_reg()

    def reset(self):
        self.mem_read = None
        self.mem_write = None
        self.mem_to_reg = None
        self.reg_write = None
        self.alu_result = None
        self.write_value = None
        self.reg_address = None

    def print_info_to_console(self):
        print("=================EX-TO-MEM===============================")
        print(f'MEM READ:{self.mem_read}', end='|')
        print(f'MEM WRITE:{self.mem_write}', end='|')
        print(f'ALU RESULT:{self.alu_result}', end='|')
        print(f'MEM TO REG:{self.mem_to_reg}')
        print(f'REG WRITE:{self.reg_write}', end='|')
        print(f'REG WRITE ADDR:{self.reg_address}', end='|')
        print(f'MEM WRITE VALUE:{self.write_value}')
        print("==========================================================")


class FourthStage(Unit):
    def __init__(self, ex_mem: ExToMem):
        from Stages.fifth_stage.units import MemToReg
        super().__init__()
        self.perform_task = self.work
        self.ex_mem = ex_mem
        self.memory = Memory()
        self.mem_reg = MemToReg()
        self.Units = [self.ex_mem, self.memory]
        FourthStage.initialize_memory_storage()

    def connect_parts(self):
        self.ex_mem.memory = self.memory
        self.ex_mem.mem_reg = self.mem_reg
        self.memory.mem_reg = self.mem_reg

    def work(self):
        for unit in self.Units:
            unit.clock_update()

    def print_to_console(self):
        print("^^^^^^^^^^^^^^^^^^^^^FOURTH-STAGE^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.memory.load_memory_into_list()
        self.memory.print_to_console()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("^^^^^^^^^^^^^^^^^^^^State-Register^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.mem_reg.print_info_to_console()

    def reset(self):
        self.memory.reset()
        self.ex_mem.reset()

    @staticmethod
    def clean_memory():
        try:
            os.remove(memory_file_name)
        except FileNotFoundError:
            return

    @staticmethod
    def initialize_memory_storage():
        try:
            with open(memory_file_name, "x"):
                pass
        except FileExistsError:
            return
