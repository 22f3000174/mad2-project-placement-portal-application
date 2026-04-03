<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">

      <router-link class="navbar-brand" to="/">
        Placement Portal
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-lg-center">

          <li class="nav-item">
            <router-link class="nav-link" to="/">
              Home
            </router-link>
          </li>

          <template v-if="!currentUser">
            <li class="nav-item">
              <router-link class="nav-link" to="/student/login">
                Student
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link" to="/company/login">
                Company
              </router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link" to="/admin/login">
                Admin
              </router-link>
            </li>
          </template>

          <li v-else class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
            >
              {{ currentUser.name }}
            </a>

            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <span class="dropdown-item-text fw-bold">
                  {{ currentUser.name }}
                </span>
              </li>

              <li>
                <span class="dropdown-item-text text-muted small">
                  {{ currentUser.email }}
                </span>
              </li>

              <li><hr class="dropdown-divider"></li>

              <li>
                <button class="dropdown-item text-danger" @click="logout">
                  Logout
                </button>
              </li>
            </ul>
          </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { getCurrentUser, logoutUser } from "../auth"

export default {
  name: "NavbarBar",

  data() {
    return {
      currentUser: null
    }
  },

  mounted() {
    this.currentUser = getCurrentUser()

    window.addEventListener("storage", this.refreshUser)
  },

  beforeUnmount() {
    window.removeEventListener("storage", this.refreshUser)
  },

  watch: {
    $route() {
      this.refreshUser()
    }
  },

  methods: {
    refreshUser() {
      this.currentUser = getCurrentUser()
    },

    logout() {
      logoutUser()
      this.currentUser = null

      alert("Logged out successfully")

      this.$router.push("/")
    }
  }
}
</script>