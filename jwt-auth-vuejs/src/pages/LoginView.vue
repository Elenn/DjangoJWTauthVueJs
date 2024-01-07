<template>
    <div class="row justify-content-md-center">
        <div class="col-md-3">  
            <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

            <input v-model="inputUserName" type="email" class="form-control" placeholder="Email" required>
            <input v-model="inputPassword" type="password" class="form-control" placeholder="Password" required>

            <button class="w-100 btn btn-lg btn-primary" @click="login">Login</button>
        </div>
    </div>
</template>

<script> 
import axios from 'axios';  
export default {
    name: "LoginView",
    data() {
        return {  
            inputUserName: '',
            inputPassword: '',
        }
    },
    methods: {
        login() {  
            axios.post('http://localhost:8000/api/login/', {
                username: this.inputUserName,
                password: this.inputPassword 
            })
                .then(response => {  
                    this.$store.dispatch('setAuth', true);
                    this.$store.dispatch('setToken', response.data.jwt);
                    console.log(response.data); 

                    this.$router.push('posts')   
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.$store.dispatch('setAuth', false);

                });
        }, 
    } 
 }
</script>