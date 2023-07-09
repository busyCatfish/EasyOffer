from aiogram.utils import executor
from create_bot import dp
from data_base import sql_db
from handlers import client,admin,makers
import logging


async def on_startup(_):
    sql_db.sql_start()
    print('Bot online')


client.register_handlers_client(dp)
#admin.register_handlers_admin(dp)
makers.register_handlers_makers(dp)

async def on_shutdown(dp):
    logging.warning('Shutting down..')


    # Close DB connection
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

def main():
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()