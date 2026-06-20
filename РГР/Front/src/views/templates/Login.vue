<script setup>
import {useStore} from "vuex";
import {reactive} from "vue";

const store = useStore();
const form = reactive({login: "", password: ""});

const login = async () => {
  try {
    await store.dispatch("login", form);
  } catch (e) {
    alert("Ошибка входа");
  }
};
</script>

<template>
  <main
    class="column horizontal-align vertical-align without-sidebar"
  >
    <span class="material-icons"> account_circle </span>
    <form @submit.prevent="login">
      <div class="column">
        <input
          class="bordered"
          placeholder="login"
          type="text"
          v-model="form.login"
        />
        <input
          class="bordered"
          placeholder="password"
          type="password"
          v-model="form.password"
        />
      </div>
      <button
        class="bordered"
        style="min-width: 30%"
        type="submit"
      >
        Вход
      </button>
    </form>
  </main>
</template>
