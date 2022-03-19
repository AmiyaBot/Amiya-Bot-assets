import os
import yaml

from attrdict import AttrDict

from .tools import process_bar, get_filename
from .unity import unpack_files, unpack_folders
from .image import merge_alpha_images


def unpack_all(abs_path: str = ''):
    with open(f'src/unpack/config.yaml', mode='r') as file:
        config = AttrDict(yaml.safe_load(file))

    for conf in config.unpackFiles:
        for index, item in enumerate(conf['files']):
            conf['files'][index] = abs_path + item
        unpack_files(conf['files'], conf['temp'] or conf['dest'], conf['rule'])

    for conf in config.unpackFolders:
        for index, item in enumerate(conf['folders']):
            conf['folders'][index] = abs_path + item
        unpack_folders(conf['folders'], conf['temp'] or conf['dest'], conf['rule'])


def merge_skins_images():
    conf = [
        ('temp/charpack', 'resource/images/game/skins'),
        ('temp/skinpack', 'resource/images/game/skins')
    ]
    for item in conf:
        for root, dirs, files in os.walk(item[0]):
            for img in process_bar(files, f'merging {item[0]}'):

                filename = get_filename(img, suffix=False)

                color_file = f'{root}/{filename}.png'
                alpha_file = f'{root}/{filename}[alpha].png'
                if os.path.exists(color_file) and os.path.exists(alpha_file):
                    merge_alpha_images(color_file, alpha_file, item[1])


def start(path):
    print('beginning unpack asset...\n')
    unpack_all(path)
    merge_skins_images()
