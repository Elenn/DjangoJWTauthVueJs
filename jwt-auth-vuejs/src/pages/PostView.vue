<template>
    <div class="row justify-content-md-center">
        <div class="col-md-8">
            <div class="col-md-2">
                <button class="w-100 btn btn-lg btn-primary" @click="showPosts">Show Posts</button>
                <button class="w-100 btn btn-lg btn-primary" @click="createPost">Create Posts</button>
            </div> 

            <div class="post-list" v-for="post in posts" :key="post">
                {{post.title}}: {{post.content}}
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
            posts: [],
            errorMessage:''
    }
    },
    computed: {
        tokenStr() {
            return this.$store.state.token;
        },
    },
    methods: {
        showPosts() {
            this.errorMessage = ''
            axios.get('http://localhost:8000/pages/posts/', { headers: { "Authorization": `Bearer ${this.tokenStr}`}})
                .then(response => {
                    this.posts = response.data
                    console.log(response.data);
                })
                .catch(error => {
                    this.errorMessage = ''
                    if (error.message == 'Request failed with status code 403')
                        this.errorMessage = 'You do not have access to see this data. Please login.'
                    console.error('Error:', error);
                });
        }, 
        createPost() {
            this.errorMessage = ''
            axios.post('http://localhost:8000/pages/posts/', { title: 'aaa', content: 'bbb'}, { headers: { "Authorization": `Bearer ${this.tokenStr}` } })
                .then(response => {
                    this.posts = response.data
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