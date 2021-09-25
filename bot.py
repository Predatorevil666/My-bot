"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
import time
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='bot.log', level=logging.INFO, filemode='w')

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}} # - для обхода блокировок нашего бота через прокси сервер

def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(f'Привет, пользователь! {text}')
    time.sleep(2)
    text_2 = 'Вызван /planet'
    print(text_2)
    update.message.reply_text('Может ты хочешь узнать, где находится твоя планета ?\nВведи запрос вида /planet Mars')


def planets(update, context):
        user_planet = update.message.text.split()[1]
        print(user_planet)
        try:
            planet = getattr(ephem, user_planet)()             # - получения атрибута planet обьекта ephem
            planet.compute(ephem.Date(datetime.date.today()))    # - для задания настоящего времени
            result = ephem.constellation(planet)           # - определение созвездия нашей планеты
            text = f'Планета "{planet}" находится сейчас в созвездии {result}.'
            print(text)
            update.message.reply_text(text)
        except AttributeError:
            update.message.reply_text(f'Планеты с названием "{user_planet}" я не знаю !')


def talk_to_me(update, context):
    user_text = update.message.text           # - сообщение от пользователя(хранится в update....)
    print(user_text)
    if user_text == 'привет':
        update.message.reply_text('И тебе привет')
    else:
        update.message.reply_text(user_text)      # - для отправки пользователю его же сообщение
def main():

    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)  # -Создание переменной для того чтобы бот стучался на телеграм
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planets))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # -обработчик сообщений с параметрами приема текстовых сообщений и функцией talk_to_me
    logging.info('Бот стартовал')  # - чтобы в лог файле писалось эта фраза при старте бота
    mybot.start_polling()  #-Для взаимодейтсвия бота с телеграм(просыпается и спрашивает телеграм есть для него что-то или нет)
    mybot.idle() # - чтобы работал постоянно пока мы его сами не остановим
if __name__ == "__main__":
    main()


