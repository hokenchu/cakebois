# Work with Python 3.6
import discord
import gspread
from discord.ext import tasks
from oauth2client.service_account import ServiceAccountCredentials

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

    if message.content in ["ping", "!ping", "hello", "!hello"]:
        await message.channel.send(f"Was :eyes:, {message.author.mention}")

    if message.content.startswith('!transfer'):
        args = message.content.split()
        if len(args) != 2 or not args[1].isnumeric():
            return

        links = []
        latest_messages = await message.channel.history(
            limit=int(args[1]) + 1).flatten()

        for msg in latest_messages:
            for attachment in msg.attachments:
                links.append(attachment.url)

        links.reverse()  # reverse order
        print("[Log]", f"Collected {len(links)} links from {len(latest_messages)} messages")

        scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
        "https://spreadsheets.google.com/feeds"]

        svc_cred = ServiceAccountCredentials.from_json_keyfile_name("config/discord_cakeboi.json", scope)

        user = gspread.authorize(svc_cred)
        print("[Log]", "[sheets_api.py]", "Successfully authorized Google Spreadsheets")

        # Open the spreadsheet
        # First sheet of "CakeboiSheet"
        worksheet = user.open("CakeboiSheet").sheet1

        from datetime import date

        cell_of_today = date.today().strftime("%a-%d-%b")
        row = worksheet.find(cell_of_today).row
        col = worksheet.find(cell_of_today).col
        for (index, link) in enumerate(links, start=1):
            print("[Log]", "[sheets_api.py]", f"Updated cell at (Col{col + index}|Row{row}): {link}")
            worksheet.update_cell(row, col + index, f"=IMAGE(\"{link}\")")

        print("[Log]", f"Transfer complete")
        await message.channel.send(f"Transfer completed (Sent `{len(links)}` attachments)")

if __name__ == '__main__':
    client.run(TOKEN)
