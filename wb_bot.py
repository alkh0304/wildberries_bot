from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import os
from dotenv import load_dotenv
from wb_parser import parse_data
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN')
STARTUP_MSG = (
    'Доброго времени суток! Чтобы узнать, есть ли искомый товар по тому'
    'или иному запросу в поисковой выдаче wildberries, пожалуйста введите'
    'в чат артикул товара и поисковой запрос (пример: 23501578 Омега 3)'
)

storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class WBDialog(StatesGroup):
    moscow_only = State()
    true_address = State()
    goods = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = [
        "С учетом адреса клиента",
        "По Москве"
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(STARTUP_MSG, reply_markup=keyboard)


@dp.message_handler(Text(equals="С учетом адреса клиента"))
async def get_true_address_state(message: types.Message):
    await WBDialog.true_address.set()
    await message.answer(
        "Пожалуйста введите в чат адрес "
        "(пример: Сосновоборск, Улица Энтузиастов 7)"
    )


@dp.message_handler(state=WBDialog.true_address)
async def get_true_address(
    message: types.Message, state: FSMContext
):
    await state.update_data(address=message.text)
    await WBDialog.goods.set()
    await message.answer(
        "Пожалуйста введите в чат поисковой запрос (пример: 87689628 Омега 3)"
    )


@dp.message_handler(state=WBDialog.goods)
async def get_goods_pos(
    message: types.Message, state: FSMContext
):
    await state.update_data(goods=message.text)
    data = await state.get_data()
    await message.answer("Ожидайте, производится парсинг...")
    result = parse_data(data['goods'], data['address'])
    await message.answer(f'{result}')
    await state.finish()
    await message.answer("Чтобы совершить новый запрос нажмите /start")


@dp.message_handler(Text(equals="По Москве"))
async def get_moscow_state(message: types.Message):
    await WBDialog.moscow_only.set()
    await message.answer(
        "Пожалуйста введите в чат поисковой запрос (пример: 87689628 Омега 3)"
    )


@dp.message_handler(state=WBDialog.moscow_only)
async def get_goods_pos_moscow(message: types.Message, state: FSMContext):
    await message.answer("Ожидайте, производится парсинг...")
    result = parse_data(message.text)
    await message.answer(f'{result}')
    await state.finish()
    await message.answer("Чтобы совершить новый запрос нажмите /start")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
