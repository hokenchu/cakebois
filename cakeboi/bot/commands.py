import discord

from cakeboi.util.common import local
from cakeboi.util.drive.helper import DriveUser
from cakeboi.util.sheets.helper import SheetsUser, today_string

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


async def purge(message):
    """
    !purge n

    Purges last n+1 messages (purge command counts as 1 message too)
    """

    # Interpret each 'word' of the message as an argument
    args = message.content.split()

    # !purge all
    if (args[1]) == "all":
        await message.channel.purge(limit=1000)
        return

    # !purge --help
    if len(args) > 1 and (args[1] in ["--help", "-h", "?"]):
        await message.channel.send("```Purges the last <n> messages. (Not counting the command itself)"
                                   "\n\nUsage: !purge n"
                                   "\nAlternative: !purge all (this clears the whole channel)```")
        return

    # React to incorrect use of !purge
    if len(args) != 2 or not args[1].isnumeric():
        await message.channel.send("```Usage: !purge n```")
        return

    # Do the purging
    await message.channel.purge(limit=int(args[1]) + 1)


# !upload n
async def upload(message):
    """
    Uploads recent message attachments to the drive
    """
    # Interpret each 'word' in the message as an argument
    args = message.content.split()

    # Show help
    if len(args) == 1 or (args[1] in ["--help", "-h", "?"]):
        await message.channel.send("```Uploads the last 10 screenshots (entries) "
                                   "\nto the gdrive and sorts guildname+results+screenshots into the spreadsheet"
                                   "\n\nUsage: !upload guildname result"
                                   "\n\nExample: !upload Peanut Win```")
        return

    # Login as google sheet user
    sheets_user = SheetsUser(channel_id=message.channel.id)

    # Set win/lose in sheet
    if args[-1] in ["Lose", "lose", "Defeat", "defeat"]:
        sheets_user.set_outcome("Lose")
    elif args[-1] in ["Win", "win", "Victory", "victory"]:
        sheets_user.set_outcome("Win")
    else:
        await message.channel.send("Missing battle outcome! (win/lose)"
                                   "\n\n```Example: !upload Peanut Win```"
                                   "\n\n(*Delete this + the wrong upload "
                                   "command message before you use !upload again)*")
        return

    # Set enemy guild name in sheet
    separator = ' '
    guild_name = separator.join(args[1:-1])
    sheets_user.set_guildname(guild_name)

    # Histories are sorted by latest first.
    # Reverse that for the correct chronological order
    hist = await message.channel.history(limit=10).flatten()
    hist.reverse()

    # Make a list of all recent attachments
    all_attachments = []
    for msg in hist:
        for att in msg.attachments:
            all_attachments.append(att)
            print(att)

    # Clear local tmp folder before download
    local.empty_tmp()

    # list of (soon to be) local files
    # pass this to google drive user
    all_files = []

    # Downloads 9 most recent attachments to local folder
    for (index, att) in enumerate(all_attachments[-9:], start=1):
        file_name = message.channel.name + f"{index}"  # Create correct file path
        file = await local.save(att, file_name, message.channel)  # Saves file
        all_files.append(file)  # Takes note of the path for later upload

    # Confirmation message in channel
    await message.channel.send(f"Saved {len(all_files)} files locally")

    drive_user = DriveUser(channel_id=message.channel.id)

    # creates new folder for that day and saves reference
    folder = drive_user.create_folder()

    # clears folder of any residual files
    drive_user.clear_folder(folder["id"])

    # Upload list of files
    # Receives list of google drive file references
    file_list = drive_user.upload(path_list=all_files, parent_id=folder['id'])

    # Confirmation message in channel
    await message.channel.send(f"Uploaded {len(all_files)} files to {folder['name']}")

    # Translates list of google drive files to embedded image links
    link_list = []
    for f in file_list:
        link_list.append(f"https://drive.google.com/uc?export=view&id={f['id']}")

    # Uploads image links to google spread sheet
    sheets_user = SheetsUser(channel_id=message.channel.id)
    sheets_user.upload(list_of_links=link_list)

    # Confirmation message in channel
    await message.channel.send(f"Sent {len(link_list)} images to {sheets_user.sheet_id}")
    return  # End


async def comment(message):
    """
    Posts comment to google sheet
    """
    # Interpret each 'word' in the message as an argument
    args = message.content.split()

    if len(args) == 1 or (args[1] in ["--help", "-h", "?"]):
        await message.channel.send("```Adds a text to the comment section of the spreadsheet "
                                   "\n\nUsage: !comment *text*"
                                   "\n\nExample: !comment We got lubed by Peanut```")
        return

    # takes the text after the (index8) 9th character => text after "!comment "
    text = message.content
    text = text[9:]

    # Confirmation message
    await message.channel.send("Comment for the **" + today_string() + "**" + " will be " + "\"" + text + "\"")

    # Logs into google sheets user and posts comment
    sheets_user = SheetsUser(channel_id=message.channel.id)
    sheets_user.comment(text)
    return


async def waifu(message):
    # Fun
    await message.channel.send(file=discord.File(r"../waifus/waifu.png"))


async def prefix(message):
    # Sets a new prefix
    global __PREFIX
    if len(message.content.split()) == 2:
        __PREFIX = message.content.split()[1]
        await message.channel.send(f"Prefix changed to `{__PREFIX}`")
    else:
        await message.channel.send(f"`Current prefix is `{__PREFIX}`")
    return


def get_prefix():
    # Returns the current prefix
    return __PREFIX
