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
      <button class="bordered submit-button" type="submit">
        Вход
      </button>
    </form>
  </main>
</template>

<style lang="scss" scoped>
.horizontal-align {
  text-align: center;
  justify-content: center;
}

.vertical-align {
  margin: 0;
  display: flex;
  height: 100vh;
  align-items: center;
}

.submit-button {
  height: 40px;
  width: 200px;
  margin-top: 2em;
}

@media (max-width: 768px) {
  .horizontal-align {
    text-align: center;
    justify-content: center;
  }

  .vertical-align {
    margin: 0;
    display: flex;
    height: 100vh;
    align-items: center;
  }
}
</style>
