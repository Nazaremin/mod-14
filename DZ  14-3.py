#Задача "Витамины для всех!":

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        ["Рассчитать", "Купить"],
        ["Информация"]
    ]
    keyboard.add(*[types.KeyboardButton(button) for button in buttons])
    keyboard.add(*[types.KeyboardButton(button) for button in buttons[1]])

    await message.answer("Нажмите кнопку 'Рассчитать' для начала расчета калорий.", reply_markup=keyboard)

async def main_menu(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
        types.InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
    ]
    inline_keyboard.add(*buttons)

    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)

async def get_formulas(call: types.CallbackQuery):
    formula = "Базовый обмен веществ (БОЖ) по формуле Миффлина-Сан Жеора:\n" \
              "Для мужчин: БОЖ = 66 + (6.2 * вес в кг) + (12.7 * рост в см) - (6.76 * возраст в годах)\n" \
              "Для женщин: БОЖ = 655 + (4.35 * вес в кг) + (4.7 * рост в см) - (4.7 * возраст в годах)"
    await call.answer()
    await call.message.answer(formula)

async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)

async def set_growth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)

async def set_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['growth'] = message.text
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

async def calculate_bmr(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = message.text

    age = int(data.get('age', 0))
    growth = int(data.get('growth', 0))
    weight = int(data.get('weight', 0))

    basal_metabolic_rate = 66 + (6.2 * weight) + (12.7 * growth) - (6.76 * age)

    await message.answer(f'Норма калорий: {basal_metabolic_rate} ккал в день.',
                         reply_markup=types.ReplyKeyboardRemove())

    await state.finish()

async def info_cmd(message: types.Message):
    await message.answer("Этот бот рассчитывает вашу дневную норму калорий на основе вашего возраста, роста и веса.",
                         reply_markup=types.ReplyKeyboardRemove())

def get_product_inline_keyboard():
    inline_keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Product1', callback_data='product_buying'),
        types.InlineKeyboardButton('Product2', callback_data='product_buying'),
        types.InlineKeyboardButton('Product3', callback_data='product_buying'),
        types.InlineKeyboardButton('Product4', callback_data='product_buying')
    ]
    inline_keyboard.row(*buttons[:2])
    inline_keyboard.row(*buttons[2:])
    return inline_keyboard

async def get_buying_list(message: types.Message):
    for i in range(1, 5):
        product_text = f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}'
        await message.answer(product_text)
        # Assuming you have images for each product, replace 'product_image_<i>.jpg' with actual file paths
        await message.answer_photo(open(f'file/2.jpg', 'rb'))
    await message.answer("Выберите продукт для покупки:", reply_markup=get_product_inline_keyboard())

async def send_confirm_message(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Вы успешно приобрели продукт!")

# Основная функция для запуска бота.
async def main():
    # Инициализируем бота и диспетчер.
    bot = Bot(token='')
    storage = MemoryStorage()

    dp = Dispatcher(bot, storage=storage)

    # Регистрируем обработчики для каждого состояния.

    dp.register_message_handler(start_cmd, commands=['start'], state=None)

    dp.register_message_handler(main_menu, text='Рассчитать', state=None)

    dp.register_callback_query_handler(get_formulas, text='formulas')

    dp.register_callback_query_handler(set_age, text='calories', state=None)

    dp.register_message_handler(set_growth, state=UserState.age)

    dp.register_message_handler(set_weight, state=UserState.growth)

    dp.register_message_handler(calculate_bmr, state=UserState.weight)

    dp.register_message_handler(info_cmd, text='Информация', state=None)

    dp.register_message_handler(get_buying_list, text='Купить', state=None)

    dp.register_callback_query_handler(send_confirm_message, text='product_buying')

    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
