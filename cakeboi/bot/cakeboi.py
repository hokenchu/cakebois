import discord

from cakeboi.bot import commands
from cakeboi.util import guser
from cakeboi.util import local

client = discord.Client()

__SUBSCRIBER_LIST = None


def run(token=None):
    if token is None:
        token = local.get_token('bot')

    global __SUBSCRIBER_LIST
    __SUBSCRIBER_LIST = [u['channel_id'] for u in guser.get_subscribers()]

    client.run(token)


@client.event
async def on_ready():
    """
    Things to do when bot goes online and is ready.

    Shows some basic information and tries to start all tasks
    :return:
    """
    print('Logged in as')
    print('>', f"{client.user.name} (id:{client.user.id})")
    #    loop_purge.start(3600)  # inactive time in seconds

    print("Channels in subscription:")
    for chan_id in __SUBSCRIBER_LIST:
        print(f"\t{client.get_channel(int(chan_id))} : {chan_id}")

    print("Active:")
    for guild in client.guilds:
        text_channels = []
        for channel in guild.channels:
            if type(channel) is discord.channel.TextChannel:
                text_channels.append(channel)
        print('\t', guild.name, [channel.name for channel in sorted(text_channels, key=lambda ch: ch.position)])
    print('---------------')


@client.event
async def on_message(message):
    if message.author == client.user:
        # we do not want the bot to reply to itself
        return

    if type(message.channel) != discord.TextChannel:
        """
        Blocks direct messages
        """
        # print(f"[new message] direct message > {message.author}")
        return

    if str(message.channel.id) not in __SUBSCRIBER_LIST:
        """
        Blocks from unsubscribed channels.
        Print()s can be omitted.  
        """
        return  # stops here

    print(
        f"[Info] New message in {message.guild.name}>{message.channel.name or 'DM'}>{message.author}: '{message.content[:80]}'")

    if message.content.startswith(commands.get_prefix()):
        await commands.cmd(message)

    # command to test connectivity
    if message.content in ["ping",
                           f"{commands.get_prefix()}ping",
                           "hello",
                           f"{commands.get_prefix()}hello"]:
        await message.channel.send(f"Was :eyes:, {message.author.mention}")
        return

    if "bad boy" in message.content:
        await message.channel.send("_Ich reite diesen boesen Jungen_")
