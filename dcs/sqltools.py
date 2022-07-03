#
#TODO: SQL Tools
#TODO: By DCS

#? Imports
import mysql.connector
import json

#? Main Class
class DataBase():

    version = '1.2'

    def __init__(self, config:dict, file:str = None):
        if not config and not file: raise ValueError('config dict or config file required')
        elif config: self.config = config
        elif file: 
            with open(file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)

    #? Conexion Functions
    def connect(self, otp = False):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
            self.cursor_alt = self.conexion.cursor(buffered=True)
        except Exception as error:
            print(error)
        else:
            if otp: print('Connected to database')    
    def disconnect(self, otp = False):
        self.conexion.close()
        if otp: print('Disconnected from database')

    #? Data Functions
    #* Upload Data
    def commit(self, sql):
        self.cursor.execute(sql)
        self.conexion.commit()
    #* Download Data
    def get(self, sql):
        self.cursor_alt.execute(sql)
        return self.cursor_alt.fetchall()

    #? Database update
    @property
    def database(self): return self._database
    @database.setter
    def database(self, value):
        self.config['database'] = value

    #? PRIVATE FUNCTIONS
