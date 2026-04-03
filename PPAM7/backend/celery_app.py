from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.beat_schedule = {
    'send-interview-reminders-every-minute': {
        'task': 'celery_worker.send_interview_reminders',
        'schedule': 60.0
    }
}

celery.conf.timezone = 'Asia/Kolkata'

import celery_worker