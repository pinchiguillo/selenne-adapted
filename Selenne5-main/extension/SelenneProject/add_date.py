import json
import os

path = os.path.join(os.getcwd(), 'data/thedatebase.json')

with open(path, 'r', encoding='utf8') as fd:
    data = json.load(fd)

data['dates'].append(
    {
        'name': input('Name: '),
        'date': input('Date (dd/mm/yyyy): '),
        'people': input('People: ').split(', '),
        'tags': input('Tags: ').split(', '),
        'site': input('Site: ')
    }
)

with open(path, 'w', encoding='utf8') as fd:
    json.dump(data, fd, indent=4, ensure_ascii=False)
