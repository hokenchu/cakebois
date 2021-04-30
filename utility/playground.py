async def my_function(message):
    print("content", message.content)
    print(message.attachments)
    for attachment in message.attachments:
        await attachment.save(attachment.filename)


image_types = ["png", "jpeg", "gif", "jpg"]

#    for attachment in message.attachments:
#        if any(attachment.filename.lower().endswith(image) for image in image_types):
#            await attachment.save(attachment.filename)


if __name__ == '__main__':
    print("HERRO WARUDO")
