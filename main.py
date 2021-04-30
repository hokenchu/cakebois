# Work with Python 3.6
import discord
from discord.ext import tasks

TOKEN = 'ODM3Njc1OTQ4MzQ5ODQ5NjQx.YIwAhQ.Wvc3LwhUfhkS4Qvk_cp-8H5x8iI'

client = discord.Client()
bot_channel = None;


@client.event
async def on_ready():
    print('Logged in as')
    print('>', f"{client.user.name} (id:{client.user.id})")
    global bot_channel
    bot_channel = client.get_channel(837676563583336461)
    print('>', f"[{bot_channel.guild}] \"{bot_channel.name}\" (id:{bot_channel.id})")

    print("Initiating Purging Task")
    loop_purge.start(3600) # inactive time in seconds

    print('---------------')


@tasks.loop(seconds=3600) # frequency of checks
async def loop_purge(inactivity_time):
    history = await bot_channel.history(limit=100).flatten()
    if len(history) == 0:
        return

    from datetime import datetime
    import pytz

    last = history[0].created_at.timestamp()
    now = datetime.today().astimezone(pytz.timezone('UTC')).timestamp() - 7200
    print("[Log]", f"Last message was {now - last} seconds ago")
    if now - last > inactivity_time:
        await bot_channel.purge()
        print("[Log]", f"Purged {bot_channel}")


@client.event
async def on_message(message):
    global bot_channel
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if type(message.channel) == discord.DMChannel:
        print("Why are you whispering, bro")
        print(f"[new message] direct message > {message.author}")
        return

    # Info im Terminal wenn jemand eine Nachricht schreibt
    print(f"[new message] {message.guild.name} > {message.channel.name or 'DM'} > {message.author}")

    if message.guild.id != 837676563583336458 or message.channel.id != 837676563583336461:
        print(f"[Info] Wrong channel, bro")
        return

    if message.content.startswith('!purge'):
        await message.channel.purge(limit=100)

    if message.content.startswith('!upload'):
        latest_messages = await bot_channel.history(
            limit=12).flatten()
        # Increase limit to compensate for user error

        print(latest_messages)
        # TODO filter older messages

        for msg in latest_messages:
            if msg.content.startswith("Guild:"):  # TODO Voraussetzung
                print(">> You fought against ", msg.content.replace('Guild', '').replace(':', ""))  # TODO name filtern

            if msg.content in ["win", "victory", "defeat", "lose"]:
                print(">> Lul, you ", msg.content)

            if len(msg.attachments) > 0:
                print(">> ", 'You sent some pictures')


    if message.content.startswith('!save'):
        for attachment in message.attachments:
            print(attachment.filename)
            await attachment.save(f"./resources/{attachment.filename}")


# Do not touch this. Starts the bot
client.run(TOKEN)
