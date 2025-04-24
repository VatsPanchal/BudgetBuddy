<template>
  <div class="setup-container">
    <div class="setup-window">
      <h1 class="title-name">Setup Your Budget</h1>
      <form @submit.prevent="submitSetup" class="setup-form">
        <!-- Monthly Income -->
        <div class="input-group">
          <label for="income">Monthly Income</label>
          <input
            type="number"
            id="income"
            v-model="income"
            required
            placeholder="Enter your monthly income"
            @input="updateRemainingIncome"
          />
        </div>

        <!-- Total Income and Remaining Income Display -->
        <div class="income-info">
          <p>Total Income: ${{ income }}</p>
          <p>Remaining Income: ${{ remainingIncome }}</p>
        </div>

        <!-- Expense Categories and Budgets -->
        <div
          v-for="(category, index) in categories"
          :key="index"
          class="category-row"
        >
          <div class="input-group">
            <label for="category">Category</label>
            <select v-model="category.selected" @change="updateRemainingIncome">
              <option disabled value="">Select a category</option>
              <option
                v-for="categoryOption in allCategories"
                :key="categoryOption"
                :value="categoryOption"
              >
                {{ categoryOption }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label for="budget">Budget</label>
            <input
              type="number"
              v-model="category.budget"
              :disabled="!category.selected"
              required
              placeholder="Enter budget"
              @input="updateRemainingIncome"
            />
          </div>

          <!-- Remove Button -->
          <button type="button" @click="removeCategory(index)" v-if="index > 0">
            Remove Category
          </button>
        </div>

        <!-- Add Category Button -->
        <button
          type="button"
          @click="addCategory"
          :disabled="categories.length >= allCategories.length"
        >
          Add Expense Category
        </button>

        <!-- Submit Button -->
        <button
          type="submit"
          class="submit-btn"
          :disabled="remainingIncome > 0"
        >
          Submit
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      income: 0,
      remainingIncome: 0,
      categories: [{ selected: "", budget: 0 }],
      allCategories: [
        "Food & Dining 🍔",
        "Transport 🚗",
        "Shopping 🛍️",
        "Utilities ⚡",
        "Medical & Healthcare 🏥",
        "Entertainment & Leisure 🎬",
        "Rent & Housing 🏠",
        "Miscellaneous 💰",
      ],
    };
  },
  methods: {
    // Add a new category row (only if there are categories left)
    addCategory() {
      // Avoid duplicate categories
      const selectedCategories = this.categories.map(
        (category) => category.selected
      );
      const availableCategories = this.allCategories.filter(
        (category) => !selectedCategories.includes(category)
      );
      if (availableCategories.length > 0) {
        this.categories.push({ selected: availableCategories[0], budget: 0 });
      }
    },

    // Remove a category row
    removeCategory(index) {
      this.categories.splice(index, 1);
      this.updateRemainingIncome();
    },

    // Update the remaining income when a budget is added or changed
    updateRemainingIncome() {
      let totalBudget = 0;
      this.categories.forEach((category) => {
        if (category.budget) {
          totalBudget += parseFloat(category.budget);
        }
      });
      this.remainingIncome = this.income - totalBudget;
    },

    // Handle form submission
    async submitSetup() {
      // Collect the data and send it to the backend
      const setupData = {
        income: this.income,
        categories: this.categories.map((category) => ({
          category: category.selected,
          budget: category.budget,
        })),
      };

      // Make the API call to submit the data
      try {
        const response = await axios.post(
          "http://localhost:8000/setup/",
          setupData
        );
        console.log("Setup completed:", response.data);
        // You can redirect to another page or show a success message
      } catch (error) {
        console.error("Error completing setup:", error);
      }
    },
  },
};
</script>
<style scoped>
.setup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
}

.setup-window {
  background: rgba(255, 255, 255, 0.8);
  padding: 30px;
  border-radius: 10px;
  width: 500px;
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

.input-group input,
.input-group select {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.income-info {
  font-size: 1.2rem;
  margin-bottom: 20px;
  font-weight: bold;
}

.category-row {
  margin-bottom: 20px;
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

button:disabled {
  background-color: #ccc;
}

button[type="button"] {
  background-color: #f44336;
  color: white;
  padding: 8px 16px;
  border-radius: 5px;
  border: none;
  font-size: 1rem;
}

button[type="button"]:hover {
  background-color: #e53935;
}
</style>
