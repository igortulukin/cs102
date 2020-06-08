import requests
import telebot
from datetime import datetime, timedelta
import datetime
from bs4 import BeautifulSoup

bot = telebot.TeleBot("915890602:AAH7AD7qLJc_gbYK1kx_2Xp3WB_sCmONKVU")

bot.remove_webhook()

days = {'/monday': '1day', '/tuesday': '2day', '/wednesday': '3day',
        '/thursday': '4day', '/friday': '5day',
        '/saturday': '6day', '/sunday': '7day'}


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/0/{group}/{week}raspisanie_zanyatiy_/{group}.htm'.format(
        domain='http://www.ifmo.ru/ru/schedule',
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


@bot.message_handler(commands=['start'])
def geetings():
    bot.send_message(message.chat.id, 'Дарова, в какой группе учишься?', parse_mode='HTML')


@bot.message_handler(commands=['text'])
def choose_group(message):
    web_page = get_page(message)
    if message in web_page:
        return
    else:
        message = ''
        bot.send_message(message.chat.id, 'Такой группы нет', parse_mode='HTML')


def parse_schedule(web_page, day, message):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на понедельник
    for key in days:
        if soup.find("table", attrs={"id": days[key]}) and soup.find("table", attrs={"id": day}) == None:
            bot.send_message(message.chat.id, 'Выходной', parse_mode='HTML')
            return
    if soup.find("table", attrs={"id": day}) == None:
        bot.send_message(message.chat.id, 'Такой группы нет!', parse_mode='HTML')
        return
    # Время проведения занятий
    schedule_table = soup.find("table", attrs={"id": day})
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    print(times_list)
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
    text = message.text.split()
    if len(text) == 2:
        day, group = text
        week = '0'
    elif len(text) == 3:
        day, group, week = text
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод!', parse_mode='HTML')
        return
    day = days.get(day)
    web_page = get_page(group, week)
    try:
        times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except TypeError:
        bot.send_message(message.chat.id, 'Выходной', parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    text = message.text.split()
    if len(text) == 1:
        bot.send_message(message.chat.id, 'Забыл группу!', parse_mode='HTML')
        return
    _, group = text
    day = datetime.date.today().weekday() + 2
    day = str(day) + "day"
    _, week, _ = datetime.date.today().isocalendar()
    week = (week + 1) % 2 + 1
    try:
        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except TypeError:
        bot.send_message(message.chat.id, 'Выходной', parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    text = message.text.split()
    if len(text) == 1:
        bot.send_message(message.chat.id, 'Забыл группу!', parse_mode='HTML')
        return
    _, group = text
    web_page = get_page(group)
    for i in days:
        try:
            times_lst, locations_lst, lessons_lst = parse_schedule(web_page, days[i])
            resp = ''
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id, 'Выходной', parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    text = message.text.split()
    if len(text) == 1:
        bot.send_message(message.chat.id, 'Забыл группу!', parse_mode='HTML')
        return
    _, group = text
    day = datetime.date.today().weekday() + 1
    print(day)
    day = str(day) + "day"
    _, week, _ = datetime.date.today().isocalendar()
    week = (week + 1) % 2 + 1
    now = datetime.datetime.now() + timedelta(hours=3)
    time = now.strftime("%H:%M")
    time = time.split(':')
    pos = -1
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
    for i in times_lst:
        pos += 1
        schedule_time = times_lst[pos].split('-')
        schedule_time = schedule_time[0]
        schedule_time = schedule_time.split(':')
        if int(time[0]) < int(schedule_time[0]) or (
                int(time[0]) == int(schedule_time[0]) and int(time[1]) < int(schedule_time[1])):
            print(times_lst[pos], locations_lst[pos], lessons_lst[pos])
            resp = '<b>{}</b>, {}, {}\n'.format(times_lst[pos], locations_lst[pos], lessons_lst[pos])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            return
    count = 0
    while count < 7:
        day = str(int(day.replace('day', '')) + 1) + 'day'
        if day == '7day':
            count += 1
            day = '1day'
        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
        resp = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        try:
            web_page = get_page(group, week)
            times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
            resp += '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            return
        except TypeError:
            continue
    bot.send_message(message.chat.id, 'Ближайших пар нет!', parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
