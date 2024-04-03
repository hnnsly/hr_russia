import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import Command, StateFilter
from storage import keyboards
from states.states import BaseState

bot = Bot(os.getenv('BOT_TOKEN'))
router = Dispatcher()
