def add_sequence(seq):
	line = ''
	for el in seq:
		line += el + ','
	return line[:-1] + ';'


def add_line(line, topics, if_test=False):
	s = line.split(';')
	s[-1] = s[-1][0]
	new_line = s[1] + ';'
	true_topics = []
	predicted_topics = []
	for i, res in enumerate(s):
		if i > 1:
			if '1' in res:
				if 'pred' in topics[i]:
					predicted_topics.append(topics[i].replace('_pred','').replace('_', ' '))
				else:
					true_topics.append(topics[i].replace('_', ' '))

	if if_test:
		new_line += add_sequence(predicted_topics)
	else:
		new_line += add_sequence(true_topics)
		new_line += add_sequence(predicted_topics)
		new_line += add_sequence(set(predicted_topics)-set(true_topics))
		new_line += add_sequence(set(true_topics)-set(predicted_topics))

	return new_line[:-1] + '\n'


def make_it_human_readable(path, if_test=False):
	with open(path, 'r', encoding='utf-8') as f:
		table = f.readlines()

	topics = table[0].split(';')
	topics = [t.replace('topic_','') for t in topics]
	topics[-1] = topics[-1][:-1]
	table.remove(table[0])
	
	if if_test:
		out = 'text;predicted\n'
	else:
		out = 'text;topic;predicted;extra;not_predicted\n'

	for line in table:
		out += add_line(line, topics, if_test)

	with open(path.replace('.csv', '_hr.csv'), 'w', encoding='utf-8') as f:
		f.write(out)


def main():
	path = 'predicted.csv'
	make_it_human_readable(path)


if __name__ == '__main__':
	main()