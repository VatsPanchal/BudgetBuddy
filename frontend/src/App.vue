<template>
  <div id="app">
    <header v-if="isAuthenticated">
      <nav class="navbar">
        <div class="navbar-brand">
          <h1>Budget Buddy</h1>
        </div>
      </nav>
    </header>
    <div class="theme-toggle-container">
      <button class="theme-toggle" @click="toggleTheme">
        <span class="theme-icon">{{ isDarkMode ? "🌞" : "🌙" }}</span>
      </button>
    </div>
    <main>
      <router-view @authenticated="setAuthenticated"></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      isAuthenticated: false,
      isDarkMode: localStorage.getItem("theme") === "dark",
    };
  },
  methods: {
    setAuthenticated(status) {
      this.isAuthenticated = status;
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem("theme", this.isDarkMode ? "dark" : "light");
      document.documentElement.setAttribute(
        "data-theme",
        this.isDarkMode ? "dark" : "light"
      );
    },
  },
  created() {
    // Initialize theme from localStorage or default to light
    const theme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", theme);
  },
};
</script>

<style>
:root {
  /* Light theme (default) */
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --text-primary: #212529;
  --text-secondary: #6c757d;
  --border-color: #ddd;
  --shadow-color: rgba(0, 0, 0, 0.1);
  --card-bg: #ffffff;
  --progress-bg: #e9ecef;
  --progress-fill: #4caf50;
  --error-bg: #f8d7da;
  --error-border: #f5c6cb;
  --error-text: #dc3545;
  --header-bg: #4caf50;
  --header-text: #ffffff;
}

[data-theme="dark"] {
  --bg-primary: #121212;
  --bg-secondary: #1e1e1e;
  --text-primary: #f8f9fa;
  --text-secondary: #adb5bd;
  --border-color: #444;
  --shadow-color: rgba(0, 0, 0, 0.3);
  --card-bg: #1e1e1e;
  --progress-bg: #444;
  --progress-fill: #4caf50;
  --error-bg: #4a1a1a;
  --error-border: #6a2a2a;
  --error-text: #ff6b6b;
  --header-bg: #2d2d2d;
  --header-text: #ffffff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s,
    box-shadow 0.3s;
}

body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s, color 0.3s;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-primary);
}

header {
  background-color: var(--header-bg);
  color: var(--header-text);
  padding: 1rem;
  box-shadow: 0 2px 4px var(--shadow-color);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.navbar-brand h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.theme-toggle-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
}

.theme-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
  color: var(--text-primary);
}

.theme-toggle:hover {
  background-color: var(--bg-secondary);
}

.theme-icon {
  font-size: 24px;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  background-color: var(--bg-primary);
}

@media (max-width: 768px) {
  main {
    padding: 1rem;
  }
}
</style>
