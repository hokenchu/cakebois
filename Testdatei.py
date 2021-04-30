# Work with Python 3.6
import discord

TOKEN = 'ODM3Njc1OTQ4MzQ5ODQ5NjQx.YIwAhQ.Wvc3LwhUfhkS4Qvk_cp-8H5x8iI'

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print('\t', client.user.name)
    print('\t', client.user.id)
    print('---------------')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Info im Terminal wenn jemand eine Nachricht schreibt
    print(f"[new message] {message.guild.name} > {message.channel.name} > {message.author}")

    if message.guild.id != 837676563583336458:
        print(f"Wrong server, bro")
        return

    if message.channel.id != 837676563583336461:
        print("Wrong channel, bro")
        return

    # Hier kommen wir an wenn es der richtige channel und server ist
    # Spezifischer Code ab hier

    if message.content.startswith('!hello'):
        msg = "Hello {0.author.mention}".format(message)
        await message.channel.send(msg)


# def save_locally(file):


# Do not touch this. Starts the bot
client.run(TOKEN)
