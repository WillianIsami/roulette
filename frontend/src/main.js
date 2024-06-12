import { createApp } from "vue";
import router from "./router/routes";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.min.css";

createApp(App).use(router).mount("#app");
