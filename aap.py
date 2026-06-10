from flask import Flask,render_template,request,redirect
import mysql.connector

app = Flask(__name__)

conn=mysql.connector.connect(
host="localhost",
user="root",
password="",
database="guards_monitoring"
)

cursor=conn.cursor()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():

    email=request.form['email']
    password=request.form['password']

    query="SELECT * FROM guards WHERE email=%s AND password=%s"

    cursor.execute(query,(email,password))

    user=cursor.fetchone()

    if user:
        return redirect('/dashboard')
    else:
        return "Invalid Login"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

app.run(debug=True)
