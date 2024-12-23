from flask import render_template, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from os import path
from uuid import uuid4

from forms import ProductForm, RegisterForm, LoginForm
from models import Product, User
from ext import app

users = {
    "john": {"name": "John", "surname": "Doe", "age": 24, "img": "qandakeba.jpg", "role": "Admin"},
    "joanne": {"name": "joanne", "surname": "Doette", "age": 18, "img": "images.jpg", "role": "Moderator"},
    "johnny": {"name": "johnny", "saint": "Doe", "age": 30, "img": "qandakeba.jpg", "role": "User"},
}

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products, users=users)


@app.route("/search")
def search():
    name = request.args.get("n")
    products = Product.query.filter(Product.name == name).all()
    return render_template("index.html", products=products, users=users)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", found_user=users.get(username))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data,
                        role="Guest")

        new_user.create()
        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user != None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()

    if form.validate_on_submit():
        file = form.img.data
        filename, filetype = path.splitext(file.filename)
        filename = uuid4()
        filepath = path.join(app.root_path, "static", f"{filename}{filetype}")
        file.save(filepath)

        new_product = Product(name=form.name.data,
                              price=form.price.data,
                              img=f"{filename}{filetype}")
        new_product.create()
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price, img=product.img)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.save()
        return redirect("/")
    return render_template("create_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    if current_user.role != "Admin":
        return redirect("/")

    product = Product.query.get(product_id)
    product.delete()
    return redirect("/")