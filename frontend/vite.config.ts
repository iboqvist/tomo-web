import { svelte } from "@sveltejs/vite-plugin-svelte";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [svelte()],
  // Same-origin /api in dev, mirroring the CloudFront /api/* behaviour in AWS
  server: { proxy: { "/api": "http://localhost:8000" } },
});
