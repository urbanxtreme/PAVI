import MySQLdb
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="19112005",
                     db="smart_home")
cursor = db.cursor()
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
    cursor.executemany(insert_query, devices_data)
    db.commit()
    print("Data inserted successfully!")
except Exception as e:
    db.rollback()
    print(f"Error: {str(e)}")
finally:
    db.close()
