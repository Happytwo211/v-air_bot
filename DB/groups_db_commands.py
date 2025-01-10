import sqlite3
from datetime import date

connection = sqlite3.connect('Groups.db',check_same_thread=False)
cursor = connection.cursor()


# cursor.execute('''
# CREATE TABLE schedule (
#     schedule_id INT AUTO_INCREMENT PRIMARY KEY,
#     group_id INT NOT NULL,
#     weekday TEXT NOT NULL CHECK (weekday IN ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY')),
#     start_time TIME NOT NULL,
#     end_time TIME NOT NULL,
#     classroom VARCHAR(50) NOT NULL,
#     FOREIGN KEY (group_id) REFERENCES groups(group_id)
# );
# '''
# )

connection.commit()
connection.close()
