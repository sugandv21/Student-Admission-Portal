from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudentApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    course = db.Column(db.String(120), nullable=False)
    statement = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="PENDING", index=True)  # PENDING/APPROVED/REJECTED
    created_at = db.Column(db.DateTime, nullable=False)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
