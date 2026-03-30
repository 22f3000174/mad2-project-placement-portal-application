<template>
  <div class="container mt-5">

    <div class="card shadow p-4">
      <h2 class="mb-4 text-center">Student Register</h2>

      <form @submit.prevent="registerStudent">

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Student ID</label>
            <input
              type="text"
              class="form-control"
              v-model="student_id"
              required
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Course</label>
            <input
              type="text"
              class="form-control"
              v-model="course"
              required
            >
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">First Name</label>
            <input
              type="text"
              class="form-control"
              v-model="first_name"
              required
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Last Name</label>
            <input
              type="text"
              class="form-control"
              v-model="last_name"
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
            <label class="form-label">Phone</label>
            <input
              type="text"
              class="form-control"
              v-model="phone"
              required
            >
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">CGPA</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="10"
              class="form-control"
              v-model="cgpa"
              required
            >
          </div>

          <div class="col-md-6 mb-3">
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
            Register
          </button>
        </div>

      </form>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "StudentRegister",

  data() {
    return {
      student_id: "",
      first_name: "",
      last_name: "",
      email: "",
      phone: "",
      course: "",
      cgpa: "",
      password: ""
    }
  },

  methods: {
    async registerStudent() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/student/register",
          {
            student_id: this.student_id,
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            phone: this.phone,
            course: this.course,
            cgpa: this.cgpa,
            password: this.password
          }
        )

        alert(response.data.message)

        this.$router.push("/student/login")

      } catch (error) {
        alert(error.response?.data?.message || "Registration failed")
      }
    }
  }
}
</script>