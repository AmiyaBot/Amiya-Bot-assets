import os
import re
import UnityPy

from .tools import process_bar


def unpack_files(source_files: list, destination_folder: str, rule: str):
    for file_path in source_files:
        env = UnityPy.load(file_path)

        for obj in process_bar(env.objects, f'unpacking file [{file_path}]'):
            save_img(obj, destination_folder, rule)


def unpack_folders(source_folders: str, destination_folder: str, rule: str):
    for folder in source_folders:
        for root, dirs, files in os.walk(folder):
            for file_name in process_bar(files, f'unpacking folder [{root}]'):
                file_path = os.path.join(root, file_name)
                env = UnityPy.load(file_path)

                for obj in env.objects:
                    save_img(obj, destination_folder, rule)


def save_img(obj, folder, rule):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if str(obj.type) in ['Texture2D', 'Sprite', 'ClassIDType.Texture2D', 'ClassIDType.Sprite']:
        data = obj.read()
        if rule and not re.search(re.compile(rule), data.name):
            return False

        dest = os.path.join(folder, data.name)
        dest, ext = os.path.splitext(dest)
        dest = dest + '.png'

        if not os.path.exists(dest):
            img = data.image
            img.save(dest)
