import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from buttons import feedback_button
from asgiref.sync import sync_to_async
import os
import django
import sys

sys.path.append("/Users/qudratbek/PycharmProjects/telebot-django-integration")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONF.settings")
django.setup()

from main_tg_api.models import BotUsers


TOKEN = "8055455117:AAG84ka_yBywIK7HpcuOpqSp9qu7oooRuHc"
BASE_URL = "http://127.0.0.1:9222/api/"
FEEDBACKS_ENDPOINT = "feedbacks/"

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    username = message.from_user.username or message.from_user.first_name
    await message.answer(
        f"Hi, @{username}! Choose an option:",
        reply_markup=feedback_button
    )



@dp.callback_query(lambda c: c.data == "show_feedbacks")
async def callback_show_feedbacks(callback_query: CallbackQuery):
    telegram_user_id = str(callback_query.from_user.id)

    try:
        bot_user = await sync_to_async(BotUsers.objects.get)(user_id=telegram_user_id)
        user_feedbacks = await sync_to_async(lambda: list(bot_user.feedbacks.all().order_by("-created_at")[:5]))()

    except BotUsers.DoesNotExist:
        await callback_query.message.edit_text("You have not sent any feedback yet.")
        return

    if not user_feedbacks:
        await callback_query.message.edit_text("You have not sent any feedback yet.")
        return

    text = ""
    for fb in user_feedbacks:
        text += f"ID: {fb.id}\nText: {fb.text}\nCreated At: {fb.created_at}\n{'-'*20}\n"

    await callback_query.message.edit_text(text)


@dp.callback_query(lambda c: c.data == "send_feedback")
async def callback_send_feedback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Please write your feedback and send it:")
    await state.set_state(FeedbackStates.waiting_for_feedback)


@dp.message(FeedbackStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    feedback_text = message.text

    bot_user, created = await sync_to_async(BotUsers.objects.get_or_create)(
        user_id=str(message.from_user.id),
        defaults={
            "username": message.from_user.username or None,
            "name": message.from_user.full_name or message.from_user.first_name
        }
    )

    try:
        data = {
            "user": bot_user.id,
            "text": feedback_text
        }
        response = await sync_to_async(requests.post)(BASE_URL + FEEDBACKS_ENDPOINT, json=data, timeout=5)
        response.raise_for_status()
    except Exception as e:
        await message.answer(f"Error sending feedback: {e}")
        await state.clear()
        return

    await message.answer("Thanks! Your feedback has been sent successfully.")
    await state.clear()

async def main() -> None:
    bot = Bot(token=TOKEN)
    while True:
        try:
            print("Bot started...")
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Error occurred: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
