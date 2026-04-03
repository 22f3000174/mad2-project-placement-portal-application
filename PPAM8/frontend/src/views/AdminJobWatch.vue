
<template>
  <div class="container mt-5">

    <div class="card shadow p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">All Job Postings</h2>

        <button
          class="btn btn-secondary"
          @click="$router.push('/admin-lobby')"
        >
          Back to Dashboard
        </button>
      </div>

      <div class="mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by company or job title..."
          v-model="searchText"
        >
      </div>

      <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Salary</th>
              <th>Location</th>
              <th>Skills Required</th>
              <th>Vacancies</th>
              <th width="120">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="job in filteredJobs" :key="job.id">
              <td>{{ job.company_name }}</td>
              <td>{{ job.title }}</td>
              <td>₹ {{ job.salary }}</td>
              <td>{{ job.location }}</td>
              <td>{{ job.skills_required }}</td>
              <td>{{ job.vacancies }}</td>

              <td>
                <button
                  class="btn btn-danger btn-sm"
                  @click="deleteJob(job.id)"
                >
                  Delete
                </button>
              </td>
            </tr>

            <tr v-if="filteredJobs.length === 0">
              <td colspan="7" class="text-center text-muted py-4">
                No matching job postings found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "AdminJobWatch",

  data() {
    return {
      jobs: [],
      searchText: ""
    }
  },

  computed: {
    filteredJobs() {
      return this.jobs.filter(job => {
        const text = this.searchText.toLowerCase()

        return (
          job.company_name.toLowerCase().includes(text) ||
          job.title.toLowerCase().includes(text)
        )
      })
    }
  },

  mounted() {
    const admin = localStorage.getItem("admin")

    if (!admin) {
      this.$router.push("/admin/login")
      return
    }

    this.fetchJobs()
  },

  methods: {
    async fetchJobs() {
      try {
        const response = await fetch("http://127.0.0.1:5000/admin/jobs")
        this.jobs = await response.json()
      } catch (error) {
        console.error("Failed to fetch jobs:", error)
      }
    },

    async deleteJob(id) {
      const confirmDelete = confirm(
        "Are you sure you want to delete this job posting?"
      )

      if (!confirmDelete) return

      try {
        await fetch(`http://127.0.0.1:5000/admin/job/delete/${id}`, {
          method: "DELETE"
        })

        this.fetchJobs()

      } catch (error) {
        console.error("Failed to delete job:", error)
      }
    }
  }
}
</script>

