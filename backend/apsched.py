from aiogram import Bot


async def send_notification(bot: Bot, chat_id: int, title, room):
    await bot.send_message(chat_id, f'You will have {title} in 15 minutes in {room}')
