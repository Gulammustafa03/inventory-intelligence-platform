from datetime import datetime

from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from sqlalchemy import func

from ..decorators import roles_required
from ..extensions import db
from ..models import Category, Product, Supplier

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def index():
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_suppliers = Supplier.query.count()
    total_value = db.session.query(func.coalesce(func.sum(Product.price * Product.quantity), 0)).scalar()
    low_stock = Product.query.filter(Product.quantity <= Product.minimum_stock).order_by(Product.quantity.asc()).all()
    health_score = 100 if not total_products else max(0, round(((total_products - len(low_stock)) / total_products) * 100))

    return render_template(
        "dashboard/index.html",
        total_products=total_products,
        total_categories=total_categories,
        total_suppliers=total_suppliers,
        total_value=float(total_value or 0),
        low_stock=low_stock,
        health_score=health_score,
        today=datetime.now().strftime("%B %d, %Y"),
    )


@bp.route("/analytics")
@roles_required("Admin", "Manager")
def analytics():
    return render_template("dashboard/analytics.html")


@bp.route("/analytics/data")
@roles_required("Admin", "Manager")
def analytics_data():
    by_category = (
        db.session.query(Category.name, func.coalesce(func.sum(Product.quantity), 0))
        .outerjoin(Product)
        .group_by(Category.id)
        .order_by(Category.name)
        .all()
    )
    product_quantities = Product.query.order_by(Product.quantity.desc()).limit(15).all()
    low_stock_count = Product.query.filter(Product.quantity <= Product.minimum_stock).count()
    healthy_stock_count = Product.query.filter(Product.quantity > Product.minimum_stock).count()

    return jsonify(
        {
            "inventoryByCategory": {
                "labels": [row[0] for row in by_category],
                "values": [int(row[1] or 0) for row in by_category],
            },
            "productQuantities": {
                "labels": [product.name for product in product_quantities],
                "values": [product.quantity for product in product_quantities],
            },
            "lowStockStats": {
                "labels": ["Low stock", "Healthy stock"],
                "values": [low_stock_count, healthy_stock_count],
            },
        }
    )
