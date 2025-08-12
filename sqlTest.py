import sqlite3

#shows user builds, proves that db is holding multiple builds

conn = sqlite3.connect("spare_parts.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM user_builds")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
