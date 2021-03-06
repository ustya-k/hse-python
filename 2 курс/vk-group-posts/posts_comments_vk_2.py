import matplotlib.pyplot as plt
import re
import requests
import pandas as pd
import json
from datetime import date, datetime


def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def transform_to_pd_df(json_file):
	df = pd.DataFrame(json_file)
	tags = ['copy_owner_id', 'copy_post_date', 'copy_post_id', 'copy_post_type','attachment', 'attachments', 'comments', 'date', 'from_id', 'geo', 'is_pinned', 'likes', 'marked_as_ads', 'post_type', 'reposts', 'to_id', 'reply_to_cid', 'reply_to_uid', 'from_id', 'cid']
	for tag in tags:
		if tag in df:
			df = df.drop([tag], axis=1)
	df['text'] = debr_text(df['text'])
	return df

def debr_text(texts):
	clean_texts = []
	for text in texts:
		txt = re.sub('<br>','',text)
		clean_texts.append(txt)
	return clean_texts

def get_posts(domain):
	posts = []
	posts_100 = vk_api('wall.get', domain=domain, count=100)
	posts += posts_100['response'][1:]
	posts_total = posts_100['response'][0]
	print(posts_total)
	#while len(posts) < posts_total:
	while len(posts) < 501:
		posts_100 = vk_api('wall.get', domain=domain, count=100, offset=len(posts))
		posts += posts_100['response'][1:]
	posts_df = transform_to_pd_df(posts)
	return posts_df


def get_info(df):
	df['len'] = count_len(df.text)
	try:
		df['city'], df['age'] = get_personal_info(df.signer_id)
	except:
		df['city'], df['age'] = get_personal_info(df.uid)
	return df

def get_personal_info(ids):
	city = []
	age = []
	for i in ids:
		try:
			info = vk_api('users.get', user_ids=int(i), fields='city,bdate')['response'][0]
			if re.search('[0-9]{4}', info['bdate']):
				bd = datetime.strptime(info['bdate'], '%d.%m.%Y')
				age.append(get_age(bd))
			else:
				age.append('')
			city.append(info['city'])
			#city.append('(' + str(info['city']['id']) + ',' + info['city']['title'] + ')')
		except:
			city.append('')
			age.append('')
	return city, age

def get_age(bd):
	today = date.today()
	return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))

def count_len(texts):
	lengths = []
	for text in texts:
		arr = re.sub('[!?.,;:()"\'-]', ' ', text).split()
		lengths.append(len(arr))
	return lengths


def get_comments(owner_id, post_ids):
	comments_df = pd.DataFrame(columns=['post_id','text','uid'])
	for post_id in post_ids:
		comments_post_df = get_post_comments(owner_id, post_id)
		if type(comments_post_df) != str:
			comments_df = pd.concat([comments_df, comments_post_df])
	return comments_df


def get_post_comments(owner_id, post_id):
	comments = []
	comments_100 = vk_api('wall.getComments', owner_id=-owner_id, post_id=post_id, count=100)
	comments += comments_100['response'][1:]
	comments_total = comments_100['response'][0]
	#print(comments_total)
	while len(comments) < comments_total:
		comments_100 = vk_api('wall.getComments', owner_id=-owner_id, post_id=post_id, count=100, offset=len(comments))
		comments += comments_100['response'][1:]
	try:
		comments_df = transform_to_pd_df(comments)
		comments_df['post_id'] = post_id
		return comments_df
	except:
		return ''


def get_mean(df, param):
	means = []
	for i in sorted(df[param].unique()):
		m = df[df[param] == i]['len'].mean()
		means.append(m)
	return means


def plot_graph(df, param1, param2, title):
	new_df = df[[param1, param2]]
	new_df = new_df.dropna()
	if param2 == 'city':
		new_df['city'] = id_to_name(new_df['city'])
	#new_df[param] = new_df[param].apply(lambda x: int(x))
	df_lengths = pd.DataFrame()
	df_lengths[param2] = new_df[param2].unique()
	df_lengths = df_lengths.sort_values(by=param2)
	df_lengths[param1] = get_mean(new_df, param2)

	df_lengths = df_lengths.sort_values(by=param1, ascending=False)
	#if param == 'city':
	#	df_lengths[param] = df_lengths[param].apply(lambda x: str(x))
	
	plt.figure(figsize=(40,15))
	if param2 == 'city':
		plt.bar(range(len(df_lengths[param2])), df_lengths[param1])
		plt.xticks(range(len(df_lengths[param2])), df_lengths[param2], rotation='vertical')
	else:
		plt.bar(df_lengths[param2], df_lengths[param1])
	plt.savefig(title + '.png')

def get_mean_length(ids, param1, param2, comments):
	lengths = []
	for i in ids:
		try:
			l = comments[comments[param1] == i][param2].mean()
		except:
			l = 0
		lengths.append(l)
	return lengths


def get_len_table(posts, comments):
	df = posts[['id', 'len']]
	df['comments_len'] = get_mean_length(df.id, 'post_id', 'len', comments)
	df = df.drop(['id'], axis=1)
	df2 = pd.DataFrame()
	df2['len'] = df['len'].unique()
	df2['comments_len'] = get_mean_length(df2.len, 'len', 'comments_len', df)
	return df2

def id_to_name(cities):
	unique_cities = list(cities.unique())
	unique_cities = [str(int(city)) for city in unique_cities]
	line = ','.join(unique_cities)
	res = vk_api('database.getCitiesById', city_ids=line)['response']
	id_city = {city['cid']:city['name'] for city in res}
	id_city[0] = '0'
	cities = list(cities)
	city_names = [id_city[int(i)] for i in cities]
	return city_names


def main():
	#dharma_bums
	group_domain = 'dharma_bums'
	group_id = 54566161
	posts = get_posts(group_domain)
	posts = get_info(posts)
	posts.to_csv('posts.csv')

	#posts = pd.read_csv('posts.csv')
	comments = get_comments(group_id, posts.id)
	comments = get_info(comments)
	comments.to_csv('comments.csv')

	#comments = pd.read_csv('comments.csv')
	len_post_comments = get_len_table(posts, comments)

	plot_graph(len_post_comments, 'comments_len', 'len', 'post-comments')
	plot_graph(posts, 'len', 'city', 'post-city')
	plot_graph(posts, 'len', 'age', 'post-age')
	plot_graph(comments, 'len', 'city', 'comment-city')
	plot_graph(comments, 'len', 'age', 'comment-age')


if __name__ == '__main__':
	main()
