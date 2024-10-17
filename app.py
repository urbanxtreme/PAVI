from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = '19112005'  # Your MySQL password
app.config['MYSQL_DB'] = 'smart_home'  # The name of your database

# Flask-Login configurations
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in

mysql = MySQL(app)

# User class
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
        return User(user[0])  # Return user instance based on the fetched ID
    return None

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')  # Use get to avoid KeyError

        # Check if all required fields are present
        if not username or not password or not email:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                       (username, hashed_password, email))
            mysql.connection.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except MySQLdb.IntegrityError as e:
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

        if user and check_password_hash(user[2], password):  # user[2] is the password hash
            login_user(User(user[0]))  # user[0] is the user ID
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Route to render the main dashboard page
@app.route('/')
@login_required
def home():
    return render_template('index.html')  # This will load the HTML page

# Route to fetch all devices
@app.route('/devices', methods=['GET'])
@login_required
def get_devices():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM devices")
    devices = cur.fetchall()
    cur.close()
    return jsonify(devices)

# Route to control a device (turn on/off)
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

# Route to fetch total energy consumption
@app.route('/energy', methods=['GET'])
@login_required
def get_energy():
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(energy_consumption) FROM devices WHERE status = 1")
    total_energy = cur.fetchone()[0]
    cur.close()
    return jsonify({"total_energy_consumption": total_energy})

if __name__ == '__main__':
    app.run(debug=True)
