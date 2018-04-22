from data_load import clear_data, load, binarize_data, train_test_split
from id3 import ID3
from stat import tree_prune_stat

m_data = clear_data(load("./mushroom.txt"))

for i in range(len(m_data)):
    f, l = m_data[i][0], m_data[i][-1]
    m_data[i][0] = l
    m_data[i][-1] = f

m_binary = binarize_data(m_data)
m_train, m_test = train_test_split(m_binary, 0.8)
m_tree = ID3(m_train)

tree_prune_stat(m_tree, m_train, m_test)
