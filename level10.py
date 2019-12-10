import math

f = open('input10.txt', 'r')
count_dict = {}
matrix = []
total_asteroids = 0
for line in f.readlines():
    line_content= list(line.strip("\n"))
    total_asteroids += len(list(filter(lambda x: x == "#",line_content)))
    matrix.append(line_content)


def check_if_blocked(x1,y1,x2,y2):
    slope = (y2 - y1)/(x2 - x1) if (x2- x1) is not 0 else 1000000000
    if x2 >= x1:
        k_min = x1
        k_max = x2
    else:
        k_min = x2
        k_max = x1

    if y2 >= y1:
        l_min = y1
        l_max = y2
    else:
        l_min = y2
        l_max = y1

    l = l_min
    blocked = False
    while l <= l_max:
        k = k_min
        while k <= k_max:
            if (k == x1 and l == y1) or (k == x2 and l == y2):
                k = k + 1
                continue
            s = (l - y1)/(k - x1) if (k - x1) is not 0 else 1000000000
            if s == slope and matrix[l][k] == "#":
                blocked = True
                return blocked
            k += 1
        l += 1
    return blocked



def count_visible(j,i):
    m, n = 0, 0
    visible = 0
    while m < len(matrix):
        n = 0
        while n < len(matrix[0]):
            if m == i and n == j:
                n += 1
                continue
            elif matrix[m][n] == '#':
                if not check_if_blocked(j,i,n,m):
                    visible = visible + 1
            n += 1
        m += 1
    count_dict[str(j) + "-" +str(i)] = visible

def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

i = 0
j = 0

while i < len(matrix):
    j = 0
    while j < len(matrix[0]):
        if matrix[i][j] == "#":
            count_visible(j, i)
        j = j + 1
    i = i + 1

max_key = max(count_dict.keys(), key=(lambda k: count_dict[k]))
print(count_dict[max_key])

start_coords = max_key.split('-')
x,y = int(start_coords[0]) , int(start_coords[1])
beam_origin_cord = [int(start_coords[0]) , int(start_coords[1])]
original_cord = [x,0]
line_end_cord = [x,0]

min_angle = 361
point_to_vaporize = None
distance_to_point = 0
angle_to_baseline = 361

h = 0
while h < 200:
    i = 0
    j = 0
    while i < len(matrix):
        j = 0
        while j < len(matrix[0]):
            if matrix[i][j] == "#":
                angle = get_angle(line_end_cord, beam_origin_cord,[j, i])
                atb = get_angle(original_cord, beam_origin_cord,[j, i])
                if angle < min_angle and atb != angle_to_baseline:
                    point_to_vaporize = [j,i]
                    min_angle = angle
                    distance_to_point = math.sqrt( ((beam_origin_cord[0]-j)**2)+((beam_origin_cord[1]-i)**2) )
                elif angle == min_angle and atb != angle_to_baseline:
                    d = math.sqrt( ((beam_origin_cord[0]-j)**2)+((beam_origin_cord[1]-i)**2) )
                    if d < distance_to_point:
                        distance_to_point = d
                        point_to_vaporize = [j,i]
            j = j + 1
        i = i + 1
    min_angle = 361
    line_end_cord = point_to_vaporize
    angle_to_baseline = get_angle(original_cord, beam_origin_cord,point_to_vaporize)
    if h == 199:
        print(h+1,")",point_to_vaporize, "-->", angle_to_baseline)
    matrix[point_to_vaporize[1]][point_to_vaporize[0]] = "."
    distance_to_point = 0
    h += 1
