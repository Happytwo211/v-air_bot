import sqlite3
from datetime import date

connection = sqlite3.connect('Groups.db',check_same_thread=False)
cursor = connection.cursor()

#
# cursor.execute('''
# ALTER TABLE schedule ADD COLUMN date DATE;
# ''')


cursor.execute('''
INSERT INTO schedule (group_id, week, weekday, start_time, end_time, classroom, location, date) VALUES
(1, '06.01 - 12.01', 'Четверг', '16:25', '17:55', 'кабинет 28', '3-я Мытищинская ул., 12, стр. 1', '2025-01-14')

''')

# cursor.execute('''
# INSERT INTO groups (group_id, group_name, description) VALUES
# (1, 'Гимназия РУТ МИИТ', ' место проведения: 3-я Мытищинская ул., 12, стр. 1'),
# (2, 'Школа № 1273"', 'место проведения: ул. Академика Капицы, 12');
# ''')


# cursor.execute('''
# CREATE TABLE groups (
#     group_id INT PRIMARY KEY,
#     group_name VARCHAR(50) NOT NULL,
#     description VARCHAR(255)
# );
# ''')
# cursor.execute('''
# CREATE TABLE schedule (
#     schedule_id INT AUTO_INCREMENT PRIMARY KEY,
#     group_id INT NOT NULL,
#     week TEXT NOT NULL,
#     weekday TEXT NOT NULL,
#     start_time TIME NOT NULL,
#     end_time TIME NOT NULL,
#     classroom VARCHAR(50) NOT NULL,
#     location TEXT NOT NULL,
#
#     FOREIGN KEY (group_id) REFERENCES groups(group_id)
# );
# '''
# )

connection.commit()
connection.close()
