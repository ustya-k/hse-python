import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix


def plot_confusion_matrix(df, name, title='Confusion matrix', cmap=plt.cm.Blues):
	cm = get_cm(df)
	plt.figure(figsize=(20,15))
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(topics))
	target_names = [topic.replace('topic_','').replace('_', ' ') for topic in topics]
	plt.xticks(tick_marks, target_names, rotation=90)
	plt.yticks(tick_marks, target_names)
	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.savefig('data/results/' + name + '.png')


def get_cm(df):
	cm = []

	for i, topic in enumerate(topics):
		arr = []
		for j, t in enumerate(topics_pred):
			count = 0
			sum_pos = 0
			for k, v in enumerate(df[topic].values):
				if v == 1 and df[t].values[k] == 1:
					if i == j or df[topics[j]].values[k] == 0:
						count += 1
				if v == 1:
					sum_pos += 1
			if sum_pos:
				arr.append(count/sum_pos)
			else:
				arr.append(0)
		cm.append(arr)

	return cm


def plot_cm(name, path):
	global topics
	topics = ['topic_администрация_и_управление','topic_социология','topic_информатика','topic_военное_дело','topic_производство','topic_дом_и_домашнее_хозяйство','topic_здоровье_и_медицина','topic_легкая_и_пищевая_промышленность','topic_бизнес','topic_физика','topic_происшествия','topic_наука_и_технологии','topic_лесное_хозяйство','topic_искусство_и_культура','topic_биология','topic_электроника','topic_строительство','topic_сельское_хозяйство','topic_экономика','topic_досуг,_зрелища_и_развлечения','topic_история','topic_криминал','topic_политика_и_общественная_жизнь','topic_культурология','topic_транспорт','topic_строительство_и_архитектура','topic_право','topic_энергетика','topic_астрология,_парапсихология,_эзотерика','topic_частная_жизнь','topic_астрономия','topic_филология','topic_бизнес,_коммерция,_экономика,_финансы','topic_наука_и_культура','topic_техника','topic_экология','topic_статистика','topic_психология','topic_спорт','topic_организация_и_управление','topic_образование','topic_армия_и_вооруженные_конфликты','topic_религия','topic_путешествия','topic_химия','topic_природа']
	global topics_pred
	topics_pred = [topic + '_pred' for topic in topics]
	df = pd.read_csv(path, sep=';')
	plot_confusion_matrix(df, name)


def main():
	name = 'RandomForest_bow'
	path = 'predicted_%s.csv' % name
	plot_cm(name, path)


if __name__ == '__main__':
	main()