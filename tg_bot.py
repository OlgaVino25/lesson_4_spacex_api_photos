import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="telegram.utils.request")
import argparse
import os
from dotenv import load_dotenv
from telegram import Bot
def main():
    """
    Telegram Bot для отправки сообщений и изображений в группу/канал.

    Этот скрипт позволяет отправлять текстовые сообщения и изображения через Telegram-бота.
    Поддерживает загрузку файлов с локального диска и отправку сообщений с произвольным текстом.

    Args:
        --token (str): Токен Telegram-бота (можно указать в .env как TG_BOT_TOKEN)
        --chat_id (str): ID группы/канала для отправки сообщений (можно указать в .env как TG_GROUP_CHAT_ID)
        --text (str): Текст сообщения для отправки
        --photo (str): Путь к файлу изображения для отправки
        --caption (str): Описание к отправляемому изображению

    Raises:
        ValueError: Если не указан токен бота или chat_id
        FileNotFoundError: Если указанный файл изображения не найден
        TelegramError: При ошибках при отправке сообщений через Telegram API

    Examples:
        python tg_bot.py --text "Привет, группа!"
        python tg_bot.py --photo images/space.jpg --caption "Космический снимок"
    """
    load_dotenv()

    parser = argparse.ArgumentParser(description='Отправка сообщений в Telegram через бота CosmoPicBot')
    parser.add_argument('--token', default=os.getenv('CosmoPicBot_TG_TOKEN'), metavar='', help='Telegram Bot Token (или укажите в TG_BOT_TOKEN в .env)')
    parser.add_argument('--chat_id', default=os.getenv('GROUP_CHAT_ID'), metavar='', help='ID группы/чата (или укажите в TG_GROUP_CHAT_ID в .env)')
    parser.add_argument('--text', metavar='', help='Текст сообщения для отправки')
    parser.add_argument('--photo', metavar='', help='Путь к фото для отправки в группу')
    parser.add_argument('--caption', metavar='', help='Описание для фото')
    args = parser.parse_args()

    if not args.token:
        raise ValueError("Не указан токен бота! Используйте --token или .env (TG_BOT_TOKEN)")
    if not args.chat_id:
        raise ValueError("Не указан chat_id! Используйте --chat-id или .env (TG_GROUP_CHAT_ID)")

    bot = Bot(token=args.token)

    if args.text:
        try:
            bot.send_message(chat_id=args.chat_id, text=args.text)
            print("Сообщение отправлено!")
        except TelegramError as e:
            print(f"Ошибка отправки сообщения: {e}")

    if args.photo:
        try:
            with open(args.photo, 'rb') as photo_file:
                bot.send_photo(chat_id=args.chat_id, photo=photo_file, caption=args.caption if args.caption else None)
                print("Фото отправлено!")
        except FileNotFoundError:
            print(f"Ошибка: Файл {args.photo} не найден!")
        except TelegramError as e:
            print(f"Ошибка Telegram: {e}")

if __name__ == '__main__':
    main()
