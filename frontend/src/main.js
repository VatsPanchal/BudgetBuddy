import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

// Configure axios
//axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.baseURL =
  "https://budget-buddy-backend-41557050751.us-central1.run.app";

axios.defaults.headers.common["Content-Type"] = "application/json";

// Add request interceptor for auth token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error("Error response:", error.response.data);
      if (error.response.status === 401) {
        // Unauthorized - redirect to login
        localStorage.removeItem("token");
        router.push("/login");
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error("Error request:", error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error("Error message:", error.message);
    }
    return Promise.reject(error);
  }
);

const app = createApp(App);
app.use(router);
app.mount("#app");
