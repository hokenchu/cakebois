# Work with Python 3.6

import discord
from discord.ext import tasks

from cakeboi.bot import commands

# Initial setup
__TOKEN = 'ODM3Njc1OTQ4MzQ5ODQ5NjQx.YIwAhQ.Wvc3LwhUfhkS4Qvk_cp-8H5x8iI'
client = discord.Client()
__BOT_CHANNEL = None


def run():
    client.run(__TOKEN)


@client.event
async def on_ready():
    """
    Things to do when bot goes online and is ready.

    Shows some basic information and tries to start all tasks
    :return:
    """
    print('Logged in as')
    print('>', f"{client.user.name} (id:{client.user.id})")
    global __BOT_CHANNEL
    __BOT_CHANNEL = client.get_channel(837676563583336461)
    print('>', f"[{__BOT_CHANNEL.guild}] \"{__BOT_CHANNEL.name}\" (id:{__BOT_CHANNEL.id})")
    print("Initiating Purging Task")
    loop_purge.start(3600)  # inactive time in seconds

    print('---------------')


@tasks.loop(seconds=3600)  # frequency of checks
async def loop_purge(inactivity_time=3600):
    """
    Check every 3600 seconds if there has been a message lately.
    (Default 1 hour)

    If not, purges last 100 messages.
    :param inactivity_time:
    :return:
    """
    history = await __BOT_CHANNEL.history(limit=100).flatten()
    if len(history) == 0:
        return

    from datetime import datetime
    import pytz

    last = history[0].created_at.timestamp()
    now = datetime.today().astimezone(pytz.timezone('UTC')).timestamp() - 7200
    print("[Info]", f"Last message was {now - last} seconds ago")
    if now - last > inactivity_time:
        await __BOT_CHANNEL.purge()
        print("[Log]", f"Purged {__BOT_CHANNEL}")


@client.event
async def on_message(message):
    if message.author == client.user:
        # we do not want the bot to reply to itself
        return

    if type(message.channel) == discord.DMChannel:
        print("Why are you whispering, bro")
        print(f"[new message] direct message > {message.author}")
        return

    # Info im Terminal wenn jemand eine Nachricht schreibt
    print(
        f"[Info] New message in {message.guild.name}>{message.channel.name or 'DM'}>{message.author} '{message.content[:80]}'")

    if message.guild.id != 837676563583336458 or message.channel.id != 837676563583336461:
        print(f"[Info] Wrong channel, bro")
        return

    if message.content.startswith(commands.get_prefix()):
        await commands.cmd(message)

    if message.content in ["ping", f"{commands.get_prefix()}ping",
                           "hello", f"{commands.get_prefix()}hello"]:
        await message.channel.send(f"Was :eyes:, {message.author.mention}")
        return
