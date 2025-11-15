from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_feedback_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Show last 5 feedbacks", callback_data="show_feedbacks")],
            [InlineKeyboardButton(text="Send new feedback", callback_data="send_feedback")]
        ]
    )

def feedback_buttons(fb_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Delete", callback_data=f"delete_{fb_id}"),
                InlineKeyboardButton(text="Update", callback_data=f"update_{fb_id}")
            ]
        ]
    )
