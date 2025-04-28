<template>
  <div class="create-account-container">
    <div class="create-account-window">
      <h1 class="title-name">Create Account</h1>
      <form @submit.prevent="submitForm" class="login-form">
        <div class="input-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="formData.username"
            required
            placeholder="Enter your username"
          />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            required
            placeholder="Enter your password"
          />
        </div>
        <div class="input-group">
          <label for="firstName">First Name:</label>
          <input
            type="text"
            id="firstName"
            v-model="formData.firstName"
            required
            placeholder="First Name"
          />
        </div>
        <div class="input-group">
          <label for="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            v-model="formData.lastName"
            required
            placeholder="Last Name"
          />
        </div>
        <div class="input-group">
          <label for="email">Email:</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            required
            placeholder="Enter your email"
          />
        </div>
        <div class="input-group">
          <label for="phone">Phone Number (Optional):</label>
          <input
            type="text"
            id="phone"
            v-model="formData.phone"
            placeholder="xxx-xxx-xxxx"
          />
        </div>
        <button type="submit" class="login-btn">Create Account</button>
      </form>

      <div v-if="formSubmitted" class="confirmation">
        <h3>Account Created Successfully!</h3>
        <p>Username: {{ formData.username }}</p>
        <p>Email: {{ formData.email }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

// Create an axios instance with default config
const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // Using 127.0.0.1 instead of localhost
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

export default {
  data() {
    return {
      formData: {
        username: "",
        password: "",
        firstName: "",
        lastName: "",
        email: "",
        phone: "",
      },
      formSubmitted: false,
    };
  },
  methods: {
    async submitForm() {
      if (this.validateForm()) {
        this.formSubmitted = true;
        console.log("Account creation attempt:", this.formData);

        const requestBody = {
          username: this.formData.username,
          first_name: this.formData.firstName,
          last_name: this.formData.lastName,
          email: this.formData.email,
          password: this.formData.password,
          phone: this.formData.phone || "0000000000",
        };

        try {
          console.log("Sending request to:", "http://127.0.0.1:8000/register");
          const response = await api.post("/register", requestBody);
          console.log("Account created successfully:", response.data);
          if (response.status === 200 || response.status === 201) {
            // Store the user data in localStorage or Vuex if needed
            localStorage.setItem("userData", JSON.stringify(response.data));
            // Redirect to setup page
            await this.$router.push("/setup-page");
          }
        } catch (error) {
          console.error("Full error object:", error);
          console.error("Error response:", error.response);
          console.error("Error message:", error.message);
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            alert(
              `Account creation failed: ${
                error.response.data.detail || error.response.statusText
              }`
            );
          } else if (error.request) {
            // The request was made but no response was received
            alert(
              "No response from server. Please check if the backend is running."
            );
          } else {
            // Something happened in setting up the request that triggered an Error
            alert(`Error: ${error.message}`);
          }
          this.formSubmitted = false;
        }
      } else {
        alert("Please fill all the required fields!");
      }
    },

    validateForm() {
      return (
        this.formData.username &&
        this.formData.password &&
        this.formData.firstName &&
        this.formData.lastName &&
        this.formData.email
      );
    },
  },
};
</script>

<style scoped>
.create-account-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
}

.create-account-window {
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

.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
}

button:hover {
  background-color: #45a049;
}

.confirmation {
  margin-top: 20px;
  color: green;
}
</style>
