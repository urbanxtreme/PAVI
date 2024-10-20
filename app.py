from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '19112005'
app.config['MYSQL_DB'] = 'smart_home'
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Initialize MySQL and LoginManager
mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0])
    return None

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if not username or not password or not email:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                       (username, hashed_password, email))
            mysql.connection.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except MySQLdb.IntegrityError:
            mysql.connection.rollback()
            flash('Username already exists. Please choose another one.', 'danger')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error: ' + str(e), 'danger')
        finally:
            cur.close()
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            login_user(User(user[0]))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home route
@app.route('/')
@login_required
def home():
    return render_template('index.html')

# Get devices route
@app.route('/devices', methods=['GET'])
@login_required
def get_devices():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM devices")
    devices = cur.fetchall()
    cur.close()
    return jsonify(devices)

# Control device route
@app.route('/devices/<device_name>/<action>', methods=['POST'])
@login_required
def control_device(device_name, action):
    cur = mysql.connection.cursor()
    if action == 'on':
        cur.execute("UPDATE devices SET status = 1 WHERE device_name = %s", (device_name,))
    elif action == 'off':
        cur.execute("UPDATE devices SET status = 0 WHERE device_name = %s", (device_name,))
    mysql.connection.commit()
    cur.close()
    return jsonify({device_name: action})

# Energy route
@app.route('/energy', methods=['GET'])
@login_required
def get_energy():
    cur = mysql.connection.cursor()
    cur.execute("SELECT device_name, energy_consumption, status FROM devices")
    devices = cur.fetchall()
    cur.close()
    energy_data = []
    for device in devices:
        energy_data.append({
            'device_name': device[0],
            'energy_consumption': device[1],
            'status': 'On' if device[2] else 'Off'
        })
    return render_template('energy.html', energy_data=energy_data)

# Electricity usage route
@app.route('/electricity_usage')
@login_required
def electricity_usage():
    cur = mysql.connection.cursor()
    cur.execute("SELECT device_name, energy_consumption, status FROM devices")
    devices = cur.fetchall()
    cur.close()
    electricity_data = []
    for device in devices:
        electricity_data.append({
            'device_name': device[0],
            'energy_consumption': device[1],
            'status': 'On' if device[2] else 'Off'
        })
    return render_template('electricity_usage.html', electricity_data=electricity_data)

# Water usage route
@app.route('/water_usage')
@login_required
def water_usage():
    water_data = [
        {'device_name': 'Water Heater', 'water_consumption': 30},
        {'device_name': 'Washing Machine', 'water_consumption': 50}
    ]
    return render_template('water_usage.html', water_data=water_data)

# Emergency shutdown route
@app.route('/emergency_shutdown', methods=['POST'])
@login_required
def emergency_shutdown():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE devices SET status = 0")
    mysql.connection.commit()
    cur.close()
    flash("Emergency shutdown executed successfully!", 'success')
    return redirect(url_for('home'))

# Error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
