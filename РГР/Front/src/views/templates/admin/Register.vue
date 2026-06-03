<script setup>
import Sidebar from "@/views/components/Sidebar.vue";
import {reactive} from "vue";
import api from "@/api";

const form = reactive({login: "", password: ""});

const register = async () => {
  try {
    await api.register(form);

    router.push("/Diary");
  } catch (error) {
    console.error("Registration failed:", error);
  }
};
</script>

<template>
  <Sidebar />
  <main class="column horizontal-align vertical-align">
    <span class="material-icons"> account_circle </span>
    <form @submit.prevent="register">
      <div class="column">
        <input
          class="bordered"
          placeholder="masters login"
          type="text"
          v-model="form.login"
        />
        <input
          class="bordered"
          placeholder="masters password"
          type="password"
          v-model="form.password"
        />
      </div>
      <button
        class="bordered filled"
        style="min-width: 30%"
        type="submit"
      >
        Зарегестрировать мастера
      </button>
    </form>
  </main>
</template>
