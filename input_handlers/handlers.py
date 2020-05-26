import json
from primitives.instruction import Instruction


class Reader:
    def __init__(self, path: str = ""):
        self.file_path = path

    '''Current file_path Property'''

    @property
    def file_path(self):
        return self.__filePath

    @file_path.setter
    def file_path(self, path: str):
        if type(path) is not str:
            print("<ERROR: FILE NAME IS NOT STRING>")
            self.__filePath = None
        else:
            self.__filePath = path

    '''++++++++++++++++++++++++++++++++++'''

    def read_file(self):
        try:
            with open(self.file_path, 'r') as asm_file:
                if asm_file.mode == 'r':
                    text = asm_file.readlines()
                    asm_file.close()
                    return text
        except FileNotFoundError:
            raise FileNotFoundError("<ERROR: FILE NOT FOUND>")


class Packager:
    def __init__(self, input_stream: list = None, idx_path: str = None):
        self.input_stream = input_stream
        self.index = idx_path
        self.instruction_list = []

    @property
    def input_stream(self):
        return self.__input_stream

    @input_stream.setter
    def input_stream(self, input_stream: list):
        if type(input_stream) is not list:

            self.__input_stream = None
        else:
            self.__input_stream = input_stream

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, idx_file_path: str = None):
        if type(idx_file_path) is str:
            try:
                with open(idx_file_path, 'r') as read:
                    self.__index = json.loads(read.read())
            except FileNotFoundError:
                self.__index = None

    def translate(self):
        try:
            for instruction in self.input_stream:
                instruction = Packager.ignore_comments(instruction)
                spaced = instruction.split()
                if not spaced:
                    pass
                elif spaced[0] in self.index["OpCode"]:
                    new_instruction = Instruction(instruction, self.index)
                    self.instruction_list.append(new_instruction)
                else:
                    pass
        except TypeError:
            return

    @staticmethod
    def ignore_comments(instruction: str):
        if instruction is None or instruction == "" or type(instruction) is not str:
            return ""
        else:
            if instruction[0] == "#":
                return ""
            else:
                counter = 0
                for char in instruction:
                    if char == "#":
                        break
                    else:
                        counter += 1
                instruction = instruction[0:counter]
                return instruction
