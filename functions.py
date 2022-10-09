import os
import sys
from pathlib import Path
import requests
from urllib.parse import urlparse
import random


COUNT_COMICS = 2681


def download_random_comic():
    comic_id = random.randint(1,COUNT_COMICS)
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    decoded_response = response.json()
    
    comic_url = decoded_response['img']
    comic_alt = decoded_response['alt']
    extensions = ('.jpg', '.png', '.gif')
    if comic_url.endswith(extensions):
        filename = os.path.basename(comic_url)
        img_data = requests.get(comic_url).content
        Path('files').mkdir(parents=True, exist_ok=True)
        with open(os.path.join('files', filename), 'wb') as file:
            file.write(img_data)
        return filename, comic_alt
        

def get_vk_server_address(token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    
    params = {
        'access_token': token,
        'group_id': group_id,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    server_data = response.json()
    
    return server_data['response']['upload_url']


def upload_img_on_vk_server(server_address, filename):
    
    with open(os.path.join('files', filename), 'rb') as file:
        url = server_address
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    
    return response.json()


def save_image_in_group(token, group_id, image_photo, image_server, image_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    
    params = {
        'access_token': token,
        'group_id': group_id,
        'v': '5.131',
        'photo': image_photo,
        'server': image_server,
        'hash': image_hash,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()


def public_image_in_group(token, group_id, image_id, owner_id, message):
    url = 'https://api.vk.com/method/wall.post'
    
    params = {
        'access_token': token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'v': '5.131',
        'message': message,
        'attachments': f'photo{owner_id}_{image_id}'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()
    