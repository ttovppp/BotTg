import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import json


# настройки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# токен
TOKEN = 'токен от BotFather'
# OpenAI API Key
OPENAI_API_KEY = 'ключик'
# OpenAI Model
OPENAI_MODEL = 'gpt-3.5-turbo'
# характер товарища
BOT_PERSONALITY = 'Answer in a friendly tone, '

# стартовая команда
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Приветик Чем я могу быть полезен? Проси что хочешь!')

# обработка соообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    prompt = f"{BOT_PERSONALITY}{user_input}"
    
    #Вызов OpenAI API
    response = openai_api(prompt)

    # Обратный ответ
    update.message.reply_text(response)

# взаимодействие OpenAI API
def openai_api(prompt: str) -> str:
    try:
        # запрос на OpenAI API
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
            json={'model': OPENAI_MODEL, 'messages': [{"role": "user", "content": prompt}], 'temperature': 0.5, 'max_tokens': 300},
            timeout=10
        ) 

        result = response.json()
        final_result = ''
        for i in range(0, len(result['choices'])):
            final_result += result['choices'][i]['message']['content']

        return final_result
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return " Я что-то не понял( Давай по новой!"

def main() -> None:
    # обновления
    updater = Updater(TOKEN)

    # регистрация обр.
    dp = updater.dispatcher

    # ккоманды и смс
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    
    # стартуем
    updater.start_polling()

    # пусть работает пока не остановят
    updater.idle()

if __name__ == '__main__':
    main()
