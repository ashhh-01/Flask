from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Library.db"
##Optional
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy()
db.init_app(app)
all_books = []

with app.app_context():
    class Library(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        bookName=db.Column(db.String(100),unique=True,nullable=False)
        author=db.Column(db.String(100),nullable=False)
        rating=db.Column(db.Float,nullable=False)


@app.route('/')
def home():
    all_books=db.session.query(Library).all()
    return render_template("index.html",books=all_books)

@app.route("/edit",methods=["POST","GET"])
def edit():
    if request.method=="POST":
        book_id=request.form["id"]
        book_to_update=Library.query.get(book_id)
        book_to_update.rating=request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id=request.args.get("id")
    print(request.args)
    book_selected=Library.query.get(book_id)
    return render_template("edit.html",book=book_selected)

@app.route("/delete")
def delete():
    bookid=request.args["id"]
    booktobedeleted=Library.query.get(bookid)
    db.session.delete(booktobedeleted)
    db.session.commit()
    return redirect(url_for('home'))
@app.route("/add", methods=["POST","GET"])
def add():
    if request.method=="POST":
        new=Library(bookName=request.form["book"],author=request.form["author"],rating=request.form["rating"])
        db.create_all()
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

