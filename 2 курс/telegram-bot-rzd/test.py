import requests
import json
import time
import telebot
import random
import conf
from telebot import types


keyboard = types.ReplyKeyboardMarkup(row_width=1)
btns_names = ['Плацкартный', 'Купе', 'Общий', 'СВ', 'Люкс']
btns = []
for btn in btns_names:
	keyboard.add(types.KeyboardButton(btn))


bot = telebot.TeleBot(conf.TOKEN)
city0 = ''
city1 = ''
date = ''
train_number = ''
car_type = ''
options = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который каждые две минуты проверяет, появились ли нужные вам билеты.")
	bot.send_message(message.chat.id, "Введите город отправления")
	


def city1(message):
	city0 = message.text
	bot.send_message(message.chat.id, "Введите город прибытия")
	bot.register_next_step_handler(date_out)


def date_out(message):
	city1 = message.text
	bot.send_message(message.chat.id, "Введите дату отправления в формате dd.mm.yyyy")
	bot.register_next_step_handler(show_options)


def show_options(message):
	date = message.text
	options = get_info(city0, city1, date)
	bot.send_message(message.chat.id, "Время отправления-время прибытия номер поезда")
	for option in options:
		bot.send_message(message.chat.id, '%s-%s %s' % (option['time0'], option['time1'], option['number']))
	bot.send_message(message.chat.id, "Введите номер интересующего вас поезда")
	bot.register_next_step_handler(type_choice)


def type_choice(message):
	train_number = message.text
	bot.send_message(message.chat.id, 'Выберите тип вагона', reply_markup=keyboard)
	bot.register_next_step_handler(follow_the_train)


def follow_the_train(message):
	car_type = message.text
	count = 0
	good = False
	while not good:
		for option in options:
			if option['number'] == train_number:
				for i in option['cars']:
					if i['typeLoc'] == car_type:
						good = True
						bot.send_message(message.chat.id, 'Ура! Появились билеты.')
						bot.send_message(message.chat.id, 'Всего %s' % i['freeSeats'])
						break
		if count == 0 and not good:
			bot.send_message(message.chat.id, 'За прошедший час ничего не появилось.')
			count = 30
		count -= 1
		time.sleep(120)
		options = get_info(city0, city1, date)

	bot.send_message(message.chat.id, 'Теперь вы можете выбрать другой поезд \start')


def get_city_id(city):
	req = 'http://pass.rzd.ru/suggester?stationNamePart=%s&lang=ru&lat=0&compactMode=y' % city.upper()
	#print(req)
	city = city.upper()
	respData = requests.get(req, headers=headers).text
	rJson = json.loads(respData)
	for item in rJson:
		if item['n'] == city:
			#print('Найден: '+item['n']+' -> '+str(item['c']))
			return str(item['c'])
	#print('Не найден: '+city)
	#print('Выбранный вами город не найден, попробуйте найти в списке и ввести еще раз:')
	#for item in rJson:
	#	print(item['n'])
	return None


def get_info(city0, city1, date):
	id0 = get_city_id(city0)
	id1 = get_city_id(city1)
	req1 = 'https://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5371&dir=0&tfl=3&checkSeats=0&st0='+city0+'&code0='+id0+'&dt0='+date+'&st1='+city1+'&code1='+id1+'&dt1='+date

	res = requests.get(req1, headers=headers, timeout=10)
	r = json.loads(res.text)
	rid = str(r['rid'])

	time.sleep(2)

	req2 = 'https://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5371&dir=0&tfl=3&checkSeats=0&st0='+city0+'&code0='+id0+'&dt0='+date+'&st1='+city1+'&code1='+id1+'&dt1='+date+'&rid='+rid

	res_out = json.loads(requests.get(req2, cookies=res.cookies, headers=headers, timeout=10).text)

	return res_out['tp'][0]['list']	


def main():
	print(get_info('москва', 'санкт-петербург', '09.06.2017'))




if __name__ == '__main__':
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	#bot.polling(none_stop=True)
	main()