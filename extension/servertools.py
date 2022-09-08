import discord
from discord.ext import commands
import json

import datetime

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': 's.help Server Tools',
        'specific_display': {
            's.announce [text]': 'Sends an announcement to the news channel',
            's.serverinfo': 'Displays the general server information'
            }
        }

    add_help()

    #ADD CMD
    bot.add_command(announce)
    bot.add_command(forbid_exclamations)
    bot.add_command(serverinfo)
    bot.add_command(whois)

    #END
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()

bot_version = 'Selenne 4.8.5'
version = 'ServerTools: 1.0.4'
ename = 'Server Tools'

system_path = 'db/system/servers.json'
db_path = system_path

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5, ensure_ascii= False)

def load_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        global db
        db =  json.load(f)
def save_db():
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=5, ensure_ascii = False)

@commands.command()
async def announce(ctx, *, args = None):
    load_db()
    try: server_conifg = db[str(ctx.guild.id)]
    except KeyError: await ctx.send('You havent configured Selenne, please use |s.conifg| in order to configure everything.')

    channel = await ctx.guild.fetch_channel(server_conifg['channels']['news'])
    
    #Check View
    send_btn = discord.ui.Button(label = 'Send', style=discord.ButtonStyle.green)
    del_btn = discord.ui.Button(label = 'Cancel', style=discord.ButtonStyle.danger)

    async def send_callback(interaction):
        match server_conifg['settings']['announce_config']['format']['type']:
            case 'text': await channel.send(server_conifg['settings']['announce_config']['format']['form'].replace('%msg%', args))
            case 'default_embed': await channel.send(embed=bot.embed)
            case 'custom_embed': await channel.send(server_conifg['settings']['announce_config']['format']['form'].replace('%msg%', args), embed=bot.embed)

        await interaction.response.edit_message(content = f'Announcement sent to {channel.mention}', view=None)

    async def del_callback(interaction):
        await bot.msg.delete()

    send_btn.callback = send_callback
    del_btn.callback = del_callback

    view = discord.ui.View(timeout = 600)
    view.add_item(send_btn)
    view.add_item(del_btn)
    
    #Check if exists and run if yes
    try:
        match server_conifg['settings']['announce_config']['format']['type']:
            case 'text':
                bot.msg = await ctx.send(server_conifg['settings']['announce_config']['format']['form'].replace('%msg%', args), view=view)
            case 'default_embed':
                bot.embed=discord.Embed(title = f'News - {ctx.guild.name}', description = args, color = bot.color)
                bot.embed.set_thumbnail(url=ctx.guild.icon)
                bot.msg = await ctx.send(embed=bot.embed, view=view)
            case 'custom_embed':
                embed_data = server_conifg['settings']['announce_config']['format']['custom_embed']
                # Custom datas $server_icon $author $server_color
                title = embed_data['title'].replace('%msg%', args)
                body = embed_data['body'].replace('%msg%', args)
                author = embed_data['author'].replace('%msg%', args)
                
                if embed_data['img'] == '$server_icon': img = ctx.guild.icon
                else: img = embed_data['img']

                if embed_data['color'] == '$server_color':
                    if server_conifg['settings']['color']: color = int(server_conifg['settings']['color'], 16)
                    else: color = bot.color
                
                bot.embed = discord.Embed(title=title, description=body, color=color)
                bot.embed.set_author(name=author)
                bot.embed.set_thumbnail(url=img)

                bot.msg = await ctx.send(server_conifg['settings']['announce_config']['format']['form'].replace('%msg%', args), embed=bot.embed, view=view)


            case _: pass
    except:
        server_conifg['settings']['announce_config'] = {'format':{'type':'text', 'form':'%msg%'}}
        save_db()
        #Recall the method
        await announce(ctx, args=args)
        return

@commands.command()
@commands.has_permissions(administrator=True)
async def forbid_exclamations(ctx):
    members = ctx.guild.members

    count = 0
    
    embed=discord.Embed(title = 'Removing ! from member names...', description = f'{count}/{len(members)} members processed', color=bot.color)
    log = ''
    
    msg = await ctx.send(embed=embed)

    for member in members:
        if '!' in member.display_name:
            try:
                await member.edit(nick=member.display_name.replace('!', ''))
            
            except Exception as error:
                log += f'{member.mention} has an `!` in the name, but i cant remove it'
                bot.log.error(f'SERVERTOOLS: {error}')
        
        count += 1
        embed.description = f'{count}/{len(members)} members processed'
        if log != '': embed.add_field(name = 'Log', value = log, inline=False)
        await msg.edit(embed=embed)
        
@commands.command()
@commands.has_permissions(administrator=True)
async def serverinfo(ctx):
    embed = discord.Embed(title = 'ServerInfo', color= bot.color)
    guild = ctx.guild
    embed.add_field(name = 'Owner', value = guild.owner.mention)
    embed.add_field(name = 'Creation Date', value = type(guild.created_at))
    embed.add_field(name = 'Members', value = len(guild.members))
    embed.add_field(name = 'Channels', value = len(guild.channels))
    embed.add_field(name = 'Bots', value = 'No Data')
    embed.add_field(name = 'Emogis', value = len(guild.emojis))
    embed.add_field(name = 'Max Members', value = type(guild.max_members))
    embed.add_field(name = 'Nitro Boosters', value = len(guild.premium_subscribers))

    await ctx.send(embed=embed)

@commands.command()
async def whois(ctx, user:discord.Member = None):

    if user == None:
        user = ctx.author

    rolesl = list()
    for role in user.roles:
        if role.name != '@everyone':
            rolesl.append(role.mention)


    roles = ", ".join(reversed(rolesl))


    embed = discord.Embed(title= f'Who is {user}?', colour = bot.color)

    embed.set_thumbnail(url = user.avatar)
    embed.set_footer(text = f'Requested by - {ctx.author}', icon_url = ctx.author.avatar)

    embed.add_field(name = 'ID:', value = user.id, inline=False)
    embed.add_field(name = 'Name:', value = user.display_name, inline=False)
    diff = str(datetime.datetime.now() - user.created_at.replace(tzinfo=None)).split(',')[0]
    embed.add_field(name = 'Created at:', value = f'{user.created_at.strftime("%d/%m/%Y %H:%M")} ({diff} ago)', inline=False)    #!embed.add_field(name = 'Created at:', value = user.created_at, inline=False)
    diff = str(datetime.datetime.now() - user.joined_at.replace(tzinfo=None)).split(',')[0]
    embed.add_field(name = 'Joined at:', value = f'{user.joined_at.strftime("%d/%m/%Y %H:%M")} ({diff} ago)', inline = False)    #!embed.add_field(name = 'Joined at:', value = user.joined_at, inline = False)

    if len(rolesl) > 1:
        embed.add_field(name = f'Roles: {len(rolesl)} ',value = ''.join([roles]), inline=False)
    else:
        embed.add_field(name = f'Roles: 0',value = bot.nullchar, inline=False)
    
    embed.add_field(name = 'Top Role:', value = user.top_role.mention, inline=False)

    embed.add_field(name = bot.nullchar, value = bot.nullchar, inline=False)

    await ctx.send(embed=embed)
