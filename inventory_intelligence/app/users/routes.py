from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from ..decorators import roles_required
from ..extensions import db
from ..forms import UserForm
from ..models import Role, User

bp = Blueprint("users", __name__, url_prefix="/users")


def populate_role_choices(form):
    form.role_id.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]


@bp.route("/")
@roles_required("Admin")
def index():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users/index.html", users=users)


@bp.route("/create", methods=["GET", "POST"])
@roles_required("Admin")
def create():
    form = UserForm()
    populate_role_choices(form)
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data.strip()).first():
            flash("Username already exists.", "danger")
        elif User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already exists.", "danger")
        else:
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.lower(),
                role_id=form.role_id.data,
            )
            user.set_password(form.password.data or "ChangeMe123")
            db.session.add(user)
            db.session.commit()
            flash("User created.", "success")
            return redirect(url_for("users.index"))
    return render_template("users/form.html", form=form, title="Create user")


@bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@roles_required("Admin")
def edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    populate_role_choices(form)
    if form.validate_on_submit():
        existing_username = User.query.filter(User.username == form.username.data.strip(), User.id != user.id).first()
        existing_email = User.query.filter(User.email == form.email.data.lower(), User.id != user.id).first()
        if existing_username:
            flash("Username already exists.", "danger")
        elif existing_email:
            flash("Email already exists.", "danger")
        else:
            user.username = form.username.data.strip()
            user.email = form.email.data.lower()
            user.role_id = form.role_id.data
            if form.password.data:
                user.set_password(form.password.data)
            db.session.commit()
            flash("User updated.", "success")
            return redirect(url_for("users.index"))
    return render_template("users/form.html", form=form, title="Edit user")


@bp.route("/<int:user_id>/delete", methods=["POST"])
@roles_required("Admin")
def delete(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own active account.", "warning")
    else:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted.", "info")
    return redirect(url_for("users.index"))
