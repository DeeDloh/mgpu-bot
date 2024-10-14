import datetime
import aiosqlite
import logging


async def select_day(group: str, date: datetime.datetime):
    # Передаем группу и время
    # Функция запроса в БД
    logging.info(f'Запрос расписания для группы {group} на {date}. Дни')
    async with aiosqlite.connect('../DB/MGPU.db') as db:
        cursor = await db.execute(
            f"SELECT text FROM {group}_{date.year}_day WHERE day={date.day} AND month={date.month}")
        text = await cursor.fetchone()
        if text:
            logging.info(f'Получен результат для {group}: {text[0]}')
            return text[0]
        else:
            logging.warning(f'Расписание не найдено для группы {group} на {date}')
            return 'Расписание отсутствует'


async def select_week(group: str, date: datetime.datetime):
    logging.info(f'Запрос расписания для группы {group} на {date}. Недели')
    # Передаем группу и время
    # Функция запроса в БД
    num_dayweek = date.isoweekday()
    days = []
    amo_months = []
    for i in range(1, 8):
        n_add = date + datetime.timedelta(days=-(num_dayweek - i))
        days.append(str(n_add.day))
        amo_months.append(n_add.month)
    if len(set(amo_months)) == 1:
        months = amo_months[0]
        async with aiosqlite.connect('../DB/MGPU.db') as db:
            cursor = await db.execute(
                f"SELECT text FROM {group}_{date.year}_day WHERE (day IN ({', '.join(days)}) AND month={months})")
            text = await cursor.fetchall()
            res = map(lambda x: x[0], text)
            return '\n'.join(res)
    elif len(set(amo_months)) == 2:
        fir_m, sec_m = amo_months[0], amo_months[-1]
        first_months_day = [days[i] for i in range(7) if amo_months[i] == fir_m]
        second_months_day = [days[i] for i in range(7) if amo_months[i] == sec_m]
        async with aiosqlite.connect('../DB/MGPU.db') as db:
            cursor = await db.execute(
                f"SELECT text FROM {group}_{date.year}_day WHERE (day IN ({', '.join(first_months_day)}) AND month={fir_m}) OR (day IN ({', '.join(second_months_day)}) AND month={sec_m})")
            text = await cursor.fetchall()
            res = map(lambda x: x[0], text)
            return '\n'.join(res)
