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
    client_id = os.environ['VK_CLIENT_ID']
    group_id = os.environ['VK_GROUP_ID']
    token = os.environ['VK_ACCESS_TOKEN']
    
    try:
        filename, comic_alt = download_random_comic()
        
        server_address = get_vk_server_address(token, group_id)
        
        image = upload_img_on_vk_server(server_address, filename)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    finally:
        shutil.rmtree('files')
    
    image_photo = image['photo']
    image_server = image['server']
    image_hash = image['hash']
    
    saved_image = save_image_in_group(token, group_id, image_photo, image_server, image_hash)
    
    image_id = saved_image['response'][0]['id']
    owner_id = saved_image['response'][0]['owner_id']
    
    response = public_image_in_group(token, group_id, image_id, owner_id, comic_alt)
    
    if 'error' not in response:
        print('Комикс опубликован в группе')
    