from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Student, Company, Admin, JobPosition, JobApplication, ApplicationHistory
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_mail import Mail, Message

from flask_migrate import Migrate

#imports for celery-redis csv/html imports
from celery.result import AsyncResult
from celery.result import AsyncResult
from celery_worker import celery
from flask import send_from_directory


import os

app = Flask(__name__)

#Email config for Celery-Redis================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'email@gmail.com'
app.config['MAIL_PASSWORD'] = 'app generated password'

mail = Mail(app)
# ===============================================================

# Allow Vue frontend to access Flask backend
CORS(app)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir, "uploads", "offer_letters")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir,
    "instance",
    "placement.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)
db.init_app(app)
migrate = Migrate(app, db)

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
            ),

            "interview_time": (
                existing_application.interview_time
                if existing_application else None
            ),

            "interview_mode": (
                existing_application.interview_mode
                if existing_application else None
            ),

            "interview_description": (
                existing_application.interview_description
                if existing_application else None
            ),

            "feedback": (
                existing_application.feedback
                if existing_application else None
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
                "interview_mode": application.interview_mode,
                "interview_description": application.interview_description,
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

    application.review_status = data.get(
        "review_status",
        application.review_status
    )

    application.interview_time = data.get(
        "interview_time",
        application.interview_time
    )

    application.interview_mode = data.get(
        "interview_mode",
        application.interview_mode
    )

    application.interview_description = data.get(
        "interview_description",
        application.interview_description
    )

    application.feedback = data.get(
        "feedback",
        application.feedback
    )

    db.session.commit()

    return jsonify({
        "message": "Application updated successfully"
    })

@app.route("/company/upload-offer-letter", methods=["POST"])
def upload_offer_letter():
    application_id = request.form.get("application_id")
    message = request.form.get("message", "")

    file = request.files.get("offer_letter")

    if not application_id or not file:
        return jsonify({
            "message": "Application and file are required"
        }), 400

    application = JobApplication.query.get(application_id)

    if not application:
        return jsonify({
            "message": "Application not found"
        }), 404

    filename = secure_filename(file.filename)

    # make filename unique
    filename = f"{application_id}_{filename}"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    application.offer_letter_path = filepath
    application.offer_letter_message = message
    application.review_status = "offer sent"

    db.session.commit()

    return jsonify({
        "message": "Offer letter uploaded successfully"
    })

@app.route("/student/offer-letters/<int:student_id>", methods=["GET"])
def get_student_offer_letters(student_id):
    applications = JobApplication.query.filter_by(student_id=student_id).all()

    result = []

    for application in applications:
        if not application.offer_letter_path:
            continue

        job = JobPosition.query.get(application.job_id)
        company = Company.query.get(job.company_id) if job else None

        filename = os.path.basename(application.offer_letter_path)

        result.append({
            "application_id": application.id,
            "job_title": job.title if job else "Unknown Job",
            "company_name": company.company_name if company else "Unknown Company",
            "message": application.offer_letter_message,
            "download_url": f"http://127.0.0.1:5000/company/download-offer-letter/{filename}"
        })

    return jsonify(result)

@app.route("/company/download-offer-letter/<filename>")
def download_offer_letter(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )
    
@app.route("/company/application-history", methods=["POST"])
def save_application_history():
    data = request.json

    history = ApplicationHistory(
        application_id=data["application_id"],
        student_name=data["student_name"],
        student_email=data["student_email"],
        student_course=data["student_course"],
        student_cgpa=data["student_cgpa"],
        job_id=data["job_id"],
        job_title=data["job_title"],
        job_location=data["job_location"],
        job_salary=data["job_salary"],
        review_status=data["review_status"],
        interview_time=data.get("interview_time"),
        interview_mode=data.get("interview_mode"),
        interview_description=data.get("interview_description"),
        feedback=data.get("feedback")
    )

    db.session.add(history)
    db.session.commit()

    return jsonify({"message": "History saved"})

@app.route("/company/application-history/<int:company_id>", methods=["GET"])
def get_company_application_history(company_id):
    company_jobs = JobPosition.query.filter_by(company_id=company_id).all()

    job_ids = [job.id for job in company_jobs]

    history = ApplicationHistory.query.filter(
        ApplicationHistory.job_id.in_(job_ids)
    ).order_by(ApplicationHistory.saved_at.desc()).all()

    result = []

    for item in history:
        result.append({
            "id": item.id,
            "application_id": item.application_id,
            "student_name": item.student_name,
            "student_email": item.student_email,
            "student_course": item.student_course,
            "student_cgpa": item.student_cgpa,
            "job_id": item.job_id,
            "job_title": item.job_title,
            "job_location": item.job_location,
            "job_salary": item.job_salary,
            "review_status": item.review_status,
            "interview_time": item.interview_time,
            "interview_mode": item.interview_mode,
            "interview_description": item.interview_description,
            "feedback": item.feedback,
            "saved_at": item.saved_at
        })

    return jsonify(result)

#Celery-Redis Routes===========================
@app.route('/company/interview-reminder-students/<int:company_id>', methods=['GET'])
def get_interview_reminder_students(company_id):
    jobs = JobPosition.query.filter_by(company_id=company_id).all()

    result = []

    for job in jobs:
        applications = JobApplication.query.filter_by(
            job_id=job.id,
            review_status='interview scheduled'
        ).all()

        for application in applications:
            student = Student.query.get(application.student_id)

            email_to = student.reminder_email or student.email

            result.append({
                'application_id': application.id,
                'student_name': student.full_name,
                'original_email': student.email,
                'reminder_email': email_to,
                'job_title': job.title,
                'interview_time': application.interview_time,
                'interview_mode': application.interview_mode or '',
                'message': f'''Hello {student.full_name},\n\nThis is a reminder for your interview for {job.title}.\n\nTime: {application.interview_time}\nMode / Link: {application.interview_mode}\n\nGood luck!'''
            })

    return jsonify(result)

@app.route('/company/send-interview-reminder', methods=['POST'])
def send_interview_reminder():
    data = request.json

    application = JobApplication.query.get(data['application_id'])

    if not application:
        return jsonify({'message': 'Application not found'}), 404

    student = Student.query.get(application.student_id)

    if not student:
        return jsonify({'message': 'Student not found'}), 404

    # Save override email if company changed it
    reminder_email = data.get('reminder_email')

    if reminder_email:
        student.reminder_email = reminder_email
        db.session.commit()
    else:
        reminder_email = student.email

    msg = Message(
        subject='Interview Reminder',
        sender=app.config['MAIL_USERNAME'],
        recipients=[reminder_email]
    )

    msg.body = data.get('message')

    mail.send(msg)

    return jsonify({'message': 'Reminder sent'})

#===========Routes fot html/csv imports===========
@app.route('/company/application-history/export', methods=['POST'])
def export_company_history():
    data = request.json

    task = celery.send_task(
    'celery_worker.export_application_history',
    args=[data['company_id'], data['format']]
    )

    return jsonify({
        'task_id': task.id
    })
    
@app.route('/company/application-history/export-status/<task_id>')
def export_company_history_status(task_id):
    try:
        task = celery.AsyncResult(task_id)

        if task.state == 'SUCCESS':
            filename = task.result

            return jsonify({
                'state': 'SUCCESS',
                'download_url': f'http://127.0.0.1:5000/company/application-history/download/{filename}'
            })

        elif task.state == 'FAILURE':
            return jsonify({
                'state': 'FAILURE',
                'error': str(task.result)
            })

        else:
            return jsonify({
                'state': task.state
            })

    except Exception as e:
        print("EXPORT STATUS ERROR:", str(e))
        return jsonify({
            'state': 'FAILURE',
            'error': str(e)
        }), 500
    
@app.route('/company/application-history/download/<filename>')
def download_company_history_file(filename):
    export_folder = os.path.join(app.root_path, 'exports')

    return send_from_directory(
        export_folder,
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)

