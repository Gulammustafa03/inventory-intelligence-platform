from flask import Blueprint, flash, redirect, render_template, url_for

from ..decorators import roles_required
from ..extensions import db
from ..forms import CategoryForm
from ..models import Category

bp = Blueprint("categories", __name__, url_prefix="/categories")


@bp.route("/")
@roles_required("Admin", "Manager")
def index():
    categories = Category.query.order_by(Category.name).all()
    return render_template("categories/index.html", categories=categories)


@bp.route("/create", methods=["GET", "POST"])
@roles_required("Admin", "Manager")
def create():
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data.strip()).first():
            flash("Category already exists.", "danger")
        else:
            db.session.add(Category(name=form.name.data.strip()))
            db.session.commit()
            flash("Category created.", "success")
            return redirect(url_for("categories.index"))
    return render_template("categories/form.html", form=form, title="Create category")


@bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
@roles_required("Admin", "Manager")
def edit(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data.strip()
        db.session.commit()
        flash("Category updated.", "success")
        return redirect(url_for("categories.index"))
    return render_template("categories/form.html", form=form, title="Edit category")


@bp.route("/<int:category_id>/delete", methods=["POST"])
@roles_required("Admin", "Manager")
def delete(category_id):
    category = Category.query.get_or_404(category_id)
    if category.products:
        flash("Move or delete products in this category first.", "warning")
    else:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted.", "info")
    return redirect(url_for("categories.index"))
