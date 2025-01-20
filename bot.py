import logging
import os
import requests

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()

secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

URL = 'https://yesno.wtf/api'

def get_gif_response():
    try:
        response = requests.get(URL).json()
        answer = response.get('answer')
        gif_url = response.get('image')
        return answer, gif_url
    except Exception as error:
        logging.error(f'Ошибка при запросе к API: {error}')
        return None, None

@bot.message_handler(commands=['start'])
def wake_up(message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/question')
    keyboard.add(button)

    bot.send_message(
        chat_id=chat_id,
        text=f'Здравствуйте, {name}! Этот бот поможет принять вам жизненно важные решения.',
        reply_markup=keyboard,
    )

@bot.message_handler(commands=['question'])
def new_question(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ждем ваш вопрос.")

@bot.message_handler(content_types=['text'])
def handle_question(message):
    chat_id = message.chat.id
    answer, gif_url = get_gif_response()

    if answer and gif_url:
        bot.send_message(chat_id, f'Ответ на ваш вопрос: {answer}')
        bot.send_animation(chat_id, gif_url)
    else:
        bot.send_message(chat_id, 'Извините, произошла ошибка при получении ответа.')

def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()