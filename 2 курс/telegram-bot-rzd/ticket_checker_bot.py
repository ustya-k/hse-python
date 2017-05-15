import requests
import json
import time
import telebot
import conf
import flask
from telebot import types
from requests.compat import quote


WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)


keyboard = types.ReplyKeyboardMarkup(row_width=1)
btns_names = ['Плацкартный', 'Купе', 'Общий', 'СВ', 'Люкс', 'Сидячий']
btns = []
for btn in btns_names:
    keyboard.add(types.KeyboardButton(btn))


train = {'city0': None, 'city1': None, 'date': None, 'number': None, 'car_type': None, 'options': None}

coms = ['start', 'help', 'new_search']

app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который каждые две минуты проверяет, появились ли нужные вам билеты.")
    bot.send_message(message.chat.id, "Если что-то появляется, он сразу же оповещает вас об этом.")
    bot.send_message(message.chat.id, "Иначе он будет писать раз в час, что ничего не появилось.")
    bot.send_message(message.chat.id, "Новый поиск вы можете начать командой /new_search")


@bot.message_handler(commands=['new_search'])
def new_search(message):
    sent = bot.send_message(message.chat.id, "Введите город отправления")
    bot.register_next_step_handler(sent, city1)


def city1(message):
    train['city0'] = message.text
    sent = bot.send_message(message.chat.id, "Введите город прибытия")
    bot.register_next_step_handler(sent, date_out)


def date_out(message):
    if message.text[1:] not in coms:
        train['city1'] = message.text
        sent = bot.send_message(message.chat.id, "Введите дату отправления в формате dd.mm.yyyy")
        bot.register_next_step_handler(sent, show_options)


def show_options(message):
    if message.text[1:] not in coms:
        train['date'] = message.text
        try:
            train['options'] = get_info(train['city0'], train['city1'], train['date'])
            bot.send_message(message.chat.id, "Время отправления-время прибытия номер поезда")
            for option in train['options']:
                bot.send_message(message.chat.id, '%s-%s %s' % (option['time0'], option['time1'], option['number']))
            sent = bot.send_message(message.chat.id, "Введите номер интересующего вас поезда")
            bot.register_next_step_handler(sent, type_choice)
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте ещё раз /new_search")


def type_choice(message):
    if message.text[1:] not in coms:
        train['number'] = message.text
        sent = bot.send_message(message.chat.id, 'Выберите тип вагона', reply_markup=keyboard)
        bot.register_next_step_handler(sent, follow_the_train)


def follow_the_train(message):
    if message.text[1:] not in coms:
        train['car_type'] = message.text
        count = 0
        good = False
        while not good:
            for option in train['options']:
                if option['number'] == train['number']:
                    for i in option['cars']:
                        if i['typeLoc'] == train['car_type']:
                            good = True
                            bot.send_message(message.chat.id, 'Ура! Появились билеты.')
                            bot.send_message(message.chat.id, 'Всего %s' % i['freeSeats'])
                            break
            if count == 0 and not good:
                bot.send_message(message.chat.id, 'За прошедший час ничего не появилось.')
                count = 30
            count -= 1
            if not good:
                time.sleep(118)
                try:
                    train['options'] = get_info(train['city0'], train['city1'], train['date'])
                except:
                    bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте ещё раз /new_search")

        bot.send_message(message.chat.id, 'Теперь вы можете выбрать другой поезд /new_search')


def get_city_id(city):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    req = 'https://pass.rzd.ru/suggester?stationNamePart=%s&lang=ru&lat=0&compactMode=y' % quote(city.upper())

    city = city.upper()
    resp = requests.get(req, headers=headers)

    rJson = json.loads(resp.text)
    for item in rJson:
        if item['n'] == city:
            return str(item['c'])
    for item in rJson:
        if city in item['n']:
            return str(item['c'])
    return None


def get_info(city0, city1, date):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    id0 = get_city_id(city0)
    id1 = get_city_id(city1)
    req1 = 'https://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5371&dir=0&tfl=3&checkSeats=0&st0=%s&code0=%s&dt0=%s&st1=%s&code1=%s&dt1=%s' % (quote(city0), id0, date, quote(city1), id1, date)

    res = requests.get(req1, headers=headers, timeout=10)
    r = json.loads(res.text)
    rid = str(r['rid'])

    time.sleep(2)

    req2 = 'https://pass.rzd.ru/timetable/public/ru?STRUCTURE_ID=735&layer_id=5371&dir=0&tfl=3&checkSeats=0&st0=%s&code0=%s&dt0=%s&st1=%s&code1=%s&dt1=%s&rid=%s' % (quote(city0), id0, date, quote(city1), id1, date, rid)

    res_out = json.loads(requests.get(req2, cookies=res.cookies, headers=headers, timeout=10).text)

    return res_out['tp'][0]['list']


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    bot.polling(none_stop=True)
