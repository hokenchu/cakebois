# Cakeboi

Discord slave

## Notizen

* Discord email: colobot@discord-cakeboi-312800.iam.gserviceaccount.com

## to-do

Was soll der Discord bot machen?

1. Discord Informationen interpretieren
2. Dateien aus Discord in drive hochladen (mit !upload)
3. Informationen die in den Channel gepostet werden in die passenden 
  Zellen auf dem spreadsheet hochladen (mit !entry)
4. Soll jeden Tag den txt-Channel zeitbasierend komplett purgen
5. Je nachdem in welchen txt-Channel (bzw Server) die Daten gepostet werden, soll
  der Bot den dazugehörigen Spreadsheet benutzen
6. Erstellt für jeden txt-Channel einen Ordner im Drive und für jeden Tag einen Ordner für die Info Sammlungen


# structural notes
1. Zuordnung von User - Sheet - Drive - Channel
    2. Specialization SheetUser Class **[almost]**
       - Add "win/lose" and opponent option
    4. Verify user list file
    
2. Missing
    - Remove local files after upload
    - Clear some messages after command
    - GoogleDrive > Folder per channel
    - Remove commands number argument
    - Add Win/Lose/Opponent to !upload
            
2. Commands
    1. Add user/channel/sheet/drive
    2. `...`
    

fix