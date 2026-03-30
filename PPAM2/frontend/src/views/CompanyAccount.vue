<template>
  <div class="container mt-5">

    <div class="card shadow-lg border-0 rounded-4 overflow-hidden">

      <div class="bg-primary text-white p-4">
        <h2 class="mb-1">Welcome, {{ company.name }}</h2>
        <p class="mb-0 opacity-75">
          Manage your company profile and job postings here.
        </p>
      </div>

      <div class="card-body p-4">

        <div class="row g-4 mb-4">

          <div class="col-md-6">
            <div class="border rounded-4 p-3 h-100 bg-light">
              <h5 class="mb-3">Company Information</h5>

              <p class="mb-2">
                <strong>Company Name:</strong><br>
                {{ company.name }}
              </p>

              <p class="mb-2">
                <strong>Email:</strong><br>
                {{ company.email }}
              </p>

              <p class="mb-2">
                <strong>Contact Person (HR):</strong><br>
                {{ company.contact_person || 'Not provided' }}
              </p>

              <p class="mb-0">
                <strong>Website:</strong><br>
                {{ company.website || 'Not provided' }}
              </p>
            </div>
          </div>

          <div class="col-md-6">
            <div class="border rounded-4 p-3 h-100 bg-light">
              <h5 class="mb-3">Account Status</h5>

              <div class="mb-3">
                <span
                  class="badge fs-6 px-3 py-2"
                  :class="company.is_verified ? 'bg-success' : 'bg-warning text-dark'"
                >
                  {{ company.is_verified ? 'Approved by Admin' : 'Pending Approval' }}
                </span>
              </div>

              <p class="text-muted mb-0" v-if="company.is_verified">
                Your company account is active. You can now post jobs and manage listings.
              </p>

              <p class="text-muted mb-0" v-else>
                Your account is waiting for admin approval. Job posting may be restricted until approved.
              </p>
            </div>
          </div>

        </div>

        <div class="row g-4 mb-4">

          <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body text-center p-4">
                <h4 class="mb-3">Post a New Job</h4>
                <p class="text-muted mb-4">
                  Create a new job listing with salary, location, required skills, and vacancies.
                </p>

                <router-link
                  to="/company/post-jobs"
                  class="btn btn-primary btn-lg"
                >
                  Go to Job Posting
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body text-center p-4">
                <h4 class="mb-3">View Posted Jobs</h4>
                <p class="text-muted mb-4">
                  Review the jobs you have already posted and manage them later.
                </p>

                <button class="btn btn-outline-secondary btn-lg" disabled>
                  Coming Soon
                </button>
              </div>
            </div>
          </div>

        </div>

        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-outline-secondary" @click="$router.push('/')">
            Home
          </button>

          <button class="btn btn-danger" @click="logout">
            Logout
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "CompanyAccount",

  data() {
    return {
      company: {}
    }
  },

  mounted() {
    const data = localStorage.getItem("company")

    if (!data) {
      this.$router.push("/company/login")
      return
    }

    this.company = JSON.parse(data)
  },

  methods: {
    logout() {
      localStorage.removeItem("company")
      alert("Logged out successfully")
      this.$router.push("/company/login")
    }
  }
}
</script>