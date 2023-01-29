from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key="asdadadewqada23e23da"

class RegistrationForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Login")

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/login",methods=["GET","POST"])
def login():
    login_form=RegistrationForm()
    if login_form.is_submitted():
        if login_form.email.data=="admin@email.com" and login_form.password.data=="12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html",form=login_form)

if __name__ == '__main__':
    app.run(debug=True)