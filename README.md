# Публикация комиксов в группе VK

Скрипт скачивает случайный комикс на сайте https://xkcd.com/ и
публикует его в группе VK.

## Как установить

1. Клонировать репозиторий:

    ```shell
    git clone https://github.com/semellot/xkcd.git
    ```

2. Установить зависимости:

    ```shell
    pip install -r requirements.txt
    ```

3. Создать файл `.env` с данными:

    ```dotenv
    VK_CLIENT_ID=client_id
    VK_GROUP_ID=group_id
    VK_ACCESS_TOKEN=vk_token
    ```        

## Примеры запуска скрипта

```shell
% python main.py
Комикс опубликован в группе
```