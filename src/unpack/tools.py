import sys

from typing import Union


def process_bar(data: Union[dict, list], title: str):
    data = data.keys() if type(data) is dict else data

    if not len(data):
        return None

    def print_bar(i):
        curr = int(i / len(data) * 100)
        block = int(curr / 4)
        bar = '=' * block + ' ' * (25 - block)

        print('\r', end='')
        print(
            f'> [{bar}] {curr}% {i}/{len(data)} for {title}',
            end=''
        )

        sys.stdout.flush()

    print_bar(0)
    for index, item in enumerate(data):
        yield item
        print_bar(index + 1)

    print()


def get_filename(path: str, suffix: bool = True):
    name = path.replace('\\', '/').split('/')[-1]
    if not suffix:
        name = name.split('.')[0]
    return name
