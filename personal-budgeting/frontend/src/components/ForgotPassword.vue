<template>
  <div class="forgot-password-container">
    <div class="forgot-password-window">
      <h1 class="title-name">Forgot Password</h1>
      <form @submit.prevent="handleForgotPassword" class="forgot-password-form">
        <div class="input-group">
          <label for="email">Email:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
          />
        </div>
        <button type="submit" class="submit-btn">Submit</button>
      </form>

      <div v-if="formSubmitted" class="confirmation">
        <h3>Password Reset Link Sent</h3>
        <p>
          A password reset link has been sent to your email. Please follow the
          instructions in the email to reset your password.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "", // Store the entered email address
      formSubmitted: false, // Flag to show the confirmation message
    };
  },
  methods: {
    handleForgotPassword() {
      // Simulate sending the password reset link
      this.formSubmitted = true;
      console.log("Password reset link sent to:", this.email);
      // You can replace this with a real API call to send the password reset link to the email address
    },
  },
};
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
}

.forgot-password-window {
  background: rgba(255, 255, 255, 0.8);
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
}

.title-name {
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

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
}

.submit-btn:hover {
  background-color: #45a049;
}

.confirmation {
  margin-top: 20px;
  color: green;
}
</style>
