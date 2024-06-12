import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import BetsView from "@/views/BetsView.vue";
import FaqView from "@/views/FaqView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import store from "@/store";

const routes = [
  { 
    path: "/", 
    name: "Home",
    component: HomeView,
    meta: {
      requiresAuth: true
    }
  },
  { 
    path: "/about", 
    name: "About",
    component: AboutView,
  },
  { 
    path: "/bets", 
    name: "Bets",
    component: BetsView,
    meta: {
      requiresAuth: true
    }
  },
  { 
    path: "/faq", 
    name: "Faq",
    component: FaqView,
  },
  { 
    path: "/login", 
    name: "Login",
    component: LoginView,
  },
  { 
    path: "/register", 
    name: "Register",
    component: RegisterView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
