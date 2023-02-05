from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
import random

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

##Cafe TABLE Configuration
with app.app_context():
    class Cafe(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(250), unique=True, nullable=False)
        map_url = db.Column(db.String(500), nullable=False)
        img_url = db.Column(db.String(500), nullable=False)
        location = db.Column(db.String(250), nullable=False)
        seats = db.Column(db.String(250), nullable=False)
        has_toilet = db.Column(db.Boolean, nullable=False)
        has_wifi = db.Column(db.Boolean, nullable=False)
        has_sockets = db.Column(db.Boolean, nullable=False)
        can_take_calls = db.Column(db.Boolean, nullable=False)
        coffee_price = db.Column(db.String(250), nullable=True)
        def to_dict(self):
            dictionary={}
            for column in self.__table__.columns:
                dictionary[column.name]=getattr(self,column.name)
            return dictionary
        # return {column.name:getattr(self,column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/randoms",methods=["GET"])
def randomCafes():
    rowCount=Cafe.query.count()
    randomOffset=random.randint(0,rowCount-1)
    random_cafe=Cafe.query.offset(randomOffset).first()
    
    # return jsonify(cafe={
    #     #Omit the id from the response
    #     # "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
        
    #     #Put some properties in a sub-category
    #     "amenities": {
    #       "seats": random_cafe.seats,
    #       "has_toilet": random_cafe.has_toilet,
    #       "has_wifi": random_cafe.has_wifi,
    #       "has_sockets": random_cafe.has_sockets,
    #       "can_take_calls": random_cafe.can_take_calls,
    #       "coffee_price": random_cafe.coffee_price,
    #     }
    # })

    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all",methods=["GET"])
def allCafe():
    allcafe=Cafe.query.all()
    return jsonify(cafe=[cafe.to_dict() for cafe in allcafe])

@app.route("/search")
def getlocation():
    loc=request.args["loc"]
    cafe=db.session.query(Cafe).filter_by(location=loc).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found":"Sorry, we dont have a cafe at that location."})
## HTTP POST - Create Record
@app.route("/add",methods=["POST"])
def addCafe():
    new_cafe=Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilets")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})
## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>",methods=["PATCH"])
def update(cafe_id):
    new_price=request.args.get("new_price")
    cafe_to_update=db.session.query(Cafe).get(cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price=new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."}),200
    else:
        return jsonify(response={"Failed": "Failed added the new cafe."}),404

## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>",methods=["DELETE"])
def deleteCafe(cafe_id):
    apikey=request.args.get("api-key")
    cafe_to_delete=db.session.query(Cafe).get(cafe_id)
    if apikey=="accept":
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."}),200
    else:
        return jsonify(response={"Failed": "Failed added the new cafe."}),404



if __name__ == '__main__':
    app.run(debug=True)
