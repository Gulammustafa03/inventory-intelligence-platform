from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from ..decorators import roles_required
from ..extensions import db
from ..forms import SupplierForm
from ..models import Supplier
from ..utils import notify_roles

bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")


@bp.route("/")
@roles_required("Admin", "Manager")
def index():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template("suppliers/index.html", suppliers=suppliers)


@bp.route("/create", methods=["GET", "POST"])
@roles_required("Admin", "Manager")
def create():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data.strip(),
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
        )
        db.session.add(supplier)
        db.session.commit()
        notify_roles(
            ["Admin", "Manager"],
            "New supplier added",
            f"{current_user.username} added {supplier.name}.",
        )
        flash("Supplier created.", "success")
        return redirect(url_for("suppliers.index"))
    return render_template("suppliers/form.html", form=form, title="Create supplier")


@bp.route("/<int:supplier_id>")
@roles_required("Admin", "Manager")
def detail(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template("suppliers/detail.html", supplier=supplier)


@bp.route("/<int:supplier_id>/edit", methods=["GET", "POST"])
@roles_required("Admin", "Manager")
def edit(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        supplier.name = form.name.data.strip()
        supplier.email = form.email.data
        supplier.phone = form.phone.data
        supplier.address = form.address.data
        db.session.commit()
        flash("Supplier updated.", "success")
        return redirect(url_for("suppliers.detail", supplier_id=supplier.id))
    return render_template("suppliers/form.html", form=form, title="Edit supplier")


@bp.route("/<int:supplier_id>/delete", methods=["POST"])
@roles_required("Admin", "Manager")
def delete(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if supplier.products:
        flash("Move or delete products for this supplier first.", "warning")
    else:
        db.session.delete(supplier)
        db.session.commit()
        flash("Supplier deleted.", "info")
    return redirect(url_for("suppliers.index"))
