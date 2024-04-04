from aiogram.fsm.state import StatesGroup, State


class BaseState(StatesGroup):
    choosing_age = State()
    choosing_city = State()


class Age:
    adult = "Больше 18"
    child = "Меньше 18"
