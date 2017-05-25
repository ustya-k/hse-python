import models


def test():
	path = 'data/metadata/dummies_train.csv'
	classifier = 'LogReg'
	if_test = 'train'
	stopwords_file = 'data/stop_ru.txt'
	# models.tfidf_model(classifier, path, if_test=if_test, stopwords_file=stopwords_file)
	# print('ok')
	# models.bow_model(classifier, path, if_test=if_test, stopwords_file=stopwords_file)
	# print('ok')
	models.w2v_model(classifier, path, if_test=if_test, stopwords_file=stopwords_file)
	print('ok')


if __name__ == '__main__':
	test()