import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_short_link(link,token):
    payload = {
        "access_token": token,
        "v": '5.199',
        "key": (urlparse(link)).path[1:],
        "interval": "forever",
        "intervals_count": 1
    }
    url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if 'error' in response.json():
        return False
    return True


def get_link_vk_format(token, link):
    payload = {
        'url' : link,
        'access_token' : token,
        'v':'5.199',
    }
    url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_quantity_clicks(token,short_link):
    payload = {
        "access_token": token,
        "v": '5.199',
        "key": (urlparse(short_link)).path[1:],
        "interval": "forever",
        "intervals_count": 1
    }
    url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']
    link = input('Введите адрес: ')


    try:


        if is_short_link(link,token):
                short_link = link
                print('Просмотров',get_quantity_clicks(token, short_link)['response']['stats'][0]['views'])
        else:
                short_link = get_link_vk_format(token, link)['response']['short_url']
                print(f'Сокращённая ссылка: {short_link}',
                      '\nПросмотров:',get_quantity_clicks(token, short_link)['response']['stats'][0]['views'])


    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {e}")


    except KeyError:
        print("Ошибка KeyError")


if __name__ == "__main__":
    main()
