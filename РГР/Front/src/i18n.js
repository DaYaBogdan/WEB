import {createI18n} from "vue-i18n";
import ru from "./locales/ru.js";
import en from "./locales/en.js";

const getDefaultLanguage = () => {
  const savedLanguage = localStorage.getItem("userLanguage");
  if (
    savedLanguage &&
    (savedLanguage === "ru" || savedLanguage === "en")
  ) {
    return savedLanguage;
  }
  return "ru";
};

const i18n = createI18n({
  legacy: false,
  locale: getDefaultLanguage(),
  fallbackLocale: "ru",
  messages: {
    ru,
    en,
  },
});

export default i18n;
