from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Student, Company, Admin, JobPosition, JobApplication
import os

app = Flask(__name__)

# Allow Vue frontend to access Flask backend
CORS(app)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir,
    "instance",
    "placement.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return jsonify({"message": "Backend running"})


# =====================================
# STUDENT REGISTER
# =====================================
@app.route("/student/register", methods=["POST"])
def student_register():
    data = request.json

    existing_student = Student.query.filter_by(email=data["email"]).first()

    if existing_student:
        return jsonify({"message": "Email already registered"}), 400

    student = Student(
        student_id=data["student_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        course=data["course"],
        cgpa=data["cgpa"]
    )

    student.set_password(data["password"])

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"})


# =====================================
# STUDENT LOGIN
# =====================================
@app.route("/student/login", methods=["POST"])
def student_login():
    data = request.json

    student = Student.query.filter_by(email=data["email"]).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    if not student.check_password(data["password"]):
        return jsonify({
            "success": False,
            "message": "Incorrect password"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "student": {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.full_name,
            "email": student.email,
            "phone": student.phone,
            "course": student.course,
            "cgpa": student.cgpa
        }
    })


# =====================================
# COMPANY REGISTER
# =====================================
@app.route("/company/register", methods=["POST"])
def company_register():
    data = request.json

    existing_company = Company.query.filter_by(email=data["email"]).first()

    if existing_company:
        return jsonify({"message": "Company email already registered"}), 400

    company = Company(
        company_name=data["company_name"],
        contact_person=data["contact_person"],
        email=data["email"],
        website=data["website"]
    )

    company.set_password(data["password"])

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully. Waiting for admin approval"
    })


# =====================================
# COMPANY LOGIN
# =====================================
@app.route("/company/login", methods=["POST"])
def company_login():
    data = request.json

    company = Company.query.filter_by(email=data["email"]).first()

    if not company:
        return jsonify({
            "success": False,
            "message": "Company account not found"
        }), 404

    if not company.check_password(data["password"]):
        return jsonify({
            "success": False,
            "message": "Incorrect password"
        }), 401

    # only allow verified/enabled companies
    if company.is_verified is not True:
        return jsonify({
            "success": False,
            "message": "Your company account has been disabled or not yet approved by admin"
        }), 403

    return jsonify({
        "success": True,
        "company": {
            "id": company.id,
            "name": company.company_name,
            "email": company.email,
            "contact_person": company.contact_person,
            "website": company.website,
            "is_verified": company.is_verified
        }
    })


# =====================================
# ADMIN LOGIN
# =====================================
@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.json

    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"

    if data["email"] == ADMIN_USER and data["password"] == ADMIN_PASS:
        return jsonify({
            "success": True,
            "admin": {
                "username": "admin",
                "email": "admin"
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid admin credentials"
    }), 401


# =====================================
# ADMIN - VIEW COMPANIES
# =====================================
@app.route("/admin/companies", methods=["GET"])
def get_companies():
    companies = Company.query.all()

    result = []

    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "contact_person": company.contact_person,
            "email": company.email,
            "website": company.website,
            "status": "enabled" if company.is_verified else "disabled"
        })

    return jsonify(result)


# =====================================
# ADMIN - ENABLE / DISABLE COMPANY
# =====================================
@app.route("/admin/company/status/<int:id>", methods=["PUT"])
def update_company_status(id):
    data = request.json

    company = Company.query.get(id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.is_verified = data["status"] == "enabled"

    db.session.commit()

    return jsonify({
        "message": f"Company {data['status']} successfully"
    })

@app.route("/admin/students", methods=["GET"])
def get_students():
    students = Student.query.all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "name": student.full_name,
            "email": student.email,
            "student_id": student.student_id,
            "course": student.course,
            "cgpa": student.cgpa
        })

    return jsonify(result)


@app.route("/admin/company/delete/<int:id>", methods=["DELETE"])
def delete_company(id):
    company = Company.query.get(id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    db.session.delete(company)
    db.session.commit()

    return jsonify({"message": "Company deleted successfully"})


@app.route("/admin/student/delete/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"})

@app.route("/company/post-job", methods=["POST"])
def post_job():
    data = request.json

    job = JobPosition(
        company_id=data["company_id"],
        title=data["title"],
        description=data["description"],
        salary=data["salary"],
        location=data["location"],
        skills_required=data["skills_required"],
        vacancies=data["vacancies"]
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job posted successfully"
    })
    
@app.route("/admin/jobs", methods=["GET"])
def get_all_jobs():
    jobs = JobPosition.query.all()

    result = []

    for job in jobs:
        company = Company.query.get(job.company_id)

        result.append({
            "id": job.id,
            "company_name": company.company_name if company else "Unknown",
            "title": job.title,
            "salary": job.salary,
            "location": job.location,
            "skills_required": job.skills_required,
            "vacancies": job.vacancies
        })

    return jsonify(result)


@app.route("/admin/job/delete/<int:id>", methods=["DELETE"])
def delete_job(id):
    job = JobPosition.query.get(id)

    if not job:
        return jsonify({"message": "Job not found"}), 404

    db.session.delete(job)
    db.session.commit()

    return jsonify({"message": "Job deleted successfully"})

@app.route("/student/jobs/<int:student_id>", methods=["GET"])
def get_jobs_for_students(student_id):
    jobs = JobPosition.query.all()
    print("Jobs in DB:", jobs)

    result = []

    for job in jobs:
        company = Company.query.get(job.company_id)

        existing_application = JobApplication.query.filter_by(
            student_id=student_id,
            job_id=job.id
        ).first()

        result.append({
            "id": job.id,
            "company_name": company.company_name if company else "Unknown",
            "title": job.title,
            "description": job.description,
            "salary": job.salary,
            "location": job.location,
            "skills_required": job.skills_required,
            "vacancies": job.vacancies,

            "application_status": (
                existing_application.application_status
                if existing_application else "not_applied"
            ),

            "review_status": (
                existing_application.review_status
                if existing_application else "pending"
            )
        })

    return jsonify(result)

@app.route("/student/apply-job", methods=["POST"])
def apply_job():
    data = request.json

    existing = JobApplication.query.filter_by(
        student_id=data["student_id"],
        job_id=data["job_id"]
    ).first()

    if existing:
        return jsonify({
            "message": "You have already applied for this job"
        }), 400

    application = JobApplication(
        student_id=data["student_id"],
        job_id=data["job_id"],
        application_status="applied",
        review_status="pending"
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Applied successfully"
    })

@app.route("/company/job-applications/<int:company_id>", methods=["GET"])
def get_company_job_applications(company_id):
    jobs = JobPosition.query.filter_by(company_id=company_id).all()

    result = []

    for job in jobs:
        applications = JobApplication.query.filter_by(job_id=job.id).all()

        application_list = []

        for application in applications:
            student = Student.query.get(application.student_id)

            application_list.append({
                "application_id": application.id,
                "student_name": f"{student.first_name} {student.last_name}",
                "student_email": student.email,
                "student_course": student.course,
                "student_cgpa": student.cgpa,
                "review_status": application.review_status,
                "interview_time": application.interview_time,
                "feedback": application.feedback
            })

        result.append({
            "job_id": job.id,
            "title": job.title,
            "location": job.location,
            "salary": job.salary,
            "applications": application_list
        })

    return jsonify(result)


@app.route("/company/application/update/<int:application_id>", methods=["PUT"])
def update_application_status(application_id):
    data = request.json

    application = JobApplication.query.get(application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    application.review_status = data.get("review_status", application.review_status)
    application.interview_time = data.get("interview_time", application.interview_time)
    application.feedback = data.get("feedback", application.feedback)

    db.session.commit()

    return jsonify({"message": "Application updated successfully"})

if __name__ == "__main__":
    app.run(debug=True)

