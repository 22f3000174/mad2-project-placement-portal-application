```vue
<template>
  <div class="container mt-5">
    <div class="card shadow p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Available Jobs</h2>

        <button
          class="btn btn-secondary"
          @click="$router.push('/student-lobby')"
        >
          Back
        </button>
      </div>

      <div class="mb-4">
        <input
          type="text"
          class="form-control"
          placeholder="Search by company, title, or skill..."
          v-model="searchText"
        >
      </div>

      <div
        v-for="job in filteredJobs"
        :key="job.id"
        class="card mb-4 border-0 shadow-sm"
      >
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
              <h4 class="mb-1">{{ job.title }}</h4>
              <h6 class="text-muted mb-0">{{ job.company_name }}</h6>
            </div>

            <span class="badge bg-primary fs-6">
              ₹ {{ job.salary }}
            </span>
          </div>

          <p>{{ job.description }}</p>

          <div class="row mb-3">
            <div class="col-md-4">
              <strong>Location:</strong><br>
              {{ job.location }}
            </div>

            <div class="col-md-4">
              <strong>Skills:</strong><br>
              {{ job.skills_required }}
            </div>

            <div class="col-md-4">
              <strong>Vacancies:</strong><br>
              {{ job.vacancies }}
            </div>
          </div>

          <div class="d-flex align-items-center gap-3 flex-wrap mb-3">
            <button
              class="btn"
              :class="job.application_status === 'applied' ? 'btn-secondary' : 'btn-success'"
              :disabled="job.application_status === 'applied'"
              @click="applyForJob(job.id)"
            >
              {{ job.application_status === 'applied' ? 'Applied' : 'Apply' }}
            </button>

            <span
              v-if="job.application_status === 'applied'"
              class="badge bg-info text-dark"
            >
              Review Status: {{ job.review_status }}
            </span>
          </div>

          <!-- Interview Details -->
          <div
            v-if="job.review_status === 'interview scheduled'"
            class="alert alert-warning mt-3"
          >
            <h6 class="mb-3">Interview Scheduled</h6>

            <p class="mb-2">
              <strong>Date & Time:</strong>
              {{ formatInterviewTime(job.interview_time) }}
            </p>

            <p
              v-if="job.interview_mode"
              class="mb-2"
            >
              <strong>Meeting Link / Location:</strong>

              <a
                v-if="job.interview_mode.startsWith('http')"
                :href="job.interview_mode"
                target="_blank"
                class="ms-1"
              >
                Join Interview
              </a>

              <span v-else>
                {{ job.interview_mode }}
              </span>
            </p>

            <p
              v-if="job.interview_description"
              class="mb-0"
            >
              <strong>Description:</strong>
              {{ job.interview_description }}
            </p>
          </div>

          <div
            v-if="job.feedback"
            class="alert alert-light border mt-3"
          >
            <strong>Company Feedback:</strong><br>
            {{ job.feedback }}
          </div>
        </div>
      </div>

      <div
        v-if="filteredJobs.length === 0"
        class="text-center text-muted py-5"
      >
        No jobs found.
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "StudentJobWatch",

  data() {
    return {
      jobs: [],
      searchText: ""
    }
  },

  computed: {
    filteredJobs() {
      return this.jobs.filter(job => {
        const text = this.searchText.toLowerCase()

        return (
          job.company_name.toLowerCase().includes(text) ||
          job.title.toLowerCase().includes(text) ||
          job.skills_required.toLowerCase().includes(text)
        )
      })
    }
  },

  mounted() {
    this.fetchJobs()
  },

  methods: {
    async fetchJobs() {
      try {
        const student = JSON.parse(localStorage.getItem("student"))

        const response = await axios.get(
          `http://127.0.0.1:5000/student/jobs/${student.id}`
        )

        this.jobs = response.data
      } catch (error) {
        console.error("Failed to fetch jobs", error)
      }
    },

    async applyForJob(jobId) {
      try {
        const student = JSON.parse(localStorage.getItem("student"))

        await axios.post("http://127.0.0.1:5000/student/apply-job", {
          student_id: student.id,
          job_id: jobId
        })

        const job = this.jobs.find(j => j.id === jobId)

        if (job) {
          job.application_status = "applied"
          job.review_status = "pending"
        }

        alert("Applied successfully")
      } catch (error) {
        alert(error.response?.data?.message || "Failed to apply")
      }
    },

    formatInterviewTime(time) {
      if (!time) return "Not provided"

      return new Date(time).toLocaleString()
    }
  }
}
</script>
