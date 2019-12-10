from treelib import Node, Tree
sum = 0

f = open("input6.txt", "r")
content = f.readlines()
not_processed_list= {}
tree = Tree()
parent_check = {}
parent_check_reverse = {}
nodeids = []

for line in content:
    bodies = line.split(")")
    left = bodies[0]
    right=bodies[1].rstrip("\n")
    parent_check[right] = left
    parent_check_reverse[left] = right
    nodeids.append(left)
    nodeids.append(right)

for nodeid in nodeids:
    if nodeid in parent_check:
        continue
    else:
        rootid = nodeid

unique_ids = set(nodeids)
tree.create_node(tag=rootid,identifier=rootid)


while len(unique_ids) != len(tree.all_nodes()):
    for rightNode in list(parent_check.keys()):
        if tree.get_node(parent_check[rightNode]) is not None and tree.get_node(rightNode) is None:
            tree.create_node(tag=rightNode, identifier=rightNode,
                             parent=tree.get_node(parent_check[rightNode]))

for node in tree.all_nodes():
    sum += tree.depth(node)
print(sum)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

sanIndex = 0
youInex = 0

for path in tree.paths_to_leaves():
    if path[len(path) -1] == "SAN":
        sanIndex = path[path.index('7LD'):]
    elif path[len(path) - 1] == "YOU":
        youIndex = path[path.index('7LD'):]
print (len(sanIndex) + len(youIndex) - 4)

