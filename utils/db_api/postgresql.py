from datetime import datetime, timedelta
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from config.settings import DEVELOPMENT_MODE
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        print('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # for users
    # async def create_user(self, phone, username, full_name, telegram_id):
    #     sql = "INSERT INTO Users (phone, username, full_name, telegram_id) VALUES($1, $2, $3, $4) returning *"
    #     return await self.execute(sql, phone, username, full_name, telegram_id, fetchrow=True)
    #
    # async def select_user(self, **kwargs):
    #     sql = "SELECT * FROM Users WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetch=True)
    #
    # async def select_all_users(self):
    #     sql = "SELECT * FROM Users"
    #     return await self.execute(sql, fetch=True)
    #
    # async def select_users(self, **kwargs):
    #     sql = "SELECT * FROM Users WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetch=True)

    async def create_user(self, phone, username, full_name, telegram_id, role='user'):
        sql = "INSERT INTO users (phone, username, full_name, telegram_id, role) VALUES($1, $2, $3, $4, $5) RETURNING *"
        return await self.execute(sql, phone, username, full_name, telegram_id, role, fetchrow=True)

    async def select_user(self, user_id):
        sql = "SELECT * FROM users WHERE id = $1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_user(self, user_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE users SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), user_id, fetchrow=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = $1 RETURNING *"
        return await self.execute(sql, user_id, fetchrow=True)

    # for teacher profile
    async def create_teacher_profile(self, user_id, first_name, last_name, birth_year, experience):
        sql = "INSERT INTO teacher_profile (user_id, first_name, last_name, birth_year, experience) VALUES($1, $2, $3, $4, $5) RETURNING *"
        return await self.execute(sql, user_id, first_name, last_name, birth_year, experience, fetchrow=True)

    async def select_teacher_profile(self, profile_id):
        sql = "SELECT * FROM teacher_profile WHERE id = $1"
        return await self.execute(sql, profile_id, fetchrow=True)

    async def select_teacher_profiles(self, **kwargs):
        sql = "SELECT * FROM teacher_profile WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_teacher_profile(self):
        sql = "SELECT * FROM teacher_profile"
        return await self.execute(sql, fetch=True)

    async def update_teacher_profile(self, profile_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE teacher_profile SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), profile_id, fetchrow=True)

    async def delete_teacher_profile(self, profile_id):
        sql = "DELETE FROM teacher_profile WHERE id = $1 RETURNING *"
        return await self.execute(sql, profile_id, fetchrow=True)

    # for groups
    async def create_group(self, name, teacher_id):
        sql = "INSERT INTO groups (name, teacher_id) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, name, teacher_id, fetchrow=True)

    async def select_group(self, group_id):
        sql = "SELECT * FROM groups WHERE id = $1"
        return await self.execute(sql, group_id, fetchrow=True)

    async def select_all_groups(self):
        sql = "SELECT * FROM groups"
        return await self.execute(sql, fetch=True)

    async def select_groups(self, **kwargs):
        sql = "SELECT * FROM groups WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_group(self, group_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE groups SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), group_id, fetchrow=True)

    async def delete_group(self, group_id):
        sql = "DELETE FROM groups WHERE id = $1 RETURNING *"
        return await self.execute(sql, group_id, fetchrow=True)

    # for parent's profile
    async def create_parent_profile(self, user_id, group_id, child_first_name=None, child_last_name=None):
        sql = "INSERT INTO parent_profile (user_id, group_id, child_first_name, child_last_name) VALUES($1, $2, $3, $4) RETURNING *"
        return await self.execute(sql, user_id, group_id, child_first_name, child_last_name, fetchrow=True)

    async def select_parent_profile(self, profile_id):
        sql = "SELECT * FROM parent_profile WHERE id = $1"
        return await self.execute(sql, profile_id, fetchrow=True)

    async def select_parent_profiles(self, **kwargs):
        sql = "SELECT * FROM parent_profile WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_parent_profile(self, profile_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE parent_profile SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), profile_id, fetchrow=True)

    async def delete_parent_profile(self, profile_id):
        sql = "DELETE FROM parent_profile WHERE id = $1 RETURNING *"
        return await self.execute(sql, profile_id, fetchrow=True)

    # for daily marks
    # async def create_daily_mark(self, student_id, kategory1, kategory2, kategory3, kategory4, kategory5, kategory6,
    #                             description):
    #     sql = """
    #     INSERT INTO daily_mark (student_id, kategory1, kategory2, kategory3, kategory4, kategory5, kategory6, description)
    #     VALUES($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *
    #     """
    #     return await self.execute(sql, student_id, kategory1, kategory2, kategory3, kategory4, kategory5, kategory6,
    #                               description, fetchrow=True)
    #
    # async def select_daily_mark(self, **kwargs):
    #     sql = "SELECT * FROM daily_mark WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetch=True)
    #
    # async def update_daily_mark(self, mark_id, **kwargs):
    #     set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
    #     sql = f"UPDATE daily_mark SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
    #     return await self.execute(sql, *kwargs.values(), mark_id, fetchrow=True)
    #
    # async def delete_daily_mark(self, mark_id):
    #     sql = "DELETE FROM daily_mark WHERE id = $1 RETURNING *"
    #     return await self.execute(sql, mark_id, fetchrow=True)

    # for marks

    async def create_daily_mark(self, student_id, kayfiyat, tartib, faollik, vaqtida_kelish,
                                dars_qoldirmaslik, vazifa_bajarilganligi, darsni_ozlashtirish,
                                created_at=datetime.now(),
                                description=None):
        sql = """
        INSERT INTO daily_mark (student_id, kayfiyat, tartib, faollik, vaqtida_kelish, 
                                dars_qoldirmaslik, vazifa_bajarilganligi, darsni_ozlashtirish, created_at, description)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING *
        """
        return await self.execute(sql, student_id, kayfiyat, tartib, faollik, vaqtida_kelish,
                                  dars_qoldirmaslik, vazifa_bajarilganligi, darsni_ozlashtirish, created_at,
                                  description, fetchrow=True)

    async def select_daily_mark(self, mark_id):
        sql = "SELECT * FROM daily_mark WHERE id = $1"
        return await self.execute(sql, mark_id, fetchrow=True)

    async def select_daily_marks(self, **kwargs):
        sql = "SELECT * FROM daily_mark WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_daily_mark(self, mark_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE daily_mark SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), mark_id, fetchrow=True)

    async def delete_daily_mark(self, mark_id):
        sql = "DELETE FROM daily_mark WHERE id = $1 RETURNING *"
        return await self.execute(sql, mark_id, fetchrow=True)

    import datetime

    from datetime import datetime, timedelta

    async def select_last_month_marks(self, student_id):
        # Hozirgi sanani olish
        today = datetime.now()

        # Oxirgi 30 kunning birinchi sanasini hisoblash
        thirty_days_ago = today - timedelta(days=30)

        sql = """
        SELECT * FROM daily_mark 
        WHERE student_id = $1 
          AND created_at >= $2
        """
        return await self.execute(sql, student_id, thirty_days_ago, fetch=True)

    async def select_today_marks(self, student_id):
        # Bugungi sanani olish
        today = datetime.now().date()  # Faqat sanani olish uchun date() metodidan foydalaning

        sql = """
        SELECT * FROM daily_mark 
        WHERE student_id = $1 
          AND created_at::date = $2
        """
        return await self.execute(sql, student_id, today, fetch=True)
