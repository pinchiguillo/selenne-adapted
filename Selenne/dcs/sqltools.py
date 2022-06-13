from xmlrpc import server
import mysql.connector

import json

class DataBase():
    def __init__(self, config:dict = None, file:str = None, shape:list = None):
        if not config and not file: raise ValueError('config dict or config file required')
        elif config: self.config = config
        elif file: 
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        self.shape = shape

        self.table = None

        self.done = True

    def connect(self, otp = False):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
        except Exception as error:
            print(error)
        else:
            if otp: print('Connected to database')
        
    def disconnect(self, otp = False):
        self.conexion.close()
        if otp: print('Disconnected from database')

    def addecuate_sql(self, data:dict):
        s1 = ''
        s2 = ''
        for key in data.keys():
            s1 += f'`{key}`, '
            val = data[key]
            s2 += f'\'{val}\', '
        
        s1 = s1.removesuffix(', ')
        s2 = s2.removesuffix(', ')

        return s1, s2
    
    def commit(self, sql):
        try:
            self.cursor.execute(sql)
        except mysql.connector.errors.IntegrityError:
            print('ERROR: Entry Duplicated')
            self.done = False

        self.conexion.commit()

    #! Automatic actions

    def create_table():pass
    def delete_table():pass

    def insert(self, data:list, otp = False):
        s1, s2 = self.addecuate_sql(data)

        sql = f'INSERT INTO `{self.table}` ({s1}) VALUES ({s2});'

        self.done = True
        self.commit(sql)
        if otp and self.done:
            print('Insertion Done')

    def update(self, data:list, check:dict, otp = False):
        s1 = ''
        for key in data.keys():
            s1 += f'`{key}` = \'{data[key]}\', '.replace("'", r'\"')
        s1 = s1.removesuffix(', ')

        key = list(check.keys())[0]
        check = f'`{key}` = {check[key]}'

        sql = f"UPDATE `servers` SET {s1} WHERE `servers`.{check};".replace(r'= \"', '= "').replace(r'\",', '",').replace(r'\" WHERE','" WHERE')
        #sql = "UPDATE `servers` SET `channels` = '{\"news\":654654}', `settings` = '{\"news\":true}' WHERE `servers`.`id` = 480;"
        #sql = UPDATE `servers` SET `channels` = \"{\"news\": 654654}\", `settings` = \"{\"news_cc\": 67654}\" WHERE `servers`.`id` = 480;

        self.done = True
        self.commit(sql)
        if otp and self.done:
            print('Update Done')

    def select(self, data:list, get:str = '*', otp = False):
        key = list(data.keys())[0]
        sql = f'SELECT {get} FROM `{self.table}` WHERE `{key}` = {data[key]}'

        
        self.cursor.execute(sql)

        dt = self.cursor.fetchone()
        try: return {'id': dt[0],'channels': str(dt[1], encoding='utf-8'),'settings': str(dt[2], encoding='utf-8')}
        except: pass
