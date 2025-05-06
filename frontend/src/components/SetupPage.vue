<template>
  <div class="setup-container">
    <div class="setup-card">
      <h2>Set Up Your Budget</h2>
      <p class="subtitle">Let's create a plan that works for you</p>

      <form @submit.prevent="handleSubmit" class="setup-form">
        <div class="form-group">
          <label for="income">Monthly Income</label>
          <div class="input-with-symbol">
            <span class="symbol">$</span>
            <input
              type="number"
              id="income"
              v-model="income"
              required
              min="0"
              step="0.01"
              placeholder="Enter your monthly income"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="savings">Desired Monthly Savings</label>
          <div class="input-with-symbol">
            <span class="symbol">$</span>
            <input
              type="number"
              id="savings"
              v-model="savings"
              required
              min="0"
              step="0.01"
              placeholder="Enter desired savings"
            />
          </div>
        </div>

        <div class="categories-section">
          <h3>Category Allocation</h3>
          <div class="category-list">
            <div
              v-for="(amount, category) in categories"
              :key="category"
              class="category-item"
            >
              <div class="category-header">
                <span class="category-name">{{ category }}</span>
                <button
                  type="button"
                  class="remove-category"
                  @click="removeCategory(category)"
                  v-if="category !== 'Other'"
                >
                  ×
                </button>
              </div>
              <div class="input-with-symbol">
                <span class="symbol">$</span>
                <input
                  type="number"
                  v-model="categories[category]"
                  required
                  min="0"
                  step="0.01"
                  placeholder="Enter amount"
                />
              </div>
            </div>
          </div>

          <div class="add-category" v-if="canAddCategory">
            <select v-model="newCategory" class="category-select">
              <option value="" disabled>Select a category</option>
              <option
                v-for="cat in availableCategories"
                :key="cat"
                :value="cat"
              >
                {{ cat }}
              </option>
            </select>
            <button
              type="button"
              class="btn-secondary"
              @click="addCategory"
              :disabled="!newCategory"
            >
              Add Category
            </button>
          </div>
        </div>

        <div class="budget-summary">
          <div class="summary-item">
            <span>Total Allocated:</span>
            <span>${{ totalAllocated.toFixed(2) }}</span>
          </div>
          <div class="summary-item">
            <span>Remaining Budget:</span>
            <span>${{ remainingBudget.toFixed(2) }}</span>
          </div>
        </div>

        <button
          type="submit"
          class="btn-primary"
          :disabled="loading || !isValid"
        >
          {{ loading ? "Setting Up..." : "Complete Setup" }}
        </button>

        <div class="error-message" v-if="error">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "SetupPage",
  data() {
    return {
      income: "",
      savings: "",
      categories: {
        Rent: 0,
        Food: 0,
        Transport: 0,
        Utilities: 0,
        Other: 0,
      },
      availableCategories: [
        "Entertainment",
        "Shopping",
        "Healthcare",
        "Education",
        "Travel",
      ],
      newCategory: "",
      loading: false,
      error: null,
    };
  },
  computed: {
    totalAllocated() {
      return Object.values(this.categories).reduce(
        (sum, amount) => sum + Number(amount),
        0
      );
    },
    remainingBudget() {
      return this.income - this.savings - this.totalAllocated;
    },
    isValid() {
      return (
        this.income > 0 &&
        this.savings >= 0 &&
        this.remainingBudget >= 0 &&
        Object.values(this.categories).every((amount) => amount >= 0)
      );
    },
    canAddCategory() {
      return Object.keys(this.categories).length < 10;
    },
  },
  methods: {
    addCategory() {
      if (this.newCategory && !this.categories[this.newCategory]) {
        this.categories[this.newCategory] = 0;
        this.newCategory = "";
      }
    },
    removeCategory(category) {
      this.$delete(this.categories, category);
    },
    async handleSubmit() {
      if (this.totalAllocated + this.savings > this.income) {
        this.error = "Total allocation exceeds income";
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const token = localStorage.getItem("token");
        const response = await api.post("/budget/setup", {
          income: this.income,
          savings_goal: this.savings,
          categories: this.categories,
          username: token, // Using token as username since that's what we stored
        });

        if (response.data.message === "Budget setup successful") {
          this.$router.push("/dashboard");
        }
      } catch (error) {
        if (error.response) {
          this.error = error.response.data.detail || "Failed to setup budget";
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
.setup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.setup-card {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 4px 6px var(--shadow-color);
  padding: 2rem;
  width: 100%;
  max-width: 600px;
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

.setup-form {
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

.input-with-symbol {
  position: relative;
  display: flex;
  align-items: center;
}

.symbol {
  position: absolute;
  left: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.7;
}

input {
  padding: 0.75rem 0.75rem 0.75rem 2rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  width: 100%;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

input:focus {
  outline: none;
  border-color: var(--progress-fill);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.categories-section {
  margin-top: 2rem;
}

h3 {
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-item {
  background: var(--bg-primary);
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.category-name {
  font-weight: 500;
  color: var(--text-primary);
}

.remove-category {
  background: none;
  border: none;
  color: var(--error-text);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.add-category {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.category-select {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.budget-summary {
  background: var(--bg-primary);
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  border: 1px solid var(--border-color);
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
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

.btn-secondary:disabled {
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

@media (max-width: 480px) {
  .setup-card {
    padding: 1.5rem;
  }

  .add-category {
    flex-direction: column;
  }
}
</style>
