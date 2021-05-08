# Cakeboi <img src="https://discord.com/assets/41484d92c876f76b20c7f746221e8151.svg" alt="discord_logo" width="50" height="50" />

A **SINoALICE** discord slave for documenting colosseum fights in a Google Sheet

## What does this bot do?

Parses information from discord chat


1. Upload screenshots from discord chat into a Google spreadsheet (`!upload`)
2. Write text information from discord chat into specific cells of the spreadsheet (`!comment`)
3. Differentiate between servers/channels/users and use their respective spreadsheet for commands

## How does it do that?

- Official Discord Python API to access text channels
- Official Google Drive API to load chat attachments into a Google Drive folder
- gspread (python package for simpler Google Sheets API) to write into spreadsheets

## Setup

Contact the owner **Hok#2123** on **Discord**.

- You will need to create a separate channel in your server and ...
- give this bot the necessary permissions for that channel

## Dev Team Notes

- This bot is run by its Owner on [replit](https://replit.com/)
- Services for multiple discord servers run on this single bot instance

* Discord email: colobot@discord-cakeboi-312800.iam.gserviceaccount.com


## To-do
- Missing
    - Remove local files after upload
    - Clear some messages after command
    
- Commands
    - Add user/channel/sheet/drive