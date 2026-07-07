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

<template>
  <div class="diary-wrapper">
    <Sidebar />
    <main class="diary-content">
      <div class="diary-inner">
        <div class="header">
          <h2 class="phoenix-accent-text">
            {{ t("diary.title") }}
          </h2>
          <p>{{ t("diary.description") }}</p>
        </div>

        <!-- Навигационная панель -->
        <div class="grid-buttons">
          <div class="flex">
            <button
              class="bordered flex"
              @click="openAddModal"
            >
              <p class="phoenix-accent-text buttons-text">
                {{ t("diary.addTask") }}
              </p>
              <span class="material-icons little">add</span>
            </button>
          </div>

          <div class="flex">
            <button
              class="bordered flex"
              @click="deleteSelectedTasks"
              :disabled="selectedCount === 0 || isLoading"
            >
              <p class="phoenix-accent-text buttons-text">
                {{ t("diary.deleteTask") }}
              </p>
              <span class="material-icons little">delete</span>
            </button>
          </div>
        </div>

        <hr />

        <NewTask
          v-if="showAddModal"
          :masterId="currentMasterId"
          @close="showAddModal = false"
          @success="onTaskCreated"
        />

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

        <!-- Навигация между неделями - В ЛИНИЮ -->
        <div class="nav-buttons">
          <button class="bordered" @click="prevWeek">←</button>
          <button class="bordered" @click="resetToToday">
            {{ t("diary.resetWeek") }}
          </button>
          <button class="bordered" @click="nextWeek">→</button>
        </div>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.diary-wrapper {
  display: flex;
  width: 100%;
  min-height: 100vh;
}

.diary-content {
  flex: 1;
  padding: 2rem;
  padding-bottom: 4rem;
  margin-left: calc(2rem + 32px);
  transition: margin-left 0.2s ease-out;
  overflow-x: auto;
}

.diary-inner {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 100%;
}

:global(.app.sidebar-expanded) .diary-content {
  margin-left: var(--sidebar-width);
}

.flex {
  display: flex;
  flex-direction: row;
  gap: 2em;
}

.grid-buttons {
  display: flex;
  gap: 50px;
}

.buttons-text {
  padding: 7px;
}

/* Кнопки навигации В ЛИНИЮ */
.nav-buttons {
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: center;
  margin-top: auto;
  padding-top: 20px;
  flex-wrap: wrap;
}

.nav-buttons button {
  min-width: 120px;
}

@media (max-width: 900px) {
  .little {
    padding: 4px;
  }
  .grid-buttons {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
  .diary-content {
    padding: 1rem;
    padding-bottom: 6rem;
    margin-left: 0 !important;
  }

  /* На мобилках кнопки тоже в линию, но с переносом */
  .nav-buttons {
    gap: 10px;
  }

  .nav-buttons button {
    flex: 1;
    min-width: 80px;
  }
}
</style>
