import os
from dotenv import load_dotenv
import requests
from download_utils import download_images


def fetch_nasa_photos(api_key, count=30):
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

        download_images(
            image_urls=image_urls,
            folder='nasa_images',
            filename_number='nasa_apod'
        )
    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса к NASA API: {e}')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

if __name__ == '__main__':
    load_dotenv()
    NASA_API = os.getenv('NASA_API')
    fetch_nasa_photos(NASA_API)