<template>
  <div class="create-account-container">
    <div class="create-account-window">
      <h1 class="title-name">Create Account</h1>
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
        console.log("Account created:", this.formData);

        // Construct the request body
        const requestBody = {
          username: this.formData.username,
          firstName: this.formData.firstName,
          lastName: this.formData.lastName,
          email: this.formData.email,
          password: this.formData.password,
        };

        if (this.formData.phone) {
          requestBody.phone = this.formData.phone;
        }

        try {
          // Make the API call to create the account
          const response = await axios.post(
            "http://localhost:8000/users/",
            requestBody
          );
          // const response2 = await axios.post(
          //   "http://localhost:8000/users/",
          //   requestBody
          // );
          console.log("Account created successfully:", response.data);
          this.$router.push("/setup-page");
        } catch (error) {
          console.error("Error creating account:", error);
        }
      } else {
        alert("Please fill all the required fields!");
      }
    },

    validateForm() {
      // Ensure all required fields are filled
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
