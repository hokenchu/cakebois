async def on_message(message):
    if message.content.startswith('gib img'):
        imgList = os.listdir('../imagesdb')  # Creates a list of filenames from your folder
        imgString = random.choice(imgList)
        path = "../imagesdb/" + imgString
        # Creates a string for the path to the file
        await client.send_file(message.channel, path)
