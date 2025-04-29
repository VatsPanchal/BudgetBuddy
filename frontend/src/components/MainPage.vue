<template>
  <div class="dashboard">
    <div class="header">
      <div class="menu-container">
        <button class="menu-button" @click="toggleMenu">
          <span class="menu-icon">☰</span>
        </button>
        <div v-if="showMenu" class="dropdown-menu">
          <router-link to="/profile" class="menu-item">
            <span class="menu-icon">👤</span>
            Profile
          </router-link>
          <router-link to="/edit-budget" class="menu-item">
            <span class="menu-icon">💰</span>
            Change Budget Distribution
          </router-link>
          <button class="menu-item" @click="logout">
            <span class="menu-icon">🚪</span>
            Logout
          </button>
        </div>
      </div>
      <div class="header-content">
        <div class="greeting">
          <h1>Welcome back, {{ userInfo.first_name }}!</h1>
          <p class="subtitle">Here's your financial overview for today</p>
        </div>
        <div class="date-display">
          {{ currentDate }}
        </div>
      </div>
    </div>

    <div class="content">
      <div class="budget-overview">
        <div class="budget-card">
          <h3>Monthly Budget</h3>
          <div class="budget-amount">
            ${{ budgetSummary.income.toFixed(2) }}
          </div>
          <div class="budget-details">
            <div class="detail-item">
              <span>Savings Goal</span>
              <span>${{ budgetSummary.savings_goal.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <span>Remaining</span>
              <span>${{ budgetSummary.remaining.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div class="expense-card">
          <h3>Add Expense</h3>
          <form @submit.prevent="addExpense" class="expense-form">
            <div class="form-group">
              <label for="category">Category</label>
              <select id="category" v-model="newExpense.category" required>
                <option value="" disabled>Select a category</option>
                <option
                  v-for="category in Object.keys(budgetSummary.categories)"
                  :key="category"
                  :value="category"
                >
                  {{ category }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="amount">Amount</label>
              <div class="input-with-symbol">
                <span class="symbol">$</span>
                <input
                  type="number"
                  id="amount"
                  v-model="newExpense.amount"
                  required
                  min="0"
                  step="0.01"
                  placeholder="Enter amount"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <input
                type="text"
                id="description"
                v-model="newExpense.description"
                placeholder="Add a note (optional)"
              />
            </div>

            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? "Adding..." : "Add Expense" }}
            </button>
            <div v-if="error" class="error-message">
              {{ error }}
            </div>
          </form>
        </div>
      </div>

      <div class="expense-distribution">
        <h3>Expense Distribution</h3>
        <div class="chart-container">
          <img
            v-if="chartImage"
            :src="'data:image/png;base64,' + chartImage"
            alt="Expense Distribution Chart"
            class="chart-image"
          />
          <div v-else class="no-data-message">No budget data available</div>
        </div>

        <div class="category-list">
          <div
            v-for="(amount, category) in budgetSummary.expenses"
            :key="category"
            class="category-item"
          >
            <div class="category-info">
              <span class="category-name">{{ category }}</span>
              <span class="category-amount">${{ amount.toFixed(2) }}</span>
            </div>
            <div class="progress-bar">
              <div
                class="progress"
                :style="{ width: getProgressPercentage(category) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div class="expense-history">
        <h3>Expense History</h3>

        <!-- Filter, Search, and Sort Controls -->
        <div class="expense-controls">
          <div class="control-group">
            <label for="category-filter">Filter by Category:</label>
            <select id="category-filter" v-model="selectedCategory">
              <option value="">All Categories</option>
              <option
                v-for="category in Object.keys(budgetSummary.categories)"
                :key="category"
                :value="category"
              >
                {{ category }}
              </option>
            </select>
          </div>

          <div class="control-group">
            <label for="search">Search:</label>
            <input
              type="text"
              id="search"
              v-model="searchQuery"
              placeholder="Search by description..."
            />
          </div>

          <div class="control-group">
            <label for="sort">Sort by:</label>
            <select id="sort" v-model="sortBy">
              <option value="date-desc">Date (Newest First)</option>
              <option value="date-asc">Date (Oldest First)</option>
              <option value="amount-desc">Amount (High to Low)</option>
              <option value="amount-asc">Amount (Low to High)</option>
              <option value="category">Category (A-Z)</option>
            </select>
          </div>
        </div>

        <div class="expense-list" v-if="filteredExpenses.length > 0">
          <div
            v-for="expense in filteredExpenses"
            :key="expense.id"
            class="expense-item"
          >
            <div class="expense-info">
              <span class="expense-category">{{ expense.category }}</span>
              <span class="expense-amount"
                >${{ expense.amount_spent.toFixed(2) }}</span
              >
              <span class="expense-description">{{ expense.description }}</span>
              <span class="expense-date">{{
                formatDate(expense.created_at)
              }}</span>
            </div>
            <button
              class="delete-btn"
              @click="deleteExpense(expense.id)"
              :disabled="loading"
            >
              Delete
            </button>
          </div>
        </div>
        <div v-else class="no-expenses">No expenses found.</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MainPage",
  data() {
    return {
      budgetSummary: {
        income: 0,
        savings_goal: 0,
        categories: {},
        expenses: {},
        remaining: 0,
      },
      userInfo: {
        first_name: "",
        last_name: "",
        username: "",
        email: "",
      },
      currentDate: "",
      chartImage: null,
      newExpense: {
        category: "",
        amount: "",
        description: "",
      },
      loading: false,
      error: null,
      showMenu: false,
      expenses: [],
      selectedCategory: "",
      searchQuery: "",
      sortBy: "date-desc",
    };
  },
  computed: {
    filteredCategories() {
      return Object.fromEntries(
        Object.entries(this.budgetSummary.categories).filter(
          ([_, budget]) => budget > 0
        )
      );
    },
    filteredExpenses() {
      let filtered = [...this.expenses];

      // Apply category filter
      if (this.selectedCategory) {
        filtered = filtered.filter(
          (expense) => expense.category === this.selectedCategory
        );
      }

      // Apply search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter((expense) =>
          expense.description.toLowerCase().includes(query)
        );
      }

      // Apply sorting
      switch (this.sortBy) {
        case "date-desc":
          filtered.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          break;
        case "date-asc":
          filtered.sort(
            (a, b) => new Date(a.created_at) - new Date(b.created_at)
          );
          break;
        case "amount-desc":
          filtered.sort((a, b) => b.amount_spent - a.amount_spent);
          break;
        case "amount-asc":
          filtered.sort((a, b) => a.amount_spent - b.amount_spent);
          break;
        case "category":
          filtered.sort((a, b) => a.category.localeCompare(b.category));
          break;
      }

      return filtered;
    },
  },
  async created() {
    await this.fetchUserInfo();
    await this.fetchBudgetSummary();
    await this.fetchChart();
    await this.fetchExpenses();
    this.updateCurrentDate();
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    handleClickOutside(event) {
      const menuContainer = this.$el.querySelector(".menu-container");
      if (menuContainer && !menuContainer.contains(event.target)) {
        this.showMenu = false;
      }
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    logout() {
      localStorage.removeItem("token");
      this.$emit("authenticated", false);
      this.$router.push("/login");
    },
    async fetchBudgetSummary() {
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
        this.budgetSummary = response.data;
      } catch (error) {
        console.error("Error fetching budget summary:", error);
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async fetchChart() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("/api/budget/chart", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.chartImage = response.data.image;
      } catch (error) {
        console.error("Error fetching chart:", error);
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    async fetchExpenses() {
      try {
        const response = await axios.get("/api/budget/expenses");
        this.expenses = response.data;
      } catch (error) {
        console.error("Error fetching expenses:", error);
      }
    },
    async addExpense() {
      this.loading = true;
      this.error = null;

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.post(
          "/api/budget/expense",
          this.newExpense,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        await this.fetchBudgetSummary();
        await this.fetchChart();
        await this.fetchExpenses();
        this.newExpense = {
          category: "",
          amount: "",
          description: "",
        };
      } catch (err) {
        console.error("Error adding expense:", err);
        this.error = err.response?.data?.detail || "Failed to add expense";
      } finally {
        this.loading = false;
      }
    },
    getProgressPercentage(category) {
      const budget = this.budgetSummary.categories[category] || 0;
      const spent = this.budgetSummary.expenses[category] || 0;
      return (spent / budget) * 100;
    },
    async deleteExpense(expenseId) {
      if (!confirm("Are you sure you want to delete this expense?")) {
        return;
      }

      this.loading = true;
      try {
        await axios.delete(`/api/budget/expense/${expenseId}`);
        // Remove the expense from the list
        this.expenses = this.expenses.filter((exp) => exp.id !== expenseId);
        // Refresh the budget summary and chart
        await this.fetchBudgetSummary();
        await this.fetchChart();
      } catch (error) {
        console.error("Error deleting expense:", error);
        alert("Failed to delete expense. Please try again.");
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return (
        date.toLocaleDateString() +
        " " +
        date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      );
    },
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("/api/auth/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.userInfo = response.data;
      } catch (error) {
        console.error("Error fetching user info:", error);
        if (error.response?.status === 401) {
          this.$router.push("/login");
        }
      }
    },
    updateCurrentDate() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-US", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
};
</script>

<style>
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background-color: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: 0 4px 6px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.header-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-left: 20px;
}

.greeting h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  background: linear-gradient(45deg, var(--progress-fill), #43a047);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.greeting .subtitle {
  margin: 8px 0 0;
  color: var(--text-secondary);
  font-size: 16px;
}

.date-display {
  color: var(--text-secondary);
  font-size: 16px;
  padding: 8px 16px;
  background: var(--bg-primary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.menu-container {
  position: relative;
}

.menu-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  margin-right: 15px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.menu-button:hover {
  background-color: var(--border-color);
}

.menu-icon {
  font-size: 24px;
  color: var(--text-primary);
}

.content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.budget-overview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.budget-card,
.expense-card,
.expense-distribution,
.expense-history {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--shadow-color);
  padding: 1.5rem;
  border: 1px solid var(--border-color);
}

h3 {
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.budget-amount {
  font-size: 2rem;
  font-weight: 600;
  color: var(--progress-fill);
  margin-bottom: 1rem;
}

.budget-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  color: var(--text-primary);
}

.expense-form {
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

select,
input {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
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
  padding-left: 2rem;
  width: 100%;
}

select:focus,
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

.expense-distribution {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--shadow-color);
  padding: 1.5rem;
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem 0;
  min-height: 400px;
  background: var(--card-bg);
  border-radius: 8px;
  padding: 1rem;
}

.chart-image {
  max-width: 100%;
  height: auto;
}

.no-data-message {
  color: var(--text-secondary);
  opacity: 0.7;
  font-style: italic;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.category-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-info {
  display: flex;
  justify-content: space-between;
  font-weight: 500;
}

.progress-bar {
  height: 8px;
  background: var(--progress-bg);
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: var(--progress-fill);
  transition: width 0.3s ease;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow-color);
  min-width: 200px;
  z-index: 1000;
  margin-top: 5px;
  border: 1px solid var(--border-color);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  text-decoration: none;
  color: var(--text-primary);
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: var(--bg-secondary);
}

.menu-item .menu-icon {
  margin-right: 10px;
  font-size: 18px;
}

@media (max-width: 768px) {
  .budget-overview {
    grid-template-columns: 1fr;
  }
}

.expense-history {
  margin-top: 2rem;
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--shadow-color);
  padding: 1.5rem;
}

.expense-history h3 {
  color: var(--progress-fill);
  margin-bottom: 1rem;
}

.expense-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 4px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 200px;
}

.control-group label {
  font-weight: 500;
  color: var(--text-primary);
}

.control-group select,
.control-group input {
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 0.9rem;
}

.control-group select:focus,
.control-group input:focus {
  outline: none;
  border-color: var(--progress-fill);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.expense-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.expense-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 4px;
  border-left: 4px solid var(--progress-fill);
}

.expense-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.expense-category {
  font-weight: 500;
  color: var(--progress-fill);
}

.expense-amount {
  font-weight: bold;
}

.expense-description {
  color: var(--text-secondary);
  font-style: italic;
}

.expense-date {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.delete-btn {
  background: var(--error-text);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.delete-btn:hover {
  background: var(--error-border);
}

.delete-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.no-expenses {
  text-align: center;
  color: var(--text-secondary);
  padding: 2rem;
}

@media (max-width: 768px) {
  .expense-controls {
    flex-direction: column;
  }

  .control-group {
    width: 100%;
  }
}

.error-message {
  color: var(--error-text);
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: var(--error-bg);
  border: 1px solid var(--error-border);
  border-radius: 4px;
  font-size: 0.9rem;
}
</style>
