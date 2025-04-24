import { createApp } from "vue"; // For Vue 3
import App from "./App.vue";
import router from "./router"; // Import the router instance

createApp(App)
  .use(router) // Use the router
  .mount("#app"); // Mount the app
