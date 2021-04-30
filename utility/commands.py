from utility.files import *


# !help
async def command_help(message):
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
async def command_purge(message):
    args = message.content.split()
    if len(args) > 1 and (args[1] in ["--help", "-h", "?"]):
        await message.channel.send("```Purges the last <n> messages. (Not counting the command itself)"
                                   "\n\nUsage: !purge n```")
        return

    if len(args) != 2 or not args[1].isnumeric():
        await message.channel.send("```Usage: !purge n```")
        return
    await message.channel.purge(limit=int(args[1]) + 1)


# !upload n
async def command_upload(message):
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
        await save_all(msg)