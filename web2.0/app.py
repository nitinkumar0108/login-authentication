import email
from click import password_option
from flask import Flask,render_template, url_for, request
import requests

from passlib.hash import pbkdf2_sha256

app=Flask(__name__)



@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')





    
@app.route('/register',methods=['GET','POST'])
def register():
     if request.method=='POST':
        first=request.form.get('fname')
        last=request.form.get('lname')
        email=request.form.get('email')
        password=request.form.get('password')
        if not isinstance(password,str):
            password=str(password)
        hash_pass=pbkdf2_sha256.hash(password)
        data={'first':first,'last':last,'email':email,'password':hash_pass}
        return render_template('display_registered.html',data=data)

     return render_template('register.html')
    
@app.route('/login', methods=['POST'])
def contact():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        if not isinstance(password,str):
            password=str(password)
            data={'email':email , 'password':password}
            return render_template('index.html', data=data)
    return render_template('contact.html')

@app.route('/display')
def display():
    user1={'f':'Asif','l':'Iqbal','e':'asif@gmail.com','p':pbkdf2_sha256.hash('9098')}
    user2={'f':'Nitin','l':'Kumar','e':'nitin@gmail.com','p':pbkdf2_sha256.hash('5678')}
    user3={'f':'Sahil','l':'Bhardwaj','e':'sahil@gmail.com','p':pbkdf2_sha256.hash('5678')}
    users=[
            user1,
            user2,
            user3
          ]
    return render_template('display.html',users=users)

if __name__=='__main__':
    app.run(debug=True,port=5001)