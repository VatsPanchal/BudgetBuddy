const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  // configureWebpack: {
  //   resolve: {
  //     alias: {
  //       vue: "@vue/runtime-core",
  //     },
  //   },
  // },
  chainWebpack: (config) => {
    config.plugin("define").tap((definitions) => {
      Object.assign(definitions[0], {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false",
        __VUE_OPTIONS_API__: "true",
        __VUE_PROD_DEVTOOLS__: "false",
      });
      return definitions;
    });
  },
  lintOnSave: false,
  devServer: {
    proxy: {
      "/api": {
        target:
          process.env.VUE_APP_API_URL ||
          "https://budget-buddy-backend-41557050751.us-central1.run.app",
        changeOrigin: true,
      },
    },
  },
  // Add production configuration
  publicPath: process.env.NODE_ENV === "production" ? "/" : "/",
  productionSourceMap: false,
});
