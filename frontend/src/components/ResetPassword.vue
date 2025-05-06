<template>
  <div class="reset-password-container">
    <div class="reset-password-card">
      <h2>Reset Your Password</h2>
      <p class="subtitle">Enter your new password</p>

      <form @submit.prevent="handleSubmit" class="reset-password-form">
        <div class="form-group">
          <label for="newPassword">New Password</label>
          <input
            type="password"
            id="newPassword"
            v-model="newPassword"
            required
            minlength="8"
            placeholder="Enter new password"
            @input="validatePassword"
          />
          <span class="error" v-if="passwordError">{{ passwordError }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm New Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
            minlength="8"
            placeholder="Confirm new password"
            @input="validatePassword"
          />
          <span class="error" v-if="confirmError">{{ confirmError }}</span>
        </div>

        <button
          type="submit"
          class="btn-primary"
          :disabled="loading || passwordError || confirmError"
        >
          {{ loading ? "Resetting..." : "Reset Password" }}
        </button>

        <div class="error-message" v-if="error">
          {{ error }}
        </div>
      </form>

      <div class="back-to-login">
        <router-link to="/login" class="btn-link">
          ← Back to Login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "ResetPassword",
  data() {
    return {
      newPassword: "",
      confirmPassword: "",
      loading: false,
      error: null,
      passwordError: null,
      confirmError: null,
    };
  },
  methods: {
    validatePassword() {
      // Reset errors
      this.passwordError = null;
      this.confirmError = null;

      // Validate password length
      if (this.newPassword.length < 8) {
        this.passwordError = "Password must be at least 8 characters long";
        return false;
      }

      // Validate password match
      if (this.newPassword !== this.confirmPassword) {
        this.confirmError = "Passwords do not match";
        return false;
      }

      return true;
    },
    async handleSubmit() {
      if (!this.validatePassword()) {
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        console.log("Sending reset password request");
        const response = await api.post("/auth/reset-password", {
          token: this.$route.query.email,
          new_password: this.newPassword,
        });
        console.log("Response received:", response.data);

        if (response.data.message === "Password updated successfully") {
          // Redirect to login page
          this.$router.push("/login");
        }
      } catch (error) {
        console.error("Error details:", error.response?.data);
        if (error.response?.status === 422) {
          const details = error.response.data.detail;
          if (Array.isArray(details)) {
            this.error = details[0].msg;
          } else {
            this.error = "Invalid password format";
          }
        } else if (error.response?.status === 400) {
          this.error = "Invalid reset token";
        } else {
          this.error = "An error occurred. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.reset-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.reset-password-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
}

h2 {
  color: #4caf50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #6c757d;
  text-align: center;
  margin-bottom: 2rem;
}

.reset-password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #6c757d;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.btn-primary {
  background-color: #4caf50;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #43a047;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-link {
  color: #4caf50;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.btn-link:hover {
  color: #43a047;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.back-to-login {
  text-align: center;
  margin-top: 1rem;
}

.error {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
