<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <h2>Reset Your Password</h2>
      <p class="subtitle">Enter your email to receive a password reset link</p>

      <form
        @submit.prevent="handleSubmit"
        class="forgot-password-form"
        v-if="!resetSent"
      >
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
            @input="validateEmail"
          />
          <span class="error" v-if="emailError">{{ emailError }}</span>
        </div>

        <button
          type="submit"
          class="btn-primary"
          :disabled="loading || emailError"
        >
          {{ loading ? "Sending..." : "Send Reset Link" }}
        </button>

        <div class="error-message" v-if="error">
          {{ error }}
        </div>
      </form>

      <div class="success-message" v-else>
        <p>A password reset link has been sent to your email.</p>
        <p>
          Please check your inbox and follow the instructions to reset your
          password.
        </p>
        <router-link to="/login" class="btn-secondary">
          Return to Login
        </router-link>
      </div>

      <div class="back-to-login">
        <router-link to="/login" class="btn-link">
          ← Back to Login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ForgotPassword",
  data() {
    return {
      email: "",
      loading: false,
      error: null,
      emailError: null,
      resetSent: false,
    };
  },
  methods: {
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.emailError = "Email is required";
        return false;
      }
      if (!emailRegex.test(this.email)) {
        this.emailError = "Please enter a valid email address";
        return false;
      }
      this.emailError = null;
      return true;
    },
    async handleSubmit() {
      if (!this.validateEmail()) {
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        console.log("Sending request with email:", this.email);
        const response = await axios.post("/api/auth/forgot-password", {
          email: this.email,
        });
        console.log("Response received:", response.data);

        if (response.data.message) {
          this.resetSent = true;
          // Redirect to reset password page with email as query parameter
          this.$router.push({
            path: "/reset-password",
            query: { email: this.email },
          });
        }
      } catch (error) {
        console.error("Error details:", error.response?.data);
        if (error.response?.status === 404) {
          this.error = "No account found with this email address";
        } else if (error.response?.status === 422) {
          // Handle validation errors from the backend
          const details = error.response.data.detail;
          if (Array.isArray(details)) {
            this.error = details[0].msg;
          } else {
            this.error = "Invalid email format";
          }
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
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.forgot-password-card {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 4px 6px var(--shadow-color);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--border-color);
}

h2 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: var(--text-secondary);
  opacity: 0.8;
  text-align: center;
  margin-bottom: 2rem;
}

.forgot-password-form {
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
  color: var(--text-secondary);
}

input {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

input::placeholder {
  color: var(--text-secondary);
}

input:focus {
  outline: none;
  border-color: var(--progress-fill);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.btn-primary {
  background-color: var(--progress-fill);
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

.btn-secondary {
  background-color: var(--bg-primary);
  color: var(--progress-fill);
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--progress-fill);
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: var(--progress-fill);
  color: white;
}

.btn-link {
  color: var(--progress-fill);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.btn-link:hover {
  color: #43a047;
}

.error-message {
  color: var(--error-text);
  background-color: var(--error-bg);
  border: 1px solid var(--error-border);
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.success-message {
  text-align: center;
  color: var(--success-text);
  background-color: var(--success-bg);
  border: 1px solid var(--success-border);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.back-to-login {
  text-align: center;
  margin-top: 1rem;
}

.error {
  color: var(--error-text);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
