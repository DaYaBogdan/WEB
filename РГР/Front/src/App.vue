<template>
  <div
    class="app"
    :class="{'sidebar-expanded': isSidebarExpanded}"
  >
    <RouterView />
  </div>
</template>

<script setup>
import {computed, onMounted} from "vue";
import {useStore} from "vuex";
import {useI18n} from "vue-i18n";

const store = useStore();
const {locale} = useI18n();
const isSidebarExpanded = computed(
  () => store.state.isSidebarExpanded || false,
);
const settings = computed(() => store.getters.getSettings);

// Функция применения темы
const applyTheme = (themeName) => {
  if (
    themeName &&
    (themeName === "light" || themeName === "dark")
  ) {
    document.documentElement.setAttribute(
      "data-theme",
      themeName,
    );
    localStorage.setItem("userTheme", themeName);
  }
};

// Функция применения языка
const applyLanguage = (language) => {
  if (language && (language === "ru" || language === "en")) {
    locale.value = language;
    localStorage.setItem("userLanguage", language);
  }
};

onMounted(async () => {
  // 1. Сначала загружаем настройки с сервера
  try {
    await store.dispatch("getSettings");
  } catch (error) {
    console.error("Failed to load settings:", error);
  }

  // 2. Определяем тему
  let theme = "light";

  if (settings.value && settings.value.theme) {
    theme = settings.value.theme;
  } else {
    const savedTheme = localStorage.getItem("userTheme");
    if (
      savedTheme &&
      (savedTheme === "light" || savedTheme === "dark")
    ) {
      theme = savedTheme;
    }
  }

  // 3. Определяем язык
  let language = "ru";

  if (settings.value && settings.value.language) {
    language = settings.value.language;
  } else {
    const savedLanguage = localStorage.getItem("userLanguage");
    if (
      savedLanguage &&
      (savedLanguage === "ru" || savedLanguage === "en")
    ) {
      language = savedLanguage;
    }
  }

  // 4. Применяем настройки
  applyTheme(theme);
  applyLanguage(language);

  // 5. Инициализация состояния sidebar
  const savedState =
    localStorage.getItem("is_expanded") === "true";
  if (savedState !== isSidebarExpanded.value && store.commit) {
    store.commit("TOGGLE_SIDEBAR");
  }
});
</script>

<style lang="scss">
@import "@/css/Style.scss";

.app {
  min-height: 100vh;
  background: var(--bg-color);
  color: var(--text-color);
}

.app > main,
.app .sidebarred {
  margin-left: calc(2rem + 32px);
  transition: margin-left 0.2s ease-out;
}

.app.sidebar-expanded > main,
.app.sidebar-expanded .sidebarred {
  margin-left: var(--sidebar-width);
}

@media (max-width: 768px) {
  .app > main,
  .app .sidebarred {
    margin-left: 0;
    padding-left: calc(2rem + 32px);
  }
}
</style>
