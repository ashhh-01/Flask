from flask import Flask,render_template,request
import requests
import smtplib 
import os
from dotenv import load_dotenv


API="https://api.npoint.io/06a0f4462dd0209c9938"
response=requests.get(API).json()
load_dotenv("../../../Python/Python/Python Env/env/.env")
EMAIL=os.getenv("EMAIL1")
PASSWORD=os.getenv("PASSWORD1")

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",allpost=response)

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/post.html/<int:index>")
def post(index):
    for blog in response:
        if blog["id"]==index:
            requested_blog=blog
    return render_template("post.html",post=requested_blog)

@app.route("/contact.html",methods=["GET","POST"])
def recieved_data():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        message=request.form["message"]
        phone=request.form["phone"]
        sendemail(name,email,phone,message)
        return render_template("contact.html",sent_message=True)
    return render_template("contact.html",sent_message=False)

def sendemail(name,email,phone,message):
    email_msg=f"Subject:New Message\n\nName: {name}\n Email:{email}\nPhone:{phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(EMAIL,PASSWORD)
        connection.sendmail(from_addr=email,to_addrs=email,msg=email_msg)

if __name__=="__main__":
    app.run(debug=True)