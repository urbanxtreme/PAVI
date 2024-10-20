import MySQLdb
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '19112005',
    'db': 'smart_home'
}

devices_data = [
    ('Air Conditioner', 0, 1.5),
    ('Lights', 0, 0.1),
    ('Refrigerator', 1, 0.8),
    ('Heater', 0, 2.5),
    ('Washing Machine', 0, 0.6)
]

insert_query = """
    INSERT INTO devices (device_name, status, energy_consumption) 
    VALUES (%s, %s, %s)
"""

try:
    with MySQLdb.connect(**db_config) as db:
        cursor = db.cursor()
        cursor.executemany(insert_query, devices_data)
        db.commit()
        logging.info("Data inserted successfully!")
except MySQLdb.Error as e:
    logging.error(f"Database error: {e}")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
