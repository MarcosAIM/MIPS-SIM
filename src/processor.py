from input_handlers.handlers import Packager, Reader
from primitives.index import Index
from Stages.first_stage.units import FirstStage
from Stages.second_stage.units import SecondStage
from Stages.third_stage.units import ThirdStage
from Stages.fourth_stage.units import FourthStage
from Stages.fifth_stage.units import FifthStage
from primitives.components import Unit

'''
1. Call Load file with path of file
2. Call set_packager to translate it for the Instruction Memory
3. Call load_instruction_memory to load it
4. Call load_file_into_im to do this process
'''


class Processor(Unit):
    def __init__(self):
        super().__init__()
        self.mode = 0
        self.set_mode()
        self.reader = Reader()
        self.file_stream = None
        self.index_path = None
        self.packager = Packager()
        self.first_stage = FirstStage(self.packager)
        self.second_stage = SecondStage(self.first_stage.if_id)
        self.third_stage = ThirdStage(self.first_stage.address_mux, self.second_stage.id_ex)
        self.fourth_stage = FourthStage(self.third_stage.ex_mem)
        self.fifth_stage = FifthStage(self.fourth_stage.mem_reg, self.second_stage.rm)
        self.set_index()
        self.connect_stages()
        self.scheduler = []
        self.code = 0

    '''Creates Index JSON FILE FOR PACKAGER and sets Packager to use index json file'''

    def set_index(self):
        Index.create_index()
        self.index_path = Index.absolute_path
        self.packager.index = str(self.index_path)

    '''Sets the path name of the file and reads it into an input stream'''

    def load_file(self, path_of_file):
        self.reader.file_path = path_of_file
        self.file_stream = self.reader.read_file()

    '''SETS PACKAGER INPUT STREAM, Then translates it for IM. call after loading file from READER'''

    def set_packager(self):
        self.packager.input_stream = self.file_stream
        self.packager.translate()

    '''First Translate input stream from file then loads it into instruction memory. call after set_packager'''

    def load_instruction_memory(self):
        self.first_stage.load_instruction_memory()

    '''Loads the specified asm file into the Instruction Memory'''

    def load_file_into_im(self, file_path: str):
        if type(file_path) is str:
            self.load_file(file_path)
            self.set_packager()
            self.load_instruction_memory()
        else:
            print("<ERROR: FILE NOT LOADED INTO IM>")

    '''Connects All Stage Components'''

    def connect_stages(self):
        self.first_stage.connect_parts()
        self.second_stage.connect_parts()
        self.third_stage.connect_parts()
        self.fourth_stage.connect_parts()
        self.fifth_stage.connect_parts()

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode: int):
        if type(mode) is not int:
            self.__mode = 1
        else:
            self.__mode = mode
            self.set_mode()

    def set_mode(self):
        if self.mode == 1:
            self.perform_task = self.cycle_all_one_by_one
        elif self.mode == 11:
            self.perform_task = self.pipeline_instructions
        elif self.mode == 22:
            self.perform_task = self.pipeline_ins_to_end
        else:
            self.perform_task = self.cycle_instruction_through_all_stages

    '''mode = 0. pass next instruction through all stages'''

    def pipeline_instructions(self):
        Unit.update_time()
        counter = 0
        delete = None
        for stage in self.scheduler:
            if stage == 2:
                self.second_stage.clock_update()
                self.scheduler[counter] += 1  # increase stage
            elif stage == 3:
                self.third_stage.clock_update()
                self.scheduler[counter] += 1  # increase stage
            elif stage == 4:
                self.fourth_stage.clock_update()
                self.scheduler[counter] += 1  # increase stage
            elif stage == 5:
                self.fifth_stage.clock_update()
                self.scheduler[counter] += 1  # increase stage
            else:
                delete = counter
            counter += 1

        if delete is not None:
            self.scheduler.pop(delete)  # get rid of it

        self.first_stage.clock_update()
        if not self.first_stage.IM.end_reached:
            self.scheduler.append(2)

        if len(self.scheduler) == 0:
            self.code = 0
        else:
            self.code = 1

    def pipeline_ins_to_end(self):
        code = 1
        while code == 1:
            self.pipeline_instructions()
            code = self.code

    def cycle_instruction_through_all_stages(self):
        self.first_stage.clock_update()
        Unit.update_time()
        if not self.first_stage.IM.end_reached:
            self.second_stage.clock_update()
            Unit.update_time()
            self.third_stage.clock_update()
            Unit.update_time()
            self.fourth_stage.clock_update()
            Unit.update_time()
            self.fifth_stage.clock_update()
            Unit.update_time()
            self.code = 1
        else:
            self.code = 0

    '''mode = 1 pass all instructions through all stages one by one'''

    def cycle_all_one_by_one(self):
        while not self.first_stage.IM.end_reached:
            self.cycle_instruction_through_all_stages()

    def clean(self):
        self.first_stage.reset()
        self.second_stage.reset()
        self.third_stage.reset()
        self.fourth_stage.reset()
        self.fourth_stage.clean_memory()
        self.fifth_stage.reset()
        Unit.clock_time = 0

    @staticmethod
    def delete_index():
        Index.destroy_index()
