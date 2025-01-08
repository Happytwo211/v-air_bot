import sqlite3
from datetime import date
connection = sqlite3.connect('Groups.db',check_same_thread=False)

cursor = connection.cursor()

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


print(List.list_table())


connection.commit()
connection.close()
