import MySQLdb

# Connect to the MySQL database
db = MySQLdb.connect(host="localhost",
                     user="root",  # Your MySQL username
                     passwd="19112005",  # Your MySQL password
                     db="smart_home")  # Your database name

cursor = db.cursor()

# Sample data to insert into the devices table
devices_data = [
    ('Air Conditioner', 0, 1.5),  # 'Off' status (0), energy consumption 1.5 kWh
    ('Lights', 0, 0.1),  # 'Off' status (0), energy consumption 0.1 kWh
    ('Refrigerator', 1, 0.8),  # 'On' status (1), energy consumption 0.8 kWh
    ('Heater', 0, 2.5),  # 'Off' status (0), energy consumption 2.5 kWh
    ('Washing Machine', 0, 0.6)  # 'Off' status (0), energy consumption 0.6 kWh
]

# SQL query to insert data into the devices table
insert_query = """
    INSERT INTO devices (device_name, status, energy_consumption) 
    VALUES (%s, %s, %s)
"""

try:
    # Execute the insert query for each device in devices_data
    cursor.executemany(insert_query, devices_data)

    # Commit the changes to the database
    db.commit()
    print("Data inserted successfully!")
except Exception as e:
    # Rollback in case of error
    db.rollback()
    print(f"Error: {str(e)}")
finally:
    # Close the database connection
    db.close()
