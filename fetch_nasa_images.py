import argparse
import os
from dotenv import load_dotenv
import requests
from download_utils import download_images


def fetch_nasa_photos(api_key, folder, filename_number, count=30):
    """Получает фото NASA"""
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': count,
        'thumbs': True
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        image_urls = [item['url'] for item in data if item['media_type'] == 'image']
        
        if image_urls:
            print(f'Найдено {len(image_urls)} фото. Скачиваю...')
            download_images(
                image_urls=image_urls,
                folder=folder,
                filename_number=filename_number
            )
            print('Готово!')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса к NASA API: {e}')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description='Скачивание фото NASA')
    parser.add_argument('--key', default=os.getenv('NASA_API'), help='NASA API ключ')
    parser.add_argument('--folder', default='nasa_images', metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_number', default='nasa', metavar='', help='Имя файлов (по умолчанию: nasa)')
    parser.add_argument('--count', type=int, default=30, metavar='', help='Количество фото')
    args = parser.parse_args()

    if not args.key:
        raise ValueError('API ключ должен быть указан через --key или в .env файле')
    
    fetch_nasa_photos(
        api_key=args.key,
        folder=args.folder,
        filename_number=args.filename_number,
        count=args.count
    )

if __name__ == '__main__':
    main()