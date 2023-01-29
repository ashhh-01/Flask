from flask import Flask, render_template,redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,URL
import csv

COFFEE=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url=StringField("Url",validators=[DataRequired(),URL()])
    location=StringField("location",validators=[DataRequired()])
    openTime=StringField("Open Time e.g. 8AM",validators=[DataRequired()])
    closingTime=StringField("Closing Time e.g. 5:30PM",validators=[DataRequired()])
    coffeeRating=SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifiRating=SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power=SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["POST","GET"])
def add_cafe():
    form = CafeForm()
    if form.is_submitted():
        with open("./Flask/Coffee/cafe-data.csv",encoding="utf-8",mode="a") as csv_file:
            csv_file.write(f"\n{form.cafe.data}),"
                f"{form.location.data},"
                f"{form.openTime.data},"
                f"{form.closingTime.data},"
                f"{form.coffeeRating.data},"
                f"{form.wifiRating.data},"
                f"{form.power.data},")
            return redirect('/add')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('./Flask/Coffee/cafe-data.csv',encoding="utf-8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
