import { createRouter, createWebHistory } from "vue-router";
import UserLogin from "@/components/UserLogin.vue";
import CreateNewAccount from "@/components/CreateNewAccount.vue";
import ForgotPassword from "@/components/ForgotPassword.vue";
import SetupPage from "@/components/SetupPage.vue";

// Create the router instance
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Use WebHistory for Vue 3
  routes: [
    {
      path: "/",
      name: "UserLogin",
      component: UserLogin,
    },
    {
      path: "/create-account",
      name: "CreateNewAccount",
      component: CreateNewAccount,
    },
    {
      path: "/forgot-password",
      name: "ForgotPassword",
      component: ForgotPassword,
    },
    {
      path: "/setup-page",
      name: "SetupPage",
      component: SetupPage,
    },
  ],
});

export default router;
