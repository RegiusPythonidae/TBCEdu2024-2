from ext import app, db
from models import Product

products = [
    {"name": "Samsung Galaxy A24", "price": 900, "img": "images.jpg"},
    {"name": "iPhone 13 PRO MAX", "price": 3000, "img": "qandakeba.jpg"},
    {"name": "Samsung Galaxy S24 Ultra", "price": 3000, "img": "images.jpg"},
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for product in products:
        new_product = Product(name=product["name"], price=product["price"], img=product["img"])
        db.session.add(new_product)
    db.session.commit()
