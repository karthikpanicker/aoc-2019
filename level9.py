from collections import defaultdict

class Interpreter:
    def __init__(self,instruction,previous):
        self.instructions = instruction
        self.instr_index = 0
        self.halted = False
        self.current_output_signal = 0
        self.previous_amp = previous
        self.waiting_for_input = False
        self.relative_base = 0

    def set_prev_amplifier(self,amp):
        self.previous_amp = amp

    def is_halted(self):
        return self.halted

    def get_output(self):
        return self.current_output_signal

    def get_pos(self,param_no):
        instr_length = 5
        operation_code_length = 2
        operation = str(self.instructions[self.instr_index])
        operation = operation.zfill(instr_length)
        #immediate = 1 position = 0 relative = 2
        digits = [int(d) for d in operation]
        mode = digits[instr_length - param_no - operation_code_length]
        if mode == 1:
            return self.instr_index + param_no

        x = self.instructions[self.instr_index + param_no]
        if mode == 2:
            return self.relative_base + x
        elif mode == 0:
            return x

    def get_param(self,param_no):
        return self.instructions[self.get_pos(param_no)]

    def parse(self, proginput=[]):
        while self.instr_index < len(self.instructions):
            operation = self.instructions[self.instr_index]
            if operation == 99:
                self.halted = True
                return self.current_output_signal
            opcode = self.instructions[self.instr_index] % 10
            if opcode == 3:
                pos = self.get_pos(1)
                self.instructions[pos] = proginput[0]
                self.instr_index = self.instr_index + 2
            elif opcode == 4:
                p = self.get_param(1)
                self.current_output_signal = p
                self.instr_index = self.instr_index + 2
            elif opcode == 1:
                p1, p2 = self.get_param(1) , self.get_param(2)
                pos = self.get_pos(3)
                self.instructions[pos] = p1 + p2
                self.instr_index = self.instr_index + 4
            elif opcode == 2:
                p1, p2 = self.get_param(1), self.get_param(2)
                pos = self.get_pos(3)
                self.instructions[pos] = p1 * p2
                self.instr_index = self.instr_index + 4
            elif opcode == 5:
                p1 = self.get_param(1)
                if p1 != 0:
                    self.instr_index = self.get_param(2)
                    continue
                self.instr_index = self.instr_index + 3
            elif opcode == 6:
                p1 = self.get_param(1)
                if p1 == 0:
                    self.instr_index = self.get_param(2)
                    continue
                self.instr_index = self.instr_index + 3
            elif opcode == 7:
                p1, p2 = self.get_param(1), self.get_param(2)
                out_pos = self.get_pos(3)
                self.instructions[out_pos] = int(p1 < p2)
                self.instr_index = self.instr_index + 4
            elif opcode == 8:
                p1, p2 = self.get_param(1), self.get_param(2)
                out_pos = self.get_pos(3)
                self.instructions[out_pos] = int(p1 == p2)
                self.instr_index = self.instr_index + 4
            elif opcode == 9:
                p = self.get_param(1)
                self.relative_base += p
                self.instr_index = self.instr_index + 2


def execute_amplifiers(amplifiers, phases):
    iterations = 0
    while not amplifiers[4].is_halted():
        index = 0
        for phase in phases:
            amplifiers[index].parse([int(phase), amplifiers[index].previous_amp.get_output()])
            index+=1
        iterations+=1
    return amplifiers[4].get_output()


f = open("input9.txt", "r")
initial_instruction = list(map(lambda x: int(x),f.readline().split(",")))
instruction_map = {x:y for x, y in enumerate(initial_instruction,0)}
def_dict = defaultdict(int, instruction_map)
amp = Interpreter(def_dict.copy(), None)
amp1 = Interpreter(def_dict.copy(), None)
print(amp.parse([1]))
print(amp1.parse([2]))




