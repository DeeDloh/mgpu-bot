from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_day_keyboard(group, date):
    # Передаем группу и время
    buttons = [[InlineKeyboardButton(text="⬅️", callback_data=f'day_left_{group}_{date}'),
                InlineKeyboardButton(text="🏠", callback_data=f'day_now_{group}_{date}'),
                InlineKeyboardButton(text="➡️", callback_data=f'day_right_{group}_{date}')],
               [InlineKeyboardButton(text="Неделя", callback_data=f'day_week_{group}_{date}')]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_week_keyboard(group, date):
    # Передаем группу и время
    buttons = [[InlineKeyboardButton(text="⬅️", callback_data=f'week_left_{group}_{date}'),
                InlineKeyboardButton(text="🏠", callback_data=f'week_now_{group}_{date}'),
                InlineKeyboardButton(text="➡️", callback_data=f'week_right_{group}_{date}')],
               [InlineKeyboardButton(text="День", callback_data=f'week_day_{group}_{date}')]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
