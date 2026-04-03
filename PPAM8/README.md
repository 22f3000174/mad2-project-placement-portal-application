# mad2-project-placement-portal-application

# Redis cache applied to on the following:

# Cached the company applications route:
/company/job-applications/<company_id>
with cache key:
company_job_applications_<company_id>
# Cached the company application history route:
/company/application-history/<company_id>
with cache key:
company_application_history_<company_id>
# Cached the student jobs route:
/student/jobs/<student_id>
with cache key:
student_jobs_<student_id>
# Cleared those caches whenever data changes:
In /student/apply-job:
cache.delete(f"student_jobs_{data['student_id']}")
In /company/application/update/<application_id>:
cache.delete(f"company_job_applications_{job.company_id}")
cache.delete(f"company_application_history_{job.company_id}")
cache.delete(f"student_jobs_{application.student_id}")

# expiry policies:
student_jobs expires after 60 seconds
company_job_applications expires after 60 seconds
company_application_history expires after 120 seconds
# implemented refresh by manually deleting the cache whenever the underlying data changes.
