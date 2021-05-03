import discord

from cakeboi.util.common import local
from cakeboi.util.sheets.helper import SheetsUser

__PREFIX = '!'


async def cmd(message):
    """
    Decides which command gets called.

    Commands need to be added here to be available
    """
    cmd_text = message.content.split()[0]

    cmd_dict = {
        "help": cmd_help,
        "purge": purge,
        "transfer": transfer,
        "comment": comment,
        "save": save_locally,  # FIXME allow saving locally?
        "waifu": waifu,
        "prefix": prefix
    }

    cmd_func = cmd_dict.get(cmd_text.replace(__PREFIX, ""))
    if cmd_func is not None:
        print("[Log]", "[commands.py]", f"Executing {cmd_func}()")
        await cmd_func(message)
    return


# !help
async def cmd_help(message):
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


# !upload
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

    hist = await message.channel.history(
        limit=int(args[1]) + 1).flatten()

    hist.reverse()

    file_list = []
    for msg in hist:
        for (index, att) in enumerate(msg.attachments, start=0):
            file_list.append(local.save(attachment=att, filename_base=index))

    await message.channel.send(f"Saved {len(file_list)} files locally")


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

    sheets_user = SheetsUser(channel_id=message.channel.id)
    sheets_user.upload(links)

    print("[Log]", f"Transfer complete")
    await message.channel.send(f"Transfer completed (Sent `{len(links)}` attachments)")


async def comment(message):
    from datetime import datetime, timedelta

    text = message.content
    text = text[9:]

    datum = datetime.today() - timedelta(hours=21)
    datum = datum.strftime("%a-%d-%b")

    await message.channel.send("Comment for the **" + datum + "**" + " will be " + "\"" + text + "\"")

    sheets_user = SheetsUser(channel_id=message.channel.id)
    sheets_user.comment(text)
    return


async def waifu(message):
    await message.channel.send(file=discord.File(r"../waifus/waifu.png"))


async def prefix(message):
    global __PREFIX
    if len(message.content.split()) == 2:
        __PREFIX = message.content.split()[1]
        await message.channel.send(f"Prefix changed to `{__PREFIX}`")
    else:
        await message.channel.send(f"`Current prefix is `{__PREFIX}`")
    return


def get_prefix():
    return __PREFIX
