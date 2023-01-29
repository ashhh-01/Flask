from flask import Flask
from flask import render_template
import requests,datetime

app=Flask(__name__)


@app.route("/blog")
def get_blog():
    response=requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    allblog=response.json()
    return render_template("index.html",allblog=allblog)


@app.route("/guess/<name>")
def guess(name):
    year=datetime.datetime.now().year
    ageResp=requests.get(f"https://api.agify.io/?name={name}")
    genderResp=requests.get(f"https://api.genderize.io/?name={name}")
    gender=genderResp.json()["gender"]
    age=ageResp.json()["age"]
    return render_template("guess.html",year=year,name=name,age=age,gender=gender)

if __name__=="__main__":
    app.run(debug=True)