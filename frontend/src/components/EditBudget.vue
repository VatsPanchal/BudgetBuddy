<template>
  <div class="edit-budget">
    <div class="header">
      <h1>Edit Budget Distribution</h1>
      <router-link to="/dashboard" class="back-button"
        >← Back to Dashboard</router-link
      >
    </div>

    <div class="budget-form">
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
            placeholder="Enter monthly income"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="savings">Savings Goal (%)</label>
        <div class="input-with-symbol">
          <input
            type="number"
            id="savings"
            v-model="savingsPercentage"
            required
            min="0"
            max="100"
            step="1"
            placeholder="Enter savings percentage"
          />
          <span class="symbol">%</span>
        </div>
      </div>

      <div class="categories">
        <h3>Category Distribution</h3>
        <div class="category-list">
          <div
            v-for="(category, index) in categories"
            :key="index"
            class="category-item"
          >
            <div class="category-header">
              <input
                type="text"
                v-model="category.name"
                placeholder="Category name"
                required
              />
              <div class="input-with-symbol">
                <span class="symbol">$</span>
                <input
                  type="number"
                  v-model="category.amount"
                  required
                  min="0"
                  step="0.01"
                  placeholder="Amount"
                  :class="{ 'error-input': hasCategoryError(category.name) }"
                />
              </div>
            </div>
            <div v-if="hasCategoryError(category.name)" class="error-message">
              Cannot reduce budget below current spending of ${{
                getCategorySpending(category.name).toFixed(2)
              }}
            </div>
          </div>
        </div>

        <button class="add-category" @click="addCategory">
          + Add Category
        </button>
      </div>

      <div class="form-actions">
        <button
          class="btn-primary"
          @click="updateBudget"
          :disabled="loading || hasErrors"
        >
          {{ loading ? "Updating..." : "Update Budget" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditBudget",
  data() {
    return {
      income: 0,
      savingsPercentage: 0,
      categories: [],
      currentSpending: {},
      loading: false,
      error: null,
    };
  },
  computed: {
    hasErrors() {
      return this.categories.some((category) =>
        this.hasCategoryError(category.name)
      );
    },
  },
  async created() {
    await this.fetchCurrentBudget();
    await this.fetchCurrentSpending();
  },
  methods: {
    async fetchCurrentBudget() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("/api/budget/summary", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.income = response.data.income;
        this.savingsPercentage =
          (response.data.savings_goal / response.data.income) * 100;

        // Convert categories object to array format
        this.categories = Object.entries(response.data.categories).map(
          ([name, amount]) => ({
            name,
            amount,
          })
        );
      } catch (error) {
        console.error("Error fetching budget:", error);
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async fetchCurrentSpending() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("/api/budget/expenses", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Calculate total spending per category
        this.currentSpending = response.data.reduce((acc, expense) => {
          acc[expense.category] =
            (acc[expense.category] || 0) + expense.amount_spent;
          return acc;
        }, {});
      } catch (error) {
        console.error("Error fetching expenses:", error);
      }
    },
    addCategory() {
      this.categories.push({ name: "", amount: 0 });
    },
    hasCategoryError(categoryName) {
      const currentSpending = this.getCategorySpending(categoryName);
      const category = this.categories.find((c) => c.name === categoryName);
      return category && category.amount < currentSpending;
    },
    getCategorySpending(categoryName) {
      return this.currentSpending[categoryName] || 0;
    },
    async updateBudget() {
      if (this.hasErrors) {
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const savingsAmount = (this.income * this.savingsPercentage) / 100;
        const categories = this.categories.reduce((acc, category) => {
          acc[category.name] = category.amount;
          return acc;
        }, {});

        await axios.post(
          "/api/budget/update",
          {
            income: this.income,
            savings_goal: savingsAmount,
            categories: categories,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.$router.push("/dashboard");
      } catch (error) {
        console.error("Error updating budget:", error);
        this.error = error.response?.data?.detail || "Failed to update budget";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.edit-budget {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.back-button {
  color: var(--progress-fill);
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.budget-form {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--shadow-color);
  padding: 2rem;
  border: 1px solid var(--border-color);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
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
  width: 100%;
  padding: 0.75rem;
  padding-left: 2rem;
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

.error-input {
  border-color: var(--error-text);
}

.error-message {
  color: var(--error-text);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.categories {
  margin-top: 2rem;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.category-item {
  background: var(--bg-secondary);
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}

.category-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.category-header input {
  flex: 1;
}

.add-category {
  background: none;
  border: 2px dashed var(--progress-fill);
  color: var(--progress-fill);
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  width: 100%;
  transition: all 0.2s;
}

.add-category:hover {
  background: var(--bg-secondary);
}

.form-actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
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

@media (max-width: 768px) {
  .edit-budget {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .category-header {
    flex-direction: column;
  }
}
</style>
