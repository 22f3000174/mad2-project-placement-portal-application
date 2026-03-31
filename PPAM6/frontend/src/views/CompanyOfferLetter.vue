```vue
<template>
  <div class="container mt-5">
    <div class="card shadow p-4 mx-auto" style="max-width: 700px;">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Upload Offer Letter</h2>

        <button
          class="btn btn-secondary"
          @click="$router.push('/company-lobby')"
        >
          Back
        </button>
      </div>

      <div class="mb-3">
        <label class="form-label">Select Student</label>

        <select
          class="form-select"
          v-model="selectedApplicationId"
        >
          <option disabled value="">Choose a student</option>

          <option
            v-for="application in applications"
            :key="application.application_id"
            :value="application.application_id"
          >
            {{ application.student_name }} - {{ application.job_title }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Offer Letter File</label>

        <input
          type="file"
          class="form-control"
          accept=".pdf,.doc,.docx"
          @change="handleFile"
        >

        <small class="text-muted">
          Upload PDF or Word document
        </small>
      </div>

      <div class="mb-3">
        <label class="form-label">Message to Student</label>

        <textarea
          class="form-control"
          rows="4"
          v-model="message"
          placeholder="Congratulations! Please find your offer letter attached."
        ></textarea>
      </div>

      <div
        v-if="selectedFile"
        class="alert alert-light border"
      >
        Selected File: {{ selectedFile.name }}
      </div>

      <button
        class="btn btn-success w-100"
        :disabled="!selectedApplicationId || !selectedFile || uploading"
        @click="uploadOfferLetter"
      >
        {{ uploading ? 'Uploading...' : 'Send Offer Letter' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyOfferLetter",

  data() {
    return {
      applications: [],
      selectedApplicationId: "",
      selectedFile: null,
      message: "",
      uploading: false
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

        const list = []

        response.data.forEach(job => {
          job.applications.forEach(application => {
            if (
              application.review_status === "selected" ||
              application.review_status === "offer pending"
            ) {
              list.push({
                application_id: application.application_id,
                student_name: application.student_name,
                job_title: job.title
              })
            }
          })
        })

        this.applications = list
      } catch (error) {
        alert("Failed to load selected students")
      }
    },

    handleFile(event) {
      this.selectedFile = event.target.files[0]
    },

    async uploadOfferLetter() {
      try {
        this.uploading = true

        const formData = new FormData()
        formData.append("application_id", this.selectedApplicationId)
        formData.append("message", this.message)
        formData.append("offer_letter", this.selectedFile)

        await axios.post(
          "http://127.0.0.1:5000/company/upload-offer-letter",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
        )

        alert("Offer letter uploaded successfully")

        this.selectedApplicationId = ""
        this.selectedFile = null
        this.message = ""
      } catch (error) {
        alert(
          error.response?.data?.message ||
          "Failed to upload offer letter"
        )
      } finally {
        this.uploading = false
      }
    }
  }
}
</script>

