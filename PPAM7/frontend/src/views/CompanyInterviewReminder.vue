<template>
  <div class="container mt-5">
    <div class="card shadow p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Send Interview Reminder</h2>

        <button
          class="btn btn-secondary"
          @click="$router.push('/company-lobby')"
        >
          Back
        </button>
      </div>

      <div
        v-for="student in students"
        :key="student.application_id"
        class="card mb-4 border-0 shadow-sm"
      >
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
              <h4 class="mb-1">{{ student.student_name }}</h4>
              <div class="text-muted">{{ student.job_title }}</div>
            </div>

            <span class="badge bg-warning text-dark fs-6">
              Interview Scheduled
            </span>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Current Email</strong>
              <input
                type="email"
                class="form-control mt-1"
                :value="student.original_email"
                disabled
              >
            </div>

            <div class="col-md-6">
              <strong>Reminder Email Override</strong>
              <input
                type="email"
                class="form-control mt-1"
                v-model="student.reminder_email"
                placeholder="Leave empty to use current email"
              >
            </div>
          </div>

          <div class="mb-3">
            <strong>Interview Time</strong>
            <div>{{ student.interview_time }}</div>
          </div>

          <div class="mb-3">
            <strong>Interview Link / Mode</strong>
            <input
              type="text"
              class="form-control"
              v-model="student.interview_mode"
            >
          </div>

          <div class="mb-3">
            <strong>Email Message</strong>
            <textarea
              class="form-control"
              rows="5"
              v-model="student.message"
            ></textarea>
          </div>

          <button
            class="btn btn-primary"
            @click="sendReminder(student)"
          >
            Send Reminder
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyInterviewReminder",

  data() {
    return {
      students: []
    }
  },

  mounted() {
    this.fetchStudents()
  },

  methods: {
    async fetchStudents() {
      try {
        const company = JSON.parse(localStorage.getItem("company"))

        const response = await axios.get(
          `http://127.0.0.1:5000/company/interview-reminder-students/${company.id}`
        )

        this.students = response.data
      } catch (error) {
        alert("Failed to load students")
      }
    },

    async sendReminder(student) {
      try {
        await axios.post(
          "http://127.0.0.1:5000/company/send-interview-reminder",
          {
            application_id: student.application_id,
            reminder_email: student.reminder_email,
            interview_mode: student.interview_mode,
            message: student.message
          }
        )

        alert("Reminder email sent")
      } catch (error) {
        alert(error.response?.data?.message || "Failed to send reminder")
      }
    }
  }
}
</script>
