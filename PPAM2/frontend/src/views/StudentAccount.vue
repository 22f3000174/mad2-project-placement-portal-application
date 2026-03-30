<template>
  <div class="container mt-5">

    <div class="card shadow p-4">
      <h2 class="mb-4">Student Account</h2>

      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label"><strong>Name</strong></label>
          <input type="text" class="form-control" :value="student.name" readonly>
        </div>

        <div class="col-md-6">
          <label class="form-label"><strong>Email</strong></label>
          <input type="text" class="form-control" :value="student.email" readonly>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label"><strong>Student ID</strong></label>
          <input type="text" class="form-control" :value="student.student_id" readonly>
        </div>

        <div class="col-md-6">
          <label class="form-label"><strong>Course</strong></label>
          <input type="text" class="form-control" :value="student.course" readonly>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label"><strong>Phone</strong></label>
          <input type="text" class="form-control" :value="student.phone" readonly>
        </div>

        <div class="col-md-6">
          <label class="form-label"><strong>CGPA</strong></label>
          <input type="text" class="form-control" :value="student.cgpa" readonly>
        </div>
      </div>

      <div class="text-end mt-3">
        <button class="btn btn-secondary me-2" @click="$router.push('/student-lobby')">
          Back
        </button>

        <button class="btn btn-danger" @click="logout">
          Logout
        </button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "StudentAccount",

  data() {
    return {
      student: {}
    }
  },

  mounted() {
    const data = localStorage.getItem("student")

    if (data) {
      this.student = JSON.parse(data)
    } else {
      this.$router.push("/student/login")
    }
  },

  methods: {
    logout() {
      localStorage.removeItem("student")
      this.$router.push("/student/login")
    }
  }
}
</script>
