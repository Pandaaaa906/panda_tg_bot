import logging
from io import BytesIO
from os.path import splitext

from telethon import events  # , sync
from PIL import Image
from telethon.utils import is_image
from settings import client, LOGGER_NAME
from utils import get_media_filename, private_chat_only, attachment_required, with_limited_file_size

FORMAT = '%(asctime)-15s %(levelname)s %(funcName)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)


help_text = '''\
If you send me an image, i will convert to png format and resize into suitable size for telegram sticker.
'''

MAX_FILE_SIZE = 8*1024**2  # 8MB


@client.on(events.NewMessage(incoming=True, pattern='/help'))
async def handle_help(event):
    chat = await event.get_input_chat()
    await event.client.send_message(chat, help_text)


@client.on(events.NewMessage(incoming=True, forwards=False))
@private_chat_only
@attachment_required
@with_limited_file_size(MAX_FILE_SIZE)
async def convert_image_to_sticker(event):
    """
    Receive image then convert to png format and resize into suitable size for telegram sticker
    """
    logger.debug("Start working")
    message = event.message
    with BytesIO() as in_f, BytesIO() as out_f:
        success = await client.download_media(event.message, file=in_f)
        if success is None:
            logger.debug("Fail to download media")
            return
        in_f.flush()
        in_f.seek(0)
        if not is_image(in_f):
            logger.debug("Media is not image")
            return
        in_f.seek(0)

        img = Image.open(in_f)
        w, h = img.size
        ratio = w / h
        new_size = w > h and (512, int(512 / ratio)) or (int(512 * ratio), 512)
        new_img = img.resize(new_size, Image.ANTIALIAS)

        file_name, ext = splitext(get_media_filename(message.media))
        out_f.name = f"Resized_{file_name}.png"
        new_img.save(out_f)
        out_f.flush()
        out_f.seek(0)
        chat = await event.get_input_chat()
        logger.debug(f"Sending Resized File:{out_f.name}")
        await event.client.send_file(chat, file=out_f, force_document=True)


if __name__ == '__main__':
    with client:
        logger.info("Starting Connection")
        client.run_until_disconnected()
