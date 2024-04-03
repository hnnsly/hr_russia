from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import Command, StateFilter


from bot.bot import router
from storage import keyboards

@router.message(F.text.lower() == "вакансии")
async def send_jobs(message: Message):
    await message.answer(
        text="Вот список вакансий для вас:"
    )