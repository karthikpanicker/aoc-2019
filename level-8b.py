f = open('input8.txt','r')
data = f.readline()
digits = [int(d) for d in data]
layers=[]
val_dic = {}
index = 0
while index < len(digits):
    layers.append(digits[index:index+150])
    index += 150

index = 0
add_list = []
while index < 150:
    for layer in layers:
        if layer[index] == 1 or layer[index] == 0:
            val = "*" if layer[index] == 1 else " "
            add_list.append(val)
            break
    index = index + 1
    if index % 25 == 0:
        s = ""
        print(s.join(add_list))
        add_list.clear()


