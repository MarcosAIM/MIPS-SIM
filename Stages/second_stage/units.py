from primitives.components import Unit, Mux


class RegisterMemory(Unit):
    from Stages.third_stage.units import IDToEX

    def __init__(self, id_ex: IDToEX = None):
        super().__init__()
        self.perform_task = self.work
        self.Registers = []
        for _ in range(0, 32):
            self.Registers.append(0)
        self.readPort = '0'
        self.readPort2 = '0'
        self.outPort = 0
        self.outPort2 = 0
        self.writePort = '0'
        self.writeData = 0
        self.regWrite = 0
        self.id_ex = id_ex

    def handle_write_to_register(self):
        if self.regWrite == 1:
            index = int(self.writePort, 2)
            if index != 0:
                self.Registers[index] = self.writeData
                self.regWrite = 0

    def set_out_port_values(self):
        self.outPort = self.Registers[int(self.readPort, 2)]
        self.outPort2 = self.Registers[int(self.readPort2, 2)]

    def send_values(self):
        self.id_ex.val_one = self.outPort
        self.id_ex.val_two = self.outPort2

    def work(self):
        self.set_out_port_values()
        self.send_values()

    def print_info_to_console(self):
        print("========================REGISTER MEMORY=============================")
        print(f"Register {0:02} 00:{self.Registers[0]}", end='|')
        print(f"Register {8:02} t0:{self.Registers[8]}", end='|')
        print(f"Register {16:02} s0:{self.Registers[16]}", end='|')
        print(f"Register {24:02} t8:{self.Registers[24]}")

        print(f"Register {1:02} at:{self.Registers[1]}", end='|')
        print(f"Register {9:02} t1:{self.Registers[9]}", end='|')
        print(f"Register {17:02} s1:{self.Registers[17]}", end='|')
        print(f"Register {25:02} t9:{self.Registers[25]}")

        print(f"Register {2:02} v0:{self.Registers[2]}", end='|')
        print(f"Register {10:02} t2:{self.Registers[10]}", end='|')
        print(f"Register {18:02} s2:{self.Registers[18]}", end='|')
        print(f"Register {26:02} k0:{self.Registers[26]}")

        print(f"Register {3:02} v1:{self.Registers[3]}", end='|')
        print(f"Register {11:02} t3:{self.Registers[11]}", end='|')
        print(f"Register {19:02} s3:{self.Registers[19]}", end='|')
        print(f"Register {27:02} k1:{self.Registers[27]}")

        print(f"Register {4:02} a0:{self.Registers[4]}", end='|')
        print(f"Register {12:02} t4:{self.Registers[12]}", end='|')
        print(f"Register {20:02} s4:{self.Registers[20]}", end='|')
        print(f"Register {28:02} gp:{self.Registers[28]}")

        print(f"Register {5:02} a1:{self.Registers[5]}", end='|')
        print(f"Register {13:02} t5:{self.Registers[13]}", end='|')
        print(f"Register {21:02} s5:{self.Registers[21]}", end='|')
        print(f"Register {29:02} sp:{self.Registers[29]}")

        print(f"Register {6:02} a2:{self.Registers[6]}", end='|')
        print(f"Register {14:02} t6:{self.Registers[14]}", end='|')
        print(f"Register {22:02} s6:{self.Registers[22]}", end='|')
        print(f"Register {30:02} fp:{self.Registers[30]}")

        print(f"Register {7:02} a3:{self.Registers[7]}", end='|')
        print(f"Register {15:02} t7:{self.Registers[15]}", end='|')
        print(f"Register {23:02} s7:{self.Registers[23]}", end='|')
        print(f"Register {31:02} ra:{self.Registers[31]}")
        print("====================================================================")

        '''
        print("===================REGISTER MEMORY========================")
        for x in range(0, 32):
            if x % 4 is not 3 or x is 0:
                print(f"Register {x:02}:{self.Registers[x]}", end='|')
            else:
                print(f"Register {x:02}: {self.Registers[x]}")
        print("==========================================================")
        '''
    def reset(self):
        self.Registers.clear()
        for _ in range(0, 32):
            self.Registers.append(0)
        self.readPort = '0'
        self.readPort2 = '0'
        self.outPort = 0
        self.outPort2 = 0
        self.writePort = '0'
        self.writeData = 0
        self.regWrite = 0


class WAMux(Mux):
    from Stages.third_stage.units import IDToEX

    def __init__(self, id_ex: IDToEX = None):
        super().__init__()
        self.id_ex = id_ex

    def send_input_zero(self):
        self.id_ex.write_address = self.input_zero

    def send_input_one(self):
        self.id_ex.write_address = self.input_one


class ControlUnit(Unit):
    from Stages.third_stage.units import IDToEX

    def __init__(self, wa_mux: WAMux = None, id_ex: IDToEX = None):
        """RegDst, RegWrite, PC_SRC, MEM_READ ,MEM_WRITE ,MEM_TO_REG ,ALU_SRC ,__ALU_CTRL__"""
        super().__init__()
        self.R_SIGNALS = [0, 1, 0, 0, 0, 1, 0]
        self.SHIFT_SIGNALS = [0, 1, 0, 0, 0, 1, 1]
        self.BEQ_SIGNALS = [0, 0, 1, 0, 0, 0, 0]
        self.ADDI_SIGNALS = [1, 1, 0, 0, 0, 1, 1]
        self.SW_SIGNALS = [0, 0, 0, 0, 1, 0, 1]
        self.LW_SIGNALS = [1, 1, 0, 1, 0, 0, 1]
        self.J_SIGNALS = [0, 0, 1, 0, 0, 0, 0]
        self.op_code = None
        self.function = None
        self.wa_mux = wa_mux
        self.id_ex = id_ex
        self.Signal = [0, 0, 0, 0, 0, 0, 0]
        self.perform_task = self.work

    def set_control_signals(self):
        if self.op_code == 28:
            self.Signal = self.R_SIGNALS
        elif self.op_code == 0:
            if self.function == 0 or self.function == 2:
                self.Signal = self.SHIFT_SIGNALS
            else:
                self.Signal = self.R_SIGNALS
        elif self.op_code == 4:
            self.Signal = self.BEQ_SIGNALS
        elif self.op_code == 8:
            self.Signal = self.ADDI_SIGNALS
        elif self.op_code == 43:
            self.Signal = self.SW_SIGNALS
        elif self.op_code == 35:
            self.Signal = self.LW_SIGNALS
        elif self.op_code == 2:
            self.Signal = self.J_SIGNALS

    def send_signals(self):
        if len(self.Signal) == 0:
            return
        else:
            self.wa_mux.in_signal = self.Signal[0]
            self.id_ex.reg_write = self.Signal[1]
            self.id_ex.pc_src = self.Signal[2]
            self.id_ex.mem_read = self.Signal[3]
            self.id_ex.mem_write = self.Signal[4]
            self.id_ex.mem_to_reg = self.Signal[5]
            self.id_ex.alu_src = self.Signal[6]
            if self.op_code == 0:
                self.id_ex.alu_ctrl = self.function
            elif self.op_code == 2:
                self.id_ex.alu_ctrl = 77  # jump
            else:
                self.id_ex.alu_ctrl = self.op_code

    def work(self):
        self.set_control_signals()
        self.send_signals()

    def print_info_to_console(self):
        """RegDst, RegWrite, PC_SRC, MEM_READ ,MEM_WRITE ,MEM_TO_REG ,ALU_SRC ,__ALU_CTRL__"""
        print("=================CONTROL UNIT SIGNALS=====================")
        print("RegDst:" + str(self.Signal[0]), end=' ')
        print("RegWrite:" + str(self.Signal[1]), end=' ')
        print("PC_SRC:" + str(self.Signal[2]), end=' ')
        print("MEM_READ:" + str(self.Signal[3]))
        print("MEM_WRITE:" + str(self.Signal[4]), end=' ')
        print("MEM_TO_REG:" + str(self.Signal[5]), end=' ')
        print("ALU_SRC:" + str(self.Signal[6]), end=' ')
        print("ALU_CTRL:" + str(self.id_ex.alu_ctrl))
        print("==========================================================")

    def reset(self):
        self.Signal = [0, 0, 0, 0, 0, 0, 0]
        self.op_code = None
        self.function = None


class IFToID(Unit):
    from Stages.third_stage.units import IDToEX

    def __init__(self, rm: RegisterMemory = None, cu: ControlUnit = None, wam: WAMux = None, id_to_ex: IDToEX = None):
        from primitives.instruction import Instruction
        super().__init__()
        self.perform_task = self.work
        self.pc_address = None
        self.current_instruction: Instruction = Instruction("eop")

        self.rm = rm
        self.cu = cu
        self.wa_mux = wam
        self.id_to_ex = id_to_ex

    def send_to_rm(self):
        try:
            if self.current_instruction.op_code == 28:
                self.rm.readPort = self.current_instruction.instruction_bits[6:11]
            elif self.current_instruction.function_value == 0 or self.current_instruction.function_value == 2:
                self.rm.readPort = self.current_instruction.instruction_bits[11:16]
            else:
                self.rm.readPort = self.current_instruction.instruction_bits[6:11]
            self.rm.readPort2 = self.current_instruction.instruction_bits[11:16]
        except TypeError:
            return

    def send_to_cu(self):
        self.cu.op_code = self.current_instruction.op_code
        self.cu.function = self.current_instruction.function_value

    def send_to_wam(self):
        try:
            self.wa_mux.input_zero = self.current_instruction.instruction_bits[16:21]
            self.wa_mux.input_one = self.current_instruction.instruction_bits[11:16]
        except TypeError:
            return

    def send_to_id_ex(self):
        self.id_to_ex.pc_address = self.pc_address
        self.id_to_ex.val_imm = self.current_instruction.immediate_value

    def print_info_to_console(self):
        print("=================IF-TO-ID=================================")
        print(f"INSTRUCTION BITS: {self.current_instruction.instruction_bits}")
        print("==========================================================")

    def work(self):
        self.send_to_cu()
        self.send_to_rm()
        self.send_to_wam()
        self.send_to_id_ex()

    def reset(self):
        from primitives.instruction import Instruction
        self.pc_address = None
        self.current_instruction: Instruction = Instruction("eop")


class SecondStage(Unit):
    def __init__(self, if_id: IFToID):
        from Stages.third_stage.units import IDToEX
        super().__init__()
        self.perform_task = self.work
        self.if_id = if_id
        self.cu = ControlUnit()
        self.wa_mux = WAMux()
        self.rm = RegisterMemory()
        self.id_ex = IDToEX()
        self.Units = [self.if_id, self.cu, self.wa_mux, self.rm]

    def connect_parts(self):
        self.if_id.cu = self.cu
        self.if_id.wa_mux = self.wa_mux
        self.if_id.rm = self.rm
        self.if_id.id_to_ex = self.id_ex
        self.cu.wa_mux = self.wa_mux
        self.cu.id_ex = self.id_ex
        self.wa_mux.id_ex = self.id_ex
        self.rm.id_ex = self.id_ex

    def work(self):
        for unit in self.Units:
            unit.clock_update()

    def print_to_console(self):
        print("^^^^^^^^^^^^^^^^^^^^SECOND-STAGE^^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.cu.print_info_to_console()
        self.rm.print_info_to_console()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("^^^^^^^^^^^^^^^^^^^^State-Register^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.id_ex.print_info_to_console()

    def reset(self):
        self.rm.reset()
        self.if_id.reset()
        self.cu.reset()
