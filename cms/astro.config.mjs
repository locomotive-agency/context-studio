import { defineConfig } from "astro/config";

export default defineConfig({
  server: { host: "127.0.0.1", port: 4321 },
  vite: {
    server: {
      allowedHosts: true,
      proxy: {
        "/api": "http://127.0.0.1:8001",
        "/mcp": "http://127.0.0.1:8001",
      },
    },
  },
});
