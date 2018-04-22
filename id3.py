from math import log


def X(S, i, v):
	return list(filter(lambda row: row[i] == v, S))


def q(S, i, v):
	return len(X(S, i, v)) / len(S)


def p(S, v):
	return 0 if len(S) == 0 else q(S, -1, v)


def H(S):
	p0, p1 = p(S, 0), p(S, 1)
	return -p0 * (log(p0) if p0 > 0 else 0) - p1 * (log(p1) if p1 > 0 else 0)


def IG(S, i):
	return H(S) - q(S, i, 0) * H(X(S, i, 0)) - q(S, i, 1) * H(X(S, i, 1))


def ID3(S, tree=None, index=0):
	if tree is None:
		tree = {}

	ss = sum([row[-1] for row in S])

	if ss == len(S) or ss == 0:
		tree[index] = (S[0][-1], 1)
		return tree

	igs = [IG(S, i) for i in range(len(S[0]) - 1)]
	j = igs.index(max(igs))

	tree[index] = (j, 0)

	tree = ID3(X(S, j, 0), tree, 2 * index + 1)
	tree = ID3(X(S, j, 1), tree, 2 * index + 2)

	return tree


def tree_walk(tree, x, i=0):
	if tree[i][1] == 0:
		return tree_walk(tree, x, 2 * i + 1 + x[tree[i][0]])
	else:
		return tree[i][0], x[-1]

def accuracy_test(tree, test):
	test_count = len(test)
	err_first_order = 0
	err_second_order = 0

	for x in test:
		received, expected = tree_walk(tree, x)
		if received != expected:
			if expected == 1:
				err_first_order += 1
			else:
				err_second_order += 1

	err_count = err_first_order + err_second_order

	return (test_count - err_count) / test_count, err_first_order, err_second_order

def remove_orphans(tree):
	ac = set()

	def mark(index):
		if index in tree.keys():
			ac.add(index)
			if tree[index][1] == 0:
				mark(2 * index + 1)
				mark(2 * index + 2)

	mark(0)
	rem = list(set(tree.keys()).difference(ac))

	for r in rem:
		del tree[r]

	return tree


def prune_get_subtrees(tree):
	trees = []
	for k in tree.keys():
		if tree[k][1] == 0:
			c1 = dict(tree)
			c2 = dict(tree)
			c1[k] = (1, 1)
			c2[k] = (0, 1)
			trees.append(remove_orphans(c1))
			trees.append(remove_orphans(c2))

	return trees

def count_leaves(tree):
	leaves = 0
	for node in tree.values():
		if node[1] == 1:
			leaves += 1
	return leaves


def pruning_select_best(tree, test):
	main_acc, _, _ = accuracy_test(tree, test)
	main_leaves = count_leaves(tree)

	sub_trees = prune_get_subtrees(tree)
	sub_alpha = []

	for i in range(len(sub_trees)):
		acc, _, _ = accuracy_test(sub_trees[i], test)
		leaves = count_leaves(sub_trees[i])
		alpha = (main_acc - acc) / (main_leaves - leaves)
		sub_alpha.append(alpha)

	return sub_trees[sub_alpha.index(min(sub_alpha))]



