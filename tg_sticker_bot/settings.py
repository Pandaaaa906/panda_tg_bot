import socks
from telethon import TelegramClient
from secret_settings import api_id, api_hash, bot_token

client = TelegramClient('tg_bot',
                        api_id=api_id,
                        api_hash=api_hash,
                        proxy=(socks.SOCKS5, 'host.docker.internal', 8087),
                        flood_sleep_threshold=20).start(bot_token=bot_token)

APP_NAME = "TG_BOT"

