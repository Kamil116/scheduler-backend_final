from aiogram import Bot


async def send_notification(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Message')
