from flask import Flask,render_template, url_for, request,redirect, session
import requests
from passlib.hash import pbkdf2_sha256
import sqlite3 as sql
import os
import hashlib


database='my.db'
table='entries'

def get_db(database):
    if not os.path.isfile(database):
        conn=sql.connect(database)
        query='''CREATentry (fname TEXT,lname TEXT,email TEXT,
                password REAL)'''
        conn.execute(query)
    conn=sql.connect(database)
    return conn

def insert_data(database,data):
    with sql.connect(database) as conn:
        cursor=conn.cursor()
        query=f'''INSERT INTO entry (fname,lname,email,
                password) VALUES (?,?,?,?)'''
        cursor.execute(query,data)
        conn.commit()

app=Flask(__name__)

# To convert the user input password as MD5
def check_password(hash_pass,password):
    return hash_pass == pbkdf2_sha256.hash(password.encode())

# Takes the inputed username and passwords as arguments, and compare them against the users table
def validate(Email, password):
    conn = sql.connect(database)
    completion = True
    with conn:


        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entry")
        rows = cursor.fetchall()
        for row in rows:

            dbUser = row[2]
            dbPass = row[3]
            if dbUser == Email:

                completion = check_password(dbPass, password)

        return completion

@app.route('/createDB')
def createDB():
    if not os.path.isfile(database):
        conn=sql.connect(database)
    return '<h1> Database Successfully Created!'

@app.route('/createTable')
def createTable():
    conn=sql.connect(database)
    query=f'''CREATE TABLE entry (fname TEXT,lname TEXT,email TEXT,
                password REAL)'''
    conn.execute(query)
    conn.close()
    return f'<h1> Table: entry Successfully Created!'


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST' and 'email' in request.form and 'password' in request.form:

        email=request.form.get('email')
        password=request.form.get('password')
        hash_pass=pbkdf2_sha256.hash(password)

        with sql.connect(database) as conn:
            conn=sql.connect(database)
            cursor=conn.cursor()
            query=f"SELECT * from entry WHERE email='{email}' AND Password = '{password}';"
            cursor.execute(query)
            data={'email':email , 'password':password}
            completion = validate(email, password)
            if completion == True:
                return "failed" 
                
            else:
                return render_template('index.html', data=data) 
                
            
    return render_template('login.html')



        # if not isinstance(password,str):
        #     password=str(password)
            
        #     insert_data(database,data)
            # return render_template('index.html', data=data)
    # return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
     if request.method=='POST':
        first=request.form.get('fname')
        last=request.form.get('lname')
        email=request.form.get('email')
        password=request.form.get('password')
        conn=get_db(database)
        # Create cursor
        
        if not isinstance(password,str):
            password=str(password)
        hash_pass=pbkdf2_sha256.hash(password)
        # data={'first':first,'last':last,'email':email,'password':hash_pass}
        cursor=conn.cursor()
        query='''INSERT INTO entry (fname,lname,email,
                password) VALUES (?,?,?,?)'''
        # data={'first':first,'last':last,'email':email,'password':hash_pass}
        data=[first,last,email,hash_pass]
        cursor.execute(query,data)
        conn.commit()
        conn.close()
        return render_template('display_registered.html',data=data)

     return render_template('register.html')

@app.route('/news')
def news():
    url="https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=b179b8999c434e45b86d1e01e9232015"
    r=requests.get(url).json()
    case={
        'articles':r['articles']
    }
    return render_template("news.html", case=case)
    


@app.route('/contact')
def contact():
    return render_template('contact.html')
    


@app.route('/display')
def display():
    
    with sql.connect(database) as conn:
        cursor=conn.cursor()
        
        query=f"select * from entry"        
        cursor.execute(query)
        data=cursor.fetchall()
        # print(data)

        return render_template('display.html',data=data,info="Registered")
  

if __name__=='__main__':
    app.run(debug=True,port=5004)
