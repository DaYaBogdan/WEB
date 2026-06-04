import {defineConfig} from "vite";
import vue from "@vitejs/plugin-vue";
import {VitePWA} from "vite-plugin-pwa";
import {fileURLToPath, URL} from "url";
import VueDevTools from "vite-plugin-vue-devtools";

export default defineConfig({
  plugins: [
    vue(),
    VueDevTools(), //-------- Потом отрубить
    VitePWA({
      devOptions: {
        enabled: false, // Пока отрублено
      },
      registerType: "autoUpdate",
      includeAssets: [
        "phoenix_144x144.png",
        "phoenix_192x192.png",
        "phoenix_512x512.png",
        "favicon.ico",
      ],
      manifest: {
        name: "Дневник",
        short_name: "Дневник",
        description: "Ежедневник для записи задач и событий",
        theme_color: "#FF6A13",
        background_color: "#ffffff",
        display: "standalone",
        start_url: "/",
        scope: "/",
        icons: [
          {
            src: "/phoenix_144x144.png",
            sizes: "144x144",
            type: "image/png",
            purpose: "any maskable",
          },
          {
            src: "/phoenix_192x192.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "any maskable",
          },
          {
            src: "/phoenix_512x512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any maskable",
          },
        ],
      },
      workbox: {
        globPatterns: [
          "**/*.{js,css,html}",
          "**/*.{ico,png,svg,jpg,jpeg,webp}",
          "**/*.{woff,woff2,ttf,eot}",
        ],
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
        runtimeCaching: [
          {
            urlPattern: /\/api\/diary\/getTasks\/.*/,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-tasks-cache",
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /\/api\/managing\/getAllClients/,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-clients-cache",
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /\/api\/diary\/deleteTask\/.*/,
            handler: "NetworkOnly",
            options: {
              backgroundSync: {
                name: "delete-queue",
                options: {
                  maxRetentionTime: 24 * 60,
                },
              },
            },
          },
        ],
      },
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
