import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import AboutView from '@/views/AboutView.vue';
import BetsView from '@/views/BetsView.vue';
import FaqView from '@/views/FaqView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';


const routes = [
    { path: "/", component: HomeView },
    { path: "/about", component: AboutView },
    { path: "/bets", component: BetsView},
    { path: "/faq", component: FaqView },
    { path: "/login", component: LoginView },
    { path: "/register", component: RegisterView},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
