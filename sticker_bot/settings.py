from os import environ, path

import socks
from telethon import TelegramClient

BASE_DIR = path.dirname(path.abspath(__file__))

APP_NAME = environ.get('APP_NAME') or "STICKER_BOT"
PROXY_HOST = environ.get('PROXY_HOST')
PROXY_PORT = int(environ.get('PROXY_PORT'))

api_id = environ.get('api_id')
api_hash = environ.get('api_hash')
bot_token = environ.get('bot_token')

proxy = None
if PROXY_HOST:
    proxy = (socks.SOCKS5, PROXY_HOST, PROXY_PORT)

client = TelegramClient(path.join(BASE_DIR, 'session', APP_NAME),
                        api_id=api_id,
                        api_hash=api_hash,
                        proxy=proxy,
                        flood_sleep_threshold=20).start(bot_token=bot_token)



