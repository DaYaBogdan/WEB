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
    console.log("Tasks loaded:", tasks.value);
  } catch (error) {
    console.error("Failed to load tasks:", error);
  }
};
</script>

<template>
  <aside :class="`${is_expanded && 'is-expanded'}`">
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
      <RouterLink class="button" :to="{name: 'Diary'}"
        ><span class="material-icons"> home </span>
        <span class="text">Главная страница</span>
      </RouterLink>

      <RouterLink class="button" :to="{name: 'Clients'}"
        ><span class="material-icons"> group </span>
        <span class="text">Список клиентов</span>
      </RouterLink>

      <div v-if="adminPanelState">
        <hr />
        <RouterLink class="button" :to="{name: 'Masters'}"
          ><span class="material-icons">
            supervisor_account
          </span>
          <span class="text">Мастера</span>
        </RouterLink>
        <!-- <RouterLink class="button" :to="{name: 'AllTasks'}"
          ><span class="material-icons"> event_note </span>
          <span class="text">Все записи</span>
        </RouterLink> -->
      </div>

      <button class="button" @click="logout" style="">
        <span class="material-icons">logout</span>
        <span class="text">Выход</span>
      </button>
    </div>

    <div class="flex"></div>
  </aside>
</template>
