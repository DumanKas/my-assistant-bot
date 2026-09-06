from aiogram import Router, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from gemini import ask_gemini2
from database import save_message, get_history, clear_history, save_note, get_notes
class Notes_save(StatesGroup):
    waiting_for_text = State()
router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Добрый день! Нажми /ask и напиши вопрос для помощи ИИ")

@router.message(Command("ask"))
async def ask_handler(message: Message):
    user_id = message.from_user.id
    question = message.text.replace("/ask ", "").strip()
    save_message(user_id, "user", question)
    history = get_history(user_id)
    answer = await ask_gemini2(history)
    if len(answer) > 4096:
        answer = answer[:4096]
    save_message(user_id, "assistant", answer)
    await message.answer(answer)


@router.message(Command('clear'))
async def clear_handler(message: Message):
    user_id = message.from_user.id
    history = clear_history(user_id)
    if history == "В истории ничего нет":
        await message.answer("История уже пуста")
    else:
        await message.answer("История очищена")

@router.message(Command('notes'))
async def notes_handler(message: Message):
    user_id = message.from_user.id
    notes = get_notes(user_id)
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
async def waiting_for_text_handler(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    save_note(user_id, text)
    await message.answer(f"Заметка сохранена успешно:\n\n {text}")
    await state.clear()
