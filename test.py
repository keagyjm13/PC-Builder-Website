import sqlite3

#debug file, checking compat tables

conn = sqlite3.connect("spare_parts.db")
cursor = conn.cursor()

for table in ['cpu_motherboard_compatibility', 'motherboard_memory_compatibility', 'gpu_case_compatibility', 'gpu_psu_compatibility']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table} has {count} rows")
    
    

cursor.execute("SELECT * FROM motherboard_memory_compatibility;")
rows = cursor.fetchall()

for row in rows:
    print(f"Motherboard: {row[0]}, Memory Type: {row[1]}, Max Speed: {row[2]}")


conn.close()
    


