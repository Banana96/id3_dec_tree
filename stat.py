from id3 import count_leaves, accuracy_test, pruning_select_best


def tree_stat(tree, test):
	nodes = len(tree.keys())
	leaves = count_leaves(tree)
	acc, fo, so = accuracy_test(tree, test)

	print("Node count:    {} ({} leaves, {} vertices)".format(nodes, leaves, nodes - leaves))
	print("Accuracy:      {:.2f}%".format(100 * acc))
	print("Test set size: {}".format(len(test)))
	print("Error count:   {} ({} 1st order errors, {} 2nd order errors)".format(fo + so, fo, so))


def tree_prune_stat(tree, train, test):
	print(" ======== Before pruning ========")
	tree_stat(tree, test)

	print(" ======== After pruning  ========")
	tree_stat(pruning_select_best(tree, train), test)
