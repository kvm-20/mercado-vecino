import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // En desarrollo local (npm run dev) se reenvía /api a la API
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        rewrite: (ruta) => ruta.replace(/^\/api/, ""),
      },
    },
  },
});
