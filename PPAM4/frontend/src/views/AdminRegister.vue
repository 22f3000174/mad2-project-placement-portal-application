<template>

<div class="container mt-5">

<h2>Admin Register</h2>

<form @submit.prevent="registerAdmin">

<div class="mb-3">
<label>Username</label>
<input type="text" v-model="username" class="form-control">
</div>

<div class="mb-3">
<label>Email</label>
<input type="email" v-model="email" class="form-control">
</div>

<div class="mb-3">
<label>Password</label>
<input type="password" v-model="password" class="form-control">
</div>

<button class="btn btn-success">
Register
</button>

</form>

</div>

</template>


<script>

import axios from "axios"

export default {

data(){
return{
username:"",
email:"",
password:""
}
},

methods:{

async registerAdmin(){

console.log("Admin Register Clicked")

try{

await axios.post("http://127.0.0.1:5000/admin/register",{

username:this.username,
email:this.email,
password:this.password

})

alert("Admin Registered Successfully")

}catch(error){

alert(error.response.data.message)

}

}


}

}

</script>
