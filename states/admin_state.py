from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    admin = State()

    choosing_message_name = State()
    changing_message_content = State()

    choosing_article_name = State()
    choosing_article_is_job = State()
    choosing_article_for_adult = State()
    choosing_article_content = State()
    choosing_article_link = State()

    deleting_article = State()
    agreeing_deleting_article = State()


admins = ("hnnssssssly",)


