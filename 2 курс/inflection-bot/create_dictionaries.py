from pymorphy2 import MorphAnalyzer
import re


def get_pos(word):
	if re.search('[^А-Яа-яЁё-]', word):
		return None
	else:
		ana = morph.parse(word)
		pos = [ana[0].tag.POS, ana[0].normal_form]
		if 'перемес' in word:
			print(word)
			print(pos)
		return pos


def save_dictionaries(dicts):
	for d in dicts:
		lines = '\n'.join(dicts[d]['dict'])
		with open('dictionaries/%s.txt' % d, 'w', encoding='utf-8') as f:
			f.write(lines)


def create_dictionaries(path):
	with open(path, 'r', encoding='utf-8') as f:
		all_words = f.read().split('\n')

	POS = {'nouns': {'tags': {'NOUN'}, 'dict': set()}, 'verbs': {'tags': {'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND'}, 'dict': set()}, 'adjectives': {'tags': {'ADJF', 'ADJS', 'COMP'}, 'dict': set()}, 'numerals': {'tags': {'NUMR'}, 'dict': set()}, 'adverbs': {'tags': {'ADVB'}, 'dict': set()}, 'pronouns': {'tags': {'NPRO'}, 'dict': set()}, 'prepositions': {'tags': {'PREP'}, 'dict': set()}, 'conjunctions': {'tags': {'CONJ'}, 'dict': set()}, 'particles': {'tags': {'PRCL'}, 'dict': set()}, 'interjections': {'tags': {'INTJ'}, 'dict': set()}, 'predicatives': {'tags': {'PRED'}, 'dict': set()}}

	for word in all_words:
		word_pos = get_pos(word)
		if word_pos != None:
			for p in POS:
				if word_pos[0] in POS[p]['tags'] and word_pos[0] != None:
					POS[p]['dict'].add(word_pos[1])
					break

	save_dictionaries(POS)



def main():
	path = '1grams-3.txt'
	create_dictionaries(path)


if __name__ == '__main__':
	morph = MorphAnalyzer()
	main()