import discord
import json

embed=discord.Embed(title="A", description="texto")
embed.set_author(name="pinchiguillo")
embed.add_field(name="a", value="a", inline=False)
embed.set_footer(text = 'Apuntes creados por pinchiguillo')

with open('temp.embed.json', 'w', encoding='utf-8') as f:
    json.dump(embed.to_dict(), f, indent=4, ensure_ascii=False)