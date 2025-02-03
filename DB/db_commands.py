import sqlite3

connection = sqlite3.connect('db_groups.db',check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
INSERT INTO schedule (group_id, week, weekday, start_time, end_time, classroom, location, date) VALUES
(1, 'zalupa', 'ЧТ', 'test', 'test', 'test', '3-я Мытищинская ул., 12, стр. 1', '2025-02-10')

''')

connection.commit()
connection.close()