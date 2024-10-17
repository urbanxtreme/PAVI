from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '19112005'
app.config['MYSQL_DB'] = 'smart_home'
mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM devices")
        devices = cur.fetchall()
        cur.close()
        return jsonify(devices)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/devices/<device_name>/<action>', methods=['POST'])
def control_device(device_name, action):
    try:
        cur = mysql.connection.cursor()
        if action == 'on':
            cur.execute("UPDATE devices SET status = 1 WHERE device_name = %s", (device_name,))
        elif action == 'off':
            cur.execute("UPDATE devices SET status = 0 WHERE device_name = %s", (device_name,))
        mysql.connection.commit()
        cur.close()
        return jsonify({device_name: action})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/energy', methods=['GET'])
def get_energy():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(energy_consumption) FROM devices WHERE status = 1")
        total_energy = cur.fetchone()[0]
        total_energy = total_energy if total_energy else 0
        cur.close()
        return jsonify({"total_energy_consumption": total_energy})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
