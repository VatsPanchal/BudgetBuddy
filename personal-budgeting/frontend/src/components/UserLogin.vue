<template>
  <div class="login-container">
    <div class="login-window">
      <h1 class="app-name">Spend Wise</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Enter your username"
          />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" class="login-btn">Login</button>
      </form>
      <div class="forgot-password">
        <a href="#" @click="handleForgotPassword">Forgot Password?</a>
      </div>
      <div class="create-account">
        <p>
          Don't have an account?
          <a href="#" @click="handleCreateAccount">Create Account</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      console.log("Logging in with:", this.username, this.password);
    },
    handleForgotPassword() {
      //alert("Redirecting to forgot password page");
      this.$router.push("/forgot-password");
    },
    handleCreateAccount() {
      // alert("Redirecting to create account page");
      this.$router.push("/create-account");
    },
  },
};
</script>

<style scoped>
/* Styling for your login page */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
}

.login-window {
  background: rgba(255, 255, 255, 0.8);
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
}

.app-name {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
}

.forgot-password {
  margin-top: 10px;
}

.forgot-password a {
  color: #007bff;
  text-decoration: none;
}

.create-account {
  margin-top: 20px;
}

.create-account a {
  color: #007bff;
  text-decoration: none;
}
</style>
