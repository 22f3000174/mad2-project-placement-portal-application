from celery_app import celery

# imports for sending basic email reminders
from flask_mail import Message
from app import app, mail
from models import (
    db,
    JobApplication,
    Student,
    JobPosition,
    Company,
    ApplicationHistory
)

# imports to export/download csv and html docs
import csv
import os
from datetime import datetime


# Code to send interview remainders
@celery.task(name='celery_worker.send_interview_reminders')
def send_interview_reminders():
    with app.app_context():
        applications = JobApplication.query.filter_by(
            review_status='interview scheduled',
            reminder_sent=False
        ).all()

        for application in applications:
            student = Student.query.get(application.student_id)
            job = JobPosition.query.get(application.job_id)
            company = Company.query.get(job.company_id)

            email_to = (
                student.reminder_email
                if hasattr(student, 'reminder_email') and student.reminder_email
                else student.email
            )

            msg = Message(
                subject='Interview Reminder',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email_to]
            )

            msg.body = f"""
Hello {student.first_name},

This is a reminder for your interview.

Company: {company.company_name}
Job: {job.title}
Time: {application.interview_time}
Mode / Link: {application.interview_mode}
Description: {application.interview_description}

Good luck!
"""

            mail.send(msg)
            application.reminder_sent = True
            db.session.commit()



# code to export application history


@celery.task(name='celery_worker.export_application_history')
def export_application_history(company_id, export_format):
    with app.app_context():
        jobs = JobPosition.query.filter_by(company_id=company_id).all()
        job_ids = [job.id for job in jobs]

        history = ApplicationHistory.query.filter(
            ApplicationHistory.job_id.in_(job_ids)
        ).order_by(ApplicationHistory.saved_at.desc()).all()

        export_folder = os.path.join(app.root_path, 'exports')
        os.makedirs(export_folder, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if export_format == 'csv':
            filename = f'application_history_{company_id}_{timestamp}.csv'
            filepath = os.path.join(export_folder, filename)

            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow([
                    'Student Name',
                    'Student Email',
                    'Course',
                    'CGPA',
                    'Job Title',
                    'Job Location',
                    'Salary',
                    'Review Status',
                    'Interview Time',
                    'Interview Mode',
                    'Interview Description',
                    'Feedback',
                    'Saved At'
                ])

                for item in history:
                    writer.writerow([
                        item.student_name,
                        item.student_email,
                        item.student_course,
                        item.student_cgpa,
                        item.job_title,
                        item.job_location,
                        item.job_salary,
                        item.review_status,
                        item.interview_time,
                        item.interview_mode,
                        item.interview_description,
                        item.feedback,
                        item.saved_at
                    ])

        else:
            filename = f'application_history_{company_id}_{timestamp}.html'
            filepath = os.path.join(export_folder, filename)

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write("""
                <html>
                <head>
                    <title>Application History</title>
                    <style>
                        body { font-family: Arial; margin: 30px; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { border: 1px solid #ccc; padding: 10px; }
                        th { background: #f0f0f0; }
                    </style>
                </head>
                <body>
                    <h1>Application History</h1>
                    <table>
                        <tr>
                            <th>Student</th>
                            <th>Email</th>
                            <th>Job</th>
                            <th>Status</th>
                            <th>Interview Time</th>
                            <th>Feedback</th>
                            <th>Saved At</th>
                        </tr>
                """)

                for item in history:
                    file.write(f"""
                    <tr>
                        <td>{item.student_name}</td>
                        <td>{item.student_email}</td>
                        <td>{item.job_title}</td>
                        <td>{item.review_status}</td>
                        <td>{item.interview_time or '-'}</td>
                        <td>{item.feedback or '-'}</td>
                        <td>{item.saved_at}</td>
                    </tr>
                    """)

                file.write("""
                    </table>
                </body>
                </html>
                """)

        return filename

