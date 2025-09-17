# app.py

'''
Youtube video for k8s demo: https://youtu.be/s_o8dwzRlu4?si=wFTKsznd4i6FEHBV
'''

from flask import Flask, render_template, request
import os
import requests
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


EXTERNAL_API = os.getenv("API_URL")

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Joel1234@localhost:3306/flask_db'
# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
# MYSQL_USER = os.getenv('MYSQL_USER')
# MYSQL_PWD = os.getenv('MYSQL_PASSWORD')
# MYSQL_HOSTNAME = os.getenv('MYSQL_HOSTNAME')
# MYSQL_DB = os.getenv('MYSQL_DATABASE')
# SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOSTNAME}:3306/{MYSQL_DB}'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(80))
    price = db.Column(db.Integer)


with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/explore", methods=["GET","POST"])
def explore():
    print(request.method)
    username  = None
    if request.method == "POST":
        print(request.form.get("username"))
        username = request.form.get("username")

    return render_template("explore.html", username=username)

@app.route('/external-api')
def fetch_data():
    try:
        resp = requests.get(EXTERNAL_API)
        data = resp.json()
    except:
        return {"Error":"API Error"}
    response = {
        "app": "Flask App",
        "data": data
    }

    return response

@app.route('/cars_api', methods=['GET','POST'])
def cars_api():
    if request.method == "POST":
        model = request.json['model']
        price = request.json['price']
        car = Cars(model=model,price=price)
        db.session.add(car)
        db.session.commit()
        return {"status":"Success", "msg":"Resource Added"}
    cars = Cars.query.all()
    # print(cars[0].id)
    response = []
    for car in cars:
        car_json = {}
        car_json['id'] = car.id
        car_json["model"] = car.model
        car_json["price"] = car.price
        response.append(car_json)

    return response

@app.route('/cars',methods=['GET','POST'])
def cars():
    if request.method=="POST":
        model = request.form['model']
        price = int(request.form['price'])
        car = Cars(model=model,price=price)
        db.session.add(car)
        db.session.commit()
    
    cars = Cars.query.order_by(db.desc(Cars.id)).all()
    return render_template("cars.html", cars=cars)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


'''
docker image build command:
    docker buildx build --platform=linux/amd64 -t joeljozarackal/flask-k8s:v2 .

network:
docker network create mynet

mysql:
docker run -d --name my-mysql --network mynet --env-file .env mysql:8.0

docker buildx build --platform=linux/amd64 -t joeljozarackal/flask-k8s:v4mysqldb .
docker run -d --name my-app --network mynet --env-file .env -p 5001:5001 joeljozarackal/flask-k8s:v4mysqldb


curl -X POST http://localhost:30100/cars_api -H "Content-Type: application/json" \
-d '{"model" : "Benz E class", "price":"4500"}'

curl -X POST http://localhost:50259/cars_api -H "Content-Type: application/json" \
-d '{"model" : "Benz E class", "price":"4500"}'

'''