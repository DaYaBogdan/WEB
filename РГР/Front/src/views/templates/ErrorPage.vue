<template>
  <main class="ErrorPage">
    <div class="horizontal-align vertical-align flex">
      <h1 class="phoenix-accent bordered">404</h1>
      <h2 class="phoenix-accent-text">
        {{ t("missing.no_page") }}
      </h2>
    </div>
  </main>
</template>

<script setup>
import {useI18n} from "vue-i18n";
const {t} = useI18n();
</script>
