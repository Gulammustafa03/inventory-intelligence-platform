from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


def utc_now():
    return datetime.now(timezone.utc)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", back_populates="role", lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    role = db.relationship("Role", back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        return self.role.name if self.role else ""

    def has_role(self, *roles):
        return self.role_name in roles

    def __repr__(self):
        return f"<User {self.username}>"

    notifications = db.relationship("Notification", back_populates="user", lazy=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)

    products = db.relationship("Product", back_populates="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    address = db.Column(db.Text, nullable=True)

    products = db.relationship("Product", back_populates="supplier", lazy=True)

    def __repr__(self):
        return f"<Supplier {self.name}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    sku = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    minimum_stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    category = db.relationship("Category", back_populates="products")
    supplier = db.relationship("Supplier", back_populates="products")

    @property
    def inventory_value(self):
        return float(self.price or 0) * int(self.quantity or 0)

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_stock


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)

    user = db.relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.title}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
