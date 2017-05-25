from gensim.models import Word2Vec
import pandas as pd
import os


def get_corpus(path):
	df = pd.read_csv(path)
	corpus_df = df['text'].values
	corpus = [str(sent) for sent in corpus_df]
	return corpus


def get_new_model(output_path, name, size=300, data_path='data/metadata/df_w_text.csv', **kwargs):
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	corpus = get_corpus(data_path)
	model = Word2Vec(corpus, size, **kwargs)
	model.save(output_path + name)


def main():
	path = 'data/word2vec_models/'
	name = 'test_model.wv'
	get_new_model(path, name)
	

if __name__ == '__main__':
	main()