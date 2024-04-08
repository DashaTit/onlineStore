from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from pars.parser import Pars
import json


pars = Pars()
pars.get_data()
pars.get_result()
# pars.img_load()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    # discription = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.title



@app.route('/')
def index():
    with open('result.json', encoding='utf-8') as f:
        templates = json.load(f)
    # items = Item.query.order_by(Item.price).all()
    return render_template('index.html', templates=templates)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=["POST", 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'error'
    else:
        return render_template('create.html')
    



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)