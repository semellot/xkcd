from dotenv import load_dotenv
import os
import shutil

from functions import (
    download_random_comic,
    get_vk_server_address,
    upload_img_on_vk_server,
    save_image_in_group,
    public_image_in_group
)

if __name__ == '__main__':
    load_dotenv()
    client_id = os.environ['CLIENT_ID']
    group_id = os.environ['GROUP_ID']
    token = os.environ['ACCESS_TOKEN']
    
    try:
        # сохранить последний комикс
        filename, comic_alt = download_random_comic()
        
        # получить адрес сервера vk
        server_address = get_vk_server_address(token, group_id)
        
        # загрузить фото на сервер vk
        image_data = upload_img_on_vk_server(server_address, filename)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    finally:
        shutil.rmtree('files')
    
    image_photo = image_data['photo']
    image_server = image_data['server']
    image_hash = image_data['hash']
    
    # сохранить комикс в группе
    saved_image_data = save_image_in_group(token, group_id, image_photo, image_server, image_hash)
    
    image_id = saved_image_data['response'][0]['id']
    owner_id = saved_image_data['response'][0]['owner_id']
    
    # Сделать публикацию
    response = public_image_in_group(token, group_id, image_id, owner_id, comic_alt)
    
    if 'error' not in response:
        print('Комикс опубликован в группе')
    