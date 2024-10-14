# Импорт библиотек
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import datetime
from datetime import datetime as dt
import json
import logging

# Импорт вспомогательных функций
from buttons.inline_day import get_day_keyboard, get_week_keyboard
from db_script import select_day, select_week
from code import TOKEN_TG

# Делаем список доступных групп. После реализуем обновление списка, каждый день
with open('../data/groups.json', encoding='UTF-8') as f:
    GROUPS = dict(json.load(f))
    AVAIL_GROUP = list(GROUPS.keys())

bot = Bot(token=TOKEN_TG)

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    # Пока пустая. Рассказать что надо отправить чтобы получить расписание
    await message.answer('Команда старт')


@dp.message(F.text)
async def group(message: types.Message):
    # Проверка, что пользователь ввел группу. Иначе пишем не группы.
    # После отправляем ему расписание. Готовый текст из расписание берем из БД
    if message.text in AVAIL_GROUP:
        logging.info(f'Запрос группы: {message.text}')
        gr = f'<blockquote><b>{message.text}</b></blockquote>'
        text = await select_day(GROUPS[message.text], dt.today())
        await message.answer(text=(f'{gr}\n' + text), parse_mode='HTML',
                             reply_markup=get_day_keyboard(message.text, dt.today().strftime(
                                 '%Y.%m.%d')))  # Для создания кнопки, передаем группу и время
    else:
        logging.warning(f'Пользователь ввел неверную группу: {message.text}')
        await message.answer('не группа')


@dp.callback_query(F.data.startswith('day_'))
async def day_callback(callback: types.CallbackQuery):
    # Функция реакции на кнопки. Вправо, влево, на текущую дату.
    # Функция только для кнопок когда расписание стоити на день
    _, action, group, date = callback.data.split("_")
    date = dt.strptime(date, '%Y.%m.%d')
    try:
        if action == 'right':
            date = date + datetime.timedelta(days=1)
            gr = f'<blockquote><b>{group}</b></blockquote>'
            text = await select_day(GROUPS[group], date)
            await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                             reply_markup=get_day_keyboard(group, date.strftime('%Y.%m.%d')))
        elif action == 'left':
            date = date - datetime.timedelta(days=1)
            gr = f'<blockquote><b>{group}</b></blockquote>'
            text = await select_day(GROUPS[group], date)
            await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                             reply_markup=get_day_keyboard(group, date.strftime('%Y.%m.%d')))
        elif action == 'now':
            today = dt.today().replace(hour=0, minute=0, second=0, microsecond=0)
            if date != today:
                date = today
                gr = f'<blockquote><b>{group}</b></blockquote>'
                text = await select_day(GROUPS[group], date)
                await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                                 reply_markup=get_day_keyboard(group, date.strftime('%Y.%m.%d')))
        elif action == 'week':
            gr = f'<blockquote><b>{group}</b></blockquote>'
            text = await select_week(GROUPS[group], date)
            await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                             reply_markup=get_week_keyboard(group, date.strftime('%Y.%m.%d')))
        else:
            raise ValueError('Неизвестный callback_query')
    except Exception as e:
        logging.error(f"Ошибка в обработке callback: {e}", exc_info=True)


@dp.callback_query(F.data.startswith('week_'))
async def day_callback(callback: types.CallbackQuery):
    # Функция реакции на кнопки. Вправо, влево, на текущую дату.
    # Функция только для кнопок когда расписание стоити на день
    _, action, group, date = callback.data.split("_")
    date = dt.strptime(date, '%Y.%m.%d')
    try:
        if action == 'right':
            date = date + datetime.timedelta(days=7)
            gr = f'<blockquote><b>{group}</b></blockquote>'
            text = await select_week(GROUPS[group], date)
            await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                             reply_markup=get_week_keyboard(group, date.strftime('%Y.%m.%d')))
        elif action == 'left':
            date = date - datetime.timedelta(days=7)
            gr = f'<blockquote><b>{group}</b></blockquote>'
            text = await select_week(GROUPS[group], date)
            await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                             reply_markup=get_week_keyboard(group, date.strftime('%Y.%m.%d')))
        elif action == 'now':
            today = dt.today().replace(hour=0, minute=0, second=0, microsecond=0)
            if date != today:
                date = today
                gr = f'<blockquote><b>{group}</b></blockquote>'
                text = await select_week(GROUPS[group], date)
                await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                                 reply_markup=get_week_keyboard(group, date.strftime('%Y.%m.%d')))
        elif action == 'day':
            gr = f'<blockquote><b>{group}</b></blockquote>'
            text = await select_day(GROUPS[group], date)
            await callback.message.edit_text(text=(f'{gr}\n' + text), parse_mode='HTML',
                                             reply_markup=get_day_keyboard(group, date.strftime('%Y.%m.%d')))
        else:
            raise ValueError('Неизвестный callback_query')
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {e}")


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("app.log"),
                                  logging.StreamHandler()])
    logging.info('Бот запущен и начал опрос')
    await dp.start_polling(bot)


asyncio.run(on_startup(dp))
