# Work with Python 3.6
import discord
from discord.ext import tasks
from utility.commands import *

# Initial setup
TOKEN = 'ODM3Njc1OTQ4MzQ5ODQ5NjQx.YIwAhQ.Wvc3LwhUfhkS4Qvk_cp-8H5x8iI'
client = discord.Client()
bot_channel = None

@client.event
async def on_ready():
    """
    Things to do when bot goes online and is ready.

    Shows some basic information and tries to start all tasks
    :return:
    """
    print('Logged in as')
    print('>', f"{client.user.name} (id:{client.user.id})")
    global bot_channel
    bot_channel = client.get_channel(837676563583336461)
    print('>', f"[{bot_channel.guild}] \"{bot_channel.name}\" (id:{bot_channel.id})")

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
    history = await bot_channel.history(limit=100).flatten()
    if len(history) == 0:
        return

    from datetime import datetime
    import pytz

    last = history[0].created_at.timestamp()
    now = datetime.today().astimezone(pytz.timezone('UTC')).timestamp() - 7200
    print("[Info]", f"Last message was {now - last} seconds ago")
    if now - last > inactivity_time:
        await bot_channel.purge()
        print("[Log]", f"Purged {bot_channel}")



@client.event
async def on_message(message):
    """
    Check which commands to listen to.

    Implement actual commands in utility.commands.py
    :param message:
    :return:
    """
    global bot_channel
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if type(message.channel) == discord.DMChannel:
        print("Why are you whispering, bro")
        print(f"[new message] direct message > {message.author}")
        return

    # Info im Terminal wenn jemand eine Nachricht schreibt
    print(f"[Info] New message in {message.guild.name}>{message.channel.name or 'DM'}>{message.author} '{message.content[:80]}'")

    if message.guild.id != 837676563583336458 or message.channel.id != 837676563583336461:
        print(f"[Info] Wrong channel, bro")
        return

    if message.content.startswith('!purge'):
        await command_purge(message)

    if message.content.startswith('!upload'):
        await command_upload(message)

    if message.content.startswith('!help'):
        await command_help(message)

    if message.content.startswith('!waifu'):
        await message.channel.send(file=discord.File(r"./waifus/waifu.png"))

    if message.content.startswith('!transfer'):
        await command_transfer(message)

if __name__ == '__main__':
    client.run(TOKEN)
