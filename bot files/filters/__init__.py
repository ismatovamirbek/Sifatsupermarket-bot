from aiogram import Dispatcher

from loader import dp
from .group_filter import IsGroup
from .private_filter import IsPrivate


if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
