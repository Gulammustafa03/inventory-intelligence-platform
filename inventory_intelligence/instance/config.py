import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-in-production")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(BASE_DIR, "instance", "inventory_intelligence.sqlite"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
