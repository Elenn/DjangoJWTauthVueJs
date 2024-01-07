<template>
    <div class="row justify-content-md-center">
        <div class="col-md-8">
            <div class="col-md-2">
                <button class="w-100 btn btn-lg btn-primary" @click="showUser">Show Current User</button> 
            </div> 
            <div v-if="user">
                Wellcome {{user.username}}:
            </div>
            <span>{{errorMessage}}</span>
        </div>
    </div>
</template>

<script>

import axios from 'axios';
export default {
    name: "PostView",
    data() {
        return {
            user: '',
            errorMessage:''
    }
    },
    computed: {
        tokenStr() {
            return this.$store.state.token;
        },
    },
    methods: {
        showUser() {
            this.errorMessage = ''
            axios.get('http://localhost:8000/api/user/', { headers: { "Authorization": `Bearer ${this.tokenStr}`}})
                .then(response => {
                    this.user = response.data
                    console.log(response.data);
                })
                .catch(error => {
                    this.errorMessage = ''
                    if (error.message == 'Request failed with status code 403')
                        this.errorMessage = 'You do not have access to see this data. Please login.'
                    console.error('Error:', error);
                });
        }, 
    }
    }
</script>