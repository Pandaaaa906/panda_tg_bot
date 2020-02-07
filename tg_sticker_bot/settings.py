from socks import SOCKS5
from telethon import TelegramClient
from tg_sticker_bot.secret_settings import api_id, api_hash

client = TelegramClient('tg_bot',
                        api_id=api_id,
                        api_hash=api_hash,
                        proxy=(SOCKS5, 'localhost', 8087),
                        flood_sleep_threshold=20)

APP_NAME = "TG_BOT"

