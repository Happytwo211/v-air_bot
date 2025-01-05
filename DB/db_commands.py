import sqlite3

connection = sqlite3.connect('Groups.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Groups (
    Group_Name TEXT PRIMARY KEY,
    Week TEXT ,
    Day TEXT ,
    Year TEXT 
);
''')

# def add_value(Group_Name,Week,Day,Year):
#     cursor.execute(
#         'INSERT INTO Groups (Group_Name, Week, Day, Year) VAlUES (?,?,?,?)', (Group_Name,)
#     )
#     connection.commit()

def add_group_name(Group_Name):
    cursor.execute(
        'INSERT INTO Groups (Group_Name) VAlUES (?)', (Group_Name,)
    )
    connection.commit()
#
#
#
# def list_tasks():
#   cursor.execute('SELECT * FROM Groups')
#   tasks = cursor.fetchall()
#   for task in tasks:
#     print(task)
#
add_group_name('Group_Test_1')
# add_value(Group_Name='group_test', Week='06.05-10.05_test', Day='Day_test',Year='Year_test')
connection.commit()
connection.close()
