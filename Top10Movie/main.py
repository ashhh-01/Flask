from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os 
from dotenv import load_dotenv

load_dotenv("../../../Python/Python/Python Env/env/.env")

TMBDAPI=os.getenv("TMDBAPI")
APIACCESS=os.getenv("APIACCESS")

URL=f"https://api.themoviedb.org/3/search/movie?api_key={TMBDAPI}&query="
IMGURL="https://image.tmdb.org/t/p/original"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy()
db.init_app(app)

## Database
with app.app_context():
    class Movie(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        title=db.Column(db.String(100),unique=True,nullable=False)
        year=db.Column(db.String(100),nullable=True)
        description=db.Column(db.String(100),nullable=True)
        rating=db.Column(db.Integer,nullable=True)
        ranking=db.Column(db.Integer,nullable=True)
        review=db.Column(db.String(100),nullable=True)
        img_url=db.Column(db.String(100),nullable=True)

## Add form

class AddForm(FlaskForm):
    title=StringField("Movie title",validators=[DataRequired()])
    submit=SubmitField("Add movie")


## Edit Form
class EditForm(FlaskForm):
    rating=StringField("Your rating out of 10 eg. 7.5",validators=[DataRequired()])
    review=StringField("Your review",validators=[DataRequired()])
    done=SubmitField("Done")

@app.route("/")
def home():
#     new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#     db.create_all()
#     db.session.add(new_movie)
#     db.session.commit()
    # allmovies=db.session.query(Movie).all()

    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

@app.route("/add",methods=["POSt","GET"])
def add():
    addform=AddForm()
    if addform.is_submitted():
        title=request.form["title"]
        response=requests.get(URL+title).json()
        moviedata=response["results"]
        return render_template("select.html",listofmovies=moviedata)
    return render_template("add.html",form=addform)

@app.route("/find")
def find_movie():
    movie_id=request.args["id"]
    if movie_id:
        url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMBDAPI}"
        data=requests.get(url).json()
        new_movie = Movie(
            title=data["original_title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{IMGURL}{data['poster_path']}",
            description=data["overview"])
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit',id=new_movie.id))


@app.route("/edit",methods=["POST","GET"])
def edit():
    form=EditForm()
    bookId=request.args["id"]
    if form.is_submitted():
        bookToUpdate=Movie.query.get(bookId)
        bookToUpdate.rating=request.form["rating"]
        bookToUpdate.review=request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",form=form)

@app.route("/delete")
def delete():
    bookid=request.args["id"]
    booktoDelete=Movie.query.get(bookid)
    db.session.delete(booktoDelete)
    db.session.commit()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
