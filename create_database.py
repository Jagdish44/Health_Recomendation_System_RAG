import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('diet_recommendations.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_conditions (
    id INTEGER PRIMARY KEY,
    condition TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY,
    name TEXT,
    calories INTEGER,
    protein INTEGER,
    fat INTEGER,
    carbs INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS diet_recommendations (
    id INTEGER PRIMARY KEY,
    condition_id INTEGER,
    food_id INTEGER,
    FOREIGN KEY (condition_id) REFERENCES health_conditions (id),
    FOREIGN KEY (food_id) REFERENCES foods (id)
)
''')

# Insert sample data
conditions = [
    ('Diabetes',), 
    ('Hypertension',),
    ('Obesity',),
    ('High Cholesterol',),
    ('Anemia',),
    ('Osteoporosis',),
    ('Celiac Disease',)
]

foods = [
    ('Broccoli', 55, 3.7, 0.6, 11.2),
    ('Chicken Breast', 165, 31, 3.6, 0),
    ('Oatmeal', 150, 5, 3, 27),
    ('Apple', 95, 0.5, 0.3, 25),
    ('Almonds', 576, 21, 49, 22),
    ('Spinach', 23, 2.9, 0.4, 3.6),
    ('Salmon', 206, 22, 12, 0),
    ('Quinoa', 120, 4.1, 1.9, 21.3),
    ('Lentils', 116, 9, 0.4, 20),
    ('Greek Yogurt', 59, 10, 0.4, 3.6),
    ('Brown Rice', 123, 2.7, 1, 25.6),
    ('Blueberries', 57, 0.7, 0.3, 14.5),
    ('Eggs', 78, 6.3, 5.3, 0.6),
    ('Sweet Potato', 86, 1.6, 0.1, 20.1),
    ('Avocado', 160, 2, 15, 9),
    ('Beef', 250, 26, 15, 0),
    ('Chickpeas', 164, 8.9, 2.6, 27.4),
    ('Carrots', 41, 0.9, 0.2, 9.6),
    ('Walnuts', 654, 15, 65, 14),
    ('Banana', 89, 1.1, 0.3, 23)
]

cursor.executemany('INSERT OR IGNORE INTO health_conditions (condition) VALUES (?)', conditions)
cursor.executemany('INSERT OR IGNORE INTO foods (name, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?)', foods)

recommendations = [
    (1, 1),  # Diabetes -> Broccoli
    (1, 4),  # Diabetes -> Apple
    (1, 3),  # Diabetes -> Oatmeal
    (1, 6),  # Diabetes -> Spinach
    (2, 1),  # Hypertension -> Broccoli
    (2, 3),  # Hypertension -> Oatmeal
    (2, 6),  # Hypertension -> Spinach
    (2, 12),  # Hypertension -> Blueberries
    (3, 1),  # Obesity -> Broccoli
    (3, 2),  # Obesity -> Chicken Breast
    (3, 7),  # Obesity -> Salmon
    (3, 13), # Obesity -> Eggs
    (4, 7),  # High Cholesterol -> Salmon
    (4, 10), # High Cholesterol -> Greek Yogurt
    (4, 11), # High Cholesterol -> Brown Rice
    (4, 5),  # High Cholesterol -> Almonds
    (5, 6),  # Anemia -> Spinach
    (5, 7),  # Anemia -> Salmon
    (5, 10), # Anemia -> Greek Yogurt
    (5, 16), # Anemia -> Beef
    (6, 1),  # Osteoporosis -> Broccoli
    (6, 10), # Osteoporosis -> Greek Yogurt
    (6, 14), # Osteoporosis -> Sweet Potato
    (6, 17), # Osteoporosis -> Chickpeas
    (7, 8),  # Celiac Disease -> Quinoa
    (7, 9),  # Celiac Disease -> Lentils
    (7, 10), # Celiac Disease -> Greek Yogurt
    (7, 11), # Celiac Disease -> Brown Rice
]

cursor.executemany('INSERT OR IGNORE INTO diet_recommendations (condition_id, food_id) VALUES (?, ?)', recommendations)

conn.commit()
conn.close()
