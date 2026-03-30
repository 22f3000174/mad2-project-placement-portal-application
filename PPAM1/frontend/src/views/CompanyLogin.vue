<template>
  <div class="container mt-5">

    <div class="card shadow p-4 mx-auto" style="max-width: 500px;">
      <h2 class="mb-4 text-center">Company Login</h2>

      <form @submit.prevent="loginCompany">

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            v-model="email"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            v-model="password"
            required
          >
        </div>

        <div class="d-grid mb-3">
          <button type="submit" class="btn btn-success">
            Login
          </button>
        </div>

        <div class="text-center">
          <p class="mb-0">
            Don't have a company account?
            <router-link to="/company/register">
              Register here
            </router-link>
          </p>
        </div>

      </form>
    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyLogin",

  data() {
    return {
      email: "",
      password: ""
    }
  },

  methods: {
    async loginCompany() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/company/login",
          {
            email: this.email,
            password: this.password
          }
        )

        localStorage.setItem(
          "company",
          JSON.stringify(response.data.company)
        )

        this.$router.push("/company-lobby")

      } catch (error) {
        alert(error.response?.data?.message || "Login failed")
      }
    }
  }
}
</script>
