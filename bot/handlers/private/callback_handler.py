from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton

from bot.functions import books_list, book_data, book_inline_buttons, main_menu_list, basket_data, basket_buttons
from bot.handlers.private.main_handler import basket
from db import Product, Category
from db.models.order import Order

cbrt = Router()


@cbrt.callback_query(F.data.startswith('category_'))  # menu of books' list
async def category_books_list(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    category_name = (await Category().get(category_id)).name
    books = (await Product().get_products_by_category_id(category_id))
    ikb = books_list(books)
    if basket:
        count = len(basket)
        ikb.row(InlineKeyboardButton(text=f'Savat({count})', callback_data='savat'))
    try:
        await callback.message.edit_text(f'{category_name}', reply_markup=ikb.as_markup())
    except:
        await callback.message.answer(f'{category_name}', reply_markup=ikb.as_markup())


@cbrt.callback_query(F.data.startswith('booksave_'))  # book information
async def save_book(callback: CallbackQuery):
    await callback.message.delete()
    book_id = int(callback.data.split('booksave_')[-1])
    data = await Product().get(book_id)
    count = 1
    text = book_data(data)
    ikb = book_inline_buttons(count, data.category_id, data.id)  # category_id book_id
    await callback.message.answer_photo(f'{data.photo}', caption=text, reply_markup=ikb.as_markup())


@cbrt.callback_query(F.data == 'back_to_category')  # return to menu of category's list
async def back_to_list(callback: CallbackQuery):
    await main_menu_list(callback, basket)


@cbrt.callback_query(F.data.startswith('-1_') | F.data.startswith('1_'))  # change count of books before buying
async def back_to_list(callback: CallbackQuery):
    callback_data = callback.data.split('_')
    book_id = int(callback_data[-1])
    data = await Product().get(book_id)
    count = int(callback_data[1])
    diff = int(callback_data[0])
    if count + diff >= 1:
        count += diff
    else:
        count = 1
    ikb = book_inline_buttons(count, data.category_id, data.id)  # category_id book_id
    ch_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.bot.edit_message_reply_markup(chat_id=ch_id, message_id=message_id, reply_markup=ikb.as_markup())


@cbrt.callback_query(F.data.startswith('savatkaqushish_'))
async def add_to_savat(callback: CallbackQuery):
    await callback.message.delete()
    data = callback.data.split('_')
    count = int(data[-1])
    book_id = int(data[1])
    data = await Product().get(book_id)
    if str(book_id) not in basket.keys():
        basket[str(book_id)] = {"title": data.name.strip(), "price": data.price, "count": count}
    else:
        basket[str(book_id)]['count'] += count
    await main_menu_list(callback, basket, edit=False)


@cbrt.callback_query(F.data == 'savat')
async def savat_information(callback: CallbackQuery):
    text = await basket_data(basket)
    ikb = basket_buttons()
    await callback.message.edit_text(text, reply_markup=ikb.as_markup())


@cbrt.callback_query(F.data == 'delete_savat')
async def delete_savat(callback: CallbackQuery):
    await callback.message.delete()
    basket.clear()
    await main_menu_list(callback, basket, edit=False)


@cbrt.callback_query(F.data == 'make_order')
async def make_order(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.message.from_user.id
    for book_id, book in basket.items():
        await Order.create(user_id=user_id, product_id=int(book_id), count=int(book['count']))
    basket.clear()
    await callback.answer('Zakaz qabul qilindi')
    await main_menu_list(callback, basket, edit=False)
