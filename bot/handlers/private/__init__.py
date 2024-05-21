from aiogram import Router

from bot.handlers.private.callback_handler import cbrt
from bot.handlers.private.main_handler import rt

private_handler_router = Router()

private_handler_router.include_routers(
    cbrt,
    rt
)
