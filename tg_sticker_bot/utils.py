import re
from functools import wraps

from telethon.tl.types import DocumentAttributeFilename, User, InputPeerUser
from hurry.filesize import size

import logging
from settings import APP_NAME

logger = logging.getLogger(APP_NAME)


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


def with_limited_file_size(max_file_size: int):
    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(event):
            message = event.message
            file_size = get_media_filesize(message.media)
            if file_size > max_file_size:
                msg = f"Only image file size under {size(max_file_size)} will be process, {size(file_size)} is too big."
                logger.info(msg)
                chat = await event.get_input_chat()
                await event.client.send_message(chat, msg, force_document=True)
                return
            ret = await func(event)
            return ret

        return wrapper

    return outer_wrapper


def involved_only(func):
    @wraps(func)
    async def wrapper(event):
        client = event.client
        me = await client.get_me()
        if re.match(f"@{me.username}", event.text) is None:
            logger.debug("Not involved.")
            return
        ret = await func(event)
        return ret

    return wrapper


def dont_reply_myself(func):
    @wraps(func)
    async def wrapper(event):
        me = await event.client.get_me()
        if event.sender.id == me.id:
            return
        ret = await func(event)
        return ret

    return wrapper


async def get_sender_info(event):
    sender = await event.get_sender()
    if sender is None:
        return
    full_name = ' '.join(filter(lambda x: x, (sender.first_name, sender.last_name)))
    return f'{sender.id}:{sender.username}{f"({full_name})" if full_name else ""}'
