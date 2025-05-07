<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Welcome to Budget Buddy</h2>
      <p class="subtitle">Take control of your finances today</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username or Email</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Enter your username or email"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? "Logging in..." : "Login" }}
          </button>
          <button type="button" class="btn-link" @click="forgotPassword">
            Forgot Password?
          </button>
        </div>

        <div class="error-message" v-if="error">
          {{ error }}
        </div>
      </form>

      <div class="signup-prompt">
        <p>Don't have an account?</p>
        <router-link to="/create-account" class="btn-secondary">
          Create New Account
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post("/api/auth/login", {
          username: this.username,
          password: this.password,
        });

        if (response.data.access_token) {
          localStorage.setItem("token", response.data.access_token);
          this.$emit("authenticated", true);
          this.$router.push("/dashboard");
        }
      } catch (err) {
        if (err.response && err.response.data.detail) {
          this.error = err.response.data.detail;
        } else {
          this.error = "An error occurred during login";
        }
      } finally {
        this.loading = false;
      }
    },
    forgotPassword() {
      this.$router.push("/forgot-password");
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.login-card {
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

.login-form {
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

input:focus {
  outline: none;
  border-color: var(--progress-fill);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.btn-link {
  background: none;
  border: none;
  color: var(--progress-fill);
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
}

.btn-link:hover {
  text-decoration: underline;
}

.error-message {
  color: var(--error-text);
  background-color: var(--error-bg);
  border: 1px solid var(--error-border);
  text-align: center;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.signup-prompt {
  margin-top: 2rem;
  text-align: center;
}

.signup-prompt p {
  margin-bottom: 1rem;
  color: var(--text-secondary);
  opacity: 0.8;
}

.btn-secondary {
  display: inline-block;
  background-color: var(--bg-primary);
  color: var(--progress-fill);
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--progress-fill);
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: var(--progress-fill);
  color: white;
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
