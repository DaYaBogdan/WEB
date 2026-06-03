import {ref} from "vue";

export default {
  install(app) {
    // Глобальное состояние сети
    const isOnline = ref(navigator.onLine);

    const updateOnlineStatus = () => {
      isOnline.value = navigator.onLine;
      if (isOnline.value) {
        console.log("Соединение восстановлено");
        // Можно показать toast-уведомление
      } else {
        console.log("Нет соединения с интернетом");
        // Можно показать toast-уведомление
      }
    };

    window.addEventListener("online", updateOnlineStatus);
    window.addEventListener("offline", updateOnlineStatus);

    // Добавляем глобальное свойство
    app.config.globalProperties.$isOnline = isOnline;
    app.provide("isOnline", isOnline);
  },
};
