import { createApp } from "vue";
import router from "./router/routes";
import store from "./store";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "@/assets/styles/theme.css";

createApp(App).use(store).use(router).mount("#app");
