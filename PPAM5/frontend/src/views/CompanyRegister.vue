<template>
  <div class="container mt-5">

    <div class="card shadow p-4">
      <h2 class="mb-4 text-center">Company Register</h2>

      <form @submit.prevent="registerCompany">

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Company Name</label>
            <input
              type="text"
              class="form-control"
              v-model="company_name"
              required
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Contact Person (HR)</label>
            <input
              type="text"
              class="form-control"
              v-model="contact_person"
              required
            >
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              v-model="email"
              required
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Website</label>
            <input
              type="text"
              class="form-control"
              v-model="website"
              placeholder="https://example.com"
            >
          </div>
        </div>

        <div class="row">
          <div class="col-md-12 mb-3">
            <label class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              v-model="password"
              required
            >
          </div>
        </div>

        <div class="d-grid mt-3">
          <button class="btn btn-success" type="submit">
            Register Company
          </button>
        </div>

      </form>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyRegister",

  data() {
    return {
      company_name: "",
      contact_person: "",
      email: "",
      website: "",
      password: ""
    }
  },

  methods: {
    async registerCompany() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/company/register",
          {
            company_name: this.company_name,
            contact_person: this.contact_person,
            email: this.email,
            website: this.website,
            password: this.password
          }
        )

        alert(response.data.message)

        this.$router.push("/company/login")

      } catch (error) {
        alert(error.response?.data?.message || "Registration failed")
      }
    }
  }
}
</script>