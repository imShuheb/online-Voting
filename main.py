from flask import Flask, app, redirect,request,flash,session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from mysql.connector import (connection)
from flask_login import login_manager,login_required,LoginManager,logout_user,login_user
from flask_login import UserMixin
from flask_mail import Mail
import os,random

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = ''
)

mail = Mail(app)
app.config['UPLOAD_FOLDER'] = r''
app.config['SQLALCHEMY_DATABASE_URI'] = 'Your_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

con=connection.MySQLConnection(user='root', password='',
                                 host='127.0.0.1',
                                 port = '3307',
                                 database='voter',
                                 auth_plugin='mysql_native_password')
cur= con.cursor()

login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Voter.query.get(int(id)) or Admin.query.get(int(id))

class Voter(db.Model,UserMixin):
    __tablename__ = 'Voter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    name = db.Column(db.String(64))
    mobile = db.Column(db.String(64))
    email = db.Column(db.String(64),unique=True, index=True)
    adhar = db.Column(db.String(50))
    valid = db.Column(db.String(20))

class Admin(db.Model,UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    
class Candidit(db.Model,UserMixin):
    __tablename__ = 'candidit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    name = db.Column(db.String(64))
    mobile = db.Column(db.String(64))
    address = db.Column(db.String(200))
    photo = db.Column(db.String(60))
    qualification = db.Column(db.String(60))
    email = db.Column(db.String(64), index=True)
    adhar = db.Column(db.String(60))
    votes = db.Column(db.String(6000))

@app.route('/home')
@login_required
def home():
    cand = Candidit.query.all()
    return render_template('home.html',cand = cand)

@app.route('/vote/<int:id>')
def cal(id):
    result = Candidit.query.filter_by(id = id).first()
    no = result.votes 
    no += str(1)
    sql = "UPDATE Candidit SET votes = %s WHERE id = %s"
    val = (no,id)
    cur.execute(sql, val)
    con.commit()
    print(len(no))
    flash('Voted Successfully', category='success')
    return redirect('/logout')

@app.route('/delete/<int:id>',methods = ['GET','POST'])
@login_required
def delete(id):
    cand = Candidit.query.filter_by(id = id).first()
    if cand:
        db.session.delete(cand)
        db.session.commit()
        flash('Candidit Removed',category='error')
    return redirect('/edit')

@app.route('/result',methods=['GET','POST'])
@login_required
def result():
    cand = Candidit.query.all()
    return render_template('results.html',cand = cand)

@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    cand = Candidit.query.all()
    return render_template('edit.html',cand = cand)

@app.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name')
        phone = request.form.get('phone')
        adhar = request.form.get('adhar')
        qualify = request.form.get('qualify')
        address =request.form.get('address')
        files = request.files['cand_pic']

        if not files:
            flash('Image not uploaded.', category='error')
            return redirect('/admin')
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(files.filename)))  
        filename = secure_filename(files.filename)

        data = Candidit(name = username,email = email,mobile = phone,adhar = adhar,address = address,qualification = qualify,photo = filename,votes = "1")
        db.session.add(data)
        db.session.commit()
        return redirect('/admin')
    return render_template('admin.html')

# this is login model
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        adhar = request.form.get('adhar')
        otp = request.form.get('otp')
        voter = Voter.query.filter_by(adhar = adhar).first()
        if voter:
            if voter.adhar == adhar and voter.valid == otp :
                login_user(voter, remember=True)
                return redirect('/home')
            else:
                flash('Incorrect otp or password',category='error')
                return redirect('/login')
    return render_template("login.html")

@app.route('/admin_log',methods=['GET','POST'])
def adlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email = username).first()
        if admin:
            if admin.email == username and admin.password == password :
                login_user(admin, remember=True)
                return redirect('/admin')
            else:
                flash('Incorrect password',category='error')
                return redirect('/login')
    return render_template("admin_log.html")

#this is log_out model
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
        
# this is the sign up model 
@app.route('/',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name')
        phone = request.form.get('phone')
        adhar = request.form.get('adhar')
        no = votvalid(adhar)
        val = valid(email)
        if (no == 1):
            flash('already Voted',category='error')
            return redirect('/signin')
        elif (val == 1):
            flash('Already Voted', category='error')
            return redirect('/signin')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(adhar) < 12:
            flash('Adhar No must be at least 12 characters.', category='error')
        else:
            ran = random.randrange(500000)
            data = Voter(mobile = phone,name = username ,email = email , adhar = adhar,valid = ran)
            sub = 'Registeration OTP'
            mail.send_message(subject=sub,
                      body="This is the OTP __"+str(ran)+"""__ If you want you can share since you can 
                      login only once through this OTP""",
                      recipients = email.split(),
                      sender=email)
            db.session.add(data)
            db.session.commit()
            return redirect('/login')
    return  render_template("sign_up.html")

def votvalid(adhar):
    voter = Voter.query.filter_by(adhar = adhar).all()
    if voter:
        return 1
    else:
        return 0

def valid(email):
    email = Voter.query.filter_by(email = email).all()
    if email:
        return 1
    else:
        return 0
  
if __name__ == '__main__':
    app.run(debug=True,port=5000)

