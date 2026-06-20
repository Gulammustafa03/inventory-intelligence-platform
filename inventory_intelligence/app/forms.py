from flask_wtf import FlaskForm
from wtforms import DecimalField, EmailField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Save category")


class SupplierForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=160)])
    email = EmailField("Email", validators=[Optional(), Email(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Save supplier")


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=160)])
    sku = StringField("SKU", validators=[DataRequired(), Length(max=80)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    price = DecimalField("Price", places=2, validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    minimum_stock = IntegerField("Minimum stock", validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    supplier_id = SelectField("Supplier", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save product")


class StockUpdateForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Update stock")


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[Optional(), Length(min=8, max=128)])
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save user")
