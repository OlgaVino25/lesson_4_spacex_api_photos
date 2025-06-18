import argparse
import os
from dotenv import load_dotenv
import requests
from download_utils import download_images
from datetime import datetime


def fetch_epic_photos(api_key, folder, filename_prefix, max_downloads=None):
    """
    Скачивает последние фотографии Земли NASA API.

    Запрашивает данные из NASA API EPIC и скачивает до 10 последних фотографий Земли в формате PNG.

    Args:
        api_key (str): Ключ API NASA
        folder (str): Папка для сохранения изображений
        filename_prefix (str): Префикс имени файла для сохраненных изображений
        max_downloads (int, optional): Максимальное количество фото.
            Если None — скачивает все доступные. По умолчанию None.

    Returns:
        None
    """
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    earth_images = response.json()
    image_urls = []
    for image in earth_images:
        capture_date = datetime.fromisoformat(image['date'])
        formatted_date = capture_date.strftime('%Y/%m/%d')
        image_name = image['image']
        url = f"https://epic.gsfc.nasa.gov/archive/natural/{formatted_date}/png/{image_name}.png"
        image_urls.append(url)

    images_to_download = image_urls[:max_downloads] if max_downloads else image_urls
    print(f'Скачиваю {len(images_to_download)} изображений...')
    download_images(
        image_urls=images_to_download,
        folder=folder,
        filename_prefix=filename_prefix
    )
    print('Готово!')


def parse_arguments(default_key=None, default_folder='epic_images'):
    """Парсит аргументы командной строки и загружает переменные окружения.

    Args:
        default_key: Значение ключа по умолчанию (из окружения)
        default_folder: Папка для сохранения по умолчанию

    Returns:
        Namespace: Объект с аргументами командной строки

    Raises:
        ValueError: Если не указан API ключ
    """
    parser = argparse.ArgumentParser(description='Скачивание фото EPIC')
    parser.add_argument('--key', default=default_key, help='NASA API ключ')
    parser.add_argument('--folder', default=default_folder, metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_prefix', default='epic_photo', metavar='', help='Имя файлов (по умолчанию: epic_photo)')
    parser.add_argument('-md', '--max_downloads', type=int, default=None, metavar='', help='Макс. количество фото (по умолчанию — все)')
    return parser.parse_args()


def main():
    load_dotenv()
    env_key = os.getenv('NASA_API_KEY')
    default_folder = 'epic_images'
    args = parse_arguments(default_key=env_key, default_folder=default_folder)

    fetch_epic_photos(
        api_key=args.key,
        folder=args.folder,
        filename_prefix=args.filename_prefix,
        max_downloads=args.max_downloads
        )


if __name__ == '__main__':
    main()
