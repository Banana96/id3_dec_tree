from data_load import load
from id3 import ID3
from stat import tree_prune_stat

dane = load("./data1.txt", cast_to_int=True)
test = load("./test1.txt", cast_to_int=True)
tree = ID3(dane)

tree_prune_stat(tree, dane, test)