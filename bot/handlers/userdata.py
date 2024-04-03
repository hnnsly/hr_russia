from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import Command, StateFilter

from bot.bot import router
from storage import keyboards
from states.states import BaseState, Age


@router.message(StateFilter(None), Command("age"))  # фильтр срабатывает если нету стейта и ввели /age
async def cmd_age(message: Message, state: FSMContext):  # FSMContext это хранилище стейтов
    await message.answer(
        text=f"{message.from_user.first_name}, сколько вам лет?",
        reply_markup=keyboards.age()
    )
    await state.set_state(BaseState.choosing_age)  # устанавливаем стейт выбора возраста


@router.message(BaseState.choosing_age, F.text.in_(Age.adult, Age.child))
async def age_chosen(message: Message, state: FSMContext):
    # await state.update_data(chosen_age=message.text.lower()) # засовываем возраст в стейт для доступа в выборе города
    await message.answer(
        text="Отлично, вот вакансии для вас:",
        reply_markup=keyboards.jobs()
    )
    await state.clear()  # очищаем стейт для дальнейшей работы бота
    # await state.set_state(BaseState.choosing_city) # переводит стейт на выбор города


@router.message(BaseState.choosing_age)  # если ввели возраст не с кнопок
async def incorrect_age(message: Message):
    await message.answer(
        text="Выберите из предложенных вариантов:",
        reply_markup=keyboards.age_reply_markup()
    )

# TODO: На случай если все таки сделаем сбор городов
# @router.message(BaseState.choosing_age, F.text.in_(Age.adult, Age.child))
# async def age_chosen(message: Message, state:FSMContext):
#     await state.update_data(chosen_food=message.text.lower())
#     await message.answer(
#         text="Отлично, из какого вы города?"
#     )
#     await state.set_state(BaseState.choosing_city)
#
# @router.message(BaseState.choosing_city)
# async def city_chosen(message: Message, state:FSMContext):
#     age_data = await state.get_data()
#     await message.answer(
#         text=f"Отлично, {message.from_user.first_name}, запомним, что вам {age_data} лет и вы из {message.text}."
#     )
#     await state.clear()
