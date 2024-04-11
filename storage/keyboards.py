import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from storage.articles import ArticleDB


def format_keyboard(values):
    values_count = len(values)
    rows_count = math.ceil(values_count/3)

    result = [
        [] for _ in range(rows_count)
    ]

    for i in range(values_count):
        result[int(i//3)].append(
            KeyboardButton(text=values[i])
        )

    return result


def age_reply_markup():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Больше 18"),
             KeyboardButton(text="Меньше 18")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return kb


def job_adult_reply_markup():
    kb = ReplyKeyboardMarkup(
        keyboard=format_keyboard(
            ArticleDB.get_adult_jobs_names()
        ),
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return kb

def all_jobs_reply_markup():
    kb = ReplyKeyboardMarkup(
        keyboard=format_keyboard(
            ArticleDB.get_all_jobs_names()
        ),
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return kb


def job_child_reply_markup():
    kb = ReplyKeyboardMarkup(
        keyboard=format_keyboard(
            ArticleDB.get_child_jobs_names()
        ),
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return kb


def inline_link(name: str, link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, url=link)]
        ]
    )
    return kb


def yes_no_reply_markup():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Да"),
         KeyboardButton(text="Нет")]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return kb


def admin_confirm_keyboard(confirmation_keys):
    kb = ReplyKeyboardMarkup(
        keyboard=format_keyboard(
            confirmation_keys
        ),
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return kb

