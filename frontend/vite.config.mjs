import { defineConfig } from "vite";
import { resolve } from "path";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
    base: "/static",
    build: {
        manifest: "manifest.json",
        outDir: resolve("./assets"),
        assetsDir: "django-assets",
        rollupOptions: {
            input: resolve("./js/main.js"),
        },
    },
    server: {
        host: "0.0.0.0",
        port: 5173,
        strictPort: true,
        allowedHosts: ["vite"],
    },
    plugins: [tailwindcss()],
});
