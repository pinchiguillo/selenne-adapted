import os
try:
    import discord
except ImportError: os.system('pip install -U git+https://github.com/Rapptz/discord.py')
try:
    import PyNaCl
except ImportError: os.system('pip install PyNaCl')
try:
    import youtube_dl
except ImportError: os.system('pip install youtube_dl')