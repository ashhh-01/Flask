from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.Float, nullable=False)

    # new_book = Book (id=1, title="Potter", author="Va", rating=9.7)
    # db.create_all()
    # db.session.add(new_book)
    # db.session.commit()
    book_id=99021
    all=Book.query.get(book_id)
    db.session.delete(all)
    db.session.commit()
