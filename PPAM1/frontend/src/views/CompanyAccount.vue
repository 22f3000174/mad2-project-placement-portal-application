<template>
  <div class="container mt-5">

    <div class="card shadow p-4">
      <h2 class="mb-4">Company Account</h2>

      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label"><strong>Company Name</strong></label>
          <input type="text" class="form-control" :value="company.name" readonly>
        </div>

        <div class="col-md-6">
          <label class="form-label"><strong>Email</strong></label>
          <input type="text" class="form-control" :value="company.email" readonly>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label"><strong>Contact Person (HR)</strong></label>
          <input type="text" class="form-control" :value="company.contact_person" readonly>
        </div>

        <div class="col-md-6">
          <label class="form-label"><strong>Website</strong></label>
          <input type="text" class="form-control" :value="company.website" readonly>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label"><strong>Status</strong></label>
          <input
            type="text"
            class="form-control"
            :value="company.is_verified ? 'Approved' : 'Pending Approval'"
            readonly
          >
        </div>
      </div>

      <div class="text-end mt-3">
        <button class="btn btn-secondary me-2" @click="$router.push('/company-lobby')">
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
  name: "CompanyAccount",

  data() {
    return {
      company: {}
    }
  },

  mounted() {
    const data = localStorage.getItem("company")

    if (data) {
      this.company = JSON.parse(data)
    } else {
      this.$router.push("/company/login")
    }
  },

  methods: {
    logout() {
      localStorage.removeItem("company")
      this.$router.push("/company/login")
    }
  }
}
</script>