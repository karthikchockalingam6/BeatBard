import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
import requests
import json
import os
from apikeys import *

# intents=discord.Intents.default()
# intents.members=True

queues = {} #dictionary

def check_queue(ctx,id):
    if queues[id]!=[]:
        voice=ctx.guild.voice_client
        source=queues[id].pop(0)
        player=voice.play(source) 
 
client = commands.Bot(command_prefix="!", intents=discord.Intents.all()) 

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game('with Discord Tools'))
    print("BeatBard is ready for use :)")
    print("-----------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hi, I'am BeatBard how can i help you ?")

@client.event
async def on_member_join(user:discord, *, message=None):
    url = "https://quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com/quote"
    querystring = {"token":"ipworld.info"}
    headers = {
	    "X-RapidAPI-Key": Motivation_API_key,
	    "X-RapidAPI-Host": "quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    channel = client.get_channel(1135107444654215238)
    await channel.send("Welcome :) to Çhö's Server ")
    api= discord.Embed(title="Welcome :) to Çhö's Server",description=json.loads(response.text)['text']+" - "+json.loads(response.text)['author'],color=0x7CFC00)
    #DM
    # message = "Welcome to Çhö's Server!"
    # embed = discord.Embed(title=message)
    # await user.send(embed=embed)
    await user.send(embed=api)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1135107444654215238)
    await channel.send("GoodBye :(")
    await channel.send(member)
    
@client.command()
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        # source = FFmpegPCMAudio('Violin.mp3')
        # player=voice.play(source)
        
    else:
        await ctx.send("You are not in a voice channel, You must be in a voice channel to run this command.")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()  #guild=server
        await ctx.send("See you again in the voice channel soon.")
    else:
        await ctx.send("I'm not in a voice channel.")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("At the moment, There is no audio playing in the voice channel.")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("At the moment, No song is paused.")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send("The music has been stopped ,type \"!play {music name}\" to play songs.")

@client.command(pass_context = True)
async def play(ctx,arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.mp3')
    player=voice.play(source,after=lambda x=None: check_queue(ctx,ctx.message.guild.id))
    await ctx.send("You are now listening to {}.".format(arg))

@client.command(pass_context = True)
async def queue(ctx,arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.mp3') 

    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id]=[source]

    await ctx.send("{} is added to Queue.".format(arg))

@client.event
async def on_message(message):
    await client.process_commands(message) 
    lis=["Pen","Paper","Eraser"]
    for i in lis:
        if message.content==i:
            await message.delete()
            await message.channel.send("Improper word \"{}\" detected and Deleted.".format(i))


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx,member:discord.Member, *,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have permission to kick people :(")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been Banned')

@ban.error
async def ban_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have permission to ban people :(" )

@client.command()
async def embed(ctx):
    embed = discord.Embed(title='Test',url='https://google.com',description='Testing Embeds',color=0x4dff4d)
    embed.set_author(name=ctx.author.display_name,url='https://www.linkedin.com/in/karthik-chockalingam6/')
    embed.set_thumbnail(url='https://cdn.vectorstock.com/i/preview-1x/48/64/javascript-emblem-black-letters-on-yellow-bg-vector-28264864.jpg')
    embed.add_field(name="Test123",value="123456789",inline=True)
    embed.add_field(name="Test2",value="gggggg",inline=True)
    embed.set_footer(text='End of Testing footer')
    await ctx.send(embed=embed)

@client.command()
async def dm(ctx,user:discord.Member,*,message=None):
    message = "Welcome to Çhö's Server"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

client.run(Bot_Token)