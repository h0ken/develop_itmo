import json
import telebot
from consts import API_TOKEN

# Загрузка FAQ из файла
with open('parsing_faq_itmo/faq_itmo.json', 'r', encoding='utf-8') as f:
    faq_list = json.load(f)  # список словарей {"question": ..., "answer": ...}

bot = telebot.TeleBot(API_TOKEN)

def find_best_answer(user_question):
    user_question_lower = user_question.lower()
    # Сначала ищем точное вхождение по вопросу
    for item in faq_list:
        if user_question_lower in item['question'].lower():
            return item['answer']
    # Если не нашли, ищем совпадение по ключевым словам
    user_words = set(user_question_lower.split())
    for item in faq_list:
        question_words = set(item['question'].lower().split())
        if user_words.intersection(question_words):
            return item['answer']
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я помощник по программам ИТМО. Задайте любой вопрос из раздела 'Часто задаваемые вопросы'."
    )

@bot.message_handler(func=lambda message: True)
def handle_question(message):
    user_text = message.text
    answer = find_best_answer(user_text)
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(
            message.chat.id,
            "Извините, я не смог найти ответ на ваш вопрос. Попробуйте сформулировать иначе."
        )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
