import secrets
from random import Random

from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot import router
from states.admin_state import admin_usernames, AdminState
from states.user_data_state import BaseState, Age
from storage import keyboards, messages
from storage.articles import ArticleDB, Article
from storage.keyboards import format_keyboard
from storage.messages import MessageDB
from storage.users import UserDB

admin_actions = ["добавить пост", "удалить пост", "изменить сообщение"]
messages_names = ["start", "help", "вакансии от 18", "вакансии до 18", "нет ответа", "не найден возраст"]
admin_choose_actions_kb = ReplyKeyboardMarkup(
    keyboard=keyboards.format_keyboard(admin_actions),
    resize_keyboard=True,
    one_time_keyboard=True
)
message_name_kb = ReplyKeyboardMarkup(
    keyboard=keyboards.format_keyboard(messages_names),
    resize_keyboard=True,
    one_time_keyboard=True
)

confirmation_keys = [
    "N13RLgA_Ga3",
    "19875-3175-1935-9731",
    "bljBTLBLJ",
    "V9v977Vp9;P7vfV",
    "-9UV33-3",
    "kgdngksngsnpgndspgs",
    "09mu3V0VMY"
]




@router.message(
    StateFilter(None),
    lambda message: message.from_user.username in admin_usernames,
    Command("admin")
)
async def enter_admin_panel(message: Message, state: FSMContext):
    await message.answer(
        text="вы вошли в админ панель, выберите действие\n"
             "\nСУКА ВНИМАТЕЛЬНО ВВОДИ ЭТУ ХУЙНЮ"
             "\nВНИМАТЕЛЬНО ЗНАЧИТ ВНИМАТЕЛЬНО НАХУЙ"
             "\nза кривой базар и ошибки при использовании я тебе ебало разбью хуесос"
             "\nЕСЛИ ПРОЕБАЛСЯ ТО ПИШИ /exit"
             "\nПРИ ЛЮБОМ ПИЗДЕ ЕСЛИ ЧТО ТО ИДЕТ НЕ ТАК ПИШИ /exit"
             "\nЯ ТЕБЕ НОУТ НАХУЙ СОЖГУ ЕСЛИ ЧТО ТО БУДЕТ НЕ ТАК ТЫ МЕНЯ ПОНЯЛ СУКА"
             "я псих сука",
        reply_markup=admin_choose_actions_kb
    )
    await state.set_state(AdminState.admin)


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    Command("exit")
)
async def exit_admin_panel(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вышли из админ панели."
    )
    await state.clear()


@router.message(
    AdminState.admin,
    lambda message: message.from_user.username in admin_usernames,
    F.text.in_(admin_actions)
)
async def action_chosen(message: Message, state: FSMContext):
    if message.text == admin_actions[0]:
        await state.update_data(action="add_article")
        await message.answer(
            text="Введите НАЗВАНИЕ СУКА НАЗВАНИЕ ПОНИМАЕШЬ нового поста:"
        )
        await state.set_state(AdminState.choosing_article_name)

    elif message.text == admin_actions[1]:
        await state.update_data(action="delete_article")
        await message.answer(
            text="Выберите пост ДЛЯ УДАЛЕНИЕ УДАЛИТЬ ОНО ИСЧЕЗНЕТ",
            reply_markup=keyboards.all_jobs_reply_markup()
        )
        await state.set_state(AdminState.choosing_article_name)

    elif message.text == admin_actions[2]:
        await state.update_data(action="edit_message")
        await state.set_state(AdminState.choosing_message_name)
        await message.answer(
            text="Выберите СООБЩЕНИЕ для редактирования: ",
            reply_markup=message_name_kb
        )

    else:
        await message.answer(
            text=f"ТУПОРЫЛЫЙ ДОЛБАЕБ ПОД НАЗВАНИЕМ{message.from_user.first_name.upper()}\nНЕВЕРНЫЙ ВВОД БЛЯТЬ НА КНОПКИ НАЖИМАЙ НА КЛАВИАТУРЕ",
            reply_markup=admin_choose_actions_kb
        )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.choosing_message_name
)
async def message_name_chosen(message: Message, state: FSMContext):
    if message.text in messages_names:
        await state.update_data(message_name=message.text)
        await state.set_state(AdminState.changing_message_content)
        await message.answer(
            text=f"Выберите новое СОДЕРЖАНИЕ БЛЯТЬ ДЛИННЫЙ ТЕКСТ\nС О Д Е Р Ж А Н И Е'{message.text}':")
    else:
        await message.answer(
            text=f"ТУПОРЫЛЫЙ ДОЛБАЕБ ПОД НАЗВАНИЕМ{message.from_user.first_name.upper()}\nТАКОЙ КНОПКИ НЕ СУЩЕСТВУЕТ\nВНИМАТЕЛЬНЕЕ БЛЯТЬ",
            reply_markup=message_name_kb
        )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.changing_message_content,
)
async def message_content_changed(message: Message, state: FSMContext):
    message_data = await state.get_data()
    MessageDB.change_message(messages.Message(
        message_data["message_name"],
        message.text if message.text != "" else "Пусто")
    )
    await state.clear()
    await message.answer(
        text=f"Успешно! Вы изменили сообщение '{message_data}', новое содержание - '{message.text}'\nВы вышли из админ-панели."
    )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.choosing_article_name,
)
async def article_name_chosen(message: Message, state: FSMContext):
    action = await state.get_data()

    if action["action"] == "delete_article":
        await state.set_state(AdminState.agreeing_deleting_article)

        if message.text in ArticleDB.get_adult_jobs_names() or message.text in ArticleDB.get_child_jobs_names():
            await state.update_data(article_name=message.text)

            confirmation_key = secrets.choice(confirmation_keys)
            await state.update_data(confirmation_key=confirmation_key)

            article_data = ArticleDB.get_article_by_name(message.text)

            await message.answer(
                text=f"ПОСМОТРИ ВНИМАТЕЛЬНО БЛЯТЬ\n"
                     f"В Н И М А Т Е Л Ь Н О\n"
                     f"ИЛИ УМРЕТ ТВОЯ МАМАША ЕБЛИВАЯ\n"
                     f"Вы уверены, что хотите удалить пост \"{message.text}\"?\n"
                     f"Название: {article_data.name}\n"
                     f"Является ли работой: {article_data.is_job}\n"
                     f"для подтверждения нажмите {confirmation_key}"
                     f"Для совершеннолетних: {article_data.for_adult}\n"
                     f"Содержание: {article_data.content}\n"
                     f"Ссылка: {article_data.link if article_data.link is not None else 'пусто'}",
                reply_markup=keyboards.admin_confirm_keyboard(confirmation_keys)
            )
        else:
            await message.answer(
                text="не то название, пиздуй отсюда\nВы вышли из админ-панели."
            )
            await state.clear()
    else:
        if len(message.text) < 42:
            await state.update_data(article_name=message.text)
            await state.set_state(AdminState.choosing_article_is_job)
            await message.answer(
                text="Будет ли появляться пост при выводе клавиатуры вакансий?(/jobs)"
                     "\nЭТО РАБОТА ИЛИ НЕТ?",
                reply_markup=keyboards.yes_no_reply_markup()
            )
        else:
            await message.answer(text="ТУПОРЫЛЫЙ ЕБАНАТ НАЗВАНИЕ СКАЗАЛИ БЛЯТЬ")


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.choosing_article_is_job
)
async def article_is_job_chosen(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.update_data(article_is_job=True)
        await state.set_state(AdminState.choosing_article_for_adult)

        await message.answer(
            text="Пост для совершеннолетних? (будет показываться только пользователям, указавшим возраст больше 18)"
                 "\nДЛЯ ВЗРОСЛЫХ ИЛИ НЕТ",
            reply_markup=keyboards.yes_no_reply_markup()
        )
    elif message.text.lower() == "нет":
        await state.update_data(article_is_job=False)
        await state.set_state(AdminState.choosing_article_for_adult)

        await message.answer(
            text="Пост для совершеннолетних? (будет показываться только пользователям, указавшим возраст больше 18)"
                 "\nДЛЯ ВЗРОСЛЫХ ИЛИ НЕТ",
            reply_markup=keyboards.yes_no_reply_markup()
        )
    else:
        await message.answer(
            text=f"ТУПОРЫЛЫЙ ДОЛБАЕБ ПОД НАЗВАНИЕМ{message.from_user.first_name.upper()}\nНеверный ввод, попробуйте ещё раз.",
            reply_markup=keyboards.yes_no_reply_markup()
        )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.choosing_article_for_adult
)
async def article_for_adult_chosen(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.update_data(article_for_adult=True)
        await state.set_state(AdminState.choosing_article_content)
        await message.answer(
            text="Введи СОДЕРЖАНИЕ СУКА\nС О Д Е Р Ж А Н И Е поста (то что будет показываться если его вызвать)"
        )
    elif message.text.lower() == "нет":
        await state.update_data(article_for_adult=False)
        await state.set_state(AdminState.choosing_article_content)
        await message.answer(
            text="Введи СОДЕРЖАНИЕ СУКА\nС О Д Е Р Ж А Н И Е поста (то что будет показываться если его вызвать)"
        )
    else:
        await message.answer(
            text=f"ТУПОРЫЛЫЙ ДОЛБАЕБ ПОД НАЗВАНИЕМ{message.from_user.first_name.upper()}\nНеверный ввод, попробуйте ещё раз.",
            reply_markup=keyboards.yes_no_reply_markup()
        )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.choosing_article_content
)
async def article_content_chosen(message: Message, state: FSMContext):
    await state.update_data(article_content=message.text)
    await state.set_state(AdminState.confirming_article_content)
    await message.answer(
        text="Ты уверен что это правильное содержание?",
        reply_markup=keyboards.yes_no_reply_markup()
    )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.confirming_article_content
)
async def article_content_confirmed(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.answer(
            text="отлично молодец возьми с полки огурец\nВыберите ссылку, кнопка с которой будет под постом (ВВЕДИТЕ НЕТ ЕСЛИ ССЫЛКИ НЕТУ)"
        )
        await state.set_state(AdminState.choosing_article_link)
    else:
        await message.answer(
            text="я не понял че ты там нахуй промямлил так что пиздуй из админ панели\nВы вышли из админ-панели."
        )
        await state.clear()


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.choosing_article_link
)
async def article_link_chosen(message: Message, state: FSMContext):
    await state.update_data(article_link=message.text if message.text.lower() != "нет" else "")

    art = await state.get_data()
    await state.set_state(AdminState.confirming_final_article)

    confirmation_key = secrets.choice(confirmation_keys)
    await state.update_data(confirmation_key=confirmation_key)

    await message.answer(
        text=f"Вы уверены в том, что сделали все правильно и хотите это добавить?\n"
             f"Название - '{art['article_name']}'\n"
             f"Является ли работой - '{art['article_is_job']}'\n"
             f"чтобы подтвердить, нажмите {confirmation_key} на клавиатуре\n"
             f"Для совершеннолетних - '{art['article_for_adult']}'\n"
             f"Содержание - '{art['article_content']}'"
             f"Ссылка - '{art['article_link']}'",
        reply_markup=keyboards.admin_confirm_keyboard(confirmation_keys)
    )


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.confirming_final_article
)
async def article_confirmed(message:Message, state:FSMContext):
    article_data = await state.get_data()
    confirmation_key = article_data['confirmation_key']
    if message.text == confirmation_key:
        await message.answer("малаца, добавил твою хуйню, ищи себя в /jobs\nВы вышли из админ-панели")
        complete_article = Article(name=article_data["article_name"],
                                   is_job=article_data["article_is_job"],
                                   for_adult=article_data["article_for_adult"],
                                   content=article_data["article_content"],
                                   link=article_data["article_link"]
                                   )
        ArticleDB.add_article(complete_article)
    else:
        await message.answer("пиздуй нахуй отсюда, внимательнее блять надо\nВы вышли из админ-панели.")
    await state.clear()


@router.message(
    lambda message: message.from_user.username in admin_usernames,
    AdminState.agreeing_deleting_article
)
async def delete_article(message: Message, state: FSMContext):

    article_name_and_confirm_data = await state.get_data()
    article_name = article_name_and_confirm_data["article_name"]
    confirmation_key = article_name_and_confirm_data["confirmation_key"]

    if message.text == confirmation_key:
        ArticleDB.delete_article_by_name(article_name)
        await message.answer(f"Пост \"{article_name}\" был удалён.\nВы вышли из админ-панели.")
        await state.clear()
    else:
        await message.answer(f"пиздуй нахуй отсюда, внимательнее блять надо быть\nВы вышли из админ-панели.")
        await state.clear()
