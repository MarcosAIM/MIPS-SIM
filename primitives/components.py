class Unit:
    clock_time = 0

    def __init__(self):
        self.perform_task = self.perform

    def clock_update(self):
        if callable(self.perform_task):
            self.perform_task()

    def perform(self):
        pass

    @staticmethod
    def update_time():
        Unit.clock_time += 1


class Mux(Unit):
    def __init__(self):
        super().__init__()
        self.input_zero = None
        self.input_one = None
        self.in_signal = 0
        self.output = None
        self.perform_task = self.work

    def send_input_zero(self):
        pass

    def send_input_one(self):
        pass

    def work(self):
        if self.in_signal == 0:
            self.send_input_zero()
        else:
            self.send_input_one()
