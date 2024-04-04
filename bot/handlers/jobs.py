from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message

from bot import router
from storage import keyboards
from storage.articles import ArticleDB
from storage.keyboards import inline_link
from storage.messages import MessageDB
from storage.users import UserDB


@router.message(
    # UserDB.get_user_age(str(F.from_user.username)) == 30 and  # 30 - больше 18 лет

    lambda message: UserDB.get_user_age(message.from_user.username) == 30,
    F.text.lower().in_(("вакансии", "/jobs")),
    StateFilter(None)
)
async def send_adult_jobs(message: Message):
    await message.answer(
        # text="Вот список вакансий для вас:",
        text=MessageDB.get_message_by_name("вакансии от 18").content,
        reply_markup=keyboards.job_adult_reply_markup()
    )


@router.message(
    # UserDB.get_user_age(F.from_user.id) == 20 and  # 20 - меньше 18 лет

    lambda message: UserDB.get_user_age(message.from_user.username) == 20,
    F.text.lower() == "вакансии",
    StateFilter(None)
)
async def send_child_jobs(message: Message):
    await message.answer(
        # text="Вот список вакансий для вас:",
        text=MessageDB.get_message_by_name("вакансии до 18").content,
        reply_markup=keyboards.job_child_reply_markup()
    )


@router.message(
    # UserDB.get_user_age(F.from_user.id) == 30 and
    # F.text.lower() in ArticleDB.get_adult_jobs_names())

    lambda message: UserDB.get_user_age(message.from_user.username) == 30 and message.text.lower() in ArticleDB.get_adult_jobs_names(),
    StateFilter(None)
)
async def send_chosen_adult_job(message: Message):
    response = ArticleDB.get_article_by_name(message.text)
    await message.answer(
        text=response.content,
        reply_markup=inline_link("Cсылка",response.link) if response.link is not None else None
    )


@router.message(
    # UserDB.get_user_age(F.from_user.id) == 30 and
    # F.text.lower() in ArticleDB.get_adult_jobs_names())

    lambda message: UserDB.get_user_age(message.from_user.username) == 20 and message.text.lower() in ArticleDB.get_child_jobs_names(),
    StateFilter(None)
)
async def send_chosen_child_job(message: Message):
    response = ArticleDB.get_article_by_name(message.text.lower())
    await message.answer(
        text=response.content,
        reply_markup=inline_link("Cсылка",response.link) if response.link is not None else None
    )

# @router.message(
#     #UserDB.get_user_age(F.from_user.id) == 20 and
#     #F.text.lower() in ArticleDB.get_adult_jobs_names()
#     StateFilter(None)
# )
# async def send_chosen_child_job(message: Message):
#     await message.answer(text="")
