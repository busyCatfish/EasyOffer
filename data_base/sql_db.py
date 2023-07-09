from create_bot import bot
import pymysql.cursors

class sqldb():
    connection = pymysql.connect(host='',
                             port = ,user='',
                             password='',
                             database='',
                             cursorclass=pymysql.cursors.DictCursor)

def sql_start():
    if sqldb.connection:
        with sqldb.connection.cursor() as cursor:
            create_table_query = "CREATE TABLE IF NOT EXISTS `ordersPhoto`(`id` int(11) NOT NULL AUTO_INCREMENT," \
                                 " `MakerID`varchar(25) ," \
                                 " `UserID`varchar(25) ," \
                                 "`ReadyForWork` int(1),PRIMARY KEY (`id`))"
            cursor.execute(create_table_query)
            print('Data base connected Ok!')
            sqldb.connection.commit()


def sql_add_newWork(workInfo):
    with sqldb.connection.cursor() as cursor:
        insert_query = 'UPDATE `ordersPhoto` SET `UserID`=%s,`ReadyForWork`="1" WHERE `MakerID`=%s'
        data_sql = [workInfo[0], workInfo[1]]
        cursor.execute(insert_query, tuple(data_sql))
        sqldb.connection.commit()


async def sql_add_finishedWork(state):
    async with state.proxy() as data:
        with sqldb.connection.cursor() as cursor:
            insert_query = 'UPDATE `ordersPhoto` SET `ReadyForWork`="0" WHERE `MakerID`=%s'
            data_sql = [data['makerID']]
            cursor.execute(insert_query, tuple(data_sql))
            sqldb.connection.commit()

async def sql_add_readReadiness(makerID):
    with sqldb.connection.cursor() as cursor:
        insert_query = 'SELECT `ReadyForWork` FROM `ordersPhoto` WHERE `MakerID`=%s'
        cursor.execute(insert_query, makerID)
        result = cursor.fetchall()
        return result

def sql_find_userID(makerID):
    with sqldb.connection.cursor() as cursor:
        insert_query = 'SELECT `UserID` FROM `ordersPhoto` WHERE `MakerID`=%s'
        cursor.execute(insert_query, makerID)
        result = cursor.fetchall()[0]
        return result['UserID']


def sql_find_makerID(makerID):
    with sqldb.connection.cursor() as cursor:
        insert_query = 'SELECT `MakerID` FROM `ordersPhoto` WHERE `MakerID`=%s'
        cursor.execute(insert_query, makerID)
        result = cursor.fetchall()
        return result

# async def sql_add_command(order):
#     with sqldb.connection.cursor() as cursor:
#         insert_query = 'INSERT INTO `orders` (`order`,`adress`,`price`) VALUES (%s,%s,%s)'
#         cursor.execute(insert_query,tuple(order))
#         sqldb.connection.commit()
    # cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))


# async def sql_read(message):
#     with connection.cursor() as cursor:
#         select_all_rows = 'SELECT * FROM `menu`'
#         cursor.execute(select_all_rows)
#         rows = cursor.fetchall()
#         for row in rows:
#             await bot.send_photo(message.from_user.id, row['img'], f'{row["name"]}\n Description: {row["description"]}\n Price: {row["price"]}')

# async def sql_read2():
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM `orders`')
#         return cursor.fetchall()

# async def sql_delete_command(data):
#     with connection.cursor() as cursor:
#         delete_query = "DELETE FROM `menu` WHERE name = %s;"
#         cursor.execute(delete_query,(data,))
#         connection.commit()

