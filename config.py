from telnetlib import SE
import discord
import logging
import json

#! Config
TOCKEN = 'TOCKEN'
TOCKEN_FILE = 'TOCKEN.secure'     #! files ended in .secure will be ignored by github if .gitignore is not modified

PREFIX = ['s5.', 'S5.']
activity = 'DCS'
description = 'DCS Official BOT'
status = discord.Status.invisible

color = 0xfe2a9b
colours = {"green":0x00ff11,"yellow":0xfaff00,"red":0xff0000,"blue":0x00b3ff,"purple":0x8c00ff}

log = logging.INFO
warn_onready = False

SQL = {"user": "","password": "","host": "","database": "","raise_on_warnings": True}
SQL_FILE = 'SQL.secure'

staff_file = 'db/system/staff.json'

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
