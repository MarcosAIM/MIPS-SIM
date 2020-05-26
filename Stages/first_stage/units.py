from primitives.components import Unit, Mux
from input_handlers.handlers import Packager


class InstructionMemory(Unit):
    from Stages.second_stage.units import IFToID

    def __init__(self, if_to_id: IFToID = None):
        super().__init__()
        self.end_reached = False
        self.perform_task = self.work
        self.instruction_list = ["Head"]
        self.current_instruction = None
        self.current_pc_address = 0
        self.if_to_id = if_to_id

    @property
    def current_pc_address(self):
        return self.__current_pc_address

    @current_pc_address.setter
    def current_pc_address(self, current_pc_address: int):
        self.__current_pc_address = current_pc_address
        if not self.end_reached and self.__current_pc_address <= len(self.instruction_list) * 4 - 4:
            self.current_instruction = self.instruction_list[current_pc_address // 4]

    def send_instruction_to_if_to_id(self):
        self.if_to_id.current_instruction = self.current_instruction

    def load_program(self, instructions):
        if isinstance(instructions, list):
            self.instruction_list = instructions
        else:
            pass

    def work(self):
        self.send_instruction_to_if_to_id()

    def print_info_to_console(self):
        print("================INSTRUCTION MEMORY INFO===================")
        if self.current_instruction is not None and self.current_instruction != 'Head':
            print("CURRENT INSTRUCTION: " + str(self.current_instruction.instruction_string))
        else:
            print("CURRENT INSTRUCTION: NONE ")
        print("==========================================================")

    def reset(self):
        self.instruction_list = ["Head"]
        self.current_instruction = None
        self.current_pc_address = 0
        self.end_reached = False


class AddressMux(Mux):
    def __init__(self):
        super().__init__()
        self.input_zero = 0

    def reset(self):
        self.input_zero = 0


class AddPC:
    def __init__(self, address_mux: AddressMux = None):
        super().__init__()
        self.operand_two = 4
        self.operand_one = 0
        self.result = 0
        self.address_mux = address_mux

    def add_to_result(self):
        self.result = self.operand_one + self.operand_two

    @property
    def operand_one(self):
        return self.__operand_one

    @operand_one.setter
    def operand_one(self, op_one):
        self.__operand_one = op_one
        self.add_to_result()

    def send_address_to_mux(self):
        self.address_mux.input_zero = self.result

    def reset(self):
        self.operand_one = 0
        self.result = 0


class Pc(Unit):
    from Stages.second_stage.units import IFToID

    def __init__(self, if_to_id: IFToID = None, instruction_memory: InstructionMemory = None, add_pc: AddPC = None,
                 address_mux: AddressMux = None):
        super().__init__()
        self.perform_task = self.work
        self.current_pc_address = 0
        self.if_to_id = if_to_id
        self.instruction_memory = instruction_memory
        self.add_pc = add_pc
        self.address_mux = address_mux

    def send_next_instruction_to_im(self):
        self.instruction_memory.current_pc_address = self.current_pc_address

    def send_next_instruction_to_if_to_id(self):
        self.if_to_id.pc_address = self.current_pc_address

    def send_instruction_to_add_pc(self):
        self.add_pc.operand_one = self.current_pc_address

    def get_ins_from_address_mux(self):
        if self.address_mux.in_signal == 0:
            self.current_pc_address = self.address_mux.input_zero
        else:
            self.current_pc_address = self.address_mux.input_one
            self.address_mux.in_signal = 0

    def determine_end_of_ins(self):
        if self.current_pc_address >= len(self.instruction_memory.instruction_list) * 4:
            self.instruction_memory.end_reached = True
            self.instruction_memory.current_instruction.instruction_string = 'end of instructions.'

    def work(self):
        self.get_ins_from_address_mux()
        self.determine_end_of_ins()
        if not self.instruction_memory.end_reached:
            self.send_next_instruction_to_im()
            self.send_instruction_to_add_pc()
            self.add_pc.send_address_to_mux()
            self.get_ins_from_address_mux()
            self.send_next_instruction_to_if_to_id()

    def print_info_to_console(self):
        print("=======================PC INFO============================")
        print("PC Address:" + str(self.current_pc_address))
        print("==========================================================")

    def reset(self):
        self.current_pc_address = 0


class FirstStage(Unit):
    def __init__(self, packager: Packager):
        from Stages.second_stage.units import IFToID
        super().__init__()
        self.perform_task = self.work
        self.packager = packager
        self.pc = Pc()
        self.IM = InstructionMemory()
        self.if_id = IFToID()
        self.add_pc = AddPC()
        self.address_mux = AddressMux()
        self.Units = [self.pc, self.IM]

    def load_instruction_memory(self):
        self.IM.load_program(self.packager.instruction_list)
        self.pc.current_pc_address = 0
        self.IM.end_reached = False

    def connect_parts(self):
        self.pc.if_to_id = self.if_id
        self.pc.instruction_memory = self.IM
        self.IM.if_to_id = self.if_id
        self.pc.add_pc = self.add_pc
        self.add_pc.address_mux = self.address_mux
        self.pc.address_mux = self.address_mux

    def work(self):
        if not self.IM.end_reached:
            for unit in self.Units:
                unit.clock_update()
        else:
            print("END REACHED. RELOAD INSTRUCTION MEMORY")

    def print_info_to_console(self):
        print("^^^^^^^^^^^^^^^^^^^^^FIRST-STAGE^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.pc.print_info_to_console()
        self.IM.print_info_to_console()
        print("^^^^^^^^^^^^^^^^^^^^State-Register^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.if_id.print_info_to_console()

    def reset(self):
        self.pc.reset()
        self.IM.reset()
        self.address_mux.reset()
        self.add_pc.reset()
