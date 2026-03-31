# CompanyJobWatch.vue

````vue
<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Job Applications</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company-lobby')"
      >
        Back
      </button>
    </div>

    <div
      v-for="job in jobs"
      :key="job.job_id"
      class="card shadow mb-4"
    >
      <div class="card-header bg-dark text-white">
        <h4 class="mb-1">{{ job.title }}</h4>
        <small>{{ job.location }} | ₹ {{ job.salary }}</small>
      </div>

      <div class="card-body">
        <div
          v-if="job.applications.length === 0"
          class="text-muted"
        >
          No students have applied yet.
        </div>

        <div
          v-for="application in job.applications"
          :key="application.application_id"
          class="border rounded p-3 mb-3"
        >
          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Name:</strong>
              {{ application.student_name }}
            </div>

            <div class="col-md-6">
              <strong>Email:</strong>
              {{ application.student_email }}
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Course:</strong>
              {{ application.student_course }}
            </div>

            <div class="col-md-6">
              <strong>CGPA:</strong>
              {{ application.student_cgpa }}
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Review Status</label>

            <select
              class="form-select"
              v-model="application.review_status"
            >
              <option value="pending">Pending</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="interview scheduled">Interview Scheduled</option>
              <option value="selected">Selected</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div
            v-if="application.review_status === 'interview scheduled'"
            class="row mb-3"
          >
            <div class="col-md-6">
              <label class="form-label">Interview Date & Time</label>
              <input
                type="datetime-local"
                class="form-control"
                v-model="application.interview_time"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label">Interview Mode / Link</label>
              <input
                type="text"
                class="form-control"
                v-model="application.interview_mode"
                placeholder="Google Meet link / Office location"
              />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Interview Description</label>
            <textarea
              class="form-control"
              rows="2"
              v-model="application.interview_description"
              placeholder="Technical round, bring resume, etc."
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Feedback</label>

            <textarea
              class="form-control"
              rows="3"
              v-model="application.feedback"
              placeholder="Optional feedback for the student"
            ></textarea>
          </div>

          <button
            class="btn btn-primary"
            @click="saveApplication(job, application)"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyJobWatch",

  data() {
    return {
      jobs: []
    }
  },

  mounted() {
    this.fetchApplications()
  },

  methods: {
    async fetchApplications() {
      try {
        const company = JSON.parse(localStorage.getItem("company"))

        const response = await axios.get(
          `http://127.0.0.1:5000/company/job-applications/${company.id}`
        )

        this.jobs = response.data.map(job => ({
          ...job,
          applications: job.applications.map(app => ({
            ...app,
            interview_mode: app.interview_mode || "",
            interview_description: app.interview_description || "",
            feedback: app.feedback || ""
          }))
        }))
      } catch (error) {
        alert("Failed to load applications")
      }
    },

    async saveApplication(job, application) {
      try {
        if (
          application.review_status === "interview scheduled" &&
          !application.interview_time
        ) {
          alert("Please choose an interview date and time")
          return
        }

        // First update the current application
        await axios.put(
          `http://127.0.0.1:5000/company/application/update/${application.application_id}`,
          {
            review_status: application.review_status,
            interview_time: application.interview_time,
            interview_mode: application.interview_mode,
            interview_description: application.interview_description,
            feedback: application.feedback
          }
        )

        // Then save a full snapshot into ApplicationHistory
        await axios.post(
          "http://127.0.0.1:5000/company/application-history",
          {
            application_id: application.application_id,
            student_name: application.student_name,
            student_email: application.student_email,
            student_course: application.student_course,
            student_cgpa: application.student_cgpa,

            job_id: job.job_id,
            job_title: job.title,
            job_location: job.location,
            job_salary: job.salary,

            review_status: application.review_status,
            interview_time: application.interview_time,
            interview_mode: application.interview_mode,
            interview_description: application.interview_description,
            feedback: application.feedback
          }
        )

        alert("Application and history saved successfully")
      } catch (error) {
        alert(
          error.response?.data?.message ||
          "Failed to save application"
        )
      }
    }
  }
}
</script>
