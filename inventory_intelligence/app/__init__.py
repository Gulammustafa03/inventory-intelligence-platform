from sqlalchemy import inspect


from flask import Flask, redirect, render_template, url_for

from .extensions import csrf, db, login_manager, migrate, oauth, socketio
from .models import Role, User
from .utils import format_currency


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py", silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    oauth.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    app.jinja_env.filters["format_currency"] = format_currency
    app.add_template_filter(format_currency, name="format_currency")

    if (
        app.config.get("GOOGLE_CLIENT_ID")
        and app.config.get("GOOGLE_CLIENT_SECRET")
    ):
        oauth.register(
            name="google",
            client_id=app.config["GOOGLE_CLIENT_ID"],
            client_secret=app.config["GOOGLE_CLIENT_SECRET"],
            access_token_url="https://oauth2.googleapis.com/token",
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            api_base_url="https://www.googleapis.com/oauth2/v1/",
            client_kwargs={
                "scope": "openid email profile"
            },
            jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        )

    @app.context_processor
    def _template_helpers():
        from flask import current_app, url_for

        def has_endpoint(endpoint_name: str) -> bool:
            return endpoint_name in current_app.view_functions

        def safe_url_for(endpoint_name: str, **values):
            try:
                return url_for(endpoint_name, **values)
            except Exception:
                return None

        return dict(has_endpoint=has_endpoint, safe_url_for=safe_url_for)
    from .auth.routes import bp as auth_bp
    from .categories.routes import bp as categories_bp
    from .dashboard.routes import bp as dashboard_bp
    from .inventory.routes import bp as inventory_bp
    from .suppliers.routes import bp as suppliers_bp
    from .users.routes import bp as users_bp
    from .notifications.routes import bp as notifications_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)

    

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.index"))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.cli.command("seed-data")
    def seed_data():
        seed_defaults()
        print("Seed data is ready.")

    def seed_defaults():
        for role_name in ("Admin", "Manager", "Employee"):
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
        db.session.flush()

        admin_role = Role.query.filter_by(name="Admin").first()
        admin = User.query.filter_by(email="admin@example.com").first()
        if admin:
            admin.username = "gulammustafacse0398"
            admin.role = admin_role
            admin.set_password("cse0123@gM")
        else:
            admin = User(username="gulammustafacse0398", email="admin@example.com", role=admin_role)
            admin.set_password("cse0123@gM")
            db.session.add(admin)
        db.session.commit()

    with app.app_context():
        inspector = inspect(db.engine)
        if inspector.has_table("role") and inspector.has_table("user"):
            seed_defaults()

    return app
