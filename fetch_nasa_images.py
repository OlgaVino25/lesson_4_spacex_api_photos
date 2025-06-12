import argparse
import os
from dotenv import load_dotenv
import requests
from download_utils import download_images


def fetch_nasa_photos(api_key, folder, filename_prefix, count=30):
    """
    Скачивает изображения NASA API.

    Этот скрипт запрашивает данные из NASA API EPIC и скачивает до 10 последних фотографий Земли в формате PNG.

    Args:
        api_key (str): Ключ API NASA
        folder (str): Папка для сохранения изображений
        filename_prefix (str): Префикс имени файла для сохраненных изображений
        count (int): Количество изображений для загрузки (по умолчанию 30)

    Returns:
        None

    Example:
        python fetch_nasa_images.py --key YOUR_API_KEY --folder nasa_images --filename_prefix nasa --count 30
    """
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

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description='Скачивание фото NASA')
    parser.add_argument('--key', default=os.getenv('NASA_API'), help='NASA API ключ')
    parser.add_argument('--folder', default='nasa_images', metavar='', help='Папка для сохранения')
    parser.add_argument('--filename_prefix', default='nasa', metavar='', help='Имя файлов (по умолчанию: nasa)')
    parser.add_argument('--count', type=int, default=30, metavar='', help='Количество фото')
    args = parser.parse_args()

    if not args.key:
        raise ValueError('API ключ должен быть указан через --key или в .env файле')
    
    fetch_nasa_photos(
        api_key=args.key,
        folder=args.folder,
        filename_prefix=args.filename_prefix,
        count=args.count
    )

if __name__ == '__main__':
    main()