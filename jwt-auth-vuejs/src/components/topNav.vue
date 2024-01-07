<template>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
                <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
                <router-link to="/posts" class="nav-link">Posts</router-link>
            </li>
            <li class="nav-item">
                <router-link to="/user" class="nav-link">User</router-link>
            </li>
        </ul>
        <ul class="navbar-nav">
            <li class="nav-item">
                <router-link to="/login" class="nav-link" v-if="!auth">Login</router-link>
            </li>
            <li class="nav-item">
                <router-link to="/login" class="nav-link" @click="logout"  v-if="auth">Logout</router-link>
            </li>
        </ul> 
    </nav>
</template>

<script> 
export default {
    name: "topNav",
    computed: {
        auth() {
            return this.$store.state.authenticated;
        },
    },
    methods: {
        logout() { 
            this.$store.dispatch('setAuth', false);
            this.$store.dispatch('setToken', '');
            this.$router.push('login') 
        }
    }
}
</script>
