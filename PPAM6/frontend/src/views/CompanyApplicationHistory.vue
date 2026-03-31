```vue
<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="mb-1">Application History</h2>
        <p class="text-muted mb-0">
          Complete history of applicant status changes for your company.
        </p>
      </div>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company-lobby')"
      >
        Back
      </button>
    </div>

    <div
      v-if="history.length === 0"
      class="alert alert-light border text-center"
    >
      No history records found.
    </div>

    <div
      v-for="record in history"
      :key="record.id"
      class="card shadow-sm mb-4 border-0"
    >
      <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
        <div>
          <h5 class="mb-1">{{ record.student_name }}</h5>
          <small>{{ record.job_title }}</small>
        </div>

        <span class="badge bg-info text-dark fs-6">
          {{ record.review_status }}
        </span>
      </div>

      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-6">
            <strong>Email:</strong><br>
            {{ record.student_email }}
          </div>

          <div class="col-md-3">
            <strong>Course:</strong><br>
            {{ record.student_course }}
          </div>

          <div class="col-md-3">
            <strong>CGPA:</strong><br>
            {{ record.student_cgpa }}
          </div>
        </div>

        <div class="row mb-3">
          <div class="col-md-4">
            <strong>Job Location:</strong><br>
            {{ record.job_location }}
          </div>

          <div class="col-md-4">
            <strong>Salary:</strong><br>
            ₹ {{ record.job_salary }}
          </div>

          <div class="col-md-4">
            <strong>Saved At:</strong><br>
            {{ formatDate(record.saved_at) }}
          </div>
        </div>

        <div
          v-if="record.interview_time"
          class="mb-3"
        >
          <strong>Interview Time:</strong><br>
          {{ formatDate(record.interview_time) }}
        </div>

        <div
          v-if="record.interview_mode"
          class="mb-3"
        >
          <strong>Interview Link / Mode:</strong><br>

          <a
            v-if="record.interview_mode.startsWith('http')"
            :href="record.interview_mode"
            target="_blank"
          >
            {{ record.interview_mode }}
          </a>

          <span v-else>
            {{ record.interview_mode }}
          </span>
        </div>

        <div
          v-if="record.interview_description"
          class="mb-3"
        >
          <strong>Interview Description:</strong><br>
          {{ record.interview_description }}
        </div>

        <div
          v-if="record.feedback"
          class="mb-3"
        >
          <strong>Feedback:</strong><br>
          {{ record.feedback }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyApplicationHistory",

  data() {
    return {
      history: []
    }
  },

  mounted() {
    this.fetchHistory()
  },

  methods: {
    async fetchHistory() {
      try {
        const company = JSON.parse(localStorage.getItem("company"))

        const response = await axios.get(
          `http://127.0.0.1:5000/company/application-history/${company.id}`
        )

        this.history = response.data
      } catch (error) {
        alert("Failed to load application history")
      }
    },

    formatDate(value) {
      if (!value) return "-"
      return new Date(value).toLocaleString()
    }
  }
}
</script>
