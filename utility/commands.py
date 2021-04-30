from utility.files import *


# !help
async def command_help(message):
    commandList = """
    ```
    all commands:
        !command --help
        !command -h
        !command ?
    
    !upload n
    !purge n
    """

    await message.channel.send(commandList)


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
        limit=int(args[1])+1).flatten()

    for msg in latest_messages:
        await save_all(msg)

    # TODO filter older messages

    # for msg in latest_messages:
    #     if msg.content.startswith("Guild:"):  # TODO Voraussetzung
    #         print(">> You fought against ", msg.content.replace('Guild', '').replace(':', ""))  # TODO name filtern
    #
    #     if msg.content in ["win", "victory", "defeat", "lose"]:
    #         print(">> Lul, you ", msg.content)
    #
    #     if len(msg.attachments) > 0:
    #         print(">> ", 'You sent some pictures')
