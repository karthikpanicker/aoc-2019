class Image:
    def __init__(self,data, width, height):
        self.pixel_data = data
        self.image_width = width
        self.image_height = height
        self.layers = {}
        self.init_layers()
        self.merged_layer = {}

    def init_layers(self):
        pixel_per_layer = self.image_width * self.image_height
        index = 0
        while index < len(self.pixel_data):
            self.layers[int(index/pixel_per_layer)] = Layer(self.pixel_data[index:index+pixel_per_layer],
                                                       self.image_width,self.image_height)
            index += pixel_per_layer

    def merge_layers(self):
        index = 0
        layer_row_list = []
        while index < self.image_height:
            sub_layers_across_layer = []
            for layer in self.layers.values():
                sub_layers_across_layer.append(layer.get_sub_layer(index))
            layer_row_list.append(LayerRow(self.merge_sub_layer(sub_layers_across_layer)))
            index += 1
        return layer_row_list

    def merge_sub_layer(self,sub_layer_list):
        index = 0
        result = []
        while index < self.image_width:
            for sub_layer in sub_layer_list:
                if sub_layer.get_pixel_at_index(index) == 1 or sub_layer.get_pixel_at_index(index) == 0:
                    result.append("o" if sub_layer.get_pixel_at_index(index) == 1 else " ")
                    break
            index +=1
        return result


class Layer:
    def __init__(self,data,width, height):
        self.pixel_layer_data = data
        self.image_width = width
        self.image_height = height
        self.sub_layers = {}
        self.init_sub_layers()

    def init_sub_layers(self):
        index = 0
        while index < len(self.pixel_layer_data):
            self.sub_layers[int(index/self.image_width)] = LayerRow(self.pixel_layer_data[index:index + self.image_width])
            index += self.image_width

    def get_sub_layer(self,index):
        return self.sub_layers[index]

class LayerRow:
    def __init__(self,rowdata):
        self.row_data = rowdata

    def get_pixel_at_index(self,index):
        return self.row_data[index]

    def __str__(self):
        return "".join(self.row_data)


f = open('input8.txt','r')
data = f.readline()
digits = [int(d) for d in data]
img = Image(digits,25,6)
zc = 0
lz = 100000000000
mv = 0
for layer in img.layers.values():
    zc = len(list(filter(lambda x: x == 0, layer.pixel_layer_data)))
    if lz > zc:
        lz = zc
        mv = len(list(filter(lambda x: x == 1,layer.pixel_layer_data))) * len(list(filter(lambda x: x == 2, layer.pixel_layer_data)))
print(mv)
for layer_row in img.merge_layers():
    print(layer_row)
