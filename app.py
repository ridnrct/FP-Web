from flask import Flask, flash, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import re
from datetime import datetime, timedelta
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
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

# Konfigurasi Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ridhanurrachmat240802@gmail.com'  
app.config['MAIL_PASSWORD'] = 'wnhw whcf moqn ioqc'    
mail = Mail(app)

# Serializer untuk membuat token verifikasi
serializer = URLSafeTimedSerializer(app.secret_key)

# Route User Login
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_login WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()
        if account:
            if not account['is_verified']:
                msg = 'Please verify your email before logging in.'
            else:
                session['loggedin'] = True
                session['email'] = account['email']
                session['username'] = account['username']
                return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect email / password!'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'username' in request.form:
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_login WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Email is already registered!'
        else:
            token = serializer.dumps(email, salt='email-confirm-salt')

            verification_url = url_for('confirm_email', token=token, _external=True)
            try:
                message = Message('Confirm Your Email', sender='your_email@gmail.com', recipients=[email])
                message.body = f'Hi {username},\n\nPlease confirm your email by clicking on the link below:\n{verification_url}\n\nIf you did not request this, please ignore this email.'
                mail.send(message)

                msg = 'A confirmation email has been sent to your email address. Please confirm your email to activate your account.'
            except Exception as e:
                msg = f"Error sending email: {e}"

            cursor.execute(
                'INSERT INTO user_login (email, password, username, is_verified) VALUES (%s, %s, %s, %s)',
                (email, password, username, False)
            )
            mysql.connection.commit()
            cursor.close()
    return render_template('register.html', msg=msg, success=False)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=3600) 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE user_login SET is_verified = %s WHERE email = %s', (True, email))
        mysql.connection.commit()
        cursor.close()

        flash('Your email has been confirmed. You can now log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('register'))


@app.route('/admin_login', methods=['GET', 'POST'])
def log_admin():
    msg = ''
    if request.method == 'POST' and 'emailAdmin' in request.form and 'passwordAdmin' in request.form:
        email = request.form['emailAdmin']
        password = request.form['passwordAdmin']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        session.pop('loggedin', None)
        cursor.execute('SELECT * FROM admin_login WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()
        if account:
            session['loggedinAdmin'] = True
            session['emailAdmin'] = account['email']
            session['usernameAdmin'] = account['username']
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect email or password!'
    return render_template('log_admin.html', msg=msg)


@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    if 'loggedinAdmin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item')
        data = cursor.fetchall()
        return render_template('admin.html', data=data)
    return redirect(url_for('log_admin'))

@app.route('/admin', methods=['GET'])
def admin():
    if 'loggedinAdmin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item_user')
        data = cursor.fetchall()
        return render_template('dashboard_admin.html', data=data)
    return redirect(url_for('log_admin'))

# Route Logout User and Admin
@app.route('/logout')
def logout():
    if 'loggedin' or 'loggedinAdmin' in session:
        session.clear()
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
    if 'loggedinAdmin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item_user')
        data = cursor.fetchall()
        return render_template('dashboard_admin.html', data=data)
    elif 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item_user')
        data = cursor.fetchall()
        return render_template('dashboard.html', data=data)
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
    if 'loggedin' or 'loggedinAdmin' in session:
        return render_template('add_item.html')
    msg = 'Please login !'
    return render_template('login.html', msg = msg)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route add item add data
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'loggedin' or 'loggedinAdmin' in session:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            if 'loggedin' in session:
                email = session['email']
            elif 'loggedinAdmin' in session:
                email = session['emailAdmin']  
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
                    notify_admin()
                    flash('Pengajuan item berhasil! Menunggu persetujuan admin.', 'success')
            return redirect(url_for('dashboard'))
        print("Redirecting to additem")
        return redirect(url_for('additem'))
    print("Redirecting to login")
    return redirect(url_for('login'))

def notify_admin():
    sender_email = "ridhanurrachmat240802@gmail.com"  
    sender_password = "wnhw whcf moqn ioqc" 

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT email FROM admin_login')
    admins = cursor.fetchall()

    subject = "Notifikasi: Item Baru Menunggu Persetujuan"
    body = "Ada item baru yang membutuhkan persetujuan Anda. Silakan login ke dashboard untuk meninjau."

    for admin in admins:
        recipient_email = admin['email']

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  
                server.login(sender_email, sender_password) 
                server.sendmail(sender_email, recipient_email, message.as_string())  
            print(f"Notifikasi berhasil dikirim ke {recipient_email}")
        except Exception as e:
            print(f"Gagal mengirim email ke {recipient_email}: {e}")
    
    cursor.close()

# Route Reject
@app.route('/reject_item/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tbl_item WHERE id = %s', (item_id,))
    rejected_item = cursor.fetchone()
    cursor.execute('DELETE FROM tbl_item WHERE id = %s', (item_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin_dashboard', reload=True))

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
        return redirect(url_for('admin_dashboard', reload=True))


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
    return redirect(url_for('admin_dashboard', reload=True))

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