import itertools


class Amplifier:
    def __init__(self,instruction,previous):
        self.intructions = instruction
        self.instr_index = 0
        self.halted = False
        self.current_output_signal = 0
        self.previous_amp = previous
        self.waiting_for_input = False
        self.is_phase_set = False

    def set_prev_amplifier(self,amp):
        self.previous_amp = amp

    def is_halted(self):
        return self.halted

    def get_output(self):
        return self.current_output_signal

    def get_values_to_operate(self,operation, index):
        digits = [int(d) for d in str(operation)]
        param1Mode = 0
        param2Mode = 0
        # print(opcode)
        if len(digits) == 3:
            param1Mode = digits[0]
        if len(digits) == 4:
            param1Mode = digits[1]
            param2Mode = digits[0]

        elems = []
        if param1Mode == 0:
            elems.append(self.intructions[self.intructions[index + 1]])
        else:
            elems.append(self.intructions[index + 1])
        if param2Mode == 0:
            if operation % 10 == 4:
                elems.append(self.intructions[self.intructions[index + 1]])
            else:
                elems.append(self.intructions[self.intructions[index + 2]])
        else:
            elems.append(self.intructions[index + 2])
        return elems

    def parse(self, proginput=[]):
        while self.instr_index < len(self.intructions):
            operation = self.intructions[self.instr_index]
            opcode = self.intructions[self.instr_index] % 10
            if opcode == 3:
                if not self.is_phase_set:
                    self.intructions[self.intructions[self.instr_index + 1]] = proginput[0]
                    self.is_phase_set = True
                elif proginput[1] is not None:
                    self.intructions[self.intructions[self.instr_index + 1]] = proginput[1]
                    proginput[1] = None
                elif proginput[1] is None:
                    self.waiting_for_input = True
                    return
            elif opcode == 4:
                args = self.get_values_to_operate(operation, self.instr_index)
                self.current_output_signal = args[0]
            elif opcode == 1:
                args = self.get_values_to_operate(operation, self.instr_index)
                self.intructions[self.intructions[self.instr_index + 3]] = args[0] + args[1]
            elif opcode == 2:
                args = self.get_values_to_operate(operation, self.instr_index)
                self.intructions[self.intructions[self.instr_index + 3]] = args[0] * args[1]
            elif opcode == 5:
                args = self.get_values_to_operate(operation, self.instr_index)
                if args[0] != 0:
                    self.instr_index = args[1]
                    continue
            elif opcode == 6:
                args = self.get_values_to_operate(operation, self.instr_index)
                if args[0] == 0:
                    self.instr_index = args[1]
                    continue
            elif opcode == 7:
                args = self.get_values_to_operate(operation, self.instr_index)
                if args[0] < args[1]:
                    self.intructions[self.intructions[self.instr_index + 3]] = 1
                else:
                    self.intructions[self.intructions[self.instr_index + 3]] = 0
            elif opcode == 8:
                args = self.get_values_to_operate(operation, self.instr_index)
                if args[0] == args[1]:
                    self.intructions[self.intructions[self.instr_index + 3]] = 1
                else:
                    self.intructions[self.intructions[self.instr_index + 3]] = 0
            elif opcode == 9:
                self.halted = True
                return

                # Logic to find opcode
            if opcode == 3 or opcode == 4:
                self.instr_index = self.instr_index + 2
            elif opcode == 5 or opcode == 6:
                self.instr_index = self.instr_index + 3
            elif opcode == 1 or opcode == 2 or opcode == 0 \
                    or opcode == 7 or opcode == 8:
                self.instr_index = self.instr_index + 4


def execute_amplifiers(amplifiers, phases):
    iterations = 0
    while not amplifiers[4].is_halted():
        index = 0
        for phase in phases:
            amplifiers[index].parse([int(phase), amplifiers[index].previous_amp.get_output()])
            index+=1
        iterations+=1
    return amplifiers[4].get_output()


def create_amplifiers():
    amplifiers = {}
    for i in range(5):
        if i != 0:
            amplifiers[i] = Amplifier(initial_instruction.copy(), amplifiers[i - 1])
        else:
            amplifiers[i] = Amplifier(initial_instruction.copy(), None)
    amplifiers[0].set_prev_amplifier(amplifiers[4])
    return amplifiers


f = open("input7.txt", "r")
initial_instruction = list(map(lambda x: int(x),f.readline().split(",")))
best_signal = 0
m = '98765'
for phases in itertools.permutations(m, 5):
    proginput = 0
    signal_strength = execute_amplifiers(create_amplifiers(),phases)
    if signal_strength > best_signal:
        best_signal = signal_strength
print(best_signal)


