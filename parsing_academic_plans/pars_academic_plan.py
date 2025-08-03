import requests
import re

# Функция, которая получает html-код страницы по ссылке
def load_page(url):
    print(f"Загружаем страницу: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Страница успешно загружена")
        return response.text
    else:
        print(f"Ошибка при загрузке страницы: {response.status_code}")
        return None

# Функция, которая ищет в html-коде ссылку на PDF учебного плана
def find_academic_plan_link(html_text):
    print("Ищем ссылку на учебный план...")
    # Регулярное выражение для поиска ссылки academic_plan
    pattern = r'"academic_plan":"(https://api\.itmo\.su/constructor-ep/api/v1/static/programs/\d+/plan/abit/pdf)"'
    match = re.search(pattern, html_text)
    if match:
        print("Ссылка на учебный план найдена!")
        # Убираем экранирование слэшей, если есть
        pdf_url = match.group(1).replace('\\u002F', '/')
        return pdf_url
    else:
        print("Ссылка на учебный план не найдена :(")
        return None

# Функция, которая скачивает PDF по ссылке и сохраняет его на диск
def download_pdf(pdf_url, filename):
    print(f"Скачиваем PDF по ссылке: {pdf_url}")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(pdf_url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF успешно сохранён в файл: {filename}")
    else:
        print(f"Ошибка при скачивании PDF: {response.status_code}")

# Главная часть программы — обрабатываем список программ
def main():
    program_urls = [
        "https://abit.itmo.ru/program/master/ai",
        "https://abit.itmo.ru/program/master/ai_product"
    ]
    
    for url in program_urls:
        html = load_page(url)
        if html is None:
            continue  # если страницу не загрузили — переходим к следующему URL
        
        pdf_url = find_academic_plan_link(html)
        if pdf_url is None:
            continue  # если ссылку не нашли — переходим к следующему URL
        
        # Имя файла возьмём из последней части URL программы
        program_name = url.rstrip('/').split('/')[-1]
        filename = program_name + "_academic_plan.pdf"
        
        download_pdf(pdf_url, filename)

if __name__ == "__main__":
    main()
