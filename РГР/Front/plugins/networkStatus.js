import {ref} from "vue";

export default {
  install(app) {
    const isOnline = ref(navigator.onLine);

    const updateOnlineStatus = () => {
      isOnline.value = navigator.onLine;
      if (isOnline.value) {
        console.log("Соединение восстановлено");
      } else {
        console.log("Нет соединения с интернетом");
      }
    };

    window.addEventListener("online", updateOnlineStatus);
    window.addEventListener("offline", updateOnlineStatus);

    app.config.globalProperties.$isOnline = isOnline;
    app.provide("isOnline", isOnline);
  },
};
