<script setup>
import {ref} from "vue";
import {useStore} from "vuex";
import {computed} from "vue";

const store = useStore();

const adminPanelState = computed(
  () => store.getters.userRole === "admin",
);

const is_expanded = ref(
  localStorage.getItem("is_expanded") === "true",
);

const ToggleMenu = () => {
  is_expanded.value = !is_expanded.value;
  localStorage.setItem("is_expanded", is_expanded.value);
};

const logout = async () => {
  try {
    await store.dispatch("logout");
  } catch (error) {
    console.error("Failed to logout:", error);
  }
};
</script>

<template>
  <aside :class="{'is-expanded': is_expanded}">
    <div class="logo">
      <img src="/phoenix.ico" alt="Vue" />
    </div>
    <div class="menu-toggle-wrap">
      <button class="menu-toggle" @click="ToggleMenu">
        <span class="material-icons"
          >keyboard_double_arrow_right</span
        >
      </button>
    </div>
    <div class="menu">
      <h3>Меню</h3>
      <RouterLink class="button" :to="{name: 'Diary'}">
        <span class="material-icons">home</span>
        <span class="text">Главная страница</span>
      </RouterLink>

      <RouterLink class="button" :to="{name: 'Clients'}">
        <span class="material-icons">group</span>
        <span class="text">Список клиентов</span>
      </RouterLink>

      <div v-if="adminPanelState">
        <RouterLink class="button" :to="{name: 'Masters'}">
          <span class="material-icons"
            >supervisor_account</span
          >
          <span class="text">Мастера</span>
        </RouterLink>
        <RouterLink class="button" :to="{name: 'AllTasks'}">
          <span class="material-icons">event_note</span>
          <span class="text">Все записи</span>
        </RouterLink>
      </div>

      <RouterLink class="button" :to="{name: 'Settings'}">
        <span class="material-icons">settings</span>
        <span class="text">Настройки</span>
      </RouterLink>

      <button class="button logout" @click="logout">
        <span class="material-icons">logout</span>
        <span class="text">Выход</span>
      </button>
    </div>
  </aside>
</template>

<style scoped lang="scss">
aside {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 100;
  display: flex;
  flex-direction: column;
  width: var(--sidebar-collapsed-width);
  background-color: var(--dark);
  color: var(--light);
  transition: 0.3s ease-out;
  overflow: hidden;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

  .flex {
    flex: 1 1 0;
  }

  .logo {
    margin-bottom: 1rem;
    flex-shrink: 0;

    img {
      width: 2rem;
    }
  }

  .menu-toggle-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
    position: relative;
    transition: 0.2s ease-out;
    flex-shrink: 0;

    .menu-toggle {
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      transition: 0.2s ease-out;

      .material-icons {
        font-size: 2rem;
        color: var(--primary);
        transition: 0.2s ease-out;
      }

      &:hover {
        .material-icons {
          transform: translateX(0.5rem);
        }
      }
    }
  }

  h3,
  .button .text,
  .master-text {
    opacity: 0;
    transition: 0.3s ease-out;
    white-space: nowrap;
  }

  h3 {
    padding: 0rem 1rem;
    color: var(--grey);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
  }

  .menu {
    flex: 1;
    margin: 0 -1rem;
    overflow-y: auto;
    overflow-x: hidden;

    // Стилизация скроллбара
    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-track {
      background: var(--dark-alt);
    }

    &::-webkit-scrollbar-thumb {
      background: var(--primary);
      border-radius: 2px;
    }

    .button {
      display: flex;
      align-items: center;
      text-decoration: none;
      padding: 0.5rem 1rem;
      transition: 0.2s ease-out;
      cursor: pointer;
      background: none;
      border: none;
      width: 100%;
      text-align: left;
      gap: 1rem;
      white-space: nowrap;

      .material-icons {
        font-size: 2rem;
        color: var(--light);
        transition: 0.2s ease-out;
        flex-shrink: 0;
      }

      .text {
        color: var(--light);
        transition: 0.2s ease-out;
      }

      &:hover,
      &.router-link-exact-active {
        background-color: var(--dark-alt);

        .material-icons,
        .text {
          color: var(--primary);
        }
      }

      &.router-link-exact-active {
        border-right: 5px solid var(--primary);
      }
    }

    .logout {
      margin-top: auto;
      margin-bottom: 0;

      .material-icons {
        margin-right: 0;
      }

      &:hover {
        background-color: var(--dark-alt);

        .material-icons,
        .text {
          color: var(--error);
        }
      }
    }

    .just-text {
      display: flex;
      align-items: center;
      text-decoration: none;
      padding: 0.5rem 1rem;
      transition: 0.2s ease-out;
      gap: 1rem;
      white-space: nowrap;

      .material-icons {
        font-size: 2rem;
        color: var(--light);
        transition: 0.2s ease-out;
      }

      .text {
        color: var(--light);
        transition: 0.2s ease-out;
      }
    }

    .master-text {
      padding: 20px 10px;
      text-align: center;
      color: var(--light);
      transition: 0.2s ease-out;
    }
  }

  // Развернутое состояние
  &.is-expanded {
    width: var(--sidebar-width);

    .menu-toggle-wrap {
      .menu-toggle {
        transform: rotate(-180deg);
      }
    }

    h3,
    .button .text,
    .master-text {
      opacity: 1;
    }

    .button {
      .material-icons {
        margin-right: 1rem;
      }
    }
  }
}

.button {
  color: var(--light);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;

  .material-icons,
  .text {
    color: inherit;
  }

  &:hover,
  &.router-link-exact-active {
    .material-icons,
    .text {
      color: var(--primary);
    }
  }
}

aside {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 100;
  width: calc(2rem + 32px);
  background-color: var(--dark);
  color: var(--light);
  transition: 0.2s ease-out;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

aside.is-expanded {
  width: var(--sidebar-width);
}

.logo {
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.logo img {
  width: 2rem;
}

.menu-toggle-wrap {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.menu-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.menu-toggle .material-icons {
  font-size: 2rem;
  color: var(--primary);
  transition: 0.2s ease-out;
}

.menu-toggle:hover .material-icons {
  transform: translateX(0.5rem);
}

.menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow-y: auto;
  overflow-x: hidden;
}

.menu h3 {
  padding: 0 1rem;
  color: var(--grey);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  opacity: 0;
  transition: 0.3s ease-out;
  white-space: nowrap;
}

aside.is-expanded h3 {
  opacity: 1;
}

.button {
  display: flex;
  align-items: center;
  text-decoration: none;
  padding: 0.5rem 1rem;
  transition: 0.2s ease-out;
  cursor: pointer;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  gap: 1rem;
  white-space: nowrap;
}

.button .material-icons {
  font-size: 2rem;
  color: var(--light);
  transition: 0.2s ease-out;
  flex-shrink: 0;
}

.button .text {
  color: var(--light);
  transition: 0.2s ease-out;
  opacity: 0;
}

aside.is-expanded .button .text {
  opacity: 1;
}

.button:hover,
.button.router-link-exact-active {
  background-color: var(--dark-alt);
}

.button:hover .material-icons,
.button:hover .text,
.button.router-link-exact-active .material-icons,
.button.router-link-exact-active .text {
  color: var(--primary);
}

.button.router-link-exact-active {
  border-right: 5px solid var(--primary);
}

.logout {
  margin-top: auto;
}

.logout:hover .material-icons,
.logout:hover .text {
  color: var(--error);
}

/* Стилизация скроллбара */
.menu::-webkit-scrollbar {
  width: 4px;
}

.menu::-webkit-scrollbar-track {
  background: var(--dark-alt);
}

.menu::-webkit-scrollbar-thumb {
  background: var(--primary);
  border-radius: 2px;
}

@media (max-width: 768px) {
  aside {
    // Перемещаем вниз
    position: fixed;
    bottom: 0;
    left: 0;
    top: auto;
    height: auto;
    width: 100% !important;
    flex-direction: row !important;
    align-items: center;
    justify-content: space-around;
    padding: 0.5rem 0.75rem;
    background-color: var(--dark);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
    z-index: 100;
    transform: none !important; // Отключаем анимацию слайда
    transition: none !important;

    // Скрываем элементы десктопной версии
    .logo,
    .menu-toggle-wrap,
    h3,
    .master-text,
    .flex {
      display: none !important;
    }

    // Основной контейнер меню
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

      // Убираем скроллбар
      &::-webkit-scrollbar {
        display: none;
      }

      // Стили для кнопок в нижней панели
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

        // Активный/текущий пункт
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

        // Специальный стиль для кнопки выхода
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

      // Стили для обычного текста (если используется)
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

      // Скрываем все h3 внутри меню
      h3 {
        display: none !important;
      }
    }

    // Полностью отключаем развернутое состояние
    &.is-expanded {
      width: 100% !important;
      transform: none !important;

      // Убеждаемся, что все скрытые элементы остаются скрытыми
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

  // Удаляем область для свайпа на мобильных
  .sidebar-touch-area {
    display: none !important;
  }

  // Скрываем оверлей
  aside::before {
    display: none !important;
  }

  // Анимация появления при загрузке
  aside {
    animation: slideUp 0.3s ease-out;
  }

  @keyframes slideUp {
    from {
      transform: translateY(100%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
}

// Для очень маленьких экранов уменьшаем размеры
@media (max-width: 400px) {
  aside {
    padding: 0.4rem 0.4rem;

    .menu {
      .button,
      .just-text {
        min-width: 40px;
        padding: 0.2rem 0.3rem;

        .material-icons {
          font-size: 1.4rem !important;
        }

        .text {
          font-size: 0.5rem !important;
        }
      }
    }
  }
}

// Для планшетов, если нужно также показывать нижнюю панель
@media (min-width: 769px) and (max-width: 1024px) {
  // Опционально: можно оставить десктопную версию или тоже переключить
  // По умолчанию оставляем десктопную
}

// Поддержка безопасной зоны (notch)
@supports (padding: max(0px)) {
  aside {
    padding-left: max(0.75rem, env(safe-area-inset-left));
    padding-right: max(0.75rem, env(safe-area-inset-right));
    padding-bottom: max(0.5rem, env(safe-area-inset-bottom));
  }
}
</style>

<style scoped lang="scss"></style>
