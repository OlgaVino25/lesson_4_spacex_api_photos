import argparse
import os
from dotenv import load_dotenv
import requests
from download_utils import download_images
from datetime import datetime


def fetch_epic_photos(api_key, folder, filename_prefix):
    """
    Скачивает последние фотографии Земли NASA API.

    Этот скрипт запрашивает данные из NASA API EPIC и скачивает до 10 последних фотографий Земли в формате PNG.

    Args:
        api_key (str): Ключ API NASA
        folder (str): Папка для сохранения изображений
        filename_prefix (str): Префикс имени файла для сохраненных изображений
        MAX_DOWNLOADS (int): константа для ограничения количества загрузок

    Returns:
        None

    Example:
        python fetch_epic_images.py --key your_nasa_api_key --folder epic_images --filename_prefix epic_photo
    """
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        earth_images_metadata = response.json()

        image_urls = []
        for image_metadata in earth_images_metadata:
            capture_date = datetime.fromisoformat(image_metadata['date'])
            formatted_date = capture_date.strftime('%Y/%m/%d')
            image_name = image_metadata['image']
            url = f"https://epic.gsfc.nasa.gov/archive/natural/{formatted_date}/png/{image_name}.png"
            image_urls.append(url)
        
        MAX_DOWNLOADS = 10
        print(f'Скачиваю...')
        download_images(
            image_urls=image_urls[:MAX_DOWNLOADS],
            folder=folder,
            filename_prefix=filename_prefix
        )
        print('Готово!')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Ошибка авторизации: недействительный NASA API ключ")
            print("Проверьте правильность ключа: https://api.nasa.gov/")
        elif e.response.status_code == 404:
            print("Данные не найдены. Проверьте доступность изображений на сайте EPIC")
        else:
            print(f"Ошибка NASA API ({e.response.status_code}): {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения. Проверьте интернет-соединение")
    except requests.exceptions.Timeout:
        print("Превышено время ожидания. Повторите попытку позже")
    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки данных: {str(e)}")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        raise


def parse_arguments():
    """Парсит аргументы командной строки и загружает переменные окружения.
    
    Returns:
        Namespace: Объект с аргументами командной строки
        
    Raises:
        ValueError: Если не указан API ключ
    """
    load_dotenv()

    parser = argparse.ArgumentParser(description='Скачивание фото EPIC')
    parser.add_argument('--key', default=os.getenv('NASA_API'), help='NASA API ключ')
    parser.add_argument('--folder', default='epic_images', metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_prefix', default='epic_photo', metavar='', help='Имя файлов (по умолчанию: epic_photo)')
    args = parser.parse_args()
    if not args.key:
        raise ValueError('API ключ должен быть указан через --key или в .env файле')
    return args

def main():
    args = parse_arguments()
    
    fetch_epic_photos(
        api_key=args.key,
        folder=args.folder,
        filename_prefix=args.filename_prefix
    )

if __name__ == '__main__':
    main()