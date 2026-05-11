<script setup>
import {useStore} from "vuex";
import Sidebar from "./Sidebar.vue";
const store = useStore();
</script>

<template>
  <Sidebar v-if="!store.state.choosing" />
  <main class="OrdersPage">
    <div class="flex">
      <div class="order_block column">
        <span class="material-icons"> add </span>
        <p>Добавить заказ?</p>
      </div>
      <div v-for="value in source" class="order_block column">
        <img src=".../public/favicon.ico" />
        <button>Изменить информацию</button>
        <button>Удалить заказ</button>
      </div>
    </div>
  </main>
</template>

<style lang="sass" scoped>
$background_color: black
$main_color: gray
$box_color: white
$text_color: black

.material-icons
  font-size: 10em

.OrdersPage
    min-width: 40%
    height: auto
    background-color: $main_color
    // border-radius: 1rem

    justify-content: center
    justify-self: center
    text-align: center
    vertical-align: center
    // margin-top: 5%
</style>
