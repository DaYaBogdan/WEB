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

      <RouterLink class="button" :to="{name: 'AddClient'}"
        ><span class="material-icons"> group </span>
        <span class="text">Список клиентов</span>
      </RouterLink>

      <div v-if="adminPanelState">
        <!-- <hr /> -->
        <h3 style="margin-top: 20px">Панель админа</h3>
        <!-- <hr /> -->

        <RouterLink class="button" :to="{name: 'Register'}"
          ><span class="material-icons">
            supervisor_account
          </span>
          <span class="text">Мастера</span>
        </RouterLink>
      </div>
    </div>

    <div class="flex"></div>
  </aside>
</template>
