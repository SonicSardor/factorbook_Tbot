from aiogram.types import KeyboardButton, InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from db import Category


def main_buttons():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text='📚 Kitoblar'))
    rkb.add(KeyboardButton(text='📃 Mening buyurtmalarim'))
    rkb.add(KeyboardButton(text='🔵 Biz ijtimoiy tarmoqlarda'))
    rkb.add(KeyboardButton(text="📞 Biz bilan bog'lanish"))
    rkb.adjust(1, 1, 2)
    return rkb.as_markup(resize_keyboard=True)


def books_list(books):
    ikb = InlineKeyboardBuilder()
    for book in books:
        bid = book.id
        name = book.name.strip()
        ikb.add(InlineKeyboardButton(text=f"{name}", callback_data=f"booksave_{bid}"))
    ikb.add(InlineKeyboardButton(text='🔍Qidirsh', callback_data='search'))
    ikb.add(InlineKeyboardButton(text="Orqaga", callback_data='back_to_category'))
    ikb.adjust(2, repeat=True)
    return ikb


def category_list(categories):
    ikb = InlineKeyboardBuilder()
    for category in categories:
        cid = category.id
        name = category.name.strip()
        ikb.add(InlineKeyboardButton(text=f"{name}", callback_data=f"category_{cid}_{name}"))
    ikb.add(InlineKeyboardButton(text='🔍Qidirsh', callback_data='search'))
    ikb.adjust(2, repeat=True)
    return ikb


def book_inline_buttons(count, category_id, book_id):
    ibk = InlineKeyboardBuilder()
    ibk.add(InlineKeyboardButton(text='➖', callback_data=f'-1_{count}_{book_id}'))
    ibk.add(InlineKeyboardButton(text=f'{count}', callback_data='nothing'))
    ibk.add(InlineKeyboardButton(text='➕', callback_data=f'1_{count}_{book_id}'))
    ibk.add(InlineKeyboardButton(text='🔙Orqaga', callback_data=f'category_{category_id}'))
    ibk.add(InlineKeyboardButton(text="🛒Savatka qushish", callback_data=f"savatkaqushish_{book_id}_{count}"))
    ibk.adjust(3, 2)
    return ibk


def basket_buttons():
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text="❌ Savatni tozalash", callback_data='delete_savat'),
            InlineKeyboardButton(text="✅ Buyurtmani tasdiqlash", callback_data='make_order'),
            InlineKeyboardButton(text='⬅ Orqaga', callback_data='back_to_category'))
    ikb.adjust(1, repeat=True)
    return ikb


async def main_menu_list(message: Message | CallbackQuery, basket, edit=True):
    categories = await Category().get_all()
    ikb = category_list(categories)
    if basket:
        count = len(basket.keys())
        ikb.row(InlineKeyboardButton(text=f'🛒Savat ({count})', callback_data='savat'))
    if isinstance(message, Message):
        await message.answer('kategoriyalardan birini tanlang:', reply_markup=ikb.as_markup())
    elif isinstance(message, CallbackQuery) and edit:
        await message.message.edit_text('kategoriyalardan birini tanlang:', reply_markup=ikb.as_markup())
    else:
        await message.message.answer('kategoriyalardan birini tanlang:', reply_markup=ikb.as_markup())
