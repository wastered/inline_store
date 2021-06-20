from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import channel
from utils.db_api.commands import select_user
from utils.misc import subscription


class Authentication(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return True if await select_user(message.from_user.id) is not None else False


class WithoutAuthorization(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return True if await select_user(message.from_user.id) is None else False
