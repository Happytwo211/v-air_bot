import sqlite3

connection = sqlite3.connect('Groups.db',check_same_thread=False)
cursor = connection.cursor()

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

    def add_group_name(Group_Name):
        cursor.execute(
            'INSERT INTO Groups (Group_Name) VAlUES (?)', (Group_Name,)
        )
        connection.commit()
    def add_week(week):
        cursor.execute(
            'INSERT INTO Groups (Week) VAlUES (?)', (week,)
        )
        connection.commit()
    def add_day(Day):
        cursor.execute(
            'INSERT INTO Groups (Day) VAlUES (?)', (Day,)
        )
        connection.commit()
    def add_year(Year):
        cursor.execute(
            'INSERT INTO Groups (Year) VAlUES (?)', (Year,)
        )
        connection.commit()

class List:

    @staticmethod
    def list_table():
      cursor.execute('SELECT * FROM Groups')
      table = cursor.fetchall()
      for cells in table:
        print(cells)
        return


class Delete:



    def delete_group_name(Group_name):
        cursor.execute(
            'DELETE FROM Groups WHERE Group_name == ?',(Group_name,)
        )
        connection.commit()

    def delete_week(Week):
        cursor.execute(
            'DELETE FROM Groups WHERE Week == ?', (Week,)
        )
        connection.commit()

    def delete_day(Day):
        cursor.execute(
            'DELETE FROM Groups WHERE Day == ?',(Day,)
        )
        connection.commit()

    def delete_year(Year):
        cursor.execute(
            'DELETE FROM Groups WHERE Year == ?', (Year,)
        )
        connection.commit()



# List.list_table()
connection.commit()
connection.close()
