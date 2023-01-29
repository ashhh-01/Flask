from flask import Flask,request
from flask import render_template

app=Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def data():
    if request.method=="POST":
        username= request.form["username"]
        password=request.form["password"]
        return f'<h1>Username:{username}, password:{password}</h1>'
if __name__=="__main__":
    app.run(debug=True)