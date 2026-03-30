<template>
  <div class="container mt-5">

    <div class="card shadow p-4 mx-auto" style="max-width: 500px;">
      <h2 class="mb-4 text-center">Admin Login</h2>

      <form @submit.prevent="loginAdmin">

        <div class="mb-3">
          <label class="form-label">Username / Email</label>
          <input
            type="text"
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
          <button type="submit" class="btn btn-danger">
            Login
          </button>
        </div>

      </form>
    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "AdminLogin",

  data() {
    return {
      email: "",
      password: ""
    }
  },

  methods: {
    async loginAdmin() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/admin/login",
          {
            email: this.email,
            password: this.password
          }
        )

        localStorage.setItem(
          "admin",
          JSON.stringify(response.data.admin)
        )

        this.$router.push("/admin-lobby")

      } catch (error) {
        alert(error.response?.data?.message || "Login failed")
      }
    }
  }
}
</script>