import sqlite3

file = 'LDB/CustomProfile.sqlite'

db = sqlite3.connect(file)
#! Functions

def create_db():
    cursor = db.cursor()

    # Create Table user
    SQL = """
CREATE TABLE guilds (
    id INTEGER PRIMARY KEY,
    name TEXT,
    owner TEXT NOT NULL,
    lvl INTEGER DEFAULT 1,
    gold INTEGER DEFAULT 0,
    FOREIGN KEY (owner) REFERENCES user(id)
);

"""
    cursor.execute(SQL)
    SQL = """
CREATE TABLE user (
    id TEXT PRIMARY KEY,
    class TEXT DEFAULT NULL,
    lvl INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0,
    guild INTEGER,
    gold INTEGER DEFAULT 0,
    FOREIGN KEY (guild) REFERENCES guilds(id)
);
"""
    cursor.execute(SQL)
    SQL = """
CREATE TABLE inventory (
    player_id TEXT,
    item_name TEXT,
    quantity INTEGER,
    PRIMARY KEY (player_id, item_name),
    FOREIGN KEY (player_id) REFERENCES user(id)
);

"""
    cursor.execute(SQL)
    db.commit()

def create_user(id:str): 
    cursor = db.cursor()
    SQL = "INSERT INTO user (id) VALUES ('{}');".format(id)
    cursor.execute(SQL)
    db.commit()

def create_guild(name:str, owner:str):
    cursor = db.cursor()
    SQL = "INSERT INTO guilds (name, owner) VALUES ('{}', '{}');".format(name, owner)
    cursor.execute(SQL)
    db.commit()

def change_class(id:str, _class:str): 
    cursor = db.cursor()
    SQL = "UPDATE user SET class = '{}' WHERE id = '{}';".format(id, _class)
    cursor.execute(SQL)
    db.commit()

def level_up(id:str):
    cursor = db.cursor()
    SQL = "UPDATE user SET lvl = lvl + 1 WHERE id = '{}';".format(id)
    cursor.execute(SQL)
    db.commit()

def xp(id:str, xp:int): 
    cursor = db.cursor()
    SQL = "SELECT xp from user WHERE id = '{}'".format(id)
    cursor.execute(SQL)
    oldxp = cursor.fetchone()[0]

    SQL = "SELECT lvl from user WHERE id = '{}'".format(id)
    cursor.execute(SQL)
    lvl = cursor.fetchone()[0]
    
    while True:
        oxp = 100 + (lvl-1)**2.5

        txp = oldxp + xp
        if txp >= oxp:
            txp -= oxp
            level_up(id)
            lvl += 1
            oldxp = txp
            print(txp)
        else: break

    SQL = "UPDATE user SET xp = {} WHERE id = '{}';".format(txp, id)
    cursor.execute(SQL)
    db.commit()

def join_guild(id:str, guild:int): 
    cursor = db.cursor()
    SQL = "UPDATE user SET guild = '{}' WHERE id = '{}';".format(guild, id)
    cursor.execute(SQL)
    db.commit()

def leave_guild(id:str): 
    cursor = db.cursor()
    SQL = "UPDATE user SET guild = NULL WHERE id = '{}';".format(id)
    cursor.execute(SQL)
    db.commit()

def save_item(id:str, item:str, quantity:int = 1):
    cursor = db.cursor()
    try:
        SQL = """INSERT INTO inventory (player_id, item_name, quantity) VALUES ('{}', '{}', {});""".format(id, item, quantity)
        
        cursor.execute(SQL)
    except Exception as e:
        print('ERR:{0}', e)
        SQL = """UPDATE inventory SET quantity = quantity + 1 WHERE player_id = '0' AND item_name = 'sword';""".format(id, item, quantity)
        cursor.execute(SQL)
    db.commit()

def delete_item(id, item):
    cursor = db.cursor()
    SQL = """UPDATE inventory
SET quantity = quantity - 1
WHERE player_id = '{}' AND item_name = '{}';

DELETE FROM inventory
WHERE player_id = '{}' AND item_name = '{}' AND quantity = 0;
""".format(id, item, id, item)
    cursor.execute(SQL)
    db.commit()

#create_user(0)
#create_guild('WA', 0)
#join_guild(0, 0)

print('done!')
