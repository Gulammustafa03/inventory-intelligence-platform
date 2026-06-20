import secrets

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from ..extensions import db, oauth
from ..models import Role, User
from ..utils import notify_roles
from .forms import LoginForm, RegistrationForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip()
        user = User.query.filter(or_(User.email == identifier.lower(), User.username == identifier)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Welcome back.", "success")
            return redirect(request.args.get("next") or url_for("dashboard.index"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/google")
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if "google" not in oauth._registry:
        flash("Google login is not configured.", "warning")
        return redirect(url_for("auth.login"))

    redirect_uri = url_for("auth.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route("/google/callback")
def google_callback():
    if "google" not in oauth._registry:
        flash("Google login is not configured.", "warning")
        return redirect(url_for("auth.login"))

    token = oauth.google.authorize_access_token()
    user_info = token.get("userinfo")
    if not user_info:
        user_info = oauth.google.parse_id_token(token)

    email = user_info.get("email") if user_info else None
    if not email:
        flash("Google login failed to retrieve email.", "danger")
        return redirect(url_for("auth.login"))

    email = email.lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        employee_role = Role.query.filter_by(name="Employee").first()
        username = user_info.get("name") or email.split("@")[0]
        username = username.strip().replace(" ", "_")[:80]
        base_username = username or email.split("@")[0]
        count = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{count}"
            count += 1
        user = User(username=username, email=email, role=employee_role)
        user.set_password(secrets.token_urlsafe(16))
        db.session.add(user)
        db.session.commit()
        notify_roles(["Admin", "Manager"], "New Google user", f"{user.username} signed in with Google.")

    login_user(user)
    flash("Signed in with Google.", "success")
    return redirect(request.args.get("next") or url_for("dashboard.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username is already in use.", "danger")
        elif User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email is already registered.", "danger")
        else:
            employee_role = Role.query.filter_by(name="Employee").first()
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.lower(),
                role=employee_role,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Account created. You can sign in now.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
