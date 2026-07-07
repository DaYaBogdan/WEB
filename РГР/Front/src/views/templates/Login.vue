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
          class="bordered login-input"
          placeholder="login"
          type="text"
          v-model="form.login"
        />
        <input
          class="bordered login-input"
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

/* Переопределяем глобальные стили input только для логина */
.login-input {
  min-width: 280px !important;
  max-width: 400px !important;
  width: auto !important;
  padding: 10px 16px !important;
  font-size: 1rem;
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

  .login-input {
    min-width: 200px !important;
    max-width: 100% !important;
    width: 100% !important;
  }

  .submit-button {
    width: 100%;
    max-width: 200px;
  }
}
</style>
