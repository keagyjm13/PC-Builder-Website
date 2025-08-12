import sqlite3

conn = sqlite3.connect("spare_parts.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS cpu;
DROP TABLE IF EXISTS cpu_cooler;
DROP TABLE IF EXISTS motherboard;
DROP TABLE IF EXISTS memory;
DROP TABLE IF EXISTS storage;
DROP TABLE IF EXISTS video_card;
DROP TABLE IF EXISTS pc_case;
DROP TABLE IF EXISTS power_supply;
DROP TABLE IF EXISTS operating_system;
DROP TABLE IF EXISTS cpu_motherboard_compatibility;
DROP TABLE IF EXISTS motherboard_memory_compatibility;
DROP TABLE IF EXISTS gpu_case_compatibility;
DROP TABLE IF EXISTS gpu_psu_compatibility;
DROP TABLE IF EXISTS user_builds;

CREATE TABLE IF NOT EXISTS cpu (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    core_count INTEGER NOT NULL,
    core_clock INTEGER NOT NULL,
    boost_clock INTEGER NOT NULL,
    microarchitecture TEXT NOT NULL,
    tdp INTEGER NOT NULL,
    integrated_graphics TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS cpu_cooler (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    fan_rpm INTEGER NOT NULL,
    noise_level INTEGER,
    radiator_size INTEGER DEFAULT 0,
    color TEXT NOT NULL
    
);

CREATE TABLE IF NOT EXISTS motherboard (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    cpu_socket TEXT NOT NULL,
    memory_max INTEGER NOT NULL,
    form_factor TEXT NOT NULL,
    memory_slots INTEGER NOT NULL,
    color TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memory (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    speed INTEGER NOT NULL,
    modules TEXT NOT NULL,
    cas_latency REAL NOT NULL,
    type TEXT NOT NULL,
    price_per_gb REAL NOT NULL,
    color TEXT NOT NULL,
    fw_latency REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS storage (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    capacity TEXT NOT NULL,
    type TEXT NOT NULL,
    interface TEXT NOT NULL,
    price_per_gb REAL NOT NULL,
    cache INTEGER DEFAULT 0,
    form_factor TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS video_card (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    chipset TEXT NOT NULL,
    memory INTEGER NOT NULL,
    boost_clock INTEGER NOT NULL,
    core_clock INTEGER NOT NULL,
    color TEXT NOT NULL,
    length INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS pc_case (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    type TEXT NOT NULL,
    side_panel TEXT NOT NULL,
    external_volume REAL NOT NULL,
    color TEXT NOT NULL,
    power_supply TEXT NOT NULL,
    internal_bays INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS power_supply (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    wattage INTEGER NOT NULL,
    efficiency_rating TEXT NOT NULL,
    modular TEXT NOT NULL,
    type TEXT NOT NULL,
    color TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS operating_system (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    mode TEXT NOT NULL,
    max_memory_size INTEGER NOT NULL,
    max_memory_unit TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cpu_motherboard_compatibility (
    cpu_name TEXT NOT NULL,
    motherboard_name TEXT NOT NULL,
    FOREIGN KEY (cpu_name) REFERENCES cpu(name),
    FOREIGN KEY (motherboard_name) REFERENCES motherboard(name),
    PRIMARY KEY (cpu_name, motherboard_name)
);

CREATE TABLE IF NOT EXISTS motherboard_memory_compatibility (
    motherboard_name TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    max_speed INTEGER NOT NULL,
    FOREIGN KEY (memory_type) REFERENCES memory(type),
    FOREIGN KEY (max_speed) REFERENCES memory(speed),
    FOREIGN KEY (motherboard_name) REFERENCES motherboard(name),
    PRIMARY KEY (motherboard_name, memory_type)
);

CREATE TABLE IF NOT EXISTS gpu_case_compatibility (
    gpu_name TEXT NOT NULL,
    case_name TEXT NOT NULL,
    FOREIGN KEY (gpu_name) REFERENCES video_card(name),
    FOREIGN KEY (case_name) REFERENCES pc_case(name),
    PRIMARY KEY (gpu_name, case_name)
);

CREATE TABLE IF NOT EXISTS gpu_psu_compatibility (
    gpu_name TEXT NOT NULL,
    psu_name TEXT NOT NULL,
    min_wattage_required INTEGER NOT NULL,
    FOREIGN KEY (gpu_name) REFERENCES video_card(name),
    FOREIGN KEY (psu_name) REFERENCES power_supply(name),
    PRIMARY KEY (gpu_name, psu_name)
);

CREATE TABLE user_builds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu TEXT,
    cpu_price REAL,
    cpu_core_count INTEGER,
    cpu_core_clock REAL,
    cpu_boost_clock REAL,
    cpu_cooler TEXT,
    cpu_cooler_price REAL,
    motherboard TEXT,
    motherboard_price REAL,
    memory TEXT,
    memory_price REAL,
    storage TEXT,
    storage_price REAL,
    video_card TEXT,
    video_card_price REAL,
    pc_case TEXT,
    pc_case_price REAL,
    power_supply TEXT,
    power_supply_price REAL,
    operating_system TEXT,
    operating_system_price REAL,
    total_price REAL
);
""")

conn.commit()

# inserts
cursor.executescript("""
INSERT INTO cpu VALUES
('Intel Core i5-13600K', 319.99, 14, 3500, 5100, 'Raptor Lake', 125, 'Intel UHD Graphics 770'),
('AMD Ryzen 5 7600X', 249.99, 6, 4700, 5300, 'Zen 4', 105, 'None'),
('Intel Core i7-13700K', 419.99, 16, 3400, 5400, 'Raptor Lake', 125, 'Intel UHD Graphics 770'),
('AMD Ryzen 7 7700X', 349.99, 8, 4500, 5400, 'Zen 4', 105, 'None'),
('Intel Core i9-13900K', 589.99, 24, 3200, 5800, 'Raptor Lake', 125, 'Intel UHD Graphics 770');

INSERT INTO cpu_cooler VALUES
('be quiet! Dark Rock Pro 4', 89.99, 1500, 24, NULL, 'Black'),
('NZXT Kraken X73 RGB', 199.99, 2800, 33, 360, 'Black'),
('Cooler Master Hyper 212 Black Edition', 44.99, 2000, 26, NULL, 'Black'),
('Noctua NH-D15', 99.99, 1500, 24, NULL, 'Brown'),
('Corsair H150i Elite LCD', 259.99, 2400, 30, 360, 'Black');

INSERT INTO motherboard VALUES
('ASRock B760M Pro RS', 139.99, 'LGA 1700', 128, 'Micro ATX', 4, 'Black'),
('Gigabyte X670 AORUS Elite AX', 269.99, 'AM5', 128, 'ATX', 4, 'Black/Silver'),
('ASUS ROG Strix Z690-E', 379.99, 'LGA 1700', 128, 'ATX', 4, 'Black'),
('MSI MAG B650 Tomahawk', 219.99, 'AM5', 128, 'ATX', 4, 'Black'),
('Gigabyte B660M DS3H', 109.99, 'LGA 1700', 64, 'Micro ATX', 2, 'Black');

INSERT INTO memory VALUES
('Kingston Fury Beast DDR5 32GB (2x16GB) 5600MHz', 129.99, 5600, '2 x 16GB', 28,'DDR5', 4.06, 'Black', 32.5),
('Team T-Force Delta RGB DDR5 64GB (2x32GB) 7200MHz', 379.99, 7200, '2 x 32GB', 32, 'DDR5', 5.94, 'White', 34.0),
('Corsair Vengeance LPX 16GB (2x8GB) 3200MHz', 59.99, 3200, '2 x 8GB', 16, 'DDR4', 3.75, 'Black', 30.0),
('G.Skill Trident Z5 RGB 32GB (2x16GB) 6000MHz', 159.99, 6000, '2 x 16GB', 30, 'DDR5', 5.00, 'Silver', 31.0),
('Patriot Viper Steel 16GB (2x8GB) 3600MHz', 69.99, 3600, '2 x 8GB', 18, 'DDR4', 4.38, 'Gray', 29.5);

INSERT INTO storage VALUES
('Crucial P5 Plus 1TB NVMe SSD', 94.99, '1TB', 'NVMe SSD', 'PCIe 4.0', 0.095, 1024, 'M.2'),
('WD Black 6TB HDD', 169.99, '6TB', 'HDD', 'SATA 6Gb/s', 0.028, 256, '3.5"'),
('Samsung 980 Pro 2TB NVMe SSD', 169.99, '2TB', 'NVMe SSD', 'PCIe 4.0', 0.085, 2048, 'M.2'),
('Seagate Barracuda 2TB HDD', 49.99, '2TB', 'HDD', 'SATA 6Gb/s', 0.025, 256, '3.5"'),
('Samsung 870 EVO 1TB SSD', 79.99, '1TB', 'SATA SSD', 'SATA 6Gb/s', 0.08, 1024, '2.5"');

INSERT INTO video_card VALUES
('NVIDIA GeForce RTX 4070 Ti', 799.99, 'RTX 4070 Ti', 12, 2610, 2310, 'Black', 305),
('AMD Radeon RX 7700 XT', 449.99, 'RX 7700 XT', 12, 2544, 2171, 'Black/Red', 267),
('NVIDIA GeForce RTX 4080', 1199.99, 'RTX 4080', 16, 2505, 2205, 'Black', 336),
('AMD Radeon RX 7900 XTX', 999.99, 'RX 7900 XTX', 24, 2500, 2300, 'Black', 287),
('NVIDIA GeForce RTX 4060', 299.99, 'RTX 4060', 8, 2460, 1830, 'Black', 242);

INSERT INTO pc_case VALUES
('Cooler Master MasterBox TD500 Mesh', 99.99, 'Mid Tower', 'Tempered Glass', 47.5, 'White', 'None', 6),
('Fractal Design Define 7', 179.99, 'Full Tower', 'Solid', 58.2, 'Black', 'None', 8),
('NZXT H510', 74.99, 'Mid Tower', 'Tempered Glass', 42.0, 'Black/Red', 'None', 3),
('Lian Li PC-O11 Dynamic', 139.99, 'Mid Tower', 'Tempered Glass', 45.0, 'Black', 'None', 6),
('Phanteks Eclipse P400A', 89.99, 'Mid Tower', 'Tempered Glass', 46.5, 'White', 'None', 5);

INSERT INTO power_supply VALUES
('Seasonic FOCUS GX-750', 129.99, 750, '80+ Gold', 'Fully Modular', 'ATX', 'Black'),
('Thermaltake Toughpower GF3 1200W', 229.99, 1200,'80+ Platinum', 'Fully Modular', 'ATX', 'Black'),
('Corsair RM850x', 149.99, 850, '80+ Gold', 'Fully Modular', 'ATX', 'White'),
('EVGA SuperNOVA 1000 G5', 199.99, 1000, '80+ Gold', 'Fully Modular', 'ATX', 'Black'),
('Cooler Master MWE Gold 650 V2', 89.99, 650, '80+ Gold', 'Semi Modular', 'ATX', 'Black');

INSERT INTO operating_system VALUES
('Windows 10 Pro', 149.99, '64-bit', 128, 'GB'),
('Windows 11 Home', 139.99, '64-bit', 128, 'GB'),
('Debian 12', 0.00, '64-bit', 'Unlimited', 'GB'),
('Ubuntu 22.04', 0.00, '64-bit', 'Unlimited', 'GB'),
('Fedora 39', 0.00, '64-bit', 'Unlimited', 'GB');

""")

conn.commit()
conn.close()

#proof
print("Database and tables created and populated successfully!")
