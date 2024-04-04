from aiogram import F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import router
from storage.messages import MessageDB


@router.message(
    StateFilter(None)
)
async def incorrect_message(message: Message):
    await message.answer(text=MessageDB.get_message_by_name("нет ответа").content)


