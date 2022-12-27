import mysql.connector
import yaml
with open('config.yaml', 'r', encoding='utf8') as f:
    config = yaml.safe_load(f)

database = mysql.connector.connect(
    host = config['databases']['host'],
    username = config['databases']['username'],
    password = config['databases']['password'],
    database = config['databases']['database'],
)

with open('picklib_input.txt', 'r', encoding='utf8') as f:
    data = f.readlines()

__references__ = {
            'instagram': 'https://www.instagram.com/',
            'pixiv': 'https://www.pixiv.net/en/artworks/',
            'twitter': 'https://twitter.com/',
            'pinterest': 'https://pin.it',
        }

errors = []

cursor = database.cursor(buffered=True)
for entry in data:
    link = entry.removesuffix('\n')

    platform = None
    for __platform__ in __references__:
        if link.startswith(__references__[__platform__]): platform = __platform__

    try:
        SQL = "INSERT INTO `picklib` (`platform`, `link`, `downloaded`, `fetch_date`) VALUES ('{}', '{}', '0', CURRENT_TIMESTAMP);".format(platform, link)
        cursor.execute(SQL)
    except:
        errors.append(link)

database.commit()