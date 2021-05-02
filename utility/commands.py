from utility import sheets_api
from utility.file import *


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
async def command_upload(message):
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
        await save_all(msg)


async def command_transfer(message):
    args = message.content.split()
    if len(args) != 2 or not args[1].isnumeric():
        return

    links = []
    latest_messages = await message.channel.history(
        limit=int(args[1]) + 1).flatten()

    for msg in latest_messages:
        for attachment in msg.attachments:
            links.append(attachment.url)

    links.reverse() # reverse order
    print("[Log]", f"Collected {len(links)} links from {len(latest_messages)} messages")
    sheets_api.upload_link_batch(links)
    print("[Log]", f"Transfer complete")
    await message.channel.send(f"Transfer completed (Sent `{len(links)}` attachments)")
