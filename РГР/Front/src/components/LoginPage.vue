<!-- Этот файл нуждается в доработке:
1. Реализовать подключение к базе данных
2. Верификация пользователя и дальнейшая его аунтетификация -->

<script setup>
import router from '@/router';
import {useStore} from 'vuex';
import { ref } from 'vue';

const store = useStore()

const formData = ref({
  login: "",
  password: "",
})

const validate = ref({
  firstTry: true,
  none: false,
  incorrectData: true,
});

function validateFields () {

  validate.value.firstTry = false

  if (!formData.value.login || !formData.value.password) validate.value.nulls = true

  // else if (store.dispatch("fetchAccount", {login: formData.value.login, password: formData.value.password})) validate.value.incorrectData = true

  else {
    router.push("/Orders")
  }
};

</script>

<template>
  <main class="Login">
    <div class="column">
      <span class="material-icons">account_circle</span>
      <span> Логин </span>
      <input v-model="formData.login" placeholder="Логин/Login" type="text"></input>
      <input v-model="formData.password" placeholder="Пароль/Password" type="password"></input>
      <span v-if="!validate.none && !validate.firstTry" class="errors">Впишите данные</span>
      <span v-if="!validate.none && !validate.incorrectData && !validate.firstTry" class="errors">Неправильный логин или пароль</span>
      <span><button type="button" @click="validateFields">Войти</button></span>
    </div>
  </main>
</template>

<style lang="sass" scoped>
$border_color: gray
$main_color: white
$box_color: black
$text_color: white

span
  font-size: 3em

.material-icons
  font-size: 8em

input
  background-color: $box_color
  margin: 2em
  padding: 1em
  border-radius: 1em
  border: 5px solid $border_color

  font-size: 20px

  &::placeholder
    color: gray

button
  background-color: $box_color
  padding: 1em
  border-radius: 1em
  width: 60%
  font-size: 20px
  border: 5px solid $border_color
  color: $main_color

.Login
  min-width: 40%

  margin: 0
  padding: 0

  justify-content: center
  justify-self: center
  text-align: center
  vertical-align: center
  margin-top: 5%
</style>
