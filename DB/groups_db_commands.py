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
    def add_table_value(Group_Name, Week, Day, Year, Room_Number, Time):
        print(
            f'Вы хотите внести в таблицу:'
            f'Group_Name = {Group_Name}, Week = {Week}, Day = {Day}, Year = {Year}, Room_Number = {Room_Number}, Time = {Time}'
            )
        print(
            f'Вы подверждаете изменение данных?'
            f'"y" = yes, "n" = no'
        )
        user_input = input()

        if user_input == 'y':
            try:
                cursor.execute(
                    'INSERT INTO Groups (Group_Name, Week, Day, Year, Room_Number, Time) VAlUES (?,?,?,?,?,?)', (Group_Name, Week, Day, Year, Room_Number, Time)
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
        return table
    @staticmethod
    def list_group_name():
        data = cursor.execute("SELECT Group_Name FROM Groups")
        formated_data = '\n'.join([' '.join(map(str, row)) for row in data])
        formated_data_split = formated_data.split('\n')
        print(formated_data_split[0])
        return formated_data



List.list_group_name()

connection.commit()
connection.close()
