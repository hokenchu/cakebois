import discord

from cakeboi.util.common import local
from cakeboi.util.drive.helper import DriveUser
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
        "comment": comment,
        "waifu": waifu,
        "prefix": prefix,
        "upload": upload
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
!upload guildname result
!purge n
!comment text
    
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
                                   "\n\nUsage: !purge n"
                                   "\nAlternative: !purge all (this clears the whole channel)```")
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

    if len(args) > 1 and (args[1] in ["--help", "-h", "?"]):
        await message.channel.send("```Uploads the last 10 screenshots (entries) "
                                   "\nto the gdrive and sorts guildname+results+screenshots into the spreadsheet"
                                   "\n\nUsage: !upload guildname result"
                                   "\n\nExample: !upload Peanut Win```")
        return

    user = SheetsUser(channel_id=message.channel.id)

    if args[-1] in ["Lose", "lose", "Defeat", "defeat"]:
        user.outcome("Lose")
    elif args[-1] in ["Win", "win", "Victory", "victory"]:
        user.outcome("Win")
    else:
        await message.channel.send("Missing battle outcome! (win/lose)"
                                   "\n\n```Example: !upload Peanut Win```"
                                   "\n\n(*Delete this + the wrong upload "
                                   "command message before you use !upload again)*")
        return

    separator = ' '
    guild_name = separator.join(args[1:-1])

    user.guildnaming(guild_name)

    hist = await message.channel.history(limit=11).flatten()

    hist.reverse()

    all_attachments = []
    for msg in hist:
        for att in msg.attachments:
            all_attachments.append(att)
            print(att)

    all_files = []
    for (index, att) in enumerate(all_attachments, start=0):
        file = await local.save(att, index, message.channel)
        all_files.append(file)

    await message.channel.send(f"Saved {len(all_files)} files locally")

    user = DriveUser(channel_id=message.channel.id)
    folder = user.create_folder()
    user.clear_folder(folder["id"])
    file_list = user.upload(path_list=all_files,parent_id=folder['id'])

    await message.channel.send(f"Uploaded {len(all_files)} files to {folder['name']}")
    link_list = []
    for f in file_list:
        link_list.append(f"https://drive.google.com/uc?export=view&id={f['id']}")
    user = SheetsUser(channel_id=message.channel.id)
    user.upload(list_of_links=link_list)

    await message.channel.send(f"Sent {len(link_list)} images to {user.sheet_id}")

    return


async def comment(message):
    from datetime import datetime, timedelta
#    args = message.content.split
#    if len(args) > 1 and (args[1] in ["--help", "-h", "?"]):
#        await message.channel.send("```Adds a text to the comment section of the spreadsheet "
#                                   "\n\nUsage: !comment text"
#                                   "\n\nExample: !comment We got lubed by Peanut```") #TODO
#        return

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
