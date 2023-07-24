import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import entity
import urllib3

urllib3.disable_warnings()

headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('news.db')
cursor = conn.cursor()

# Создаем таблицу для новостей, если она еще не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        content TEXT,
        annotation TEXT,
        name_entity TEXT,
        flag_annotation TEXT,
        flag_news TEXT
    )
''')

def parse_sledcom_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим последнюю загруженную новость
        latest_news_block = soup.find('div', class_='bl-item clearfix')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            titles = latest_news_block.find_all('a')
            title = titles[1].text.strip()
            news_url = 'https://volgograd.sledcom.ru' + titles[1]['href']
            content = parse_sledcom_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставуф ляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (title, news_url, content, '-', '-', '0', '0'))
                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")

def parse_sledcom_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент <article>, содержащий текст новости
    article = soup.find('article')

    # Ищем все параграфы
    paragraphs = article.find_all('p')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
    return content

def parse_mvd_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим последнюю загруженную новость
        latest_news_block = soup.find('div', class_='sl-item-title')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            title = latest_news_block.find('a').text.strip()
            news_url = 'https://34.xn--b1aew.xn--p1ai/' + latest_news_block.find('a')['href']
            content = parse_mvd_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставуф ляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (title, news_url, content, '-', '-', '0', '0'))
                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")

def parse_mvd_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент <article>, содержащий текст новости
    article = soup.find('div', class_='article')

    # Ищем все параграфы
    paragraphs = article.find_all('p')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
    return content

def parse_volgadmin_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим последнюю загруженную новость
        latest_news_block = soup.find('div', class_='news_item')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            titles = latest_news_block.find_all('a')
            title = titles[1].text.strip()
            news_url = 'https://www.volgadmin.ru/d' + titles[1]['href']
            content = parse_volgadmin_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставуф ляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (title, news_url, content, '-', '-', '0', '0'))
                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")

def parse_volgadmin_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент <article>, содержащий текст новости
    article = soup.find('div', class_='rightcol')

    # Ищем все параграфы
    paragraphs = article.find_all('p')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
    return content

def parse_volgograd_news_page(url):
    try:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим последнюю загруженную новость
        latest_news_block = soup.find('div', class_='col-md-12 news-item')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            title = latest_news_block.find('a').text.strip()
            news_url = 'https://www.volgograd.ru' + latest_news_block.find('a')['href']
            content = parse_volgograd_news_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставуф ляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (title, news_url, content, '-', '-', '0', '0'))
                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")


def parse_volgograd_news_content(url):
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент <article>, содержащий текст новости
    article = soup.find('div', class_='news-detail')

    # Ищем все параграфы
    paragraphs = article.find_all('p')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
    return content

# Функция для парсинга страницы с новостями на сайте TASS
def parse_news_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим последнюю загруженную новость
        latest_news_block = soup.find('a', class_='tass_pkg_link-v5WdK')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            title = latest_news_block.find('span', class_='ds_ext_title-1XuEF').text.strip()
            news_url = 'https://tass.ru' + latest_news_block['href']
            content = parse_news_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                               (title, news_url, content, '-', '-', '0', '0'))
                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")


# Функция для парсинга текста новости на сайте TASS
def parse_news_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент <article>, содержащий текст новости
    article = soup.find('article')

    # Ищем все параграфы с классом 'Paragraph_paragraph__nYCys'
    paragraphs = article.find_all('p', class_='Paragraph_paragraph__nYCys')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
    # Обрезаем контент новости до фразы "ТАСС"
    #content = content.split('/ТАСС/.', 1)[1]

    return content


# Функция для парсинга страницы с новостями на сайте Генпрокуратуры
def parse_genproc_page(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим последнюю добавленную новость
        latest_news_block = soup.find('div', class_='feeds-main-page-portlet__list_item')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            title = latest_news_block.find('a', class_='feeds-main-page-portlet__list_text').text.strip()
            news_url = latest_news_block.find('a', class_='feeds-main-page-portlet__list_text')['href']
            content = parse_genproc_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                               (title, news_url, content, '-', '-', '0', '0'))
                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")

# Функция для парсинга текста новости на сайте Генпрокуратуры
def parse_genproc_content(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент с классом feeds-page__article_text
    article_text = soup.find('div', class_='feeds-page__article_text')

    # Ищем все параграфы внутри элемента
    paragraphs = article_text.find_all('p')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)

    return content


def parse_vesti_page(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим блок с классом list__item
        latest_news_block = soup.find('div', class_='list__item')

        # Проверяем, что новость найдена
        if latest_news_block:
            # Находим заголовок, ссылку и текст новости
            title = latest_news_block.find('h3', class_='list__title').text.strip()
            news_url = 'https://www.vesti.ru' + latest_news_block.find('a', href=True)['href']
            content = parse_vesti_content(news_url)

            # Проверяем, не добавлена ли уже эта новость в базу данных
            cursor.execute('SELECT id FROM news WHERE url=?', (news_url,))
            existing_news = cursor.fetchone()
            if not existing_news:
                # Вставляем данные в базу данных
                cursor.execute('INSERT INTO news (title, url, content, annotation, name_entity, flag_annotation, flag_news) VALUES (?, ?, ?, ?, ?, ?, ?)',
                               (title, news_url, content, '-', '-', '0', '0'))

                conn.commit()
                print(f"Обнаружена новая новость: {news_url}")

                # Добавление сущностей
                cursor.execute("SELECT content FROM news")
                texts = cursor.fetchall()
                entity.names_entity(texts)

            else:
                print("Новых новостей нет!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из {url}: {e}")


def parse_vesti_content(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент с классом js-mediator-article
    article = soup.find('div', class_='js-mediator-article')

    # Ищем все параграфы внутри элемента
    paragraphs = article.find_all('p')

    # Собираем текст новости из всех параграфов
    content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)

    return content

# Основной код
if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        print(f"{i}-й прогон")
        parse_sledcom_page('https://volgograd.sledcom.ru/')
        parse_mvd_page('https://34.xn--b1aew.xn--p1ai/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8')
        parse_volgadmin_page('https://www.volgadmin.ru/d/list/news/admvlg')
        parse_volgograd_news_page('https://www.volgograd.ru/news/')
        parse_news_page('https://tass.ru/tag/volgogradskaya-oblast')
        parse_genproc_page('https://epp.genproc.gov.ru/web/proc_34')
        parse_vesti_page('https://www.vesti.ru/search?q=%D0%B2%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4&type=news&sort=date')
        time.sleep(15)

# Закрываем подключение к базе данных
conn.close()


