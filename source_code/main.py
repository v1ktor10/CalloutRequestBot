import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, INFORG_CHAT_ID
from middleware.group_membership import GroupMembershipMiddleware
from handlers import start, form, confirmation

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

dp.message.middleware(GroupMembershipMiddleware(INFORG_CHAT_ID))
dp.callback_query.middleware(GroupMembershipMiddleware(INFORG_CHAT_ID))

start.register(dp)
form.register(dp)
confirmation.register(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
