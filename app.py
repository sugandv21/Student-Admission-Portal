import os
from datetime import datetime

from flask import (
    Flask, render_template, redirect, url_for, flash,
    request, session, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, StudentApplication, AdminUser
from forms import RegistrationForm, AdminLoginForm
from config import Config
from mailer import (
    mail,
    send_app_received_email,
    send_status_update_email,
    send_admin_new_application_email,
)

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Create tables and seed a default admin on first run
    with app.app_context():
        db.create_all()
        admin_email = app.config.get("ADMIN_EMAIL") or "sugan@admin.com"
        admin_password = os.getenv("ADMIN_PASSWORD", "sugan123")
        if not AdminUser.query.filter_by(email=admin_email).first():
            admin = AdminUser(
                email=admin_email.lower(),
                password_hash=generate_password_hash(admin_password),
            )
            db.session.add(admin)
            db.session.commit()
            print(f"[INIT] Created default admin: {admin_email} / {admin_password}")

    # ------------------ Public Routes ------------------

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            appn = StudentApplication(
                full_name=form.full_name.data.strip(),
                email=form.email.data.strip().lower(),
                phone=form.phone.data.strip(),
                dob=form.dob.data,
                address=form.address.data.strip(),
                course=form.course.data.strip(),
                statement=form.statement.data.strip() if form.statement.data else None,
                status="PENDING",
                created_at=datetime.utcnow(),
            )
            db.session.add(appn)
            db.session.commit()

            # Email applicant (received)
            try:
                send_app_received_email(appn)
            except Exception as e:
                print("[MAIL] Applicant confirmation error:", e)

            # Email admin (new application notification)
            try:
                send_admin_new_application_email(appn)
            except Exception as e:
                print("[MAIL] Admin notification error:", e)

            return redirect(url_for("success"))

        return render_template("register.html", form=form)

    @app.route("/success")
    def success():
        return render_template("success.html")

    # ------------------ Admin Auth ------------------

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if "admin_id" in session:
            return redirect(url_for("admin_dashboard"))
        form = AdminLoginForm()
        if form.validate_on_submit():
            admin = AdminUser.query.filter_by(email=form.email.data.strip().lower()).first()
            if admin and check_password_hash(admin.password_hash, form.password.data):
                session["admin_id"] = admin.id
                flash("Logged in successfully.", "success")
                return redirect(url_for("admin_dashboard"))
            flash("Invalid credentials.", "danger")
        return render_template("admin_login.html", form=form)

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_id", None)
        flash("Logged out.", "info")
        return redirect(url_for("admin_login"))

    def require_admin():
        if "admin_id" not in session:
            abort(403)

    # ------------------ Admin Panel ------------------

    @app.route("/admin/dashboard")
    def admin_dashboard():
        require_admin()
        status = request.args.get("status")  # optional filter
        q = StudentApplication.query.order_by(StudentApplication.created_at.desc())
        if status in {"PENDING", "APPROVED", "REJECTED"}:
            q = q.filter_by(status=status)
        applications = q.all()
        counts = {
            "total": StudentApplication.query.count(),
            "pending": StudentApplication.query.filter_by(status="PENDING").count(),
            "approved": StudentApplication.query.filter_by(status="APPROVED").count(),
            "rejected": StudentApplication.query.filter_by(status="REJECTED").count(),
        }
        return render_template(
            "admin_dashboard.html",
            applications=applications,
            counts=counts,
            status=status,
        )

    @app.route("/admin/application/<int:app_id>")
    def admin_application_detail(app_id):
        require_admin()
        appn = StudentApplication.query.get_or_404(app_id)
        return render_template("application_detail.html", app=appn)

    @app.post("/admin/application/<int:app_id>/approve")
    def approve_application(app_id):
        require_admin()
        appn = StudentApplication.query.get_or_404(app_id)
        appn.status = "APPROVED"
        db.session.commit()
        try:
            send_status_update_email(appn)
        except Exception as e:
            print("[MAIL] Status email error:", e)
        flash("Application approved and email sent.", "success")
        return redirect(url_for("admin_application_detail", app_id=app_id))

    @app.post("/admin/application/<int:app_id>/reject")
    def reject_application(app_id):
        require_admin()
        appn = StudentApplication.query.get_or_404(app_id)
        appn.status = "REJECTED"
        db.session.commit()
        try:
            send_status_update_email(appn)
        except Exception as e:
            print("[MAIL] Status email error:", e)
        flash("Application rejected and email sent.", "warning")
        return redirect(url_for("admin_application_detail", app_id=app_id))

    # ------------------ Errors ------------------

    @app.errorhandler(403)
    def forbidden(_):
        return redirect(url_for("admin_login"))

    return app


app = create_app()

if __name__ == "__main__":
    # Local run
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
