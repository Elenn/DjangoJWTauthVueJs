import { createRouter, createWebHistory } from 'vue-router' 
import LoginView from "@/pages/LoginView";
import PostView from "@/pages/PostView";
import HomeView from "@/pages/HomeView";
import UserView from "@/pages/UserView";

const routes = [ 
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView },
    { path: '/posts', component: PostView },
    { path: '/user', component: UserView },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
