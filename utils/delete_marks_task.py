from pytz import timezone
import asyncio

from loader import db


async def delete_marks_older_than_one_month():
    tz = timezone('UTC')
    while True:
        marks = await db.select_older_than_one_month_marks()
        # print('marks', marks)
        for mark in marks:
            await db.delete_daily_mark(mark_id=mark['id'])
        await asyncio.sleep(86400)
        # await asyncio.sleep(4)
