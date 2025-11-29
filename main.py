import telebot
import requests
import jsons
from typing import List, Optional

# Классы
class UsageResponse:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class MessageResponse:
    role: str
    content: str


class ChoiceResponse:
    index: int
    message: MessageResponse
    logprobs: Optional[str]
    finish_reason: str


class ModelResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[ChoiceResponse]
    usage: UsageResponse
    system_fingerprint: str


#Настройки
API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

LM_STUDIO_URL = ''

#Хранилище контекста
user_histories = {}


# Команды

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_histories[user_id] = []

    welcome_text = (
        "Привет! Я бот с памятью контекста.\n"
        "Доступные команды:\n"
        "/start - перезапуск бота\n"
        "/clear - очистить историю диалога (забыть контекст)\n"
        "/model - узнать текущую модель\n"
        "Просто напишите мне, и я отвечу, учитывая наш диалог."
    )
    bot.reply_to(message, welcome_text)


# Очистка контекста
@bot.message_handler(commands=['clear'])
def clear_context(message):
    user_id = message.from_user.id
    # Очищаем список сообщений для этого пользователя
    user_histories[user_id] = []
    bot.reply_to(message, "История диалога очищена! Я забыл всё, о чем мы говорили.")


@bot.message_handler(commands=['model'])
def send_model_name(message):
    try:
        response = requests.get('http://localhost:1234/v1/models')
        if response.status_code == 200:
            model_info = response.json()
            model_name = model_info['data'][0]['id']
            bot.reply_to(message, f"Используемая модель: {model_name}")
        else:
            bot.reply_to(message, 'Не удалось получить информацию о модели.')
    except Exception as e:
        bot.reply_to(message, f'Ошибка соединения с LM Studio: {e}')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_query = message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_query})

    request_payload = {
        "messages": user_histories[user_id],
        "temperature": 0.7,  # Можно настроить креативность
        "max_tokens": -1,  # -1 обычно значит "до лимита контекста"
        "stream": False
    }

    try:
        response = requests.post(
            LM_STUDIO_URL,
            json=request_payload
        )

        if response.status_code == 200:
            model_response: ModelResponse = jsons.loads(response.text, ModelResponse)
            assistant_reply = model_response.choices[0].message.content

            user_histories[user_id].append({"role": "assistant", "content": assistant_reply})

            bot.reply_to(message, assistant_reply)
        else:
            bot.reply_to(message, f'Ошибка API LM Studio: {response.status_code}')
            user_histories[user_id].pop()

    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка при обращении к модели: {e}')
        if user_histories.get(user_id):
            user_histories[user_id].pop()



if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
