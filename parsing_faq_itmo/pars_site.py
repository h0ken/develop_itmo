import requests
from bs4 import BeautifulSoup
import json

def parse_faq(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Классы вопросов и ответов
    QUESTION_CLASS = 'Accordion_accordion__title__tSP_0'
    ANSWER_CLASS = 'Accordion_accordion__info__wkCQC'

    # Находим все блоки, которые либо вопросы, либо ответы
    faq_blocks = soup.find_all(
        lambda tag: tag.name == 'div' and 
                    (QUESTION_CLASS in tag.get('class', []) or ANSWER_CLASS in tag.get('class', []))
    )

    faq = []
    current_question = None

    for block in faq_blocks:
        classes = block.get('class', [])
        if QUESTION_CLASS in classes:
            # Вопрос — ищем текст в <h5>
            h5 = block.find('h5')
            if h5:
                current_question = h5.get_text(strip=True)
        elif ANSWER_CLASS in classes:
            # Ответ — ищем вложенный div с текстом
            if current_question is None:
                # Если ответ встречается без вопроса — игнорируем
                continue
            inner_div = block.find('div')
            if inner_div:
                answer = inner_div.get_text(strip=True)
                faq.append({
                    "question": current_question,
                    "answer": answer
                })
                current_question = None  # сбрасываем для следующей пары

    return faq

def save_faq_to_json(faq, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)
    print(f"FAQ сохранён в файл {filename}")

if __name__ == "__main__":
    urls = [
        "https://abit.itmo.ru/program/master/ai",
        "https://abit.itmo.ru/program/master/ai_product"
    ]

    all_faq = []
    for url in urls:
        print(f"Парсим FAQ с {url} ...")
        faq = parse_faq(url)
        all_faq.extend(faq)

    save_faq_to_json(all_faq, "faq_itmo.json")
