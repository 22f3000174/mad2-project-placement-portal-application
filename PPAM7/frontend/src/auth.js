export function getCurrentUser() {
  const student = localStorage.getItem("student")
  const company = localStorage.getItem("company")
  const admin = localStorage.getItem("admin")

  if (student) {
    const data = JSON.parse(student)
    return {
      type: "student",
      name: data.name,
      email: data.email
    }
  }

  if (company) {
    const data = JSON.parse(company)
    return {
      type: "company",
      name: data.name,
      email: data.email
    }
  }

  if (admin) {
    const data = JSON.parse(admin)
    return {
      type: "admin",
      name: data.username,
      email: data.email
    }
  }

  return null
}

export function logoutUser() {
  localStorage.removeItem("student")
  localStorage.removeItem("company")
  localStorage.removeItem("admin")
}

export function isLoggedIn() {
  return getCurrentUser() !== null
}
