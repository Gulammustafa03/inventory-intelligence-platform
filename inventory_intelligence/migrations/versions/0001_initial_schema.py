"""Initial schema and default admin

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-19 00:00:00.000000

"""
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_category_name"), "category", ["name"], unique=False)
    op.create_table(
        "supplier",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_supplier_name"), "supplier", ["name"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("minimum_stock", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["supplier.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
    )
    op.create_index(op.f("ix_product_name"), "product", ["name"], unique=False)
    op.create_index(op.f("ix_product_sku"), "product", ["sku"], unique=False)
    op.create_table(
        "notification",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    role_table = sa.table("role", sa.column("id", sa.Integer), sa.column("name", sa.String))
    user_table = sa.table(
        "user",
        sa.column("username", sa.String),
        sa.column("email", sa.String),
        sa.column("password_hash", sa.String),
        sa.column("role_id", sa.Integer),
        sa.column("created_at", sa.DateTime),
    )
    op.bulk_insert(role_table, [{"id": 1, "name": "Admin"}, {"id": 2, "name": "Manager"}, {"id": 3, "name": "Employee"}])
    op.bulk_insert(
        user_table,
        [{
            "username": "gulammustafacse0398",
            "email": "admin@example.com",
            "password_hash": generate_password_hash("cse0123@gM"),
            "role_id": 1,
            "created_at": datetime.now(timezone.utc),
        }],
    )


def downgrade():
    op.drop_table("notification")
    op.drop_index(op.f("ix_product_sku"), table_name="product")
    op.drop_index(op.f("ix_product_name"), table_name="product")
    op.drop_table("product")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_supplier_name"), table_name="supplier")
    op.drop_table("supplier")
    op.drop_index(op.f("ix_category_name"), table_name="category")
    op.drop_table("category")
    op.drop_table("role")
