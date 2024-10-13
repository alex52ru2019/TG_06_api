# Разработайте телеграм-бота со своим функционалом с использованием разных сторонних api
# https://developer.nytimes.com/
# скрипт выдаст случайную короткую новость от NY Times

import asyncio
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
import requests
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, NY_TIMES_API
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

def get_random_news():
    url = f'https://api.nytimes.com/svc/topstories/v2/world.json?api-key={NY_TIMES_API}'
    response = requests.get(url)
    data = response.json()
    list_news = []
    for i in data['results']:
        if i['abstract']:
            list_news.append(i['abstract'])
    random_news = random.choice(list_news)
    return random_news

def translate_ru(text):
    return translator.translate(text, dest='ru').text

@dp.message(Command("random_news"))
async def random_news(message: Message):
    news = get_random_news()
    news_rus = translator.translate(news, dest='ru').text
    await message.answer(news_rus)
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())