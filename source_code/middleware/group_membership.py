from aiogram import Bot
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union, Iterable
from aiogram.exceptions import TelegramForbiddenError

class GroupMembershipMiddleware(BaseMiddleware):
    def __init__(self, group_chat_ids: Iterable[int], allowed_commands=None):
        if allowed_commands is None:
            allowed_commands = {None}
        self.group_chat_ids = set(group_chat_ids)
        self.allowed_commands = allowed_commands

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Any],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user

        # Разрешённые команды без проверки членства
        if isinstance(event, Message) and event.text in self.allowed_commands:
            return await handler(event, data)

        bot: Bot = data["bot"]
        for chat_id in self.group_chat_ids:
            try:
                member = await bot.get_chat_member(chat_id=chat_id, user_id=user.id)
                if member.status in {"member", "creator", "administrator"}:
                    return await handler(event, data)
            except TelegramForbiddenError:
                continue  # Бот не имеет прав, но попробуем следующий чат
            except Exception:
                continue  # Пропускаем любые другие ошибки

        await event.answer("🚫 Вы должны быть участником одной из групп: инфоргов или ГКП.")
        return None
