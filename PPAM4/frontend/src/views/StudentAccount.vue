<template>
  <div class="container mt-5">

    <div class="card shadow p-4">
      <h2 class="mb-4">Student Account</h2>
      <router-link to="/student/jobs" class="btn btn-primary">
        View Available Jobs
      </router-link>

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
