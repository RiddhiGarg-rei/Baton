import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The browser talks to /api/..., and Vite forwards it to the backend on port 8000.
// This avoids browser cross-origin (CORS) problems during development.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
