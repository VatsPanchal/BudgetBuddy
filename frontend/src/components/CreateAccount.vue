<template>
  <div class="create-account-container">
    <div class="create-account-card">
      <h2>Create Your Account</h2>
      <p class="subtitle">Start your journey to financial freedom</p>

      <form @submit.prevent="handleSubmit" class="create-account-form">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input
            type="text"
            id="firstName"
            v-model="firstName"
            required
            placeholder="Enter your first name"
          />
        </div>

        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input
            type="text"
            id="lastName"
            v-model="lastName"
            required
            placeholder="Enter your last name"
          />
        </div>

        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Choose a username"
          />
          <span class="error" v-if="usernameError">{{ usernameError }}</span>
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
          />
          <span class="error" v-if="emailError">{{ emailError }}</span>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Create a password"
          />
          <span class="error" v-if="passwordError">{{ passwordError }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
            placeholder="Confirm your password"
          />
          <span class="error" v-if="confirmPasswordError">{{
            confirmPasswordError
          }}</span>
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? "Creating Account..." : "Create Account" }}
        </button>

        <div class="error-message" v-if="error">
          {{ error }}
        </div>
      </form>

      <div class="login-prompt">
        <p>Already have an account?</p>
        <router-link to="/login" class="btn-secondary"> Login </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "CreateAccount",
  data() {
    return {
      firstName: "",
      lastName: "",
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      loading: false,
      error: null,
      usernameError: null,
      emailError: null,
      passwordError: null,
      confirmPasswordError: null,
    };
  },
  methods: {
    validateForm() {
      let isValid = true;

      // Reset errors
      this.usernameError = null;
      this.emailError = null;
      this.passwordError = null;
      this.confirmPasswordError = null;

      // Username validation
      if (this.username.length < 3) {
        this.usernameError = "Username must be at least 3 characters long";
        isValid = false;
      }

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.emailError = "Please enter a valid email address";
        isValid = false;
      }

      // Password validation
      if (this.password.length < 8) {
        this.passwordError = "Password must be at least 8 characters long";
        isValid = false;
      }

      // Confirm password validation
      if (this.password !== this.confirmPassword) {
        this.confirmPasswordError = "Passwords do not match";
        isValid = false;
      }

      return isValid;
    },
    async handleSubmit() {
      if (this.password !== this.confirmPassword) {
        this.error = "Passwords do not match";
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await api.post("/auth/register", {
          first_name: this.firstName,
          last_name: this.lastName,
          username: this.username,
          email: this.email,
          password: this.password,
        });

        if (response.data.message === "User created successfully") {
          // Store the token if provided
          if (response.data.token) {
            localStorage.setItem("token", response.data.token);
          }
          // Redirect to setup page
          this.$router.push("/setup");
        }
      } catch (error) {
        if (error.response) {
          switch (error.response.status) {
            case 400:
              this.error = error.response.data.detail || "Registration failed";
              break;
            case 422:
              this.error = "Please check your input and try again";
              break;
            default:
              this.error = "An error occurred. Please try again.";
          }
        } else {
          this.error = "Network error. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.create-account-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.create-account-card {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 4px 6px var(--shadow-color);
  padding: 2rem;
  width: 100%;
  max-width: 500px;
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

.create-account-form {
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

.error {
  color: var(--error-text);
  font-size: 0.875rem;
  margin-top: 0.25rem;
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
  margin-top: 1rem;
}

.btn-primary:hover {
  background-color: #43a047;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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

.login-prompt {
  margin-top: 2rem;
  text-align: center;
}

.login-prompt p {
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
  .create-account-card {
    padding: 1.5rem;
  }
}
</style>
