from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import json

from data_collection import Data_collection


Data_collection() #data


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model): #бд
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(500), nullable=False)

#routes
@app.route('/')
def index():
    with open('result.json', encoding='utf-8') as f:
        templates = json.load(f)
    items = Item.query.order_by(Item.id).all()
    return render_template('index.html', templates=templates)

# @app.route('/login', methods=["POST", 'GET'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         item = Item(email=email, password=password)
#         try:
#             db.session.add(item)
#             db.session.commit()
#             return redirect('/')
#         except Exception as e:
#             print(str(e))
#     else:
#         return render_template('login.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)