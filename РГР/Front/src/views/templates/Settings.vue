<script setup>
import {ref, computed, onMounted} from "vue";
import {useStore} from "vuex";
import {useI18n} from "vue-i18n";
import Sidebar from "@/views/components/Sidebar.vue";

const {t, locale} = useI18n();
const store = useStore();
const isLoading = ref(false);
const showSuccess = ref(false);

// Получаем настройки из store
const settings = computed(() => store.getters.getSettings);

// Локальное состояние для формы
const formData = ref({
  theme: "light",
  language: "ru",
});

// Доступные темы
const themes = [
  {
    value: "light",
    label: t("settings.light"),
    icon: "light_mode",
  },
  {
    value: "dark",
    label: t("settings.dark"),
    icon: "dark_mode",
  },
];

// Доступные языки
const languages = [
  {value: "ru", label: "Русский", flag: "🇷🇺"},
  {value: "en", label: "English", flag: "🇬🇧"},
];

// Применение темы
const applyTheme = (themeName) => {
  document.documentElement.setAttribute(
    "data-theme",
    themeName,
  );
  localStorage.setItem("userTheme", themeName);
};

// Применение языка
const applyLanguage = (language) => {
  locale.value = language;
  localStorage.setItem("userLanguage", language);
};

// Инициализация формы из настроек
const initForm = () => {
  if (settings.value && settings.value.theme) {
    formData.value.theme = settings.value.theme;
  } else {
    const savedTheme = localStorage.getItem("userTheme");
    formData.value.theme =
      savedTheme === "light" || savedTheme === "dark" ?
        savedTheme
      : "light";
  }

  if (settings.value && settings.value.language) {
    formData.value.language = settings.value.language;
  } else {
    const savedLanguage = localStorage.getItem("userLanguage");
    formData.value.language =
      savedLanguage === "ru" || savedLanguage === "en" ?
        savedLanguage
      : "ru";
  }
};

// Отмена изменений
const cancelChanges = () => {
  initForm();
};

// Сохранение настроек
const saveSettings = async () => {
  isLoading.value = true;

  try {
    applyTheme(formData.value.theme);
    applyLanguage(formData.value.language);

    await store.dispatch("updateSettings", {
      settingsData: {
        theme: formData.value.theme,
        language: formData.value.language,
      },
    });

    showSuccess.value = true;
    setTimeout(() => {
      showSuccess.value = false;
    }, 3000);
  } catch (error) {
    console.error("Failed to save settings:", error);
    initForm();
    alert("Не удалось сохранить настройки. Попробуйте позже.");
  } finally {
    isLoading.value = false;
  }
};

// Загрузка настроек при монтировании
const loadSettings = async () => {
  try {
    await store.dispatch("getSettings");
    initForm();
  } catch (error) {
    console.error("Failed to load settings:", error);
    initForm();
  }
};

onMounted(() => {
  loadSettings();
});
</script>

<template>
  <main>
    <div class="settings-page sidebarred">
      <Sidebar />
      <div class="settings-content">
        <div class="settings-container">
          <Transition name="slide">
            <div
              v-if="showSuccess"
              class="success-notification"
            >
              <span class="material-icons">check_circle</span>
              <span>{{ t("settings.success") }}</span>
            </div>
          </Transition>

          <div class="settings-header">
            <h2 class="phoenix-accent-text">
              {{ t("settings.title") }}
            </h2>
            <p>{{ t("settings.description") }}</p>
          </div>

          <div class="settings-form">
            <!-- Выбор темы -->
            <div class="settings-section">
              <div class="section-header">
                <span class="material-icons">palette</span>
                <h3>{{ t("settings.theme") }}</h3>
              </div>

              <div class="theme-options">
                <div
                  v-for="theme in themes"
                  :key="theme.value"
                  class="theme-card"
                  :class="{
                    active: formData.theme === theme.value,
                  }"
                  @click="formData.theme = theme.value"
                >
                  <span class="material-icons">{{
                    theme.icon
                  }}</span>
                  <span class="theme-label">{{
                    theme.label
                  }}</span>
                  <div
                    v-if="formData.theme === theme.value"
                    class="active-indicator"
                  >
                    <span class="material-icons">star</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Выбор языка -->
            <div class="settings-section">
              <div class="section-header">
                <span class="material-icons">language</span>
                <h3>{{ t("settings.language") }}</h3>
              </div>

              <div class="language-options">
                <div
                  v-for="lang in languages"
                  :key="lang.value"
                  class="language-card"
                  :class="{
                    active: formData.language === lang.value,
                  }"
                  @click="formData.language = lang.value"
                >
                  <span class="language-flag">{{
                    lang.flag
                  }}</span>
                  <span class="language-label">{{
                    lang.label
                  }}</span>
                  <div
                    v-if="formData.language === lang.value"
                    class="active-indicator"
                  >
                    <span class="material-icons">star</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Кнопки действий -->
            <div class="action-buttons">
              <button
                class="bordered"
                @click="cancelChanges"
                :disabled="isLoading"
              >
                {{ t("settings.cancel") }}
              </button>
              <button
                class="bordered"
                @click="saveSettings"
                :disabled="isLoading"
              >
                <span v-if="!isLoading">{{
                  t("settings.save")
                }}</span>
                <span v-else class="loading-spinner">{{
                  t("common.loading")
                }}</span>
                <span
                  class="material-icons little"
                  v-if="!isLoading"
                  >save</span
                >
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* Ваши существующие стили остаются без изменений */
.settings-page {
  width: 100%;
}

.settings-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  margin-left: calc(2rem + 32px);
  transition: margin-left 0.2s ease-out;
}

:global(.app.sidebar-expanded) .settings-content {
  margin-left: var(--sidebar-width);
}

.settings-container {
  max-width: 800px;
  width: 100%;
  background: var(--light);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.success-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: var(--accept);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.success-notification .material-icons {
  color: var(--light);
}

.settings-header {
  text-align: center;
  margin-bottom: 2rem;
}

.settings-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.settings-header p {
  color: var(--grey);
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-section {
  border: 1px solid var(--grey);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  background: var(--light);
}

.settings-section:hover {
  border-color: var(--secondary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.section-header .material-icons {
  color: var(--primary);
  font-size: 1.5rem;
}

.section-header h3 {
  color: var(--dark);
  font-size: 1.2rem;
}

.theme-options,
.language-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.theme-card,
.language-card {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 2px solid var(--grey);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--light);
}

.theme-card:hover,
.language-card:hover {
  transform: translateY(-2px);
  border-color: var(--secondary);
  background: linear-gradient(
    45deg,
    rgba(227, 59, 31, 0.05),
    rgba(255, 106, 19, 0.05)
  );
}

.theme-card.active,
.language-card.active {
  border-color: var(--primary);
  background: linear-gradient(
    45deg,
    rgba(227, 59, 31, 0.1),
    rgba(255, 106, 19, 0.1)
  );
  box-shadow: 0 0 0 2px rgba(227, 59, 31, 0.3);
}

.theme-card .material-icons {
  font-size: 1.5rem;
  color: var(--primary);
}

.language-flag {
  font-size: 1.5rem;
}

.theme-label,
.language-label {
  font-weight: 500;
  color: var(--dark);
}

.active-indicator {
  position: absolute;
  top: -8px;
  right: -8px;
}

.active-indicator .material-icons {
  color: var(--primary);
  font-size: 1.2rem;
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.2));
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.action-buttons button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-buttons button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .settings-content {
    margin-left: 0;
    padding: 1rem;
  }

  .settings-container {
    padding: 1rem;
  }

  .theme-options,
  .language-options {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: row;
  }

  .action-buttons button {
    width: 100%;
    justify-content: center;
  }
}
</style>
