# Libraries
import discord, asyncio, os, random, datetime
from discord.ext import commands, tasks

# Start Here
bot = discord.Client()

@bot.event
async def on_ready():
    print("Bot is ON!")

# ON MESSAGE CODE
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Gym keywords (Nugs)
    gym_keywords = ["gym","workout","gymnasium"]
    for keyword in gym_keywords:
        if keyword in message.content:
            await message.channel.send(f"Did someone say {keyword}? Nugs is our gym rat!!")
            await message.channel.send(file=discord.File('Images/gym_rat.png'))

    # Robert Quebed Joke
    robert_keywords = ["robert","quebec","QUEBEC","Robert","ROBERT"]
    for keyword in robert_keywords:
        if keyword in message.content:
            await message.channel.send(f"Quick reminder i got here...")
            await message.channel.send(file=discord.File('Images/robert_i_quit.jpg'))            

Colo_Reminded = False   ## Bool Value for Colo Reminder Message
@bot.event
## COLO REMINDER CODE
async def colo_reminder(Colo_Reminded):
    while (True):
        await bot.wait_until_ready()
        current_time = datetime.datetime.now()
        time_hour = int(current_time.hour) 
        time_minutes = int(current_time.minute)
        if (time_hour >= 21 and time_minutes >= 57 and Colo_Reminded == False):
                # Get ROLE ID
            message = f"<@&729351086091272235> Colo is open!! Get Ready!!"
                # Get channel ID to send the message
            channel = bot.get_channel(728386613264253041)
            await channel.send(message)
            print(message)
            Colo_Reminded = True
        await asyncio.sleep(10)

bot.loop.create_task(colo_reminder(Colo_Reminded))

token = "Nzk3NDA4NTU5ODcyMjEzMDEy.X_mClw.2aSb_1E7Y8hnONdVQwQNbpytVXc"
bot.run(token)
