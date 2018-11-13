#!/usr/bin/env python3
from discord.ext.commands import Bot
import datetime
import discord
import feedparser
import os
import pytz

BOT_PREFIX = ("?", "!")
TOKEN = os.environ['TOKEN']
def convert_to_local_datetime(date):
    # Set UTC
    utc = pytz.UTC
    # Set local timezone
    # TODO get dynamically
    pst = pytz.timezone('Europe/Zurich')
    # Parse the CTFtime ISO date
    d = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S') 
    # Define it's UTC
    d = utc.localize(d)
    # Convert to local timezone
    d = d.astimezone(pst) 
    # Create a human readable format
    dt = d.strftime('%d. %b %Y @ %H:%M')
    return dt

client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

@client.command()
async def ctf():
    url = 'https://ctftime.org/event/list/upcoming/rss/'
    d = feedparser.parse(url)
    # Next 3 CTFs
    for post in d.entries[:3]:
        description = ''
        # Convert to local datetime
        start = convert_to_local_datetime(post.start_date)
        finish = convert_to_local_datetime(post.finish_date)
        # Create answer
        description+= "From: %s \n Until: %s" % (start, finish)
        e=discord.Embed(title=post.title, description="["+post.title+"] ("+post.link+")")
        # https://cog-creators.github.io/discord-embed-sandbox/
        msg=discord.Embed(title=post.title, url=post.url, description=description)
        msg.set_thumbnail(url="https://ctftime.org"+post.logo_url)
        await client.say(embed=msg)

client.run(TOKEN)