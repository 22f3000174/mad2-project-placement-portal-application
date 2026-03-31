<template>
  <div class="container mt-5">
    <div class="card shadow p-4 mx-auto" style="max-width: 800px;">
      <h2 class="text-center mb-4">Post New Job</h2>

      <form @submit.prevent="postJob">

        <div class="mb-3">
          <label class="form-label">Job Title</label>
          <input
            type="text"
            class="form-control"
            v-model="title"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea
            class="form-control"
            rows="4"
            v-model="description"
            required
          ></textarea>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Salary</label>
            <input
              type="number"
              class="form-control"
              v-model="salary"
              required
            />
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Location</label>
            <input
              type="text"
              class="form-control"
              v-model="location"
              required
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Skills Required</label>
          <input
            type="text"
            class="form-control"
            placeholder="Python, SQL, Vue, Flask"
            v-model="skills_required"
            required
          />
        </div>

        <div class="mb-4">
          <label class="form-label">Vacancies</label>
          <input
            type="number"
            class="form-control"
            v-model="vacancies"
            min="1"
            required
          />
        </div>

        <div class="d-grid">
          <button class="btn btn-success" type="submit">
            Post Job
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyPostJobs",

  data() {
    return {
      title: "",
      description: "",
      salary: "",
      location: "",
      skills_required: "",
      vacancies: 1
    }
  },

  methods: {
    async postJob() {
      try {
        const company = JSON.parse(localStorage.getItem("company"))

        await axios.post("http://127.0.0.1:5000/company/post-job", {
          company_id: company.id,
          title: this.title,
          description: this.description,
          salary: this.salary,
          location: this.location,
          skills_required: this.skills_required,
          vacancies: this.vacancies
        })

        alert("Job posted successfully")

        this.$router.push("/company-lobby")

      } catch (error) {
        alert(error.response?.data?.message || "Failed to post job")
      }
    }
  }
}
</script>