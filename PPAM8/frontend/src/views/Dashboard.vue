<template>
<div class="container mt-5">

<h1 class="text-center mb-5">Placement Portal</h1>

<div class="row">

<!-- Student -->
<div class="col-md-4">
<div class="card shadow p-3">
<h3>Student</h3>

<router-link to="/student/login" class="btn btn-primary mb-2">
Login
</router-link>

<router-link to="/student/register" class="btn btn-outline-primary">
Register
</router-link>

</div>
</div>

<!-- Company -->
<div class="col-md-4">
<div class="card shadow p-3">
<h3>Company</h3>

<router-link to="/company/login" class="btn btn-success mb-2">
Login
</router-link>

<router-link to="/company/register" class="btn btn-outline-success">
Register
</router-link>

</div>
</div>

<!-- Admin -->
<div class="col-md-4">
<div class="card shadow p-3">
<h3>Admin</h3>

<router-link to="/admin/login" class="btn btn-danger mb-2">
Login
</router-link>

<!-- <router-link to="/admin/register" class="btn btn-outline-danger">
Register
</router-link> -->

</div>
</div>

</div>

</div>
</template>

<script>
export default {
name: "MainDashboard"
}
</script>
