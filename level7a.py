import itertools
f = open("input7.txt", "r")
sum = 0


def getValuesToOperate(opcode, index):
    digits = [int(d) for d in opcode]
    param1Mode = 0
    param2Mode = 0
    #print(opcode)
    if len(digits) == 3:
        param1Mode = digits[0]
    if len(digits) == 4:
        param1Mode = digits[1]
        param2Mode = digits[0]

    args = []
    if param1Mode == 0:
        args.append(variables[int(variables[index + 1])])
    else:
        args.append(variables[index + 1])
    if param2Mode == 0:
        if opcode.endswith("4"):
            args.append(variables[int(variables[index + 1])])
        else:
            args.append(variables[int(variables[index + 2])])
    else:
        args.append(variables[index + 2])
    return args

fileContent = f.readline()

variables = fileContent.split(",")

def calculate_output(instr,prev_output):
    i = 0
    second = False
    while i < len(variables):
        opcode = variables[i]
        if opcode.endswith("3"):
            if second:
                variables[int(variables[i + 1])] = prev_output
            else:
                variables[int(variables[i+1])] = instr
            second = True
        elif opcode.endswith("4"):
            args = getValuesToOperate(opcode, i)
            return args[0]
        elif opcode.endswith("1"):
            args = getValuesToOperate(opcode,i)
            variables[int(variables[i+3])] = str(int(args[0]) + int(args[1]))
        elif opcode.endswith("2"):
            args = getValuesToOperate(opcode, i)
            variables[int(variables[i+3])] = str(int(args[0]) * int(args[1]))
        elif opcode.endswith("5"):
            args = getValuesToOperate(opcode, i)
            if int(args[0]) != 0:
                i = int(args[1])
                continue
        elif opcode.endswith("6"):
            args = getValuesToOperate(opcode, i)
            if int(args[0]) == 0:
                i = int(args[1])
                continue
        elif opcode.endswith("7"):
            args = getValuesToOperate(opcode, i)
            if int(args[0]) < int(args[1]):
                variables[int(variables[i+3])] = 1
            else:
                variables[int(variables[i + 3])] = 0
        elif opcode.endswith("8"):
            args = getValuesToOperate(opcode, i)
            if int(args[0]) == int(args[1]):
                variables[int(variables[i+3])] = 1
            else:
                variables[int(variables[i + 3])] = 0
        elif opcode == "99":
            break

            # Logic to find opcode
        if opcode.endswith("3") or opcode.endswith("4"):
            i = i + 2
        elif opcode.endswith("5") or opcode.endswith("6"):
            i = i + 3
        elif opcode.endswith("1") or opcode.endswith("2") or opcode.endswith("0") \
                or opcode.endswith("7") or opcode.endswith("8"):
            i = i + 4
        elif opcode.endswith("99"):
            break


n = '01234'
a = [''.join(i) for i in itertools.permutations(n, 5)]
hello = ""
final = 0
for comb in a:
    digits = [int(d) for d in comb]
    hello = ""
    previous_output = 0
    for instr in digits:
        previous_output = calculate_output(instr,previous_output)
    if int(previous_output) > final:
        final = int(previous_output)
print(final)