from pytz import timezone
import asyncio

from loader import db


async def delete_users_that_join_one_weak_ago():
    tz = timezone('UTC')
    while True:
        users = await db.select_users_last_week()
        for user in users:
            await db.delete_user(user_id=user['id'])
        await asyncio.sleep(86400)
