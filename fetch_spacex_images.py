import requests
from download_utils import download_images


def fetch_spacex_last_launch(download_folder='images', filename_number='spacex'):
    """Получает фото запуска SpaceX"""
    api_url = 'https://api.spacexdata.com/v5/launches/5eb87d42ffd86e000604b384'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        launch_photos = response.json()
        photo_urls = launch_photos.get('links', {}).get('flickr', {}).get('original', [])
        if not photo_urls:
                print('Фотографии не найдены в запуске')
                return
        download_images(
                image_urls=photo_urls,
                folder=download_folder,
                filename_number=filename_number
            )
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе к API SpaceX: {e}')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')

if __name__ == '__main__':
    
    fetch_spacex_last_launch(
        download_folder='spacex_images',
        filename_number='spacex_launch'
    )