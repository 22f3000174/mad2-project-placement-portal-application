<template>
<div class="row g-4 mt-2">

  <div class="col-md-6">
    <div class="card border-0 shadow-sm rounded-4 h-100">
      <div class="card-body text-center p-4">
        <h4 class="mb-3">Available Jobs</h4>

        <p class="text-muted mb-4">
          Browse open job positions, apply, and track your application status.
        </p>

        <router-link
          to="/student/jobs"
          class="btn btn-primary btn-lg"
        >
          View Available Jobs
        </router-link>
      </div>
    </div>
  </div>

  <div class="col-md-6">
    <div class="card border-0 shadow-sm rounded-4 h-100">
      <div class="card-body text-center p-4">
        <h4 class="mb-3">Offer Letters</h4>

        <p class="text-muted mb-4">
          Download placement confirmation and offer letters shared by companies.
        </p>

        <router-link
          to="/student/offer-letters"
          class="btn btn-success btn-lg"
        >
          View Offer Letters
        </router-link>
      </div>
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
