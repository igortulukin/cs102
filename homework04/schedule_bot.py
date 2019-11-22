import os

import requests
from flask import Flask, request
import telebot
from datetime import datetime
from bs4 import BeautifulSoup

TOKEN = "703416161:AAH5hTppEBAjrfX1qJWMRKz08nPh5_Pj3ng"

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{week}{group}/raspisanie_zanyatiy_{group}.htm'.format(
        domain='http://www.ifmo.ru/ru/schedule',
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_day(message):
    """ Получить расписание на день """
    days = {'/monday': '1day', '/tuesday': '2day', '/wednesday': '3day',
            '/thursday': '4day', '/friday': '5day',
            '/saturday': '6day', '/sunday': '7day'}
    text = message.text.split()
    if len(text) == 2:
        day, group = text
        week = '0'
    elif len(text) == 3:
        day, group, week = text
    else:
        'Вывести : неправильный формат ввода'
    day = days.get(day)
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    day = datetime.now().isoweekday()

    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    pass


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://schedule-personal-bot.herokuapp.com/' + TOKEN)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
