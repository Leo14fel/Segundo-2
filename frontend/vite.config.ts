import { defineConfig } from "vitest/config";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 4200,
    host: "127.0.0.1",
    strictPort: true,
    proxy: {
      "/api": { target: "http://127.0.0.1:8082", changeOrigin: true },
      "/ws": { target: "ws://127.0.0.1:8082", ws: true },
    },
  },
  build: {
    rolldownOptions: {
      output: {
        codeSplitting: {
          groups: [
            { name: "vuetify", test: /node_modules[\\/]vuetify/ },
            { name: "vue-flow", test: /node_modules[\\/](@vue-flow|d3-)/ },
          ],
        },
      },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
    server: {
      deps: {
        // Vuetify importa CSS de componentes desde node_modules.
        // Inlining hace que Vite procese esos assets durante Vitest
        // en lugar de delegarlos al import nativo de Node.
        inline: [/vuetify/],
      },
    },
  },
});
