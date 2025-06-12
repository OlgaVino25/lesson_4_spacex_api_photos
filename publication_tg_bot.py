import argparse
import os
import time
import random
from pathlib import Path
from dotenv import load_dotenv
from tg_bot import send_photo

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

def collect_photos(directory: str) -> list:
    """Собирает все фотографии из директории и поддиректорий"""
    photos = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                photos.append(file_path)
    return photos

def publish_photos(
        directory: str,
        interval_hours: int,
        caption: str = None,
        shuffle: bool = False,
        token: str =os.getenv('CosmoPicBot_TG_TOKEN'),
        chat_id: str = os.getenv('GROUP_CHAT_ID')
        ):
    """Основной цикл публикации фотографий"""
    while True:
        try:
            photos = collect_photos(directory)
            if shuffle:
                random.shuffle(photos)

            for photo_path in photos:
                try:
                    if not photo_path.exists():
                        raise FileNotFoundError(f"Файл {photo_path} не найден")
                    
                    send_photo(
                        token=token,
                        chat_id=chat_id,
                        photo_path=str(photo_path),
                        caption=caption
                    )
                    print(f"Успешно опубликовано: {photo_path}")
                except (ConnectionError, requests.exceptions.RequestException) as e:
                    print(f"Сетевая ошибка при отправке {photo_path}: {e}")
                    time.sleep(300)
                except (IOError, OSError, FileNotFoundError) as e:
                    print(f"Ошибка доступа к файлу {photo_path}: {e}")
                except telegram.error.TelegramError as e:
                    print(f"Ошибка Telegram API ({e.__class__.__name__}): {e}")
                    if "retry after" in str(e).lower():
                        sleep_time = int(e.retry_after) if hasattr(e, 'retry_after') else 60
                        time.sleep(sleep_time)
                except Exception as e:
                    print(f"Неожиданная ошибка при отправке {photo_path}: {e}")
                    raise

                time.sleep(interval_hours * 3600)

        except (OSError, FileNotFoundError) as e:
            print(f"Ошибка доступа к директории: {e}. Перезапуск через 5 минут")
            time.sleep(300)
        except KeyboardInterrupt:
            print("\nРабота приложения прервана пользователем")
            break
        except Exception as e:
            print(f"Критическая ошибка: {e}. Перезапуск через 5 минут")
            time.sleep(300)

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Автоматическая публикация фотографий в Telegram')
    parser.add_argument('--token', default=os.getenv('CosmoPicBot_TG_TOKEN'), metavar='', help='Telegram Bot Token (или укажите в TG_BOT_TOKEN в .env)')
    parser.add_argument('--chat_id', default=os.getenv('GROUP_CHAT_ID'), metavar='', help='ID группы/чата (или укажите в TG_GROUP_CHAT_ID в .env)')
    parser.add_argument('--dir', required=True, type=Path, metavar='Путь', help='Обязательный путь к директории с фотографиями')
    parser.add_argument('--interval', type=int, default=4, metavar='', help='Интервал публикации в часах (по умолчанию: 4)')
    parser.add_argument( '--caption', metavar='', help='Подпись для фотографий')
    parser.add_argument( '--shuffle', action='store_true', help='Перемешивать фотографии перед отправкой')
    args = parser.parse_args()

    publish_photos(directory=args.dir, interval_hours=args.interval, caption=args.caption, shuffle=args.shuffle, token=args.token, chat_id=args.chat_id)

if __name__ == '__main__':
    main()
