import sqlite3
from datetime import date
connection = sqlite3.connect('Groups.db',check_same_thread=False)

cursor = connection.cursor()
def Miit_Value(Day, Int_Day, Month, Year, Week = None):
    cursor.execute(
                    'INSERT INTO Group_MIIT_Schedule (Week, Day, Int_Day, Month, Year) VAlUES (?,?,?,?,?)', (Week, Day, Int_Day, Month, Year))

    connection.commit()
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


Miit_Value(Day='Пятница', Int_Day='10.01', Month='January', Year='2025')


connection.commit()
connection.close()
