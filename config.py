import os
from datetime import timedelta

IS_RENDER = bool(os.getenv("RENDER"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = "/tmp/sqlite.db" if IS_RENDER else os.path.join(BASE_DIR, "sqlite.db")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-123")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("EMAIL_HOST_USER", "suganyasdv16@gmail.com")
    MAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "duczripxqitpjvbu")
    MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_FROM_EMAIL", "suganyasdv16@gmail.com")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
    ADMIN_NOTIFY_EMAIL = os.getenv("ADMIN_NOTIFY_EMAIL", ADMIN_EMAIL)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)


# import os
# from datetime import timedelta

# # Automatically create DB at the same level as app.py
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SQLITE_DB_PATH = os.path.join(BASE_DIR, "sqlite.db")

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

#     # ✅ Force SQLite database with ABSOLUTE PATH
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # ✅ Email config (your Gmail app password stays here)
#     MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
#     MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
#     MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
#     MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
#     MAIL_USERNAME = os.getenv("EMAIL_HOST_USER", "suganyasdv16@gmail.com")
#     MAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "duczripxqitpjvbu")
#     MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_FROM_EMAIL", "suganyasdv16@gmail.com")

#     # ✅ Admin notification email
#     ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "sugan@admin.com")
#     ADMIN_NOTIFY_EMAIL = os.getenv("ADMIN_NOTIFY_EMAIL", ADMIN_EMAIL)

#     PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

