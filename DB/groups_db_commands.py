import sqlite3

connection = sqlite3.connect('Groups.db',check_same_thread=False)
cursor = connection.cursor()

#Команды:

# cursor.execute(
#     'DELETE FROM Groups WHERE Group_name == ?',(Group_name,)
# )
# cursor.execute(
#     'DELETE FROM Groups WHERE Group_name == ?',(Group_name,)
# )


class TableGroupsDB:
    pass
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Groups (
        Group_Name TEXT PRIMARY KEY,
        Week TEXT ,
        Day TEXT ,
        Year TEXT
    );
    ''')

class AddValue:
    def add_table_value(Group_Name, Week, Day, Year):
        print(
            f'Вы хотите внести в таблицу:'
            f'Group_Name = {Group_Name}, Week = {Week}, Day = {Day}, Year = {Year}'
            )
        print(
            f'Вы подверждаете изменение данных?'
            f'"y" = yes, "n" = no'
        )
        user_input = input()

        if user_input == 'y':
            try:
                cursor.execute(
                    'INSERT INTO Groups (Group_Name, Week, Day, Year) VAlUES (?,?,?,?)', (Group_Name, Week, Day, Year)
                )
                connection.commit()
                print('Данные внесены')

            except:
                sqlite3.IntegrityError
                print('Данные не уникальны')

        if user_input == 'n':
            print('Данные не внесены')


class List:
    @staticmethod
    def list_table():
      cursor.execute('SELECT * FROM Groups')
      table = cursor.fetchall()
      for cells in table:
        print(cells)
        return


connection.commit()
connection.close()
