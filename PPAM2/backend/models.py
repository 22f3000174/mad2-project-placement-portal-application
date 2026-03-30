
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Database object
# Import this in app.py using:
# from models import db, Student, Company, Admin

db = SQLAlchemy()


# =========================
# STUDENT TABLE
# =========================
class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)

    # Registration fields
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)

    # Login / security
    password_hash = db.Column(db.String(255), nullable=False)

    # Optional future fields
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Helper methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# =========================
# COMPANY TABLE
# =========================
class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)

    # Registration fields
    company_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    website = db.Column(db.String(200))

    # Login / security
    password_hash = db.Column(db.String(255), nullable=False)

    # Approval system
    is_verified = db.Column(db.Boolean, default=False)

    # Optional future fields
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Helper methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class JobPosition(db.Model):
    __tablename__ = "job_position"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    skills_required = db.Column(db.String(500), nullable=False)
    vacancies = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

# =========================
# ADMIN TABLE
# =========================
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    



