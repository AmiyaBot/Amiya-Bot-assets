import os
import json
import time
import traceback
import urllib.parse

from download import download_sync
from requests_html import HTMLSession, HTML

session = HTMLSession()
cache = {}


def get_char_wiki(name):
    print(f'requesting wiki for {name}...')

    html: HTML = session.get(f'http://prts.wiki/w/{name}').html

    stage_map = {}

    for stage in html.find('#charimg > div'):
        stage_id = stage.attrs['id'].replace('img-', '')
        img = stage.find('img')

        if not img:
            continue

        url = urllib.parse.unquote(img[0].attrs['src'])

        if not url:
            continue

        stage_map[stage_id] = url

    return stage_map


def start():
    with open('skin_map.json', mode='r') as file:
        skin_map: dict = json.load(file)

    for char_id, info in skin_map.items():
        skin_folder = f'skins/{char_id}'

        if not os.path.exists(skin_folder):
            os.makedirs(skin_folder)

        if 'char_1001' in char_id:
            continue

        for item in info['skins']:
            skin_path = f'{skin_folder}/{char_id}_%s.png' % item['skin_key']

            if not os.path.exists(skin_path):
                if char_id not in cache:
                    cache[char_id] = get_char_wiki(info['name'])

                stage_map = cache[char_id]
                url = stage_map[item['skin_key']]

                res = download_sync(f'http:{url}')
                if res:
                    with open(skin_path, mode='wb') as f:
                        f.write(res)


if __name__ == '__main__':
    while True:
        try:
            start()
            break
        except Exception:
            print(traceback.format_exc())
            time.sleep(5)
            continue
