from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.database import get_categories_all_pc, get_category_pc, get_categories_all_crypto, get_categories_crypto

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рынок криптовалюты')],
                                     [KeyboardButton(text='Мои компы')],
                                     [KeyboardButton(text='Магазин компов'),
                                      KeyboardButton(text='Мой профиль')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

buy1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Купить/Продать')]])

buy = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Купить'),
                                    KeyboardButton(text='Продать')],
                                    [KeyboardButton(text='Обновить цену')]],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите действие...')
                                    
async def categories():
    all_categories = await get_categories_all_pc()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def pcs(category_id):
    all_pcs = await get_category_pc(category_id)
    keyboard = InlineKeyboardBuilder()
    for pc in all_pcs:
        keyboard.add(InlineKeyboardButton(text=pc.name, callback_data=f"item_{pc.id}"))
    return keyboard.adjust(2).as_markup()

async def categories_crypto():
    all_categories = await get_categories_all_crypto()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"cryptocategory_{category.id}"))
    return keyboard.adjust(2).as_markup()

async def cryptos(crypto_catigory_id):
    all_crypts = await get_categories_crypto(crypto_catigory_id)
    keyboard = InlineKeyboardBuilder()
    for crypto in all_crypts:
        keyboard.add(InlineKeyboardButton(text=crypto.name, callback_data=f"crypto_{crypto.id}"))
    return keyboard.adjust(2).as_markup()