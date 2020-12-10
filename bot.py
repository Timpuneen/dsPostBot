import discord
from discord import utils
from discord.ext import commands
import asyncio

import config
from stopgame import StopGame

sg = StopGame('lastkey.txt')
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(status=discord.Status.online,activity=discord.Game('minecraft'))

@client.command(pass_context = True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount+1)    
 
async def postTest(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        new_games = sg.new_games()
        if(new_games):
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game_info(ng)

                emb = discord.Embed(title = 'узнать больше(тык)', colour = discord.Color.purple(), url=nfo['link'])
                emb.set_author(name = client.user.name, icon_url=client.user.avatar_url)

                emb.set_image(url = nfo['image'])
                emb.set_thumbnail(url = 'https://cdn.discordapp.com/icons/710367180469829662/d6546c8da3c9da21c071aa2908c68a9c.webp?size=128')

                emb.add_field(name = 'Краткое описание:', value=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'])

                try:
                    await client.get_channel(config.Post_Channel).send(embed = emb)
                except Exception as error:
                    print(error)    

                sg.update_lastkey(nfo['id'])   
# RUN
loop = asyncio.get_event_loop()
loop.create_task(postTest(10))
client.run(config.TOKEN+'HxdA')