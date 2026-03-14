import { createRouter, createWebHistory } from "vue-router";

import AboutView from "@/views/AboutView.vue";
import BetsView from "@/views/BetsView.vue";
import FaqView from "@/views/FaqView.vue";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import store from "@/store";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
    meta: {
      requiresAuth: true,
    },
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
      requiresAuth: true,
    },
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

router.beforeEach(async (to, from, next) => {
  if (!store.getters.authChecked) {
    await store.dispatch("checkAuth");
  }

  const isAuthenticated = store.getters.isAuthenticated;
  if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: "Login" });
    return;
  }

  if ((to.name === "Login" || to.name === "Register") && isAuthenticated) {
    next({ name: "Home" });
    return;
  }

  next();
});

export default router;
