from os import environ

import socks
from telethon import TelegramClient
from secret_settings import api_id, api_hash, bot_token

APP_NAME = "TG_BOT"
PROXY_HOST = environ.get('PROXY_HOST')
PROXY_PORT = int(environ.get('PROXY_PORT'))

proxy = None
if PROXY_HOST:
    proxy = (socks.SOCKS5, PROXY_HOST, PROXY_PORT)

client = TelegramClient('tg_bot',
                        api_id=api_id,
                        api_hash=api_hash,
                        proxy=proxy,
                        flood_sleep_threshold=20).start(bot_token=bot_token)



