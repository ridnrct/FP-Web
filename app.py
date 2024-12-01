from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import re
from datetime import datetime, timedelta
import schedule
import time
UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = 'secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'barang_hilang'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

mysql = MySQL(app)

# Route User Login
@app.route('/', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_login WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['email']
            session['username'] = account['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tbl_item_user')
            data = cursor.fetchall()
            return render_template('dashboard.html', data=data)
        else:
            msg = 'Incorrect email / password !'
    return render_template('login.html', msg = msg)

# Route Admin Show Data
@app.route('/admin')
def admin():
    if 'loggedinAdmin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item')
        data = cursor.fetchall()
        return render_template('admin.html', data=data)
    msg = 'Please login !'
    return render_template('log_admin.html', msg=msg)

# Route Admin Login
@app.route('/admin', methods=['POST'])
def log_admin():
    if request.method == 'POST' and 'emailAdmin' in request.form and 'passwordAdmin' in request.form:
        email = request.form['emailAdmin']
        password = request.form['passwordAdmin']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin_login WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()
        if account:
            session['loggedinAdmin'] = True
            session['emailAdmin'] = account['email']
            session['passwordAdmin'] = account['password']
            session['usernameAdmin'] = account['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tbl_item')
            data = cursor.fetchall()
            return render_template('admin.html', data=data)
    return render_template('log_admin.html', msg='Login failed')

# Route Logout User and Admin
@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('loggedinAdmin', None)
        return redirect(url_for('login'))
    msg = 'Please login !'
    return render_template('login.html', msg = msg)

# Route upload image on folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route dashboard show data
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item_user')
        data = cursor.fetchall()
        return render_template('dashboard.html', data=data)
    if 'loggedinAdmin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item_user')
        data = cursor.fetchall()
        return render_template('dashboard_admin.html', data=data)
    return redirect(url_for('login'))

#Delete item as Admin
@app.route('/delete_item', methods=['POST'])
def delete_item():
    if request.method == 'POST':
        item_id = request.form['deleteItemId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM tbl_item_user WHERE id=%s', (item_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboard', reload=True))

# Route add item session
@app.route('/add_item')
def additem():
    if 'loggedin' in session:
        return render_template('add_item.html')
    msg = 'Please login !'
    return render_template('login.html', msg = msg)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route add item add data
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    print("Inside add_item route")
    if 'loggedin' in session:
        print("User is logged in")
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            email = session['email']
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(
                        'INSERT INTO tbl_item (title, description, img, email) VALUES (%s, %s, %s, %s)',
                        (title, description, filename, email)
                    )
                    mysql.connection.commit()
                    cursor.close()
            print("Redirecting to dashboard")
            return redirect(url_for('dashboard'))
        print("Redirecting to additem")
        return redirect(url_for('additem'))
    print("Redirecting to login")
    return redirect(url_for('login'))

# Route Reject
@app.route('/reject_item/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tbl_item WHERE id = %s', (item_id,))
    rejected_item = cursor.fetchone()
    cursor.execute('DELETE FROM tbl_item WHERE id = %s', (item_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin', reload=True))

# Route Edit
@app.route('/edit_item', methods=['POST'])
def edit_item():
    if request.method == 'POST':
        new_title = request.form['editTitle']
        new_description = request.form['editDescription']
        item_id = request.form['editItemId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE tbl_item SET title=%s, description=%s WHERE id=%s', (new_title, new_description, item_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin', reload=True))


# Route Accept
@app.route('/accept_item/<int:item_id>', methods=['POST'])
def accept_item(item_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tbl_item WHERE id = %s', (item_id,))
    accepted_item = cursor.fetchone()
    timestamp_column = datetime.now()
    cursor.execute('INSERT INTO tbl_item_user (id, title, description, img, email, status, timestamp_column) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                   (accepted_item['id'], accepted_item['title'], accepted_item['description'], accepted_item['img'], accepted_item['email'], 'accepted', timestamp_column))
    cursor.execute('DELETE FROM tbl_item WHERE id = %s', (item_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin', reload=True))

def delete_accepted_data():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            delete_query = "DELETE FROM tbl_item_user WHERE status = 'accepted' AND timestamp_column < %s"
            threshold_time = datetime.now() - timedelta(minutes=1)
            cursor.execute(delete_query, (threshold_time,))
            mysql.connection.commit()
            print(f"Old accepted data deleted at {datetime.now()}")
        except Exception as e:
            print(f"Error deleting old accepted data: {e}")
        finally:
            cursor.close()

schedule.every(1).minutes.do(delete_accepted_data)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
        app.run(debug=True)