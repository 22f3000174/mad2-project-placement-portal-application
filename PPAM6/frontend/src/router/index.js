import { createRouter, createWebHistory } from "vue-router"

import Dashboard from "../views/Dashboard.vue"

import StudentLogin from "../views/StudentLogin.vue"
import StudentRegister from "../views/StudentRegister.vue"
import StudentAccount from "../views/StudentAccount.vue"

import CompanyLogin from "../views/CompanyLogin.vue"
import CompanyRegister from "../views/CompanyRegister.vue"
import CompanyAccount from "../views/CompanyAccount.vue"

import AdminLogin from "../views/AdminLogin.vue"
import AdminRegister from "../views/AdminRegister.vue"
import AdminAccount from "../views/AdminAccount.vue"

import CompanyPostJobs from "../views/CompanyPostJobs.vue"

import AdminJobWatch from "../views/AdminJobWatch.vue"
import StudentJobWatch from "../views/StudentJobWatch.vue"
import CompanyJobWatch from "../views/CompanyJobWatch.vue"

import CompanyOfferLetter from "../views/CompanyOfferLetter.vue"
import StudentOfferLetter from "../views/StudentOfferLetter.vue"

import CompanyApplicationHistory from "../views/CompanyApplicationHistory.vue"
const routes = [
  { path: "/", component: Dashboard },

  { path: "/student/login", component: StudentLogin },
  { path: "/student/register", component: StudentRegister },
  { path: "/student-lobby", component: StudentAccount },

  { path: "/company/login", component: CompanyLogin },
  { path: "/company/register", component: CompanyRegister },
  { path: "/company-lobby", component: CompanyAccount },

  { path: "/admin/login", component: AdminLogin },
  { path: "/admin/register", component: AdminRegister },
  { path: "/admin-lobby", component: AdminAccount },

  { path: "/company/post-jobs", component: CompanyPostJobs },

  { path: "/admin/jobs", component: AdminJobWatch },
  { path: "/student/jobs", component: StudentJobWatch },
  { path: "/company/applications", component: CompanyJobWatch },

  { path: "/company/offer-letter", component: CompanyOfferLetter },
  { path: "/student/offer-letters", component: StudentOfferLetter },
  
  { path: "/company/application-history", component: CompanyApplicationHistory }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router