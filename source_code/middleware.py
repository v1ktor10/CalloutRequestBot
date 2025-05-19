from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union
from aiogram.exceptions import TelegramForbiddenError

class GroupMembershipMiddleware(BaseMiddleware):
    def __init__(self, group_chat_id: int, allowed_commands=None):
        if allowed_commands is None:
            allowed_commands = {None}
        self.group_chat_id = group_chat_id
        self.allowed_commands = allowed_commands

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Any],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user

        if isinstance(event, Message) and event.text in self.allowed_commands:
            return await handler(event, data)

        try:
            bot = data["bot"]
            member = await bot.get_chat_member(chat_id=self.group_chat_id, user_id=user.id)
            if member.status not in {"member", "creator", "administrator"}:
                await event.answer("🚫 Вы должны быть участником группы инфоргов.")
                return
        except TelegramForbiddenError:
            await event.answer("🚫 Бот не имеет прав на проверку группы.")
            return
        except Exception as e:
            await event.answer(f"⚠️ Ошибка при проверке группы: {e}")
            return

        return await handler(event, data)
