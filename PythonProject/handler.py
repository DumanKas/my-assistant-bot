from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from gemini import ask_gemini2
import asyncpg
from database import save_message, get_history, clear_history, save_note, get_notes,get_context
class Notes_save(StatesGroup):
    waiting_for_text = State()
router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Напиши вопрос для помощи ИИ")

@router.message(Command('clear'))
async def clear_handler(message: Message, pool: asyncpg.Pool):
    user_id = message.from_user.id
    history_cleared = await clear_history(pool,user_id)
    if not history_cleared:
        await message.answer("История уже пуста")
    else:
        await message.answer("История очищена")

@router.message(Command('notes'))
async def notes_handler(message: Message, pool: asyncpg.Pool):
    user_id = message.from_user.id
    notes = await get_notes(pool,user_id)
    if not notes:
        await message.answer("Заметок нет")
        return
    text =  "\n".join([f"*{note['text']}"   for note in notes])
    await message.answer(f"Ваши заметки:\n{text}")

@router.message(Command('add'))
async def add_handler(message: Message, state: FSMContext):
    await message.answer("Введите текст заметки")
    await state.set_state(Notes_save.waiting_for_text)

@router.message(Notes_save.waiting_for_text)
async def waiting_for_text_handler(message: Message, state: FSMContext, pool: asyncpg.Pool):
    text = message.text
    user_id = message.from_user.id
    await save_note(pool,user_id, text)
    await message.answer(f"Заметка сохранена успешно:\n\n {text}")
    await state.clear()

@router.message(F.text.startswith("/"))
async def unknown_command_handler(message: Message):
  await message.answer("Я не знаю такую команду. Напишите /help для справки.")


@router.message(F.text & ~F.text.startswith("/"))
async def ai_handler(message: Message,pool: asyncpg.Pool):
    user_id = message.from_user.id
    question = message.text.strip()

    if not question:
        await message.answer("Напишите вопрос")
        return
    await save_message(pool, user_id,"user", question)
    history = await get_context(pool, user_id,question)
    answer = await ask_gemini2(history)
    if len(answer) > 4096:
        answer = answer[:4096]


    await save_message(pool, user_id,"assistant", answer)
    await message.answer(answer)
