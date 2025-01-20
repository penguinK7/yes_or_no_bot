import logging
import os
import requests
from dotenv import load_dotenv
from telebot import TeleBot

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота
secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

# URL для API
URL = 'https://yesno.wtf/api'

def get_gif_response():
    """Получение ответа и GIF из API."""
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data.get('answer'), data.get('image')
    except requests.RequestException as error:
        logging.error(f'Ошибка при запросе к API: {error}')
        return None, None

@bot.message_handler(commands=['start'])
def wake_up(message):
    """Приветственное сообщение при запуске бота."""
    chat_id = message.chat.id
    name = message.from_user.first_name

    bot.send_message(
        chat_id=chat_id,
        text=f'Здравствуйте, {name}! Этот бот поможет принять вам жизненно важные решения. Пожалуйста, задайте свой вопрос.',
    )

@bot.message_handler(content_types=['text'])
def handle_question(message):
    """Обработка текстовых сообщений от пользователя."""
    chat_id = message.chat.id
    answer, gif_url = get_gif_response()

    if answer and gif_url:
        bot.send_message(chat_id, f'Ответ на ваш вопрос: {answer}')
        bot.send_animation(chat_id, gif_url)
    else:
        bot.send_message(chat_id, 'Извините, произошла ошибка при получении ответа.')

def main():
    """Запуск бота."""
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()