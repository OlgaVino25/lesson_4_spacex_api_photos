import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='telegram.utils.request')
import argparse
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError


def validate(token, chat_id):
    """Проверяет наличие обязательных параметров для Telegram API.
    
    Args:
        token (str): Токен Telegram-бота
        chat_id (str): ID чата/канала
        
    Raises:
        ValueError: Если не указан токен или chat_id
    """
    if not token:
        raise ValueError('Не указан токен бота!')
    if not chat_id:
        raise ValueError('Не указан chat_id!')


def handle_telegram_errors(e):
    """Обрабатывает ошибки Telegram API и преобразует в понятные исключения.
    
    Args:
        e (TelegramError): Исходное исключение
        
    Raises:
        ValueError: Для ошибок связанных с чатом или форматом
        PermissionError: Для ошибок доступа
        RuntimeError: Для других ошибок API
    """
    if "Chat not found" in str(e):
        raise ValueError(f"Чат {chat_id} не существует или бот не добавлен в него") from e
    elif "Forbidden" in str(e):
        raise PermissionError("Бот заблокирован в этом чате") from e
    elif "Too Many Requests" in str(e):
        raise RuntimeError("Превышен лимит запросов. Повторите через 10 минут") from e
    else:
        raise RuntimeError(f"Ошибка отправки: {e}") from e


def send_massage(token, chat_id, text):
    """Отправляет текстовое сообщение в Telegram чат/канал.
    
    Args:
        token (str): Токен Telegram-бота (можно указать в .env как TG_BOT_TOKEN)
        chat_id (str): ID чата/канала для отправки сообщений (можно указать в .env как TG_GROUP_CHAT_ID)
        text (str): Текст сообщения для отправки

    Raises:
        ValueError: Если не указан токен или chat_id
        TelegramError: При ошибках API Telegram
    """
    validate(token, chat_id)
    bot = Bot(token=token)

    try:
        bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        handle_telegram_errors(e)


def send_photo(token, chat_id, photo_path, caption=None):
    """Отправляет фото в Telegram чат/канал.
    
    Args:
        token (str): Токен Telegram-бота (можно указать в .env как TG_BOT_TOKEN)
        chat_id (str): ID чата/канала для отправки сообщений (можно указать в .env как TG_GROUP_CHAT_ID)
        photo_path (str): Путь к файлу изображения
        caption (str, optional): Подпись к фото
    Raises:
        ValueError: Если не указан токен или chat_id
        FileNotFoundError: Если файл не найден
        TelegramError: При ошибках API Telegram
    """
    validate(token, chat_id)
    bot = Bot(token=token)

    try:
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id=chat_id, photo=photo_file, caption=caption)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{photo_path}' не найден. Проверьте путь и права доступа") from None
    except TelegramError as e:
        handle_photo_errors(e)


def parse_arguments():
    """Парсит аргументы командной строки и переменные окружения.
    
    Returns:
        Namespace: Объект с аргументами командной строки
    """
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Отправка сообщений и фото в Telegram через бота CosmoPicBot')
    parser.add_argument('--token', default=os.getenv('CosmoPicBot_TG_TOKEN'), metavar='', help='Telegram Bot Token (или укажите в TG_BOT_TOKEN в .env)')
    parser.add_argument('--chat_id', default=os.getenv('GROUP_CHAT_ID'), metavar='', help='ID группы/чата (или укажите в TG_GROUP_CHAT_ID в .env)')
    parser.add_argument('--text', metavar='', help='Текст сообщения для отправки')
    parser.add_argument('--photo', metavar='', help='Путь к фото для отправки в группу')
    parser.add_argument('--caption', metavar='', help='Описание для фото')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    if args.text:
        send_massage(token=args.token, chat_id=args.chat_id, text=args.text)
        print('Сообщение отправлено!')

    if args.photo:
        send_photo(token=args.token, chat_id=args.chat_id, photo_path=args.photo, caption=args.caption)
        print('Фото отправлено!')

if __name__ == '__main__':
    main()
