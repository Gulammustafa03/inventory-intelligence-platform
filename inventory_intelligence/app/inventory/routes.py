from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from ..decorators import roles_required
from ..extensions import db
from ..forms import ProductForm, StockUpdateForm
from ..models import Category, Product, Supplier
from ..utils import notify_roles

bp = Blueprint("inventory", __name__, url_prefix="/inventory")


def populate_product_choices(form):
    form.category_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]
    form.supplier_id.choices = [(supplier.id, supplier.name) for supplier in Supplier.query.order_by(Supplier.name).all()]


@bp.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "", type=str).strip()
    query = Product.query
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(like), Product.sku.ilike(like), Product.description.ilike(like)))
    products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template("inventory/index.html", products=products, search=search, stock_form=StockUpdateForm())


@bp.route("/create", methods=["GET", "POST"])
@roles_required("Admin", "Manager")
def create():
    form = ProductForm()
    populate_product_choices(form)
    if not form.category_id.choices or not form.supplier_id.choices:
        flash("Create at least one category and supplier before adding products.", "warning")
        return redirect(url_for("inventory.index"))

    if form.validate_on_submit():
        if Product.query.filter_by(sku=form.sku.data.strip()).first():
            flash("SKU already exists.", "danger")
        else:
            product = Product(
                name=form.name.data.strip(),
                sku=form.sku.data.strip(),
                description=form.description.data,
                price=form.price.data,
                quantity=form.quantity.data,
                minimum_stock=form.minimum_stock.data,
                category_id=form.category_id.data,
                supplier_id=form.supplier_id.data,
            )
            db.session.add(product)
            db.session.commit()
            notify_roles(
                ["Admin", "Manager"],
                "New product added",
                f"{current_user.username} added {product.name}.",
            )
            flash("Product created.", "success")
            return redirect(url_for("inventory.index"))
    return render_template("inventory/form.html", form=form, title="Add product")


@bp.route("/<int:product_id>")
@login_required
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("inventory/detail.html", product=product, stock_form=StockUpdateForm(quantity=product.quantity))


@bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@roles_required("Admin", "Manager")
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    populate_product_choices(form)
    if form.validate_on_submit():
        existing = Product.query.filter(Product.sku == form.sku.data.strip(), Product.id != product.id).first()
        if existing:
            flash("SKU already exists.", "danger")
        else:
            product.name = form.name.data.strip()
            product.sku = form.sku.data.strip()
            product.description = form.description.data
            product.price = form.price.data
            product.quantity = form.quantity.data
            product.minimum_stock = form.minimum_stock.data
            product.category_id = form.category_id.data
            product.supplier_id = form.supplier_id.data
            db.session.commit()
            flash("Product updated.", "success")
            return redirect(url_for("inventory.detail", product_id=product.id))
    return render_template("inventory/form.html", form=form, title="Edit product")


@bp.route("/<int:product_id>/delete", methods=["POST"])
@roles_required("Admin", "Manager")
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("inventory.index"))


@bp.route("/<int:product_id>/stock", methods=["POST"])
@roles_required("Admin", "Manager", "Employee")
def update_stock(product_id):
    product = Product.query.get_or_404(product_id)
    form = StockUpdateForm()
    if form.validate_on_submit():
        product.quantity = form.quantity.data
        db.session.commit()
        flash("Stock quantity updated.", "success")
    else:
        flash("Enter a valid stock quantity.", "danger")
    return redirect(request.referrer or url_for("inventory.detail", product_id=product.id))
