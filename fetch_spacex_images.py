import argparse
import requests
from download_utils import download_images


def fetch_spacex_photos(launch_id=None, folder='images', filename_prefix='spacex'):
    """
    Скачивает фотографии запусков SpaceX с помощью официального API.

    Загружать оригинальные фотографии с запусков SpaceX.
    По умолчанию скачивает фото последнего запуска, но можно указать конкретный ID.

    Args:
        launch_id (str, optional): ID запуска SpaceX. Если не указан, скачивает фото
            последнего запуска. Пример ID: '5eb87d42ffd86e000604b384'
        folder (str, optional): Путь к папке для сохранения фотографий
        filename_prefix (str, optional): Префикс имени файлов

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: При ошибке запроса к API SpaceX.
        Exception: При других непредвиденных ошибках.
    """
    api_url = f'https://api.spacexdata.com/v5/launches/{launch_id or "latest"}'

    response = requests.get(api_url)
    response.raise_for_status()
    photos = response.json().get('links', {}).get('flickr', {}).get('original', [])
    if photos:
        print(f'Найдено {len(photos)} фото. Скачиваю...')
        download_images(photos, folder, filename_prefix)
        print('Готово!')
    else:
        print(f'Фото не найдены для запуска {launch_id or "latest"}')


def parse_arguments():
    """Парсит аргументы командной строки и загружает переменные окружения.

    Returns:
        Namespace: Объект с аргументами командной строки

    """
    parser = argparse.ArgumentParser(description='Скачивание фото запусков SpaceX')
    parser.add_argument('--id', metavar='', help='ID запуска (например: 5eb87d42ffd86e000604b384)\n''Оставьте пустым для последнего запуска')
    parser.add_argument('--folder', default='spacex_images', metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_prefix', default='spacex', metavar='', help='Имя файлов')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    fetch_spacex_photos(
        args.id, args.folder,
        args.filename_prefix
    )


if __name__ == '__main__':
    main()
