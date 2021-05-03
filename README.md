# Cakeboi

Discord slave

## Notizen

* Discord appID: 837675948349849641
* public key: 9b35b19a640fca258d61c0471f2c8428efb478423db7727f47816e78f01e6641
* Home folder: 1UtB-Xzi8uFV9WP4HQ7laflXXT_bOESXs
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
    1. ~~Base GoogleUser Class~~ **[ok]**
    2. Specialization SheetUser Class **[almost]**
       - Add "win/lose" and opponent option
    3. Specialization DriveUser Class
        - Create folder for "today"
           - ~~Sub folders?~~ nah
        - Fetch screenshots from discord
            1. 2-steps?
                1. Download to tmp folder
                2. (Upload to drive)
            2. File streams? if compatible
        - Upload to drive
            1. Naming collision
            2. meta tags
            3. Retrieve IDs/links
                - pass to object?
                - save locally?
                - direct call to SheetUser? (oof)
    4. Verify user list file
    5. ~~Save locally~~ **[ok]**
  
  
            
2. Commands
    1. Add user/channel/sheet/drive
    2. `...`