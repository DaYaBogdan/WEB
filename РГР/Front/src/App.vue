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

<!-- Mixins and their invokes -->
<style lang="scss">
@mixin fire-gradient(
  $start: #ff4d00,
  $middle: #ff8c00,
  $end: #ffd800
) {
  background: linear-gradient(45deg, $start, $middle, $end);
}

@mixin fire-gradient-text(
  $start: #ff4d00,
  $middle: #ff8c00,
  $end: #ffd800
) {
  background: linear-gradient(45deg, $start, $middle, $end);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

:root {
  --primary: #e33b1f;
  --secondary: #ff6a13;
  --accent: #ffb347;
  --error: #6f0a03;
  --accept: #168019;
  --sidebar-width: 300px;
  --sidebar-collapsed-width: calc(2rem + 32px);
  --mobile-bottom-nav-height: 70px;
  --font: "Fira sans", sans-serif;

  --light: #ffffff;
  --dark: #333333;
  --dark-alt: #f5f5f5;
  --grey: #666666;
  --text-color: #000000;
  --bg-color: #ffffff;
  --border-color: #e0e0e0;
}

// Тёмная тема
[data-theme="dark"] {
  --light: #1a1a1a;
  --dark: #ffffff;
  --dark-alt: #2d2d2d;
  --grey: #999999;
  --text-color: #ffffff;
  --bg-color: #1a1a1a;
  --border-color: #333333;

  ::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }

  ::-webkit-scrollbar-track {
    background: #2d2d2d;
  }

  ::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 5px;

    &:hover {
      background: #666;
    }
  }
}

.phoenix-accent {
  @include fire-gradient(
    var(--primary),
    var(--secondary),
    var(--accent)
  );
}

.phoenix-accent-text {
  @include fire-gradient-text(
    var(--primary),
    var(--secondary),
    var(--accent)
  );
}

.filled {
  padding: 15px;
  @extend .phoenix-accent;
  border: none;
  color: white;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    opacity: 0.9;
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}
</style>

<!-- Inputs -->
<style lang="scss">
input[type="text"] {
  min-width: 400px;
  max-width: 600px;
  background: var(--light);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  padding: 8px 12px;
  border-radius: 8px;

  &:focus {
    outline: none;
    border-color: var(--primary);
  }
}

input[type="password"] {
  min-width: 400px;
  max-width: 600px;
  background: var(--light);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  padding: 8px 12px;
  border-radius: 8px;

  &:focus {
    outline: none;
    border-color: var(--primary);
  }
}

input[type="checkbox"] {
  min-width: auto;
  max-width: auto;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin: 0;
  cursor: pointer;
}
</style>

<!-- Animations -->
<style lang="scss">
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>

<!-- Other -->
<style lang="scss">
.header {
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.header p {
  color: var(--grey);
}

.app {
  display: flex;
  min-height: 100vh;
  background: var(--bg-color);
  color: var(--text-color);

  > main,
  .main-content {
    flex: 1;
    margin-left: var(--sidebar-collapsed-width);
    padding: 2rem;
    transition: margin-left 0.3s ease-out;

    @media (max-width: 768px) {
      margin-left: 0 !important;
      padding: 1rem;
      // Добавляем отступ снизу
      padding-bottom: calc(
        var(--mobile-bottom-nav-height) + 1.5rem
      );
      // Важно: добавляем минимальную высоту, чтобы контент мог прокручиваться
      min-height: calc(
        100vh - var(--mobile-bottom-nav-height)
      );
    }
  }

  &.sidebar-expanded {
    > main,
    .main-content {
      margin-left: var(--sidebar-width);

      @media (max-width: 768px) {
        margin-left: 0;
      }
    }
  }
}

.app .sidebarred {
  margin-left: calc(2rem + 32px);
  transition: margin-left 0.2s ease-out;

  @media (max-width: 768px) {
    margin-left: 0 !important;
  }
}

.app.sidebar-expanded > main,
.app.sidebar-expanded .sidebarred {
  margin-left: var(--sidebar-width);

  @media (max-width: 768px) {
    margin-left: 0 !important;
  }
}

button {
  cursor: pointer;
}

// Стили для мобильной нижней навигации
@media (max-width: 768px) {
  aside {
    position: fixed;
    bottom: 0;
    left: 0;
    top: auto;
    height: var(--mobile-bottom-nav-height);
    width: 100% !important;
    flex-direction: row !important;
    align-items: center;
    justify-content: space-around;
    padding: 0.5rem 0.75rem;
    background-color: var(--dark);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
    z-index: 100;
    transform: none !important;
    transition: none !important;

    .logo,
    .menu-toggle-wrap,
    h3,
    .master-text,
    .flex {
      display: none !important;
    }

    .menu {
      display: flex !important;
      flex-direction: row !important;
      justify-content: space-around;
      align-items: center;
      width: 100%;
      margin: 0;
      padding: 0;
      overflow: visible !important;
      flex: none !important;
      gap: 0;

      &::-webkit-scrollbar {
        display: none;
      }

      .button {
        display: flex !important;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.3rem 0.5rem;
        gap: 0.15rem;
        min-width: 50px;
        flex: 1;
        max-width: 80px;
        background: none;
        border: none;
        border-radius: 8px;
        transition: all 0.2s ease;
        position: relative;
        white-space: normal;
        text-align: center;

        .material-icons {
          font-size: 1.6rem !important;
          margin: 0 !important;
          color: var(--grey);
          transition: color 0.2s ease;
        }

        .text {
          font-size: 0.6rem !important;
          color: var(--grey) !important;
          opacity: 1 !important;
          white-space: nowrap;
          transition: color 0.2s ease;
          line-height: 1.2;
        }

        &.router-link-exact-active {
          background-color: rgba(255, 255, 255, 0.05);
          border-right: none !important;
          border-bottom: 2px solid var(--primary);

          .material-icons {
            color: var(--primary) !important;
          }

          .text {
            color: var(--primary) !important;
          }
        }

        &:hover {
          background-color: rgba(255, 255, 255, 0.05);

          .material-icons {
            color: var(--primary);
          }

          .text {
            color: var(--light);
          }
        }

        &.logout {
          margin-top: 0 !important;

          .material-icons {
            color: var(--grey);
          }

          .text {
            color: var(--grey);
          }

          &:hover {
            .material-icons,
            .text {
              color: var(--error) !important;
            }
          }
        }
      }

      .just-text {
        display: flex !important;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.3rem 0.5rem;
        gap: 0.15rem;
        min-width: 50px;
        flex: 1;
        max-width: 80px;

        .material-icons {
          font-size: 1.6rem !important;
          margin: 0 !important;
          color: var(--grey);
        }

        .text {
          font-size: 0.6rem !important;
          color: var(--grey) !important;
          opacity: 1 !important;
          white-space: nowrap;
          line-height: 1.2;
        }
      }

      h3 {
        display: none !important;
      }
    }

    &.is-expanded {
      width: 100% !important;
      transform: none !important;

      .logo,
      .menu-toggle-wrap,
      h3,
      .master-text,
      .flex {
        display: none !important;
      }

      .menu {
        .button .text,
        .just-text .text {
          opacity: 1 !important;
        }
      }
    }
  }

  .sidebar-touch-area {
    display: none !important;
  }

  aside::before {
    display: none !important;
  }
}

.flex {
  display: flex;
  flex-direction: row;
  gap: 2em;
}

.column {
  @extend .flex;
  gap: 20px;
  flex-direction: column;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: var(--font);
}

body {
  background: var(--bg-color);
  color: var(--text-color);
  transition:
    background-color 0.3s ease,
    color 0.3s ease;
}

.bordered {
  padding: 7px;
  border-radius: 12px;
  border: 3px solid var(--secondary);
  background: transparent;
  color: var(--text-color);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    background: rgba(255, 106, 19, 0.1);
  }
}

.material-icons {
  font-size: 5rem;
  color: var(--primary);
  transition: color 0.3s ease;
}

.grid {
  display: grid;
  grid-template-columns: auto auto;
  row-gap: 20px;
  column-gap: 20px;
  justify-content: center;
}

hr {
  width: 100%;
  border-color: var(--border-color);
}

.loading {
  text-align: center;
  padding: 40px;
  opacity: 0.6;
  color: var(--text-color);
}

.weekEndDialog {
  align-items: center;
  height: 100%;
  text-align: center;
}

.day-weekend {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.huge {
  font-size: 3rem;
}

.base {
  font-size: 2.5rem;
}

.little {
  font-size: 2rem;
}
</style>

<!-- Mobile ver. -->
<style lang="scss">
@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }

  input[type="text"],
  input[type="password"] {
    min-width: 400px;
    max-width: 100%;
    width: 100%;
  }

  .day {
    min-width: 300px;
    max-width: 100%;
  }

  .flex {
    flex-direction: column;
    gap: 1rem;
  }

  .material-icons {
    font-size: 3rem;
  }

  .huge {
    font-size: 2rem;
  }

  .base {
    font-size: 1.8rem;
  }

  .little {
    font-size: 1.4rem;
  }

  .bordered {
    padding: 5px;
  }

  .filled {
    padding: 12px;
    width: 100%;
  }

  .bordered:hover {
    transform: none;
    background: transparent;
  }

  .filled:hover {
    transform: none;
    opacity: 1;
  }

  main {
    margin-bottom: 3rem;
  }
}
</style>
