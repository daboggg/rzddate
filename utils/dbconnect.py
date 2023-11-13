import logging
import aiosqlite
import sqlite3

logger = logging.getLogger('utils.dbconnect')


async def create_task_table():
    async with aiosqlite.connect('rzddate.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS task_table
             (id TEXT PRIMARY KEY NOT NULL,
             trigg_name TEXT,
             chat_id INT,
             run_date TEXT,
             date_of_trip TEXT,
             text TEXT)''')
        await db.commit()


async def add_task(id, trigg_name, chat_id, run_date, date_of_trip, text):
    async with aiosqlite.connect('rzddate.db') as db:
        await db.execute("INSERT INTO task_table(id, trigg_name, chat_id, run_date, date_of_trip, text) VALUES (?, ?, ?, ?, ?, ?)", (id, trigg_name,chat_id,run_date, date_of_trip, text))
        await db.commit()
        logger.info(f'Доблено в бд задание с id: {id}')



async def get_tasks():
    async with aiosqlite.connect('rzddate.db') as db:
        query = f'SELECT * FROM task_table'
        result_list = await db.execute_fetchall(query)
        logger.info(f'Получен список заданий из бд')
        return result_list

def delete_task(id:str)->None:
    with sqlite3.connect('rzddate.db') as db:
        query = f"DELETE FROM task_table WHERE id='{id}'"
        db.execute(query)
        db.commit()
        logger.info(f'Удалено задание из бд с id {id}')


# async def get_user_tasks(id):
#     async with aiosqlite.connect('rzddate.db') as db:
#         query = f'SELECT * FROM task_table WHERE id LIKE "{id}%"'
#         result_list = await db.execute_fetchall(query)
#         logger.info(f'Получен список заданий из с id: {id}')
#         return result_list

