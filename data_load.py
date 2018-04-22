from csv import reader


def int_cast(data):
	for i in range(len(data)):
		for j in range(len(data[i])):
			data[i][j] = int(data[i][j])
	return data


def load(filename, cast_to_int=False):
	with open(filename, "r") as f:
		data = list(list(rec) for rec in reader(f, delimiter=','))
		f.close()

	if cast_to_int:
		data = int_cast(data)

	return data


def clear_data(data):
	return list(filter(lambda row: "?" not in "".join(row), data))


def binarize_data(data):
	dicts = []
	distinct_vals = [list(set([row[i] for row in data])) for i in range(len(data[0]))]
	conv_data = []

	for val_set in distinct_vals:
		val_dict = {}
		num = 0
		for v in val_set:
			val_dict[v] = num
			num += 1
		dicts.append(val_dict)

	for m in data:
		binarized = []
		for i in range(len(m)):
			d = dicts[i]
			if len(d.values()) > 2:
				m[i] = [int(elem) for elem in list(eye(len(d.values()))[d[m[i]]])]
			else:
				m[i] = [d[m[i]]]

			binarized += m[i]
		conv_data.append(binarized)

	return conv_data


def train_test_split(data, split_ratio):
	split_point = int(len(data) * split_ratio)
	return data[:split_point], data[split_point:]
