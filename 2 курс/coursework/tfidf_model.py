import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy.sparse import csr_matrix, hstack
import random
from sklearn.multioutput import MultiOutputClassifier
import time


def df_with_dummies(df, tags):
	dummies_df = pd.get_dummies(df[tags])
	df = pd.concat([df, dummies_df], axis=1)
	df = df.drop(tags, axis=1)
	return df


def get_df(path):
	df = pd.read_csv(path)
	df = df.dropna()
	tags = ['audience_size','publisher']
	df = df_with_dummies(df, tags)
	return df


def get_features(vectorizer, data):
	data_features = vectorizer.transform(data['text'])
	features = list(data.columns.values)
	features.remove('Unnamed: 0')
	features.remove('path')
	features.remove('text')
	for el in topics:
		features.remove(el)
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

def predict(vectorizer, classifier, data):
	data_features = get_features(vectorizer, data)
	predictions_prob = classifier.predict_proba(data_features)
	predictions = classifier.predict(data_features)
	
	target = data[topics]

	predictions_prob = [pr[1] for pr in predictions_prob]
	#get not predicted
	predictions = get_not_predicted(predictions, predictions_prob, 0.4)


	predictions_df = get_predictions_table(predictions)
	#COUNT ACCURACY & PRECISION
	accuracy, precision = get_accuracy_and_precision(data, predictions_df)

	print('no extra topics')
	print(precision)

	print('perfect match')
	print(accuracy_score(target, predictions))

	return accuracy, predictions_df


def drop_extra_columns(df):
	c = list(df.columns.values)
	columns = []
	for el in c:
		if 'topic' not in el and 'text' not in el:
			columns.append(el)

	return df.drop(columns, axis=1)

def tfidf_model(rs, stopwords_file=None):
	path_train = 'data/metadata/dummies_train.csv'
	df = get_df(path_train)
	train_data, test_data = train_test_split(df, test_size=0.1, random_state=rs)

	#21,None

	if stopwords_file != None:
		with open(stopwords_file, 'r', encoding='utf-8') as f:
			stopwords = f.read().split()
	else:
		stopwords = None

	tf_vect = TfidfVectorizer(
    	min_df=2,
    	preprocessor=None, stop_words=stopwords)

	train_data_features = tf_vect.fit_transform(train_data['text'])
	train_data_features = get_features(tf_vect, train_data)


	logreg = MultiOutputClassifier(linear_model.LogisticRegression(C=1e6, intercept_scaling=3))
	logreg = logreg.fit(train_data_features, train_data[topics])

	model_accuracy, predictions_df = predict(tf_vect, logreg, test_data) 

	test_df_with_predictions = test_data.append(predictions_df)

	test_df_with_predictions = drop_extra_columns(test_df_with_predictions)

	test_df_with_predictions.to_csv('predicted.csv', sep=';')

	print('at least one match')
	print(model_accuracy)


def main():
	tfidf_model(18)


if __name__ == '__main__':
	topics = ['topic_администрация_и_управление','topic_социология','topic_информатика','topic_военное_дело','topic_производство','topic_дом_и_домашнее_хозяйство','topic_здоровье_и_медицина','topic_легкая_и_пищевая_промышленность','topic_бизнес','topic_физика','topic_происшествия','topic_наука_и_технологии','topic_лесное_хозяйство','topic_искусство_и_культура','topic_биология','topic_электроника','topic_строительство','topic_сельское_хозяйство','topic_экономика','topic_досуг,_зрелища_и_развлечения','topic_армия_и_вооруженые_конфликты','topic_история','topic_криминал','topic_политика_и_общественная_жизнь','topic_культурология','topic_транспорт','topic_строительство_и_архитектура','topic_право','topic_энергетика','topic_астрология,_парапсихология,_эзотерика','topic_частная_жизнь','topic_астрономия','topic_филология','topic_бизнес,_коммерция,_экономика,_финансы','topic_наука_и_культура','topic_техника','topic_экология','topic_статистика','topic_психология','topic_спорт','topic_организация_и_управление','topic_досуг,_зрелища,_развлечения','topic_образование','topic_армия_и_вооруженные_конфликты','topic_религия','topic_путешествия','topic_химия','topic_природа']
	main()