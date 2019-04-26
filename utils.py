import logging
from functools import wraps

from telethon.tl.types import DocumentAttributeFilename, InputPeerUser
from hurry.filesize import size

from settings import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_media_filename(media):
    attrs = media.document.attributes
    for attr in attrs:
        if not isinstance(attr, DocumentAttributeFilename):
            continue
        return attr.file_name


def get_media_filesize(media):
    document = media.document
    return document.size


def private_chat_only(func):
    @wraps(func)
    async def wrapper(event):
        chat = await event.get_input_chat()
        if not isinstance(chat, InputPeerUser):
            logger.debug(f"Chat is not private: {type(chat)}")
            return
        ret = await func(event)
        return ret

    return wrapper


def attachment_required(func):
    @wraps(func)
    async def wrapper(event):
        message = event.message
        if message.media is None or not hasattr(message.media, 'document'):
            logger.debug("Message doesn't contain a file.")
            return
        ret = await func(event)
        return ret

    return wrapper


def with_limited_file_size(MAX_FILE_SIZE: int):
    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(event):
            message = event.message
            file_size = get_media_filesize(message.media)
            if file_size > MAX_FILE_SIZE:
                msg = f"Only image file size under {size(MAX_FILE_SIZE)} will be proccess, {size(file_size)} is too big,"
                logger.info(msg)
                chat = await event.get_input_chat()
                await event.client.send_message(chat, msg, force_document=True)
                return
            ret = await func(event)
            return ret

        return wrapper

    return outer_wrapper
