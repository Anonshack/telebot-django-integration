import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async
import os
import django
import sys
sys.path.append("/Users/qudratbek/PycharmProjects/telebot-django-integration")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONF.settings")
django.setup()

from main_tg_api.models import BotUsers, FeedbackForAdmin
from buttons import main_feedback_button, feedback_buttons

TOKEN = "8055455117:AAG84ka_yBywIK7HpcuOpqSp9qu7oooRuHc"
BASE_URL = "http://127.0.0.1:9222/api/"
FEEDBACKS_ENDPOINT = "feedbacks/"

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()
    updating_feedback = State()

@dp.message(Command("start"))
async def start_handler(message: Message):
    username = message.from_user.username or message.from_user.first_name
    await message.answer(
        f"Hi, @{username}! Choose an option:",
        reply_markup=main_feedback_button()
    )

@dp.callback_query(lambda c: c.data == "send_feedback")
async def send_feedback_callback(callback_query: CallbackQuery, state: FSMContext):
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
        data = {"user": bot_user.id, "text": feedback_text}
        await sync_to_async(requests.post)(BASE_URL + FEEDBACKS_ENDPOINT, json=data, timeout=5)
    except Exception as e:
        await message.answer(f"Error sending feedback: {e}")
        await state.clear()
        return
    await message.answer("Thanks! Your feedback has been sent successfully.")
    await state.clear()

@dp.callback_query(lambda c: c.data == "show_feedbacks")
async def show_feedbacks_callback(callback_query: CallbackQuery):
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
    for fb in user_feedbacks:
        text = f"ID: {fb.id}\nText: {fb.text}\nCreated At: {fb.created_at}"
        await callback_query.message.answer(text, reply_markup=feedback_buttons(fb.id))

@dp.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_feedback_callback(callback_query: CallbackQuery):
    fb_id = int(callback_query.data.split("_")[1])
    telegram_user_id = str(callback_query.from_user.id)
    try:
        fb = await sync_to_async(FeedbackForAdmin.objects.get)(id=fb_id, user__user_id=telegram_user_id)
        await sync_to_async(fb.delete)()
        await callback_query.message.edit_text("Your feedback has been deleted.")
    except FeedbackForAdmin.DoesNotExist:
        await callback_query.message.edit_text("Feedback not found or you don't have permission.")

@dp.callback_query(lambda c: c.data.startswith("update_"))
async def update_feedback_callback(callback_query: CallbackQuery, state: FSMContext):
    fb_id = int(callback_query.data.split("_")[1])
    telegram_user_id = str(callback_query.from_user.id)
    try:
        fb = await sync_to_async(FeedbackForAdmin.objects.get)(id=fb_id, user__user_id=telegram_user_id)
        await state.update_data(feedback_id=fb.id)
        await state.set_state(FeedbackStates.updating_feedback)
        await callback_query.message.answer("Send the new text for your feedback:")
    except FeedbackForAdmin.DoesNotExist:
        await callback_query.message.answer("Feedback not found or you don't have permission.")

@dp.message(FeedbackStates.updating_feedback)
async def process_update_feedback(message: Message, state: FSMContext):
    data = await state.get_data()
    fb_id = data.get("feedback_id")
    telegram_user_id = str(message.from_user.id)
    try:
        fb = await sync_to_async(FeedbackForAdmin.objects.get)(id=fb_id, user__user_id=telegram_user_id)
        fb.text = message.text
        await sync_to_async(fb.save)()
        await message.answer("Your feedback has been updated.")
    except FeedbackForAdmin.DoesNotExist:
        await message.answer("Feedback not found or you don't have permission.")
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
