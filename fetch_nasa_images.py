import argparse
import os
from dotenv import load_dotenv
import requests
from download_utils import download_images


def fetch_nasa_photos(api_key, folder, filename_prefix, count=30):
    """
    Скачивает изображения NASA API.

    Запрашивает данные из NASA API EPIC и скачивает до 10 последних фотографий Земли в формате PNG.

    Args:
        api_key (str): Ключ API NASA
        folder (str): Папка для сохранения изображений
        filename_prefix (str): Префикс имени файла для сохраненных изображений
        count (int): Количество изображений для загрузки (по умолчанию 30)

    Returns:
        None
    """
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': count,
        'thumbs': True
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    apod_images = response.json()
    image_urls = [item['url'] for item in apod_images if item['media_type'] == 'image']

    if image_urls:
        print(f'Найдено {len(image_urls)} фото. Скачиваю...')
        download_images(
            image_urls=image_urls,
            folder=folder,
            filename_prefix=filename_prefix
        )
        print('Готово!')


def parse_arguments(default_key=None, default_folder='nasa_images'):
    """Парсит аргументы командной строки и загружает переменные окружения.

    Args:
        default_key: Значение ключа по умолчанию (из окружения)
        default_folder: Папка для сохранения по умолчанию

    Returns:
        Namespace: Объект с аргументами командной строки

    Raises:
        ValueError: Если не указан API ключ
    """
    parser = argparse.ArgumentParser(description='Скачивание фото NASA')
    parser.add_argument('--key', default=default_key, help='NASA API ключ')
    parser.add_argument('--folder', default=default_folder, metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_prefix', default='nasa', metavar='', help='Имя файлов (по умолчанию: nasa)')
    parser.add_argument('--count', type=int, default=30, metavar='', help='Количество фото')
    return parser.parse_args()


def main():
    load_dotenv()
    env_key = os.getenv('NASA_API_KEY')
    default_folder = 'nasa_images'
    args = parse_arguments(default_key=env_key, default_folder=default_folder)

    fetch_nasa_photos(
        api_key=args.key,
        folder=args.folder,
        filename_prefix=args.filename_prefix,
        count=args.count
        )


if __name__ == '__main__':
    main()
