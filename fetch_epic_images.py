import os
from dotenv import load_dotenv
import requests
from download_utils import download_images


def fetch_epic_photos(api_key):
    """Получает фото EPIC"""
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
        

        download_images(
            image_urls=image_urls[:10],
            folder='epic_images',
            filename_number='epic_photo'
        )
    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса к NASA API: {e}')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

if __name__ == '__main__':
    load_dotenv()
    NASA_API = os.getenv('NASA_API')
    fetch_epic_photos(NASA_API)