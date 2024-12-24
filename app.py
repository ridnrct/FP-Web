from flask import Flask, flash, render_template, request, redirect, url_for, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
import MySQLdb
import MySQLdb.cursors
import re
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import atexit
atexit.register(lambda: scheduler.shutdown())

UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = 'secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_fp_cc'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

mysql = MySQL(app)

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
        if len(password) < 8:
            msg = 'Password must be at least 8 characters long!'
            return render_template('register.html', msg=msg, success=False)
        if ' ' in password:
            msg = 'Password cannot contain spaces!'
            return render_template('register.html', msg=msg, success=False)
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

# Route about
@app.route('/about')
def about():
    if 'loggedin' in session:
        return render_template('about.html')
    return redirect(url_for('login'))

# Route riwayat show data
@app.route('/riwayat')
def riwayat():
    if 'loggedinAdmin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_item_history')
        data = cursor.fetchall()
        return render_template('riwayat_item.html', data=data)
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

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    try:
        if 'loggedin' or 'loggedinAdmin' in session:
            if request.method == 'POST':
                # Debugging input data
                print("DEBUG: POST request received")
                title = request.form.get('title', '')
                description = request.form.get('description', '')
                print(f"DEBUG: Title: {title}, Description: {description}")
                
                # Tentukan email berdasarkan sesi
                if 'loggedin' in session:
                    email = session.get('email', '')
                elif 'loggedinAdmin' in session:
                    email = session.get('emailAdmin', '')
                print(f"DEBUG: Email: {email}")

                flash('Pengajuan item berhasil! Menunggu persetujuan admin. Item akan terhapus otomatis setelah tiga hari ditampilkan.', 'success')

                if 'file' in request.files:
                    file = request.files['file']
                    print(f"DEBUG: File received: {file.filename}")

                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        try:
                            file.save(filepath)
                            print(f"DEBUG: File saved to {filepath}")
                        except Exception as e:
                            print(f"ERROR: File save failed: {e}")
                            flash(f"File upload error: {e}", 'danger')
                            return redirect(url_for('additem'))

                        try:
                            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                            # Masukkan data ke tbl_item
                            cursor.execute(
                                'INSERT INTO tbl_item (title, description, img, email) VALUES (%s, %s, %s, %s)',
                                (title, description, filename, email)
                            )
                            mysql.connection.commit()
                            print("DEBUG: Item inserted into database")

                            # Dapatkan item_id yang baru saja ditambahkan
                            cursor.execute('SELECT LAST_INSERT_ID() AS item_id')
                            new_item = cursor.fetchone()
                            new_item_id = new_item['item_id']  # Ini adalah item_id yang baru ditambahkan
                            print(f"DEBUG: New item ID: {new_item_id}")

                            cursor.close()
                            notify_admin()
                        except Exception as e:
                            print(f"ERROR: Database operation failed: {e}")
                            flash(f"Database error: {e}", 'danger')
                            return redirect(url_for('additem'))

                return redirect(url_for('dashboard'))
            return redirect(url_for('additem'))
        else:
            print("DEBUG: User not logged in")
            return redirect(url_for('login'))
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        flash(f"An unexpected error occurred: {e}", 'danger')
        return redirect(url_for('additem'))



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

@app.route('/reject_item/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Ambil data item yang ditolak
    cursor.execute('SELECT * FROM tbl_item WHERE item_id = %s', (item_id,))
    rejected_item = cursor.fetchone()

    if rejected_item:
        # Salin data item ke dalam tabel riwayat dengan status 'rejected'
        cursor.execute(''' 
            INSERT INTO tbl_item_history (item_id, title, description, img, email, status, action_time)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        ''', (
            rejected_item['item_id'],
            rejected_item['title'],
            rejected_item['description'],
            rejected_item['img'],
            rejected_item['email'],
            'rejected'
        ))

        # Hapus data di tabel utama
        cursor.execute('DELETE FROM tbl_item WHERE item_id = %s', (item_id,))
        
        # Commit perubahan
        mysql.connection.commit()

        # Kirimkan email pemberitahuan
        subject = "Item Anda Ditolak"
        body = f"Hallo,\n\nItem Anda dengan judul \"{rejected_item['title']}\" telah ditolak. Jika Anda memiliki pertanyaan, silakan hubungi admin.\n\nTerima kasih."
        send_email(rejected_item['email'], subject, body)
    else:
        return "Item not found", 404  # Tambahkan respons jika item tidak ditemukan

    cursor.close()
    return redirect(url_for('admin_dashboard', reload=True))


@app.route('/accept_item/<int:item_id>', methods=['POST'])
def accept_item(item_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Ambil data item yang diterima
    cursor.execute('SELECT * FROM tbl_item WHERE item_id = %s', (item_id,))
    accepted_item = cursor.fetchone()

    if accepted_item:
        # Debug: Periksa item yang ditemukan
        print("Item diterima:", accepted_item)

        timestamp_column = datetime.now()

        try:
            # Salin data item ke dalam tbl_item_user
            cursor.execute('''
                INSERT INTO tbl_item_user (item_id, title, description, img, email, status, timestamp_column)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                accepted_item['item_id'],
                accepted_item['title'],
                accepted_item['description'],
                accepted_item['img'],
                accepted_item['email'],
                'accepted',
                timestamp_column
            ))

            # Hapus data item dari tabel tbl_item
            cursor.execute('DELETE FROM tbl_item WHERE item_id = %s', (item_id,))

            # Commit perubahan
            mysql.connection.commit()

            # Kirimkan email pemberitahuan
            subject = "Item Anda Diterima"
            body = f"Hallo,\n\nItem Anda dengan judul \"{accepted_item['title']}\" telah diterima dan ditampilkan di dashboard.\n\nTerima kasih."
            send_email(accepted_item['email'], subject, body)

        except Exception as e:
            # Debug: Jika terjadi error, tampilkan pesan kesalahan
            print("Error saat menerima item:", e)
            mysql.connection.rollback()

    else:
        return "Item not found", 404  # Tambahkan respons jika item tidak ditemukan

    cursor.close()
    return redirect(url_for('admin_dashboard', reload=True))



def send_email(to_email, subject, body):
    sender_email = app.config['MAIL_USERNAME']
    sender_password = app.config['MAIL_PASSWORD']

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print(f"Email berhasil dikirim ke {to_email}")
    except Exception as e:
        print(f"Gagal mengirim email ke {to_email}: {e}")

def move_accepted_items():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='db_fp_cc')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    three_days_ago = datetime.now() - timedelta(days=3)

    cursor.execute('DELETE FROM tbl_item_user WHERE status = %s AND timestamp_column <= %s', 
                ('accepted', three_days_ago))
    accepted_items = cursor.fetchall()

    for item in accepted_items:
        cursor.execute('''
            INSERT INTO tbl_item_history (item_id, title, description, img, email, status) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            item['item_id'], 
            item['title'], 
            item['description'], 
            item['img'], 
            item['email'], 
            'accepted'
        ))
        cursor.execute('DELETE FROM tbl_item_user WHERE item_id = %s', (item['item_id'],))

    conn.commit()
    cursor.close()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(move_accepted_items, 'interval', seconds=30)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
