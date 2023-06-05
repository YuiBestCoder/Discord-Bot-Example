from re import search
import discord, os
import asyncio
import json 
from discord.ext import commands, context
import collections
import reason
from DiscordDatabase import DiscordDatabase
import mysql.connector
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
import youtube_dl
from discord import Message, app_commands, utils, Member, FFmpegPCMAudio, TextChannel
import aiohttp
from datetime import datetime
import urllib3
from urllib3 import request
# json data
import json
# pandas dataframes
import pandas as pd
from flask import Flask
from threading import Thread
import alfred
import typing
import random
import discord, os
from datetime import datetime
from discord import app_commands, utils, Webhook
from discord.ext import commands, tasks
import aiohttp
from googlesearch import search
from asyncio import sleep

role_id = any
guild_id = any

user_data = {}


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged as{0}!".format(self.user))

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=';', intents=intents)




@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity = discord.Game(name=f'hello!'))


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a member from the server."""
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned from the server.')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member from the server."""
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked from the server.')

@bot.command()
async def purge(ctx, amt):
    await ctx.channel.purge(limit = int(amt) + 1)
    msg = await ctx.send(f"Deleted {amt} messages!")
    await asyncio.sleep(3)
    await msg.delete()

os.chdir(r'C:\Users\Miku\Discord Bot')

@client.event
async def on_member_join(member):
    with open('users.json','r') as f:
        users = json.load(f)

    await client.update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    with open('users.json','r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)
    
    with open('users.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        user[user.id] = {}
        users[user.id]['experience'] = 0 
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/5))

    if lvl_start < lvl_end:
        await client.send_message(channel, '{} Has leveled up! He got this time to level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end

@client.event
async def on_message(message):
    if message.mentions:
        results = collections.find({"member": message.author.id}) 
        for result in results:
            collections.delete_one(result)
            if message.content == result:
                await message.channel.send(f"This person is currently AFK. \nFor: {reason}")
            

        await client.process_commands(message)


@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, *,reason=None):
    role = discord.utils.get(ctx.guild.roles, id=1104502706044928030)
    await member.add_roles(role, reason=reason)
    message: discord.Message = await ctx.send(f"User {member} has been muted by reason: {reason}!")
    await message.add_reaction("✔️")



@bot.command()
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")



@bot.command()
async def save_warn(ctx, member: discord.Member):
    with open('warns.json', 'r') as f:
         warns = json.load(f)

         warns[str(member.id)] += 1

    with open('warns.json', 'w') as f:
         json.dump(warns, f)

@bot.command()
async def remove_warn(ctx, member: discord.Member, amount: int):
    with open('warns.json', 'r') as f:
         warns = json.load(f)

         warns[str(member.id)] -= amount

    with open('warns.json', 'w') as f:
         json.dump(warns, f)
    
@bot.command()
async def infractions(member: discord.Member):
    with open("warns.json", "r") as f:
        warns = json.load(f)

    warns[str(context.member)]
    return warns

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    
      save_warn(ctx, member)
      dm = await bot.fetch_user(member.id)
      em=discord.Embed(title="Warning", description=f"Server: {ctx.guild.name}\nReason: {reason}")
      await dm.send(embed=em)

app = Flask('')

@app.route('/s')
def main():
    return '<meta http-equiv="refresh" content="0; URL=https://phantom.is-a.dev/support"/>'

def run():
    app.run(host="0.0.0.0", port=8080)

async def keep_alive():
    server = Thread(target=run)
    server.start()

@client.event
async def on_member_join(member):
    channel = alfred.get_channel(id)
    embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    await channel.send(embed=embed)

@bot.command()
async def helpls(ctx):
    embed = discord.Embed(title="Help", description="List of available commands:")
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.content.startswith("google"):
        query = message.content[8:]
        for j in search(query, num=5, stop=5, pause=2):
            await message.channel.send(j)


@bot.command()
async def level(ctx):
    # Get the user's ID
    user_id = ctx.author.id

    # Check if the user exists in the dictionary
    if user_id not in user_data:
        user_data[user_id] = {'name': ctx.author.name, 'discriminator': ctx.author.discriminator, 'xp': 0, 'level': 1}
        await ctx.send("Welcome to the server! You are now at level 1.")
    else:
        xp = user_data[user_id]['xp']
        level = user_data[user_id]['level']
        await ctx.send("You are currently at level {} with {} XP.".format(level, xp))

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Get the user's ID
    user_id = message.author.id

    # Check if the user exists in the dictionary
    if user_id not in user_data:
        user_data[user_id] = {'name': message.author.name, 'discriminator': message.author.discriminator, 'xp': 1, 'level': 1}
    else:
        xp = user_data[user_id]['xp']
        xp += 1
        level = user_data[user_id]['level']
        if xp > (level * 100):
            await message.channel.send("{} has leveled up to level {}!".format(message.author.mention, level + 1))
            level += 1
        user_data[user_id]['xp'] = xp
        user_data[user_id]['level'] = level

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! {latency}ms')
    
@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.author
    
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=member.avatar)
    
    await ctx.send(embed=embed)

# Define a timer start command
@bot.command()
async def start_timer(ctx):
    # Start the timer here
    await ctx.send('Timer started')

# Define a timer stop command
@bot.command()
async def stop_timer(ctx):
    # Stop the timer here
    await ctx.send('Timer stopped')






bot.run("token") # Replace with your discord bot token, you can find on discord.com/developers/applications