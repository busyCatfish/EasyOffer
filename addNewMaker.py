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

def sql_add_command(makerID):
    with sqldb.connection.cursor() as cursor:
        insert_query = 'INSERT INTO `ordersPhoto` (`MakerID`) VALUES(%s)'
        cursor.execute(insert_query, makerID)
        sqldb.connection.commit()

if __name__ == '__main__':
    sql_start()
    sql_add_command("833324650")
