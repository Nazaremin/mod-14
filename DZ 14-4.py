from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton(text='Рассчитать'))
main_menu_keyboard.add(KeyboardButton(text='Информация'))
main_menu_keyboard.add(KeyboardButton(text='Купить'))

calories_inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
calories_inline_keyboard.add(button_calories)
calories_inline_keyboard.add(button_formulas)

products_inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
products = get_all_products()
for product in products:
    button = InlineKeyboardButton(text=product[1], callback_data=f'product_buying_{product}')
    products_inline_keyboard.add(button)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


initiate_db()
get_all_products()
products = get_all_products()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup=main_menu_keyboard)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=calories_inline_keyboard)


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Привет, я бот помогающий твоему здоровью Этот бот рассчитывает вашу дневную норму калорий на основе вашего возраста, роста и веса.')


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for product in products:
        id_, title, description, price = product
        img_path = f'image_file/{id_}.jpg'
        with open(f'{img_path}', 'rb') as img:
            await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}p')
    await message.answer('Выберите продукт для покупки:', reply_markup=products_inline_keyboard)


@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith('product_buying'))
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша дневная норма калорий: {calories} ккал")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
