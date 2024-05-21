from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from bot.functions import *

basket = RedisDict('temp')
rt = Router()


@rt.message(CommandStart())  # main menu
async def welcome(message: Message):
    global basket
    user_id = message.from_user.id
    basket = await create_basket(user_id)
    await message.answer("Assalomu alaykum! Tanlang.", reply_markup=main_buttons())


@rt.message(Command('help'))
async def help_button(message: Message):
    await message.answer("""Buyruqlar: 
/start - Botni ishga tushirish
/help - Yordam""")


@rt.message(F.text == '📚 Kitoblar')  # menu of category's list
async def categorys_list(message: Message):
    await main_menu_list(message, basket)


@rt.message(F.text == '📃 Mening buyurtmalarim')
async def mening_buyurtmalarim(message: Message):
    await message.answer('🤷‍♂️ Sizda xali buyurtmalar mavjud emas.')


@rt.message(F.text == '🔵 Biz ijtimoiy tarmoqlarda')
async def bizijtimoiy(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='IKAR | Factor Books', url='https://t.me/ikar_factor'))
    ikb.row(InlineKeyboardButton(text='Factor Books', url='https://t.me/factor_books'))
    ikb.row(InlineKeyboardButton(text='"Factor Books" nashriyoti', url='https://t.me/factorbooks'))
    await message.answer('Biz ijtimoiy tarmoqlarda: ', reply_markup=ikb.as_markup())


@rt.message(F.text == "📞 Biz bilan bog'lanish")
async def bilanbog(message: Message):
    text = """Telegram: @sardor_mirzo

📞 + 998937054621

🤖 Bot Mirzoraximov Sardor (@sardor_mirza) tomonidan tayyorlandi"""
    await message.answer(text)