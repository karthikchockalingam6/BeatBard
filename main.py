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
    print("BeatBard is ready for use :)")
    print("-----------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hi, I'am BeatBard how can i help you ?")

@client.event
async def on_member_join(member):
    url = "https://quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com/quote"
    querystring = {"token":"ipworld.info"}
    headers = {
	    "X-RapidAPI-Key": Motivation_API_key,
	    "X-RapidAPI-Host": "quotes-inspirational-quotes-motivational-quotes.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    channel = client.get_channel(1135107444654215238)
    await channel.send("Welcome :) to Çhö's Server ")
    await channel.send("Today's Motivation : "+json.loads(response.text)['text']+" - "+json.loads(response.text)['author'])

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1135107444654215238)
    await channel.send("GoodBye :(")
    
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


client.run(Bot_Token)