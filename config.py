import discord
import logging

#! Config
TOCKEN = 'REDACTED_DISCORD_TOKEN'
PREFIX = ['s5.', 'S5.']
activity = 'DCS'
description = 'DCS Official BOT'
status = discord.Status.do_not_disturb
color = 0xfe2a9b
colours = {"green":0x00ff11,"yellow":0xfaff00,"red":0xff0000,"blue":0x00b3ff,"purple":0x8c00ff}
log = logging.INFO
warn_onready = False
SQL = {"user": "Selenne","password": "REDACTED_DB_PASSWORD","host": "127.0.0.1","database": "selenne","raise_on_warnings": True}
staff_file = 'db/system/staff.json'