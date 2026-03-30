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

          <div class="d-flex align-items-center gap-3">
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
    }
  }
}
</script>