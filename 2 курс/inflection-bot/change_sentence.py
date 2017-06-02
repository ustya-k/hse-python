from pymorphy2 import MorphAnalyzer
import random
import re


def get_dictionaries(path):
	POS = {'nouns': {'tags': {'NOUN'}, 'dict': set()}, 'verbs': {'tags': {'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND'}, 'dict': set()}, 'adjectives': {'tags': {'ADJF', 'ADJS', 'COMP'}, 'dict': set()}, 'numerals': {'tags': {'NUMR'}, 'dict': set()}, 'adverbs': {'tags': {'ADVB'}, 'dict': set()}, 'pronouns': {'tags': {'NPRO'}, 'dict': set()}, 'prepositions': {'tags': {'PREP'}, 'dict': set()}, 'conjunctions': {'tags': {'CONJ'}, 'dict': set()}, 'particles': {'tags': {'PRCL'}, 'dict': set()}, 'interjections': {'tags': {'INTJ'}, 'dict': set()}, 'predicatives': {'tags': {'PRED'}, 'dict': set()}}

	for p in POS:
		with open('%s%s.txt' % (path, p), 'r', encoding='utf-8') as f:
			POS[p]['dict'] = set(f.read().split('\n'))

	return POS


def get_proper_new_word(ana, p, words, morph):
	new_word = None
	while not new_word:
		new_word = random.sample(words, 1)[0]
		new_word_ana = morph.parse(new_word)[0]
		if str(new_word_ana.tag.POS) == 'UNKN' or ana.word == new_word:
			new_word = None
		#don't change prepositions
		elif p in {'prepositions','pronouns'}:
			return ana.word
		#important for nouns
		elif p in 'nouns':
			if ana.tag.gender == new_word_ana.tag.gender:
				infl = set(str(ana.tag).split()[1].split(','))
				if new_word_ana.inflect(infl):
					return new_word_ana.inflect(infl).word
				else:
					new_word = None
			else:
				new_word = None
		elif p == 'verbs':
			if ana.tag.POS == 'PRTS' and new_word_ana.tag.transitivity == 'tran' and ana.tag.aspect == new_word_ana.tag.aspect:
				infl = set(str(ana.tag).split()[1].split(','))
				infl.add('PRTS')
				infl.add(ana.tag.voice)
				return new_word_ana.inflect(infl).word
			elif ana.normal_form == 'быть' and 'futr' in ana.tag:
				if new_word_ana.tag.transitivity == 'intr':
					return ana.word + ' ' + new_word
				else:
					new_word = None
			elif ana.tag.transitivity == new_word_ana.tag.transitivity and ana.tag.aspect == new_word_ana.tag.aspect:
				if ana.tag.POS == 'INFN':
					return new_word
				infl = set(str(ana.tag).split()[1].split(','))
				if ana.tag.POS == 'GRND':
					infl.add('GRND')
				if ana.tag.POS == 'PRTF':
					infl.add('PRTF')
					infl.add(ana.tag.voice)
				if 'Impe' in ana.tag:
					infl.add('3per')
				elif new_word_ana.inflect(infl):
					return new_word_ana.inflect(infl).word
				else:
					new_word = None
			else:
				new_word = None
		elif p == 'adjectives':
			infl_adj = str(ana.tag).split()
			if 'COMP' in infl_adj[0]:
				infl = {'COMP'}
				if 'Qual' not in new_word_ana.tag or 'Fixd' in new_word_ana.tag:
					new_word = None
				else:
					return new_word_ana.inflect(infl).word
			else:
				infl = set(infl_adj[1].split(','))
				if 'Supr' in infl_adj[0] and ('Qual' not in new_word_ana.tag or 'Fixd' in new_word_ana.tag):
					new_word = None
				else:
					if 'Supr' in infl_adj[0]:
						infl.add('Supr')
					if new_word_ana.inflect(infl):
						return new_word_ana.inflect(infl).word
					else:
						new_word = None
		elif p in {'conjunctions','particles','adverbs', 'interjections', 'predicatives'}:
			return new_word


def get_new_word(word, POS, morph):
	ana = morph.parse(word)[0]
	for p in POS:
		if ana.tag.POS in POS[p]['tags']:
			new_word = get_proper_new_word(ana, p, POS[p]['dict'], morph)
			return new_word
	return word


def change_words(words):
	new_words = []
	path = 'dictionaries/'
	POS = get_dictionaries(path)
	morph = MorphAnalyzer()
	for word in words:
		new_words.append(get_new_word(word, POS, morph))
	return new_words


def check_case(words1, words2):
	for i, word in enumerate(words1):
		ch = True
		for letter in word:
			if letter.islower():
				ch = False
				break
		if ch:
			words2[i] = words2[i].upper()
		elif word[0].isupper():
			words2[i] = words2[i].title()
	return words2


def transform_sent(sent):
	words = [i.strip('.?!,"()1234567890$:%') for i in sent.split()]
	sent = re.sub('([а-яА-ЯЁёA-Za-z-]+)', '%s', sent)
	new_words = change_words(words)
	new_words = check_case(words, new_words)
	new_sent = sent % tuple(new_words)
	return new_sent


def main():
	sent = input('input a sentence: ')
	output_sent = transform_sent(sent)
	print(output_sent)


if __name__ == '__main__':
	main()