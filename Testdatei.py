# Work with Python 3.6
import discord

TOKEN = 'ODM3Njc1OTQ4MzQ5ODQ5NjQx.YIwAhQ.Wvc3LwhUfhkS4Qvk_cp-8H5x8iI'

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = "Hello {0.author.mention}".format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print('\t', client.user.name)
    print('\t', client.user.id)
    print('---------------')

client.run(TOKEN)