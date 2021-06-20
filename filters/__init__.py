from aiogram import Dispatcher

from .authentication import Authentication, WithoutAuthorization
from .is_admin import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(Authentication)
    dp.filters_factory.bind(WithoutAuthorization)
