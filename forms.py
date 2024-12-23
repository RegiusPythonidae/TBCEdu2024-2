from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, length, ValidationError, equal_to


class ProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired(),
                                                       length(min=8, max=32)])

    price = IntegerField("პროდუქტის ფასი", validators=[DataRequired()])
    img = FileField("პროდუქტის სურათი", validators=[FileRequired(),
                                                    FileSize(1000 * 1000, message="ფაილი უნდა იყოს მაქს. 1000 ბიტი"),
                                                    FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("შენახვა")


class RegisterForm(FlaskForm):
    username = StringField("იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired(),
                                                   length(min=8)])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[equal_to("password")])

    register = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired(),length(min=8)])
    remember_me = BooleanField("დამახსოვრება")

    login = SubmitField("ავტორიზაცია")