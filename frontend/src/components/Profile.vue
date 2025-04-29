<template>
  <div class="profile">
    <div class="header">
      <div class="header-content">
        <button class="back-button" @click="goBack">
          <span class="back-icon">←</span>
          Back to Dashboard
        </button>
        <h1>Profile Settings</h1>
      </div>
    </div>

    <div class="profile-content">
      <div class="user-info">
        <h2>User Information</h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="info-grid">
          <div class="info-item">
            <label>First Name:</label>
            <span>{{ userInfo.first_name }}</span>
          </div>
          <div class="info-item">
            <label>Last Name:</label>
            <span>{{ userInfo.last_name }}</span>
          </div>
          <div class="info-item">
            <label>Username:</label>
            <span>{{ userInfo.username }}</span>
          </div>
          <div class="info-item">
            <label>Email:</label>
            <span>{{ userInfo.email }}</span>
          </div>
        </div>
      </div>

      <div class="password-change">
        <h2>Change Password</h2>
        <form @submit.prevent="changePassword" class="password-form">
          <div class="form-group">
            <label for="currentPassword">Current Password</label>
            <input
              type="password"
              id="currentPassword"
              v-model="passwordData.current_password"
              required
            />
          </div>
          <div class="form-group">
            <label for="newPassword">New Password</label>
            <input
              type="password"
              id="newPassword"
              v-model="passwordData.new_password"
              required
              minlength="8"
            />
          </div>
          <div class="form-group">
            <label for="confirmPassword">Confirm New Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="passwordData.confirm_password"
              required
              minlength="8"
            />
          </div>
          <div v-if="passwordError" class="error">{{ passwordError }}</div>
          <button type="submit" class="btn-primary" :disabled="passwordLoading">
            {{ passwordLoading ? "Changing..." : "Change Password" }}
          </button>
        </form>
      </div>

      <div class="delete-account">
        <h2>Delete Account</h2>
        <p class="warning">
          Warning: This action cannot be undone. All your data will be
          permanently deleted.
        </p>
        <form @submit.prevent="confirmDelete" class="delete-form">
          <div class="form-group">
            <label for="deleteUsername">Username</label>
            <input
              type="text"
              id="deleteUsername"
              v-model="deleteData.username"
              required
              placeholder="Enter your username"
            />
          </div>
          <div class="form-group">
            <label for="deletePassword">Password</label>
            <input
              type="password"
              id="deletePassword"
              v-model="deleteData.password"
              required
              placeholder="Enter your password"
            />
          </div>
          <div v-if="deleteError" class="error">{{ deleteError }}</div>
          <button type="submit" class="btn-danger" :disabled="deleteLoading">
            {{ deleteLoading ? "Deleting..." : "Delete Account" }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Profile",
  data() {
    return {
      userInfo: {
        first_name: "",
        last_name: "",
        username: "",
        email: "",
      },
      passwordData: {
        current_password: "",
        new_password: "",
        confirm_password: "",
      },
      loading: false,
      error: null,
      passwordLoading: false,
      passwordError: null,
      deleteData: {
        username: "",
        password: "",
      },
      deleteLoading: false,
      deleteError: null,
    };
  },
  async created() {
    await this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("/api/profile/info", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.userInfo = response.data;
      } catch (error) {
        console.error("Error fetching user info:", error);
        this.error =
          error.response?.data?.detail || "Failed to load user information";
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
      } finally {
        this.loading = false;
      }
    },
    async changePassword() {
      if (
        this.passwordData.new_password !== this.passwordData.confirm_password
      ) {
        this.passwordError = "New passwords do not match";
        return;
      }

      this.passwordLoading = true;
      this.passwordError = null;

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.post(
          "/api/profile/change-password",
          {
            current_password: this.passwordData.current_password,
            new_password: this.passwordData.new_password,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Clear form and show success message
        this.passwordData = {
          current_password: "",
          new_password: "",
          confirm_password: "",
        };
        this.passwordError = "Password changed successfully!";
      } catch (error) {
        console.error("Error changing password:", error);
        if (error.response?.data?.detail) {
          if (Array.isArray(error.response.data.detail)) {
            this.passwordError = error.response.data.detail.join(", ");
          } else {
            this.passwordError = error.response.data.detail;
          }
        } else {
          this.passwordError = "Failed to change password";
        }
      } finally {
        this.passwordLoading = false;
      }
    },
    async confirmDelete() {
      if (this.deleteData.username !== this.userInfo.username) {
        this.deleteError = "Username does not match";
        return;
      }

      if (
        !confirm(
          "Are you sure you want to delete your account? This action cannot be undone."
        )
      ) {
        return;
      }

      this.deleteLoading = true;
      this.deleteError = null;

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.delete("/api/auth/delete-account", {
          data: {
            username: this.deleteData.username,
            password: this.deleteData.password,
          },
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.data.message === "Account deleted successfully") {
          // Clear all user data from localStorage
          localStorage.removeItem("token");
          localStorage.removeItem("userInfo");
          localStorage.removeItem("budgetData");
          localStorage.removeItem("expenses");

          // Clear any Vuex state if it exists
          if (this.$store) {
            this.$store.commit("clearUserData");
          }

          // Redirect to login page
          this.$router.push("/login");
        }
      } catch (error) {
        console.error("Error deleting account:", error);
        if (error.response?.data?.detail) {
          this.deleteError = error.response.data.detail;
        } else {
          this.deleteError = "Failed to delete account";
        }
      } finally {
        this.deleteLoading = false;
      }
    },
    goBack() {
      this.$router.push("/dashboard");
    },
  },
};
</script>

<style scoped>
.profile {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.header {
  margin-bottom: 30px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: var(--progress-fill);
  font-size: 16px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: var(--bg-secondary);
}

.back-icon {
  font-size: 20px;
}

h1 {
  color: var(--text-primary);
  font-size: 24px;
}

.profile-content {
  display: grid;
  gap: 2rem;
}

.user-info,
.password-change,
.delete-account {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--shadow-color);
  padding: 1.5rem;
  border: 1px solid var(--border-color);
}

h2 {
  color: var(--text-primary);
  font-size: 20px;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 500;
  color: var(--text-secondary);
}

.info-item span {
  color: var(--text-primary);
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.loading,
.error {
  text-align: center;
  padding: 1rem;
  border-radius: 4px;
}

.loading {
  color: var(--text-secondary);
}

.error {
  color: var(--error-text);
  background-color: var(--error-bg);
  border: 1px solid var(--error-border);
}

.delete-account {
  margin-top: 2rem;
}

.warning {
  color: var(--error-text);
  margin-bottom: 1rem;
  font-weight: 500;
}

.btn-danger {
  background-color: var(--error-text);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-danger:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
