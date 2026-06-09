<template>
  <Sidebar />
  <main class="sidebarred">
    <div class="column">
      <!-- Навигационная панель -->
      <div class="flex">
        <!-- Кнопка добавления записи -->
        <div class="flex">
          <button class="bordered flex" @click="openAddModal">
            <p
              class="phoenix-accent-text"
              style="margin-top: 4px; padding: 0"
            >
              {{ t("diary.addTask") }}
            </p>
            <span class="material-icons little">add</span>
          </button>
        </div>

        <!-- Кнопка удаления записи -->
        <div class="flex">
          <button
            class="bordered flex"
            @click="deleteSelectedTasks"
            :disabled="selectedCount === 0 || isLoading"
          >
            <p
              class="phoenix-accent-text"
              style="margin-top: 4px; padding: 0"
            >
              {{ t("diary.deleteTask") }}
            </p>
            <span class="material-icons little">close</span>
          </button>
        </div>
      </div>

      <!-- Разделитель -->
      <hr />

      <NewTask
        v-if="showAddModal"
        :masterId="currentMasterId"
        @close="showAddModal = false"
        @success="onTaskCreated"
      />

      <!-- Основное тело еженедельника -->
      <div class="grid" v-if="!isLoading">
        <Day
          v-for="(day, index) in weekDays"
          :key="index"
          :day="day"
        />
      </div>
      <div v-else class="loading">
        {{ t("common.loading") }}
      </div>

      <!-- Навигация между неделями -->
      <div class="flex horizontal-align">
        <button @click="prevWeek">
          {{ t("diary.prevWeek") }}
        </button>
        <button @click="resetToToday">
          {{ t("diary.resetWeek") }}
        </button>
        <button @click="nextWeek">
          {{ t("diary.nextWeek") }}
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import Day from "../components/Day.vue";
import {ref, computed, onMounted} from "vue";
import Sidebar from "../components/Sidebar.vue";
import {useStore} from "vuex";
import {useI18n} from "vue-i18n";
import NewTask from "../components/NewTask.vue";

const {t} = useI18n();
const store = useStore();

const tasks = computed(() => store.getters.getTasks);
const weekends = computed(() => store.getters.getWeekends);

const isLoading = computed(() => store.getters.isLoading);
const selectedCount = computed(
  () => store.getters.getSelectedTasksCount,
);
const error = computed(() => store.getters.getError);

const showAddModal = ref(false);
const currentMasterId = computed(() => store.state.user?.id);

// Опорная дата
const referenceDate = ref(new Date());

//---------------------DataLoading-------------------------------
const loadTasks = async () => {
  try {
    await store.dispatch("getTasks");
    console.log("Tasks loaded:", tasks.value);
  } catch (error) {
    console.error("Failed to load tasks:", error);
  }
};

const loadClients = async () => {
  try {
    await store.dispatch("getClients");
    console.log("Clients loaded");
  } catch (error) {
    console.error("Failed to load clients:", error);
  }
};

const loadWeekends = async () => {
  try {
    await store.dispatch("getWeekends");
    console.log("Weekends loaded");
  } catch (error) {
    console.error("Failed to load weekends:", error);
  }
};

//---------------------WeekdaysLogic-------------------------------
// Функция возврата названия дня недели по индексу (локализованная)
const getWeekdayName = (dayIndex) => {
  const weekdays = [
    t("diary.weekdays.sunday"),
    t("diary.weekdays.monday"),
    t("diary.weekdays.tuesday"),
    t("diary.weekdays.wednesday"),
    t("diary.weekdays.thursday"),
    t("diary.weekdays.friday"),
    t("diary.weekdays.saturday"),
  ];
  return weekdays[dayIndex];
};

// Форматирование даты: ДД.ММ
const formatDate = (date) => {
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  return `${day}.${month}`;
};

function getTasksForDay(tasksArray, currentDay) {
  if (!tasksArray || !Array.isArray(tasksArray)) {
    return [];
  }

  const targetDate = new Date(currentDay);
  targetDate.setHours(0, 0, 0, 0);

  return tasksArray.filter((task) => {
    if (!task.dateTime) return false;

    const taskDate = new Date(task.dateTime);
    taskDate.setHours(0, 0, 0, 0);

    return taskDate.getTime() === targetDate.getTime();
  });
}

// Вычисление дней недели
const weekDays = computed(() => {
  const days = [];
  const current = new Date(referenceDate.value);

  const monday = new Date(current);
  const dayOfWeek = current.getDay();
  const diffToMonday = (dayOfWeek + 6) % 7;
  monday.setDate(current.getDate() - diffToMonday);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const tasksArray =
    Array.isArray(tasks.value) ? tasks.value : [];

  for (let i = 0; i < 7; i++) {
    const currentDay = new Date(monday);
    currentDay.setDate(monday.getDate() + i);
    currentDay.setHours(0, 0, 0, 0);

    const isToday = currentDay.getTime() === today.getTime();

    const existingWeekend = weekends.value.find(
      (w) =>
        new Date(w.date).toDateString() ===
        currentDay.toDateString(),
    );

    days.push({
      date: currentDay,
      weekday: getWeekdayName(currentDay.getDay()),
      formattedDate: formatDate(currentDay),
      tasks: getTasksForDay(tasksArray, currentDay),
      isToday: isToday,
      weekend: existingWeekend,
    });
  }

  return days;
});

//---------------------NavigButtons-------------------------------
const prevWeek = () => {
  const newDate = new Date(referenceDate.value);
  newDate.setDate(newDate.getDate() - 7);
  referenceDate.value = newDate;
};

const nextWeek = () => {
  const newDate = new Date(referenceDate.value);
  newDate.setDate(newDate.getDate() + 7);
  referenceDate.value = newDate;
};

const resetToToday = () => {
  referenceDate.value = new Date();
};

//---------------------MenuButtons-------------------------------
const deleteSelectedTasks = async () => {
  try {
    await store.dispatch("deleteSelectedTasks");
  } catch (error) {
    console.error("Delete failed:", error);
  }
};

const openAddModal = () => {
  showAddModal.value = true;
};

const onTaskCreated = async () => {
  await loadTasks();
  showAddModal.value = false;
};

onMounted(() => {
  loadTasks();
  loadClients();
  loadWeekends();
});
</script>

<style lang="scss" scoped>
.page-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: calc(2rem + 32px);
  padding: 2rem;
  transition: margin-left 0.2s ease-out;
}
</style>
