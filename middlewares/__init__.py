from aiogram import Dispatcher

# from loader import dp
from .throttling import ThrottlingMiddleware


# if __name__ == "middlewares":
#     dp.middleware.setup(ThrottlingMiddleware())


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
