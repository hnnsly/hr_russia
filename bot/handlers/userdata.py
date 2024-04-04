from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import router
from states.user_data_state import BaseState, Age
from storage import keyboards
from storage.users import UserDB


@router.message(
    StateFilter(None),
    Command("age")
)  # фильтр срабатывает если нету стейта и ввели /age
async def cmd_age(message: Message, state: FSMContext):  # FSMContext это хранилище стейтов
    await message.answer(
        text=f"{message.from_user.first_name}, сколько вам лет?",
        reply_markup=keyboards.age_reply_markup()
    )
    await state.set_state(BaseState.choosing_age)  # устанавливаем стейт выбора возраста


@router.message(
    BaseState.choosing_age,
    F.text == Age.adult
)
async def age_chosen_adult(message: Message, state: FSMContext):
    if UserDB.check_user_existance(message.from_user.username):
        # await state.update_data(chosen_age=message.text.lower()) # засовываем возраст в стейт для доступа в выборе города
        UserDB.change_user_age(message.from_user.username, True)
    else:
        UserDB.add_user(message.from_user.username,True)

    await message.answer(
        text="Отлично, вот вакансии для вас:",
        reply_markup=keyboards.job_adult_reply_markup()
    )
    await state.clear()  # очищаем стейт для дальнейшей работы бота
    # await state.set_state(BaseState.choosing_city) # переводит стейт на выбор города


@router.message(
    BaseState.choosing_age,
    F.text == Age.child
)
async def age_chosen_child(message: Message, state: FSMContext):
    if UserDB.check_user_existance(message.from_user.username):
        # await state.update_data(chosen_age=message.text.lower()) # засовываем возраст в стейт для доступа в выборе города
        UserDB.change_user_age(message.from_user.username, False)
    else:
        UserDB.add_user(message.from_user.username,False)


    await message.answer(
        text="Отлично, вот вакансии для вас:",
        reply_markup=keyboards.job_child_reply_markup()
    )
    await state.clear()  # очищаем стейт для дальнейшей работы бота
    # await state.set_state(BaseState.choosing_city) # переводит стейт на выбор города


@router.message(
    BaseState.choosing_age
)  # если ввели возраст не с кнопок
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
