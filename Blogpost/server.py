from flask import Flask,render_template
import requests,datetime
from post import Post

app=Flask(__name__)


@app.route("/")
def blogs():
    year=datetime.datetime.now().year
    URL="https://api.npoint.io/9d59da5e1bd2839a8309"
    response=requests.get(URL)
    allblog=response.json()
    return render_template("index.html",posts=allblog,year=year)

@app.route("/post/<int:index>")
def show_post(index):
    URL="https://api.npoint.io/9d59da5e1bd2839a8309"
    response=requests.get(URL)
    allblog=response.json()
    return render_template("post.html",index=index,allblog=allblog)

if __name__=="__main__":
    app.run(debug=True)