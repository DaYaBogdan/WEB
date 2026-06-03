import {createApp} from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import networkStatus from "../plugins/networkStatus.js";

import "vuetify/styles";
import {createVuetify} from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const vuetify = createVuetify({components, directives});

const app = createApp(App);

// Регистрация Service Worker для PWA
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log(
          "Service Worker зарегистрирован:",
          registration,
        );

        // Проверка обновлений
        registration.addEventListener("updatefound", () => {
          const newWorker = registration.installing;
          console.log(
            "Новый Service Worker найден:",
            newWorker,
          );

          newWorker.addEventListener("statechange", () => {
            if (
              newWorker.state === "installed" &&
              navigator.serviceWorker.controller
            ) {
              console.log(
                "Доступна новая версия, обновите страницу",
              );
              // Показываем уведомление о обновлении
              if (
                confirm(
                  "Доступна новая версия приложения. Обновить?",
                )
              ) {
                window.location.reload();
              }
            }
          });
        });
      })
      .catch((error) => {
        console.error(
          "Ошибка регистрации Service Worker:",
          error,
        );
      });
  });
}

// Отслеживание статуса сети
window.addEventListener("online", () => {
  console.log("Интернет появился");
  // Можно добавить уведомление для пользователя
});

window.addEventListener("offline", () => {
  console.log("Интернет пропал");
  // Можно добавить уведомление для пользователя
});

app
  .use(router)
  .use(store)
  .use(vuetify)
  .use(networkStatus)
  .mount("#app");
