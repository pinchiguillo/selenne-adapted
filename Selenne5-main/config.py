from telnetlib import SE
import discord
import logging
import json

#! READ ME
# This file is used to configure the essential thinsg of Selenne Core, #! DONT MODIFY THE RED COMMENTED LINES (#!)
# In order to protect important data to be updated to Github files ended in .secure will not be updated #! ONLY IF YOU DONT MODIFY THE .gitignore file

#? Selenne Configuration
TOCKEN = 'TOCKEN'
TOCKEN_FILE = 'TOCKEN.secure' #* Optional

PREFIX = ['se.', 'Se.'] #* We advise to add the prefix with capitalization beacuse on mobile devices the first letter is usually capitalized
prefix_database = None #! NOT IN Selenne 5.3
activity = 'DCS'
description = 'Selenne tester bot, only private'
status = discord.Status.online #* Only use discord.Status variables

color = 0xfe2a9b
colours = {"green":0x00ff11,"yellow":0xfaff00,"red":0xff0000,"blue":0x00b3ff,"purple":0x8c00ff}

log = logging.INFO
warn_on_ready = False
intents = discord.Intents.all() #TODO: NEW IN Selenne 5.3

discord_log = True #TODO: NEW IN Selenne 5.3
discord_log_dir = {'guild': 1005188619310477403, 'channel':1005606314413666404} #TODO: NEW IN Selenne 5.3

SQL = {"user": "","password": "","host": "","database": "","raise_on_warnings": True} #* Only SQL SUPPORT IN Selenne 5.3
SQL_FILE = 'SQL.secure'

staff_file = 'db/system/staff.json' #* This file is created on Selenne.setup() if you modify this path you will have to create it manually


#! Secure vars
if TOCKEN_FILE:
    try:
        with open(TOCKEN_FILE, 'r', encoding='utf8') as f:
            TOCKEN = f.read()
    except FileNotFoundError: print(f'Could not found "{TOCKEN_FILE}", using config tocken...')

if SQL_FILE:
    try:
        with open(SQL_FILE, 'r', encoding='utf8') as f:
            SQL = json.load(f)
    except FileNotFoundError: print(f'Could not found "{SQL_FILE}", using config SQL...')
    except json.decoder.JSONDecodeError: print(f'Could not read "{SQL_FILE}", using config SQL...')
