import re
import asyncio
from aiogram import Bot, Dispatcher, types
from bs4 import BeautifulSoup

API_TOKEN = "7562843965:AAGz0ZlUZfCQUktWDwUCFrYCKIFUUXR8FCA"
TG_LINK_REGEX = r"https://t\.me/[a-zA-Z0-9_/]+"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def extract_links_from_message(message: types.Message):
    """Извлекает Telegram-ссылки из сообщения."""
    links = set()

    # Извлечение ссылок из HTML (если сообщение содержит разметку)
    if message.html_text:
        soup = BeautifulSoup(message.html_text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            if "t.me" in a_tag["href"]:
                links.add(a_tag["href"])

    # Извлечение из обычного текста
    if message.text:
        text_links = re.findall(TG_LINK_REGEX, message.text)
        links.update(text_links)

    return links

async def save_new_links_to_file(links: set):
    """Перезаписывает файл links.txt новыми ссылками из текущего сообщения."""
    with open("links.txt", "a") as file:
        for link in sorted(links):  # Сортируем для упорядоченности
            file.write(link + "\n")
    print(f"Файл перезаписан. Сохранены ссылки: {', '.join(sorted(links))}")

@dp.message()
async def find_and_save_links(message: types.Message):
    """Находит ссылки в сообщении и перезаписывает файл только новыми ссылками."""
    links = await extract_links_from_message(message)
    if links:
        await save_new_links_to_file(links)
    else:
        print("Ссылки не найдены. Файл не обновлён.")

async def main():
    """Запускает бота."""
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
