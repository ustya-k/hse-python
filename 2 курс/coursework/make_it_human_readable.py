def add_sequence(seq):
	line = ''
	for el in seq:
		line += el + ','
	return line[:-1] + ';'


def add_line(line, topics):
	s = line.split(';')
	s[-1] = s[-1][0]
	new_line = s[0] + ';'
	true_topics = []
	predicted_topics = []
	for i, res in enumerate(s):
		if i != 0:
			if res == '1':
				if 'pred' in topics[i]:
					predicted_topics.append(topics[i].replace('_pred','').replace('_', ' '))
				else:
					true_topics.append(topics[i].replace('_', ' '))
	new_line += add_sequence(true_topics)
	new_line += add_sequence(predicted_topics)
	new_line += add_sequence(set(predicted_topics)-set(true_topics))
	new_line += add_sequence(set(true_topics)-set(predicted_topics))
	return new_line[:-1] + '\n'

def main():
	with open('predicted.csv', 'r', encoding='utf-8') as f:
		table = f.readlines()

	topics = table[0].split(';')
	topics = [t.replace('topic_','') for t in topics]
	topics[-1] = topics[-1][:-1]
	table.remove(table[0])
	
	out = 'text;topic;predicted;extra;not_predicted\n'
	for line in table:
		out += add_line(line, topics)

	with open('results.csv', 'w', encoding='utf-8') as f:
		f.write(out)


if __name__ == '__main__':
	main()