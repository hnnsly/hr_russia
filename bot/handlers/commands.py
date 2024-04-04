from aiogram import F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import router
from storage.messages import MessageDB


@router.message(
    Command("start"),
    StateFilter(None)
)
async def start(message: Message):
    await message.answer(text=MessageDB.get_message_by_name("start").content)


@router.message(
    Command("help")
)
async def start(message: Message, state: FSMContext):
    await message.answer(text=MessageDB.get_message_by_name("help").content)
    await state.clear()

