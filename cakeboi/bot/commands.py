import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from cakeboi.util.common import local
from cakeboi.util.sheets import helper

cmd_dict = {
    "comment"
}

async def cmd(message):
    print("[Log]", "[commands.py]", "Command detected")


    return
    if message.content.startswith('!comment'):
        await comment(message)

    if message.content.startswith('!purge'):
        await purge(message)

    if message.content.startswith('!upload'):
        await upload(message)

    if message.content.startswith('!help'):
        await help(message)

    if message.content.startswith('!waifu'):
        await message.channel.send(file=discord.File(r"./waifus/waifu.png"))

    if message.content.startswith('!transfer'):
        await transfer(message)
    return


# !help
async def help(message):
    command_list = """```
!waifu
!upload n
!purge n
    
in general:
    !command --help
    !command -h
    !command ?
```"""
    await message.channel.send(command_list)


# !purge n
async def purge(message):
    args = message.content.split()
    if (args[1]) == "all":
        await message.channel.purge(limit=1000)
    if len(args) > 1 and (args[1] in ["--help", "-h", "?"]):
        await message.channel.send("```Purges the last <n> messages. (Not counting the command itself)"
                                   "\n\nUsage: !purge n```")
        return
    if len(args) != 2 or not args[1].isnumeric():
        await message.channel.send("```Usage: !purge n```")
        return

    await message.channel.purge(limit=int(args[1]) + 1)


# !upload n
async def upload(message):
    """
    Uploads message attachments to the drive
    :param message:
    :return:
    """
    args = message.content.split()

    if len(args) > 1 and args[1] in ["--help", "-h", "?"]:
        await message.channel.send(
            "```Checks the last <n> messages and uploads them to the drive. (Not counting the command itself)"
            "\n\nUsage: !upload n```")
        return

    if len(args) != 2 or not args[1].isnumeric():
        await message.channel.send("```Usage: !upload n```")
        return

    latest_messages = await message.channel.history(
        limit=int(args[1]) + 1).flatten()

    for msg in latest_messages:
        await local.save_all(msg)


async def transfer(message):
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
    helper.upload_link_batch(links)
    print("[Log]", f"Transfer complete")
    await message.channel.send(f"Transfer completed (Sent `{len(links)}` attachments)")


async def comment(message):
    # args = message.content.split()
    # if len(args) > 1 and (args[1] in ["--help", "-h", "?"]):
    #     await message.channel.send("```Purges the last <n> messages. (Not counting the command itself)"
    #                                "\n\nUsage: !purge n```")
    #     return
    #
    # if len(args) != 2 or not args[1].isnumeric():
    #     await message.channel.send("```Usage: !purge n```")
    #     return
    # await message.channel.purge(limit=int(args[1]) + 1)

    # !comments Das ist ein kommentar

    from datetime import datetime, timedelta
    text = message.content
    text = text[9:]

    datum = datetime.today() - timedelta(hours=21)
    print(datum)
    datum = datum.strftime("%a-%d-%b")

    await message.channel.send("Comment for the " + "**" + datum + "**" + " will be " + "\"" + text + "\"")

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive",
             "https://spreadsheets.google.com/feeds"]

    cred = ServiceAccountCredentials.from_json_keyfile_name("util/sheets/discord_cakeboi.json", scope)
    user = gspread.authorize(cred)

    # Worksheet (Reference)
    worksheet = user.open_by_key("1QPtUaV95DvA-25uokOo1qpf_58OPUkOTBRpwML_Yh48").sheet1  # Open the spreadsheet

    cell = worksheet.find(datum)  # gefundene celle mit dem datum
    worksheet.update_cell(cell.row, cell.col + 1, text)  # update mit "text"
    return

