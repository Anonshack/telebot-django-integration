from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

feedback_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Show last 5 feedbacks", callback_data="show_feedbacks")],
        [InlineKeyboardButton(text="Send new feedback", callback_data="send_feedback")]
    ]
)

