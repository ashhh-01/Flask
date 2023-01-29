from flask import Flask
import random

randnumber=random.randint(0,9)
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Guess a number between 1 and 10</h1>"\
        "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>"

@app.route("/<int:guess>")
def number(guess):
    if guess>randnumber:
        return "<h1>Too High!Try again</h1>"\
            "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"
    elif guess<randnumber:
        return "<h1>Too low! Try again</h1>"\
            "<img src=' https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    else:
        return "<h1>Correct number</h1>"\
        "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"


if __name__=="__main__":
    app.run(debug=True)