import MySQLdb

# Establish MySQL connection
db = MySQLdb.connect(host="localhost",
                     user="root",  # Your MySQL username
                     passwd="19112005",  # Your MySQL password
                     db="smart_home")  # Your database name

# Create a cursor object using the cursor() method
cursor = db.cursor()

# Sample data for devices
devices_data = [
    ('Air Conditioner', 0, 1.5),  # device_name, status, energy_consumption (in kWh)
    ('Lights', 0, 0.1),
    ('Refrigerator', 1, 0.8),
    ('Heater', 0, 2.5),
    ('Washing Machine', 0, 0.6)
]

# SQL query to insert data
insert_query = """
    INSERT INTO devices (device_name, status, energy_consumption) 
    VALUES (%s, %s, %s)
"""

try:
    # Insert data into the table
    cursor.executemany(insert_query, devices_data)

    # Commit changes
    db.commit()

    print("Data inserted successfully!")
except Exception as e:
    # Rollback in case of an error
    db.rollback()
    print(f"Error: {str(e)}")
finally:
    # Close the database connection
    db.close()
