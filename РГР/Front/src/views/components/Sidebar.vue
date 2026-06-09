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

<style scoped>
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

/* Адаптивность */
@media (max-width: 768px) {
  aside {
    position: fixed;
    z-index: 99;
  }
}
</style>
