import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_short_link(link):
    parsed_url = urlparse(link)
    if parsed_url.netloc == "vk.cc" and len(parsed_url.path) > 1:
        return True
    return False


def get_vk_link(token, link):
    payload = {
        'url' : link,
        'access_token' : token,
        'v':'5.199',
    }
    url='https://api.vk.com/method/utils.getShortLink'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_link_stats(token,short_link):
    short_vk_link = (urlparse(short_link)).path[1:]
    payload = {
        "access_token": token,
        "v": '5.199',
        "key": short_vk_link,
        "interval": "forever",
        "intervals_count": 1
    }
    url = 'https://api.vk.com/method/utils.getLinkStats'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    token = os.environ['TOKEN']
    link = input('Введите адрес: ')


    try:


        if is_short_link(link):
            short_link = link
            print('Просмотров',get_link_stats(token, short_link)['response']['stats'][0]['views'])
        else:
            short_link = get_vk_link(token, link)['response']['short_url']
            print('Сокращённая ссылка:', get_vk_link(token, link)['response']['short_url'])
            print('Просмотров',get_link_stats(token, short_link)['response']['stats'][0]['views'])


    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {e}")


    except KeyError:
        print("Ошибка KeyError")


if __name__ == "__main__":
    main()