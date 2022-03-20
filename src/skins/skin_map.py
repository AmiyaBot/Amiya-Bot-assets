import json

from core.resource.arknightsGameData import ArknightsGameData

if __name__ == '__main__':
    operators = ArknightsGameData().operators

    skin_map = {
        n.id: {
            'name': char_name,
            'skins': n.skins()
        }
        for char_name, n in operators.items()
    }

    with open('skin_map.json', mode='w+') as file:
        file.write(json.dumps(skin_map, ensure_ascii=False))
