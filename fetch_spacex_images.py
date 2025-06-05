import argparse
import requests
from download_utils import download_images


def fetch_spacex_photos(launch_id=None, download_folder='images', filename_number='spacex'):
    """Получает фото запуска SpaceX"""
    api_url = f'https://api.spacexdata.com/v5/launches/{launch_id or "latest"}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        photos = response.json().get('links', {}).get('flickr', {}).get('original', [])
        if photos:
            print(f'Найдено {len(photos)} фото. Скачиваю...')
            download_images(photos, download_folder, filename_number)
            print('Готово!')
        else:
            print(f'Фото не найдены для запуска {launch_id or "latest"}')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе к API SpaceX: {e}')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

def main():
    parser = argparse.ArgumentParser(description='Скачивание фото запусков SpaceX')
    parser.add_argument('--id', help='ID запуска (например: 5eb87d42ffd86e000604b384)\n''Оставьте пустым для последнего запуска')
    parser.add_argument('--download_folder', default='spacex_images', help='Папка для сохранения (по умолчанию: spacex_images)')
    parser.add_argument('--filename_number', default='spacex', help='Имя файлов (по умолчанию: spacex)')
    args = parser.parse_args()
    
    fetch_spacex_photos(args.id, args.download_folder, args.filename_number)

if __name__ == '__main__':
    main()