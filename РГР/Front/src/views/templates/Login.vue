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
  <main class="column horizontal-align vertical-align">
    <span class="material-icons"> account_circle </span>
    <form>
      <div class="column">
        <input
          class="bordered"
          placeholder="login"
          type="text"
        />
        <input
          class="bordered"
          placeholder="password"
          type="password"
        />
      </div>
      <button
        class="bordered filled"
        style="min-width: 30%"
        v-on:click="login()"
      >
        Вход
      </button>
    </form>
  </main>
</template>
