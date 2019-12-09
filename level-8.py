f = open('input8.txt','r')
data = f.readline()
digits = [int(d) for d in data]
i = 0
lz = 100000000000
mv = 0

while i < len(digits):
    layer = digits[i:i + 150]
    zc = len(list(filter(lambda x: x == 0, layer)))
    if lz > zc:
        lz = zc
        mv = len(list(filter(lambda x: x == 1,layer))) * len(list(filter(lambda x: x == 2, layer)))
    i += 150

print(mv)