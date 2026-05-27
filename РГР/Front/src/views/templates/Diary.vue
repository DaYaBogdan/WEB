<script setup>
import Day from "../components/Day.vue";
import Sidebar from "../components/Sidebar.vue";
import {computed, ref} from "vue";

// --- Текущая дата и время ---
const now = new Date();

// --- Получаем день недели (русский) ---
const weekDays = ref([
  "Воскресенье",
  "Понедельник",
  "Вторник",
  "Среда",
  "Четверг",
  "Пятница",
  "Суббота",
]);
const currentWeekday = computed(() => weekDays[now.getDay()]); // getDay() возвращает индекс дня недели

// --- Форматируем дату (ГГГГ-ММ-ДД) ---
const currentDate = computed(() => {
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0"); // Месяцы считаются с 0, поэтому +1
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
});
</script>

<template>
  <Sidebar />
  <main>
    <div class="flex">
      <div v-for="day in weekDays" :key="day">
        <Day :dateOfTheWeek="day" />
      </div>
    </div>
  </main>
</template>
