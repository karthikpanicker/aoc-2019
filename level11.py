from collections import defaultdict

class Robot:
    def __init__(self,instruction,previous):
        self.instructions = instruction
        self.instr_index = 0
        self.halted = False
        self.previous_amp = previous
        self.relative_base = 0
        self.panel_color_set = False
        self.panel_color = 1
        self.unique_panel = defaultdict(int)
        self.coords_list = []
        self.x = 0;
        self.y = 0
        self.current_direction = "U"

    def set_prev_amplifier(self,amp):
        self.previous_amp = amp

    def is_halted(self):
        return self.halted

    def get_output(self):
        return None

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

    def set_new_coords(self,command):
        if command == 0:
            self.current_direction = direction_map[self.current_direction]
        if command == 1:
            self.current_direction = list(direction_map.keys())[list(direction_map.values()).
                index(self.current_direction)][0]

        if self.current_direction == "U":
            self.y +=1
        elif self.current_direction == "L":
            self.x -=1
        elif self.current_direction == "D":
            self.y -=1
        elif self.current_direction == "R":
            self.x += 1

    def parse(self, proginput=[]):
        while self.instr_index < len(self.instructions):
            operation = self.instructions[self.instr_index]
            opcode = self.instructions[self.instr_index] % 10
            if operation == 99:
                self.halted = True
                return len(self.unique_panel.keys())
            if opcode == 3:
                pos = self.get_pos(1)
                self.instructions[pos] = 0 if self.unique_panel[str(self.x) + "&" + str(self.y)] == 0 else 1
                self.coords_list.append((self.x, self.y))
                self.instr_index = self.instr_index + 2
            elif opcode == 4:
                p = self.get_param(1)
                if self.panel_color_set:
                    self.set_new_coords(p)
                    self.panel_color_set = False
                else:
                    self.panel_color = p
                    self.unique_panel[str(self.x) + "&" + str(self.y)] = self.panel_color
                    self.panel_color_set = True
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


direction_map = {"U": "L", "L": "D", "D": "R", "R": "U"}
f = open("input11.txt", "r")
initial_instruction = list(map(lambda x: int(x),f.readline().split(",")))
instruction_map = {x:y for x, y in enumerate(initial_instruction,0)}
def_dict = defaultdict(int, instruction_map)
rob = Robot(def_dict.copy(), None)
rob.unique_panel["0&0"] = 0
print(rob.parse([1]))

rob = Robot(def_dict.copy(), None)
rob.unique_panel["0&0"] = 1
rob.parse([1])

vals1 = list(map(max, zip(*rob.coords_list)))
vals2 = list(map(min, zip(*rob.coords_list)))

h = vals1[1] - vals2[1]
w = vals1[0] -vals2[0]

panel = [[" " for i in range(w + 1)] for j in range(h + 1)]

for coord in rob.coords_list:
    y_val = coord[1] + abs(vals2[1])
    x_val = coord[0] + abs(vals2[0])
    val = str(rob.unique_panel[str(coord[0]) + "&" + str(coord[1])])
    panel[y_val][x_val] = "0" if val == "1" else " "

for row in reversed(panel):
    s=""
    print(s.join(row))
