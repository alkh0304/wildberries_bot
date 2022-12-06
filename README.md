# wildberries_bot

## Описание:
Бот парсит первые 100 страниц поискового запроса вайлдбериз, в поисках конкретного предмета. Бот также может учитывать местоположение клиента, при выполнении поиска.

## Стек
- [Python](https://www.python.org/);
- [Requests](https://pypi.org/project/requests/);
- [Python-dotenv](https://pypi.org/project/python-dotenv/);
- [Aiogram](https://docs.aiogram.dev/en/latest/);
- [Selenium](https://www.selenium.dev);
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/).

## Как запустить программу:

1) Клонируйте репозитроий с программой:
```
git clone https://github.com/alkh0304/wildberries_bot
```
2) В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости:
```
python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt
```
3) Создайте чат-бота Телеграм
4) Создайте в директории файл .env и поместите туда токен в формате TELEGRAM_TOKEN = 'ххххххххххх'
5) Запустите бота, введя в командной строке "python bot.py"
6) Чтобы начать работу с ботом отправьте ему "/start"

## Над проектом [Wildberries_bot](https://github.com/alkh0304/wildberries_bot) работал:

[Александр Хоменко](https://github.com/alkh0304)