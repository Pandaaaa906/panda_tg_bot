from io import BytesIO
from os.path import splitext

from cv2 import cv2
from telethon import events  # , sync
from telethon.tl.custom import Button
from telethon.utils import is_image

from loguru import logger

from resize_tools import normal_resize, seam_carving_resize
from settings import client
from utils import get_media_filename, private_chat_only, attachment_required, with_limited_file_size, get_sender_info, \
    start_up_msg

logger.add("/logs/sticker_bot.log", rotation="1 week")

help_text = (
    "If you send me an image * **as file** *, "
    "i will convert it to png format and resize into suitable size for telegram sticker."
)

MAX_FILE_SIZE = 8 * 1024 ** 2  # 8MB
NORMAL = b'normal'
SEAM_CARVING = b'seam'


@client.on(events.NewMessage(incoming=True, pattern='/help'))
@logger.catch
async def handle_help(event):
    message = event.message
    await message.reply(help_text)


@client.on(events.NewMessage(incoming=True, pattern='^'))
@logger.catch
@private_chat_only
@attachment_required
@with_limited_file_size(MAX_FILE_SIZE)
async def convert_image_to_sticker(event):
    """if sender is not None:
    Receive image then convert it to png format and resize into suitable size for telegram sticker
    """
    logger.debug("Start working")
    await get_sender_info(event)
    sender = await event.get_sender()
    f = 2 if sender.username == 'Pandaaaa906' else 1
    await event.reply(
        'Pick resize method:',
        buttons=[
                    [Button.inline('Normal(Fast)', NORMAL)],
                    [Button.inline('Seam Carving(Very Slow)', SEAM_CARVING)],
                ][:f]
    )


@client.on(events.CallbackQuery)
@logger.catch
async def handle_callback(event):
    choice = event.data
    msg = await event.get_message()
    sender = await get_sender_info(event)
    message = await msg.get_reply_message()
    # respond = event
    if choice == NORMAL:
        resize_func = normal_resize
    elif choice == SEAM_CARVING:
        resize_func = seam_carving_resize
    else:
        logger.warning(f'Get wrong resize func: {choice} from {sender!r}')
        return

    await event.edit('Request accepted, downloading')

    with BytesIO() as in_f, BytesIO() as out_f:
        success = await client.download_media(message, file=in_f)
        await event.edit('File received, processing')
        if success is None:
            logger.info("Fail to download media")
            return
        in_f.flush()
        in_f.seek(0)
        if not is_image(in_f):
            logger.debug("Media is not image")
            await event.edit('Media is not image')
            return
        in_f.seek(0)

        new_img = resize_func(in_f)

        file_name, ext = splitext(get_media_filename(message.media))
        out_f.name = f"Resized_{file_name}.png"

        is_success, im_buf_arr = cv2.imencode(".png", new_img)
        if not is_success:
            logger.debug("OpenCV can't transform img to bytes")
            return
        out_f.write(im_buf_arr.tobytes())
        out_f.flush()
        out_f.seek(0)

        prompt = f"Sending Resized File:{out_f.name!r}"
        logger.debug(f"{prompt} to {sender!r}")
        await event.edit(text=prompt)
        await message.reply(file=out_f, force_document=True)
        await event.edit("Finished")


if __name__ == '__main__':
    logger.info("Starting Connection")
    with client:
        logger.info("Connection Established")
        client.loop.run_until_complete(start_up_msg(client))
        client.run_until_disconnected()
