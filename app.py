import os
import django

from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    # Устанавливаем дефолтные команды
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify

    # Уведомляет про запуск
    # await on_startup_notify(dp)
    await set_default_commands(dp)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.telega_bot.telega_bot.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()

    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
