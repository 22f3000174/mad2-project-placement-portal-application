<template>
  <div class="container mt-5">

    <div class="card shadow p-4 mb-5">
      <h2 class="mb-4 text-center">Admin Dashboard</h2>
      <div class="mb-4 text-end">
        <router-link to="/admin/jobs" class="btn btn-primary">
          View All Job Postings
        </router-link>
      </div>

    </div>

    <div class="card shadow p-4 mb-5">
      <h3 class="mb-4">Company Accounts</h3>

      <div class="mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search company by name..."
          v-model="searchCompany"
        >
      </div>

      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Company Name</th>
            <th>Contact Person</th>
            <th>Email</th>
            <th>Website</th>
            <th>Status</th>
            <th width="280">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="company in filteredCompanies" :key="company.id">
            <td>{{ company.company_name }}</td>
            <td>{{ company.contact_person }}</td>
            <td>{{ company.email }}</td>
            <td>{{ company.website }}</td>

            <td>
              <span
                class="badge"
                :class="company.status === 'enabled' ? 'bg-success' : 'bg-danger'"
              >
                {{ company.status }}
              </span>
            </td>

            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="updateCompanyStatus(company.id, 'enabled')"
              >
                Enable
              </button>

              <button
                class="btn btn-warning btn-sm me-2"
                @click="updateCompanyStatus(company.id, 'disabled')"
              >
                Disable
              </button>

              <button
                class="btn btn-danger btn-sm"
                @click="deleteCompany(company.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card shadow p-4">
      <h3 class="mb-4">Student Accounts</h3>

      <div class="mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search student by name..."
          v-model="searchStudent"
        >
      </div>

      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Student ID</th>
            <th>Course</th>
            <th>CGPA</th>
            <th width="220">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="student in filteredStudents" :key="student.id">
            <td>{{ student.name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.student_id }}</td>
            <td>{{ student.course }}</td>
            <td>{{ student.cgpa }}</td>

            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="updateStudentStatus(student.id, 'enabled')"
              >
                Enable
              </button>

              <button
                class="btn btn-warning btn-sm me-2"
                @click="updateStudentStatus(student.id, 'disabled')"
              >
                Disable
              </button>

              <button
                class="btn btn-danger btn-sm"
                @click="deleteStudent(student.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-end mt-4">
      <button class="btn btn-secondary me-2" @click="$router.push('/')">
        Home
      </button>

      <button class="btn btn-danger" @click="logout">
        Logout
      </button>
    </div>

  </div>
</template>

<script>
export default {
  name: "AdminAccount",

  data() {
    return {
      admin: {},
      companies: [],
      students: [],
      searchCompany: "",
      searchStudent: ""
    }
  },

  computed: {
    filteredCompanies() {
      return this.companies.filter(company =>
        company.company_name
          .toLowerCase()
          .includes(this.searchCompany.toLowerCase())
      )
    },

    filteredStudents() {
      return this.students.filter(student =>
        student.name
          .toLowerCase()
          .includes(this.searchStudent.toLowerCase())
      )
    }
  },

  mounted() {
    const adminData = localStorage.getItem("admin")

    if (!adminData) {
      this.$router.push("/admin/login")
      return
    }

    this.admin = JSON.parse(adminData)

    this.fetchCompanies()
    this.fetchStudents()
  },

  methods: {
    async fetchCompanies() {
      try {
        const response = await fetch("http://127.0.0.1:5000/admin/companies")
        this.companies = await response.json()
      } catch (error) {
        console.error("Failed to fetch companies:", error)
      }
    },

    async fetchStudents() {
      try {
        const response = await fetch("http://127.0.0.1:5000/admin/students")
        this.students = await response.json()
      } catch (error) {
        console.error("Failed to fetch students:", error)
      }
    },

    async updateCompanyStatus(id, status) {
      try {
        await fetch(`http://127.0.0.1:5000/admin/company/status/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ status })
        })

        this.fetchCompanies()

      } catch (error) {
        console.error("Failed to update company:", error)
      }
    },

    async updateStudentStatus(id, status) {
      try {
        await fetch(`http://127.0.0.1:5000/admin/student/status/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ status })
        })

        this.fetchStudents()

      } catch (error) {
        console.error("Failed to update student:", error)
      }
    },

    async deleteCompany(id) {
      const confirmDelete = confirm(
        "Are you sure you want to delete this company?"
      )

      if (!confirmDelete) return

      try {
        await fetch(`http://127.0.0.1:5000/admin/company/delete/${id}`, {
          method: "DELETE"
        })

        this.fetchCompanies()

      } catch (error) {
        console.error("Failed to delete company:", error)
      }
    },

    async deleteStudent(id) {
      const confirmDelete = confirm(
        "Are you sure you want to delete this student?"
      )

      if (!confirmDelete) return

      try {
        await fetch(`http://127.0.0.1:5000/admin/student/delete/${id}`, {
          method: "DELETE"
        })

        this.fetchStudents()

      } catch (error) {
        console.error("Failed to delete student:", error)
      }
    },

    logout() {
      localStorage.removeItem("admin")
      this.$router.push("/admin/login")
    }
  }
}
</script>