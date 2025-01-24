import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


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
    return not 'error' in response.json()


def shorten_link(token, link):
    payload = {
        'url' : link,
        'access_token' : token,
        'v':'5.199',
    }
    url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(token,short_link):
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
    return response.json()['response']['stats'][0]['views']


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Сократите URL-адрес и получите статистику кликов")
    parser.add_argument(
        "link", help="Покажет сокращенную форму ссылки")
    args = parser.parse_args()
    link = args.link
    token = os.environ['VK_TOKEN']


    try:


        if is_short_link(link,token):
                short_link = link
                print('Просмотров',count_clicks(token, short_link))
        else:
                short_link = shorten_link(token, link)
                print(f'Сокращённая ссылка: {short_link}',
                      '\nПросмотров:',count_clicks(token, short_link))


    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {e}")


    except KeyError:
        print("Ошибка KeyError")


if __name__ == "__main__":
    main()
