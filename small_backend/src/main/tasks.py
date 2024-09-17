import os
from celery import shared_task
from celery.utils.log import get_task_logger
from aiogram import Bot
from dotenv import load_dotenv
import asyncio


load_dotenv()


logger = get_task_logger(__name__)

API_TOKEN = os.getenv("BOT_API_TOKEN")
bot = Bot(token=API_TOKEN)


# Асинхронная функция отправки сообщения
# Асинхронная функция отправки сообщения
async def send_message_async(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)


# Синхронная задача Celery с ручным управлением event loop
@shared_task
def first_day_send(first_name):
    chat_id = '1035560855'
    text = f"Ваше сообщение пользователю по ID {first_name}"

    # Проверяем, есть ли уже запущенный цикл событий
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Запускаем асинхронную функцию вручную через новый или существующий цикл
    loop.run_until_complete(send_message_async(chat_id, text))

    logger.debug(f"HELLO WORLD FIRST DAY IN SMALL {first_name}")

    return

# async def send_message_async(chat_id, text):
#     await bot.send_message(chat_id=chat_id, text=text)
#
#
# # Асинхронная задача Celery
# @shared_task(bind=True)
# async def first_day_send(self, first_name):
#     chat_id = '1035560855'
#     text = f"Ваше сообщение пользователю по ID {first_name}"
#
#     # Выполняем асинхронную отправку сообщения
#     await send_message_async(chat_id, text)
#
#     logger.debug(f"HELLO WORLD FIRST DAY IN SMALL {first_name}")
