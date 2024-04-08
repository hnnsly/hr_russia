from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot import router
from states.admin_state import admins, AdminState
from states.user_data_state import BaseState, Age
from storage import keyboards, messages
from storage.articles import ArticleDB, Article
from storage.messages import MessageDB
from storage.users import UserDB

admin_actions = ["добавить пост", "удалить пост", "изменить сообщение"]
messages_names = ["start", "help", "вакансии от 18", "вакансии до 18", "нет ответа","не найден возраст"]
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


@router.message(
    StateFilter(None),
    lambda message: message.from_user.username in admins,
    Command("admin")
)
async def enter_admin_panel(message: Message, state: FSMContext):
    await message.answer(
        text="вы вошли в админ панель, выберите действие\nи сука не пытайся проверить ее на ошибки, я узнаю это и сломаю тебе ебло, я не делал в каждом действии проверку на еблана, поэтому если ты решишь по приколу хуйнуть куда то пустое сообщение, твой ноут взорвется к хуям, понял меня блять?\nя псих сука",
        reply_markup=admin_choose_actions_kb
    )
    await state.set_state(AdminState.admin)


@router.message(
    lambda message: message.from_user.username in admins,
    Command("admin")
)
async def exit_admin_panel(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вышли из админ панели.",
        reply_markup=admin_choose_actions_kb
    )
    await state.clear()




@router.message(
    AdminState.admin,
    F.text.in_(admin_actions)
)
async def action_chosen(message: Message, state: FSMContext):
    if message.text == admin_actions[0]:
        await state.update_data(action="add_article")
        await message.answer(
            text="Введите название нового поста:"
        )
        await state.set_state(AdminState.choosing_article_name)

    elif message.text == admin_actions[1]:
        await state.update_data(action="delete_article")
        await message.answer(
            text="Выберите пост для удаления",
            reply_markup=keyboards.all_jobs_reply_markup()
        )
        await state.set_state(AdminState.choosing_article_name)

    elif message.text == admin_actions[2]:
        await state.update_data(action="edit_message")
        await state.set_state(AdminState.choosing_message_name)
        await message.answer(
            text="Выберите сообщение для редактирования: ",
            reply_markup=message_name_kb
        )

    else:
        await message.answer(
            text="Неверный ввод, используйте клавиатуру",
            reply_markup=admin_choose_actions_kb
        )


@router.message(
    AdminState.choosing_message_name,
)
async def message_name_chosen(message: Message, state: FSMContext):
    if message.text in messages_names:
        await state.update_data(message_name=message.text)
        await state.set_state(AdminState.changing_message_content)
        await message.answer(text="Выберите новое содержание:")
    else:
        await message.answer(
            text="Такой кнопки не существует. Попробуйте еще раз.",
            reply_markup=message_name_kb
        )


@router.message(
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
        text="Успешно! Вы вышли из админ-панели."
    )


@router.message(
    AdminState.choosing_article_name,
)
async def article_name_chosen(message: Message, state: FSMContext):
    action = await state.get_data()
    if action["action"] == "delete_article":
        await state.set_state(AdminState.agreeing_deleting_article)
        await state.update_data(article_name=message.text)
        article_data = ArticleDB.get_article_by_name(message.text)
        await message.answer(
            text=f"Вы уверены, что хотите удалить пост \"{message.text}\"?\n"
                 f"Название: {article_data.name}\n"
                 f"Является ли работой: {article_data.is_job}\n"
                 f"Для совершеннолетних: {article_data.for_adult}\n"
                 f"Содержание: {article_data.content}\n"
                 f"Ссылка: {article_data.link if article_data.link is not None else 'пусто'}",
            reply_markup=keyboards.yes_no_reply_markup()
        )
    else:
        await state.update_data(article_name=message.text)
        await state.set_state(AdminState.choosing_article_is_job)
        await message.answer(
            text="Будет ли появляться пост при выводе клавиатуры вакансий?(/jobs)",
            reply_markup=keyboards.yes_no_reply_markup()
        )


@router.message(
    AdminState.choosing_article_is_job
)
async def article_is_job_chosen(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.update_data(article_is_job=True)
        await state.set_state(AdminState.choosing_article_for_adult)
        await message.answer(
            text="Пост для совершеннолетних? (будет показываться только пользователям, указавшим возраст больше 18)",
            reply_markup=keyboards.yes_no_reply_markup()
        )
    elif message.text.lower() == "нет":
        await state.update_data(article_is_job=False)
        await state.set_state(AdminState.choosing_article_for_adult)
    else:
        await message.answer(
            text="Неверный ввод, попробуйте ещё раз.",
            reply_markup=keyboards.yes_no_reply_markup()
        )


@router.message(
    AdminState.choosing_article_for_adult
)
async def article_for_adult_chosen(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.update_data(article_for_adult=True)
        await state.set_state(AdminState.choosing_article_content)
        await message.answer(
            text="Введи содержание поста (то что будет показываться если его вызвать)"
        )
    elif message.text.lower() == "нет":
        await state.update_data(article_for_adult=False)
        await state.set_state(AdminState.choosing_article_content)
        await message.answer(
            text="Введи содержание поста (то что будет показываться если его вызвать)"
        )
    else:
        await message.answer(
            text="Неверный ввод, попробуйте ещё раз.",
            reply_markup=keyboards.yes_no_reply_markup()
        )


@router.message(
    AdminState.choosing_article_content
)
async def article_content_chosen(message: Message, state: FSMContext):
    await state.update_data(article_content=message.text)
    await state.set_state(AdminState.choosing_article_link)
    await message.answer(text="Хорошо, теперь ссылка к содержанию (если не нужна, скажи нет)")


@router.message(
    AdminState.choosing_article_link
)
async def article_link_chosen(message: Message, state: FSMContext):
    await state.update_data(article_link=message.text if message.text.lower() != "нет" else "")
    await message.answer(
        text="Отлично, я сохранил твою дрисню, можешь попытаться вызвать ее через жопс (/jobs), если конечно указал, что это работа.\nВы вышли из админ-панели."
    )
    art = await state.get_data()
    await state.clear()
    complete_article = Article(name=art["article_name"],
                               is_job=art["article_is_job"],
                               for_adult=art["article_for_adult"],
                               content=art["article_content"],
                               link=art["article_link"]
                               )
    ArticleDB.add_article(complete_article)


@router.message(
    AdminState.agreeing_deleting_article
)
async def delete_article(message: Message, state: FSMContext):
    article_name = await state.get_data()
    if message.text.lower() == "да":
        ArticleDB.delete_article_by_name(article_name["article_name"])
        await message.answer(f"Пост \"{article_name['article_name']}\" был удалён.\nВы вышли из админ-панели.")
        await state.clear()
    else:
        await message.answer(f"Пост \"{article_name['article_name']}\" не был удален.\nВы вышли из админ-панели.")
        await state.clear()
