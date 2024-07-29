import logging
from telethon import TelegramClient
from deep_translator import GoogleTranslator
from telethon.tl.functions.messages import GetHistoryRequest

# Настройки
API_ID = 'api_id'
API_HASH = 'api_hash'
PHONE = '+'
SOURCE_CHANNEL = '@'  # ID канала с новостями
TARGET_CHANNEL = '@'  # ID канала для публикации переведенных новостей
TRANSLATE_LANG = 'en'

logging.basicConfig(level=logging.INFO)

client = TelegramClient('session_name', API_ID, API_HASH)

async def fetch_last_post(channel):
    try:
        messages = await client.get_messages(channel, limit=1)
        if messages:
            return messages[0]
    except Exception as e:
        logging.error(f"Error receiving messages from channel: {e}")

async def translate_text(text, target_lang):
    try:
        translator = GoogleTranslator(target=target_lang)
        return translator.translate(text)
    except Exception as e:
        logging.error(f"Error when translating text: {e}")

async def main():
    await client.start(PHONE)
    last_post = await fetch_last_post(SOURCE_CHANNEL)
    if last_post:
        if last_post.text:
            translated_text = await translate_text(last_post.text, TRANSLATE_LANG)
            await client.send_message(TARGET_CHANNEL, translated_text)
            logging.info("The news has been successfully translated and published!")
        else:
            logging.info("The last message contains no text.")
    else:
        logging.info("Couldn't find the latest news.")

if __name__ == '__main__':
    client.loop.run_until_complete(main())