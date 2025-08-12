import sqlite3

conn = sqlite3.connect("spare_parts.db")
cursor = conn.cursor()

# Insert CPU ↔ Motherboard compatibility
cursor.executemany("""
    INSERT INTO cpu_motherboard_compatibility (cpu_name, motherboard_name) VALUES (?, ?)
""", [
    ('Intel Core i5-13600K', 'ASRock B760M Pro RS'),
    ('Intel Core i7-13700K', 'ASUS ROG Strix Z690-E'),
    ('Intel Core i9-13900K', 'Gigabyte B660M DS3H'),
    ('AMD Ryzen 5 7600X', 'Gigabyte X670 AORUS Elite AX'),
    ('AMD Ryzen 7 7700X', 'MSI MAG B650 Tomahawk')
])

# Insert Motherboard ↔ Memory compatibility
cursor.executemany("""
    INSERT INTO motherboard_memory_compatibility (motherboard_name, memory_type, max_speed) VALUES (?, ?, ?)
""", [
    ('ASRock B760M Pro RS', 'DDR5', 5600),
    ('ASUS ROG Strix Z690-E', 'DDR5', 6000),
    ('Gigabyte B660M DS3H', 'DDR4', 3200),
    ('Gigabyte X670 AORUS Elite AX', 'DDR5', 7200),
    ('MSI MAG B650 Tomahawk', 'DDR5', 6400)
])

# Insert GPU ↔ Case compatibility
cursor.executemany("""
    INSERT INTO gpu_case_compatibility (gpu_name, case_name) VALUES (?, ?)
""", [
    ('NVIDIA GeForce RTX 4070 Ti', 'Fractal Design Define 7'),
    ('AMD Radeon RX 7700 XT', 'NZXT H510'),
    ('NVIDIA GeForce RTX 4080', 'Cooler Master MasterBox TD500 Mesh'),
    ('AMD Radeon RX 7900 XTX', 'Phanteks Eclipse P400A'),
    ('NVIDIA GeForce RTX 4060', 'Lian Li PC-O11 Dynamic')
])

# Insert GPU ↔ PSU compatibility
cursor.executemany("""
    INSERT INTO gpu_psu_compatibility (gpu_name, psu_name, min_wattage_required) VALUES (?, ?, ?)
""", [
    ('NVIDIA GeForce RTX 4070 Ti', 'Corsair RM850x', 750),
    ('AMD Radeon RX 7700 XT', 'Cooler Master MWE Gold 650 V2', 600),
    ('NVIDIA GeForce RTX 4080', 'EVGA SuperNOVA 1000 G5', 850),
    ('AMD Radeon RX 7900 XTX', 'Thermaltake Toughpower GF3 1200W', 1000),
    ('NVIDIA GeForce RTX 4060', 'Seasonic FOCUS GX-750', 550)
])

conn.commit()
conn.close()

print("Compatibility data inserted!")
