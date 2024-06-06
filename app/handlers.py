from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from random import randint

import app.keyboards as kb
import app.database.database as db

router = Router()

class Crypto(StatesGroup):
    bitcoin = State()
    memcoin = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.set_user(message.from_user.id)
    await db.create_user_table(tg_id=message.from_user.id)
    await message.answer('Добро пожаловать в майнинг симулятор!', reply_markup=kb.main)


@router.message(F.text == 'Магазин компов')
async def catalog(message: Message):
    await message.answer('Выберите категорию компьютера', reply_markup=await kb.categories())
    

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.pcs(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('pc_'))
async def category(callback: CallbackQuery):
    pc_data = await db.get_pc(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {pc_data.name}\nОписание: {pc_data.description}\nЦена: {pc_data.price}$')

@router.message(F.text == 'Рынок криптовалюты')
async def crypto_catalog(message: Message):
    await message.answer('Выберите категорию крипты', reply_markup=await kb.categories_crypto())

@router.callback_query(F.data.startswith('cryptocategory_'))
async def crypto_category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.cryptos(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('crypto_'))
async def crypto_category(callback: CallbackQuery, state: FSMContext):
    crypto_data = await db.get_crypto(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {crypto_data.name}\nЦена: {crypto_data.price}$', kb.buy1)


@router.message(F.text == "Купить/Продать")
async def start_bot(message: Message, state: FSMContext):
    await message.answer('Запускаем рынок...')
    coin_price = await db.get_crypto(crypto_id=1)
    await message.answer(f'Цена одного биткоина состовляет:{coin_price.price}', reply_markup = kb.buy)
    await state.set_state(Crypto.bitcoin)


@router.message(Crypto.bitcoin)
async def process_login(message: Message, state: FSMContext) -> None:
    if message.text == "Отмена":
        await message.answer("Покупака отменена", reply_markup=kb.main)
        await state.clear()
    elif message.text == 'Обновить цену':
        coin_price = await db.get_crypto(crypto_id=1)
        update = randint(-10000, 10000)
        coin_price = update + int(coin_price.price)
        await db.update_crypto_price(crypto_id=1, new_price=coin_price)
        await message.answer(f'Цена одного биткоина состовляет:{coin_price}', reply_markup = kb.buy)


