from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'your_password'  # Your MySQL password
app.config['MYSQL_DB'] = 'smart_home'  # The name of your database

mysql = MySQL(app)


# Route to render the main dashboard page
@app.route('/')
def home():
    return render_template('index.html')  # This will load the HTML page


# Route to fetch all devices
@app.route('/devices', methods=['GET'])
def get_devices():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM devices")
    devices = cur.fetchall()
    cur.close()
    # Returning the data as JSON to the frontend
    return jsonify(devices)


# Route to control a device (turn on/off)
@app.route('/devices/<device_name>/<action>', methods=['POST'])
def control_device(device_name, action):
    cur = mysql.connection.cursor()

    # Update the status based on the action
    if action == 'on':
        cur.execute(f"UPDATE devices SET status = 1 WHERE device_name = '{device_name}'")
    elif action == 'off':
        cur.execute(f"UPDATE devices SET status = 0 WHERE device_name = '{device_name}'")

    mysql.connection.commit()
    cur.close()

    # Return the updated status
    return jsonify({device_name: action})


# Route to fetch total energy consumption
@app.route('/energy', methods=['GET'])
def get_energy():
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(energy_consumption) FROM devices WHERE status = 1")
    total_energy = cur.fetchone()[0]
    cur.close()

    # Return total energy consumption as JSON
    return jsonify({"total_energy_consumption": total_energy})


if __name__ == '__main__':
    app.run(debug=True)
