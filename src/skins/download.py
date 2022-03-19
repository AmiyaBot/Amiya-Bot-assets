import sys
import time
import requests

from io import BytesIO
from typing import Iterator

default_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
                  'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
}


def download_progress(title: str, max_size: int, chunk_size: int, iter_content: Iterator):
    def print_bar():
        curr = int(curr_size / max_size * 100)

        used = time.time() - start_time
        c_size = round(curr_size / 1024 / 1024, 2)
        size = round(max_size / 1024 / 1024, 2)
        average = (c_size / used) if used and curr_size else 0

        average_text = f'{int(average)}mb/s'
        if average < 1:
            average_text = f'{int(average * 1024)}kb/s'

        block = int(curr / 4)
        bar = '=' * block + ' ' * (25 - block)

        msg = f'{title} [{bar}] {c_size} / {size}mb ({curr}%) {average_text}'

        print('\r', end='')
        print(msg, end='')

        sys.stdout.flush()

    curr_size = 0
    start_time = time.time()

    print_bar()
    for chunk in iter_content:
        yield chunk
        curr_size += chunk_size
        print_bar()

    print()


def download_sync(url: str, headers=None, stringify=False, progress=True):
    stream = requests.get(url, headers=headers or default_headers, stream=True)
    file_size = int(stream.headers['content-length'])

    container = BytesIO()

    if stream.status_code == 200:
        iter_content = stream.iter_content(chunk_size=1024)
        if progress:
            iter_content = download_progress(url.split('/')[-1],
                                             max_size=file_size,
                                             chunk_size=1024,
                                             iter_content=iter_content)
        for chunk in iter_content:
            if chunk:
                container.write(chunk)

        content = container.getvalue()

        if stringify:
            return str(content, encoding='utf-8')
        else:
            return content
