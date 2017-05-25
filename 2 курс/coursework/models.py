import init_models
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim.models import Word2Vec
from cm_plot import plot_cm
from make_it_human_readable import make_it_human_readable


def tfidf_model(classifier, path='data/metadata/dummies_train.csv', if_test='train', stopwords_file=None):
	stopwords = init_models.get_stopwords(stopwords_file)
	tf_vect = TfidfVectorizer(
		min_df=2,
		preprocessor=None, stop_words=stopwords)
	results_df = init_models.init_model(classifier, tf_vect, path, (lambda x: x == 'test')(if_test))

	results_path = 'data/results/predicted_%s_%s_%s.csv' % (classifier, 'tfidf', if_test)
	results_df.to_csv(results_path, sep=';')
	if if_test == 'train':
		plot_cm('tfidf_%s' % classifier, results_path)

	make_it_human_readable(results_path, (lambda x: x == 'test')(if_test))


def bow_model(classifier, path='data/metadata/dummies_train.csv', if_test='train', stopwords_file=None):
	stopwords = init_models.get_stopwords(stopwords_file)
	count_vect = CountVectorizer(preprocessor=None, stop_words=stopwords)
	results_df = init_models.init_model(classifier, count_vect, path, (lambda x: x == 'test')(if_test))

	results_path = 'data/results/predicted_%s_%s_%s.csv' % (classifier, 'bow', if_test)
	results_df.to_csv(results_path, sep=';')
	if if_test == 'train':
		plot_cm('bow_%s' % classifier, results_path)

	make_it_human_readable(results_path, (lambda x: x == 'test')(if_test))


def w2v_model(classifier, path='data/metadata/dummies_train.csv', if_test='train', model_file='model_sg_ns5_300.wv', stopwords_file=None):
	stopwords = init_models.get_stopwords(stopwords_file)

	model_path = 'data/word2vec_models/'
	wv = Word2Vec.load(model_path + model_file)
	wv.init_sims(replace=True)

	results_df = init_models.init_model(classifier, 'w2v', path, (lambda x: x == 'test')(if_test), if_wv=True, w2v_model=wv)

	results_path = 'data/results/predicted_%s_%s_%s.csv' % (classifier, 'w2v', if_test)
	results_df.to_csv(results_path, sep=';')
	if if_test == 'train':
		plot_cm('w2v_%s' % classifier, results_path)

	make_it_human_readable(results_path, (lambda x: x == 'test')(if_test))