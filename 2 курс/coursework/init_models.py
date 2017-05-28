import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy import sparse
from scipy.sparse import csr_matrix, hstack
from sklearn.multioutput import MultiOutputClassifier
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import gensim
from random import randint


def df_with_dummies(df, tags):
	dummies_df = pd.get_dummies(df[tags])
	df = pd.concat([df, dummies_df], axis=1)
	df = df.drop(tags, axis=1)
	return df


def get_df(path):
	df = pd.read_csv(path)
	try:
		df = df.drop(['Unnamed: 132'], axis=1)
	except ValueError:
		pass
	try:
		tags = ['audience_size','publisher']
		df = df_with_dummies(df, tags)
	except KeyError:
		pass
	return df.dropna()


def w2v_vect(wv, data):
	data_tokenized = data.apply(lambda r: w2v_tokenize_text(r['text']), axis=1).values
	X_data_word_average = word_averaging_list(wv, data_tokenized)
	return X_data_word_average


def get_features(vectorizer, data, if_wv=False, w2v_model=None):
	if if_wv:
		data_features = w2v_vect(w2v_model, data)
	else:
		data_features = vectorizer.transform(data['text'])
	features = list(data.columns.values)
	features_to_remove = topics + ['Unnamed: 0', 'path', 'text', 'if_topic']
	for el in features_to_remove:
		try:
			features.remove(el)
		except ValueError:
			pass
	other_features = csr_matrix(data[features])
	data_features = hstack((data_features, other_features))
	return data_features


def get_predictions_table(predictions):
	topics_pred = [topic + '_pred' for topic in topics]
	predictions_df = pd.DataFrame(predictions, columns=topics_pred)
	return predictions_df


def get_not_predicted(predictions, predicted_probabilities, enough_probability):
	not_predicted_texts = []

	for i, pred in enumerate(predictions):
		number_of_predicted_topics = 0
		for j in pred:
			number_of_predicted_topics += j
		if number_of_predicted_topics == 0:
			not_predicted_texts.append(i)

	for el in not_predicted_texts:
		max_prob = 0
		max_prob_value = 0
		predictions_with_more_than_enough_prob = set()
		for i, prob in enumerate(predicted_probabilities[el]):
			if prob > max_prob_value:
				max_prob_value = prob
				max_prob = i
			if prob >= enough_probability:
				predictions_with_more_than_enough_prob.add(i)
		predictions[el][max_prob] = 1
		for prob in predictions_with_more_than_enough_prob:
			predictions[el][prob] = 1

	return predictions


def get_accuracy_and_precision(data, predictions):
	number_correct = 0
	total_number = len(predictions)
	no_extra_topics = len(predictions)
	counter = 0
	for i in data.index:
		for t in topics:
			if predictions.at[counter, t + '_pred'] == 1 and data.at[i, t] == 1:
				number_correct += 1
			if predictions.at[counter, t + '_pred'] == 1 and data.at[i, t] == 0:
				no_extra_topics -= 1
		counter += 1
	return number_correct/total_number, no_extra_topics/total_number


def predict(vectorizer, classifier, data, if_test=False, if_wv=False, w2v_model=None):
	if if_wv:
		data_features = get_features('w2v', data, True, w2v_model)
	else:
		data_features = get_features(vectorizer, data)

	predictions_prob = classifier.predict_proba(data_features)
	predictions = classifier.predict(data_features)
	

	predictions_prob = [pr[1] for pr in predictions_prob]
	#get not predicted
	predictions = get_not_predicted(predictions, predictions_prob, 0.5)


	predictions_df = get_predictions_table(predictions)

	if if_test:
		return predictions_df
	else:
		target = data[topics]
		#COUNT ACCURACY & PRECISION
		accuracy, precision = get_accuracy_and_precision(data, predictions_df)

		print('no extra topics')
		print(precision)

		print('perfect match')
		print(accuracy_score(target, predictions))

		return accuracy, predictions_df


def drop_extra_columns(df):
	c = list(df.columns.values)
	extra_columns = []
	for el in c:
		if el == 'if_topic' or ('topic' not in el and 'text' not in el):
			extra_columns.append(el)

	text = df['text']
	df = df.drop(['text'], axis=1)
	df = pd.concat([text, df], axis=1)
	df = df.drop(extra_columns, axis=1)
	return df


def get_stopwords(file):
	if file != None:
		with open(file, 'r', encoding='utf-8') as f:
			return f.read().split()
	else:
		return None


def w2v_tokenize_text(text):
	tokens = text.split()
	return tokens


def word_averaging(wv, words):
	 all_words, mean = set(), []
	
	 for word in words:
		 if isinstance(word, np.ndarray):
			 mean.append(word)
		 elif word in wv.vocab:
			 mean.append(wv.syn0norm[wv.vocab[word].index])
			 all_words.add(wv.vocab[word].index)

	 if not mean:
		 return np.zeros(wv.layer1_size,)

	 mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
	 return mean


def word_averaging_list(wv, text_list):
	l =  np.vstack([word_averaging(wv, review) for review in text_list ])
	return sparse.csr_matrix(l)


def init_model(classifier_name, vectorizer, path, if_test=False, if_wv=False, w2v_model=None, rs=randint(0,100)):
	df = get_df(path)
	global topics

	topics = ['topic_администрация_и_управление','topic_социология','topic_информатика','topic_военное_дело','topic_производство','topic_дом_и_домашнее_хозяйство','topic_здоровье_и_медицина','topic_легкая_и_пищевая_промышленность','topic_бизнес','topic_физика','topic_происшествия','topic_наука_и_технологии','topic_лесное_хозяйство','topic_искусство_и_культура','topic_биология','topic_электроника','topic_строительство','topic_сельское_хозяйство','topic_экономика','topic_досуг,_зрелища_и_развлечения','topic_история','topic_криминал','topic_политика_и_общественная_жизнь','topic_культурология','topic_транспорт','topic_строительство_и_архитектура','topic_право','topic_энергетика','topic_астрология,_парапсихология,_эзотерика','topic_частная_жизнь','topic_астрономия','topic_филология','topic_бизнес,_коммерция,_экономика,_финансы','topic_наука_и_культура','topic_техника','topic_экология','topic_статистика','topic_психология','topic_спорт','topic_организация_и_управление','topic_образование','topic_армия_и_вооруженные_конфликты','topic_религия','topic_путешествия','topic_химия','topic_природа']

	if if_test:
		train_data, test_data = train_test_split(df, test_size=0.1, random_state=rs)
		predict_path = 'data/metadata/dummies_test.csv'
		predict_data = get_df(predict_path)
		columns_drop = list(set(predict_data.columns.values) - set(df.columns.values))
		predict_data = predict_data.drop(columns_drop, axis=1)
	else:
		train_data, test_data = train_test_split(df, test_size=0.1, random_state=rs)

	if if_wv:
		train_data_features = get_features('w2v', train_data, True, w2v_model)
	else:
		train_data_features = vectorizer.fit_transform(train_data['text'])
		train_data_features = get_features(vectorizer, train_data)

	try:

		if classifier_name == 'RandomForest':
			classifier = MultiOutputClassifier(RandomForestClassifier(n_estimators=60, min_samples_split=3))
			classifier = classifier.fit(train_data_features, train_data[topics])
		elif classifier_name == 'LogReg':
			classifier = MultiOutputClassifier(linear_model.LogisticRegression(C=1e6, intercept_scaling=3))
			classifier = classifier.fit(train_data_features, train_data[topics])


		if if_test:
			model_accuracy, predictions_test_df = predict(vectorizer, classifier, test_data, if_test=False, if_wv=if_wv, w2v_model=w2v_model) 
			predictions_df = predict(vectorizer, classifier, predict_data,if_test=if_test, if_wv=if_wv, w2v_model=w2v_model)
			test_df_with_predictions = pd.concat([predict_data,predictions_df.set_index(predict_data.index)], axis=1)
		else:
			# joblib.dump(classifier, 'data/trained_models/%s.pkl' % classifier_name)
			model_accuracy, predictions_df = predict(vectorizer, classifier, test_data, if_wv=if_wv, w2v_model=w2v_model) 
			test_df_with_predictions = pd.concat([test_data,predictions_df.set_index(test_data.index)], axis=1)

		print('at least one match')
		print(model_accuracy)

		test_df_with_predictions = drop_extra_columns(test_df_with_predictions)
		return test_df_with_predictions

	# for cases when split leaves all the instances of one (or more) of the topic in test data
	except ValueError:
		rs = randint(0,100)
		#print(rs)
		return init_model(classifier_name, vectorizer, path, if_test, if_wv, w2v_model, rs=rs)
