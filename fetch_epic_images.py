import argparse
import os
from dotenv import load_dotenv
import requests
from download_utils import download_images


def fetch_epic_photos(api_key, folder, filename_number):
    """
    Скачивает последние фотографии Земли NASA API.

    Этот скрипт запрашивает данные из NASA API EPIC и скачивает до 10 последних фотографий Земли в формате PNG.

    Args:
        api_key (str): Ключ API NASA
        folder (str): Папка для сохранения изображений
        filename_number (str): Префикс имени файла для сохраненных изображений

    Raises:
        ValueError: Если API ключ не указан

    Returns:
        None

    Example:
        python epic_downloader.py --key your_nasa_api_key --folder epic_images --filename_number epic_photo
    """
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        epic_data = response.json()

        image_urls = []
        for item in epic_data:
            date_part = item['date'].split()[0].replace('-', '/')
            image_name = item['image']
            url = f"https://epic.gsfc.nasa.gov/archive/natural/{date_part}/png/{image_name}.png"
            image_urls.append(url)
        
        print(f'Скачиваю...')
        download_images(
            image_urls=image_urls[:10],
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

    parser = argparse.ArgumentParser(description='Скачивание фото EPIC')
    parser.add_argument('--key', default=os.getenv('NASA_API'), help='NASA API ключ')
    parser.add_argument('--folder', default='epic_images', metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_number', default='epic_photo', metavar='', help='Имя файлов (по умолчанию: epic_photo)')
    args = parser.parse_args()

    if not args.key:
        raise ValueError('API ключ должен быть указан через --key или в .env файле')

    fetch_epic_photos(
        api_key=args.key,
        folder=args.folder,
        filename_number=args.filename_number
    )

if __name__ == '__main__':
    main()