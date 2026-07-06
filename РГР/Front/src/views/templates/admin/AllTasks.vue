<script setup>
import {ref, computed, onMounted} from "vue";
import Sidebar from "@/views/components/Sidebar.vue";
import api from "@/api";
import {useI18n} from "vue-i18n";
import {useStore} from "vuex";

const store = useStore();
const {t} = useI18n();
// Состояние
const isLoading = ref(false);
const allTasks = ref([]);
const mastersList = ref([]);
const customersList = ref([]);
const selectedTaskIds = ref([]);

const filters = ref({
  masterId: null,
  date: null,
});

// Вычисляемые свойства
const selectedCount = computed(
  () => selectedTaskIds.value.length,
);

const filteredTasks = computed(() => {
  let tasks = [...allTasks.value];

  if (filters.value.masterId) {
    tasks = tasks.filter(
      (task) => task.master_id === filters.value.masterId,
    );
  }

  if (filters.value.date) {
    tasks = tasks.filter((task) => {
      const taskDate = formatDateForCompare(task.dateTime);
      return taskDate === filters.value.date;
    });
  }

  // Сортировка по дате и времени
  tasks.sort((a, b) => {
    const dateA = new Date(a.dateTime);
    const dateB = new Date(b.dateTime);
    return dateA - dateB;
  });

  return tasks;
});

const allSelected = computed(() => {
  return (
    filteredTasks.value.length > 0 &&
    filteredTasks.value.every((task) =>
      selectedTaskIds.value.includes(task.id),
    )
  );
});

// API методы
const fetchAllTasks = async () => {
  isLoading.value = true;
  try {
    const response = await api.getAllTasks();
    allTasks.value = response.data.tasks || response.data;
    console.log("All tasks loaded:", allTasks.value.length);
  } catch (error) {
    console.error("Failed to load all tasks:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchMasters = async () => {
  try {
    const response = await api.getMasters();
    mastersList.value = response.data;
    console.log("Masters loaded:", mastersList.value.length);
  } catch (error) {
    console.error("Failed to load masters:", error);
  }
};

const fetchCustomers = async () => {
  try {
    const response = await api.getAllCustomers(
      store.getters.getID,
    );
    customersList.value = response.data;
    console.log(
      "Customers loaded:",
      customersList.value.length,
    );
  } catch (error) {
    console.error("Failed to load customers:", error);
  }
};

// Вспомогательные функции
const getMasterName = (masterId) => {
  if (!masterId) return "Не указан";
  const master = mastersList.value.find(
    (m) => m.id === masterId,
  );
  return master?.fio || master?.login || "Мастер не найден";
};

const getCustomerName = (customerId) => {
  if (!customerId) return "Не указан";
  const customer = customersList.value.find(
    (c) => c.id === customerId,
  );
  return customer?.FIO || customer?.name || "Клиент не найден";
};

const formatDate = (dateTime) => {
  if (!dateTime) return "—";
  const date = new Date(dateTime);
  return date.toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
};

const formatTime = (dateTime) => {
  if (!dateTime) return "—";
  const date = new Date(dateTime);
  return date.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatDateForCompare = (dateTime) => {
  if (!dateTime) return "";
  const date = new Date(dateTime);
  return date.toISOString().split("T")[0];
};

// Действия с задачами
const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedTaskIds.value = [];
  } else {
    selectedTaskIds.value = filteredTasks.value.map(
      (task) => task.id,
    );
  }
};

const deleteSelectedTasks = async () => {
  if (selectedTaskIds.value.length === 0) return;

  if (
    !confirm(
      `Вы уверены, что хотите удалить ${selectedTaskIds.value.length} задачу(и)?`,
    )
  ) {
    return;
  }

  isLoading.value = true;
  try {
    // Удаляем каждую задачу по отдельности с помощью api.deleteTask
    const deletePromises = selectedTaskIds.value.map(
      (taskId) => api.deleteTask(taskId),
    );

    await Promise.all(deletePromises);

    selectedTaskIds.value = [];
    await fetchAllTasks();
    alert(`Успешно удалено ${deletePromises.length} задач`);
  } catch (error) {
    console.error("Delete failed:", error);
    alert(
      "Ошибка при удалении задач. Возможно, некоторые задачи не были удалены.",
    );
  } finally {
    isLoading.value = false;
  }
};

const clearFilters = () => {
  filters.value = {
    masterId: null,
    date: null,
  };
};

const refreshData = () => {
  fetchAllTasks();
  fetchMasters();
  fetchCustomers();
};

// Загрузка всех данных
const loadAllData = async () => {
  await Promise.all([
    fetchAllTasks(),
    fetchMasters(),
    fetchCustomers(),
  ]);
};

onMounted(() => {
  loadAllData();
});
</script>

<template>
  <Sidebar />
  <main class="sidebarred">
    <div class="column">
      <!-- Заголовок и управление -->
      <div class="grid-buttons">
        <div class="flex">
          <button class="bordered flex" @click="refreshData">
            <p class="phoenix-accent-text buttons-text">
              {{ t("common.refresh") }}
            </p>
            <span class="material-icons little">refresh</span>
          </button>
        </div>

        <div class="flex">
          <button
            class="bordered flex"
            @click="deleteSelectedTasks"
            :disabled="
              selectedTaskIds.length === 0 || isLoading
            "
          >
            <p class="phoenix-accent-text buttons-text">
              {{ t("common.deleteSelected") }}
            </p>
            <span class="material-icons little">delete</span>
          </button>
        </div>
      </div>

      <hr />

      <!-- Фильтры -->
      <div class="filters">
        <select v-model="filters.masterId" class="bordered">
          <option :value="null">
            {{ t("tasks.filters.master") }}
          </option>
          <option
            v-for="master in mastersList"
            :key="master.id"
            :value="master.id"
          >
            {{ master.fio || master.login }}
          </option>
        </select>

        <input
          type="date"
          v-model="filters.date"
          class="bordered"
        />

        <button @click="clearFilters" class="bordered">
          <p class="buttons-text">
            {{ t("tasks.filters.clear") }}
          </p>
        </button>
      </div>

      <hr />

      <!-- Основная таблица задач -->
      <div v-if="!isLoading" class="tasks-table">
        <div class="table-header grid">
          <input
            type="checkbox"
            :checked="allSelected"
            @change="toggleSelectAll"
          />
          <p>
            <strong>{{ t("tasks.master") }}</strong>
          </p>
          <p>
            <strong>{{ t("tasks.date") }}</strong>
          </p>
          <p>
            <strong>{{ t("tasks.time") }}</strong>
          </p>
          <p class="only-pc-visible">
            <strong>{{ t("tasks.client") }}</strong>
          </p>
          <p class="only-pc-visible">
            <strong>{{ t("tasks.service") }}</strong>
          </p>
          <p>
            <strong>{{ t("tasks.cost") }}</strong>
          </p>
        </div>

        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="table-row grid"
        >
          <input
            type="checkbox"
            :value="task.id"
            v-model="selectedTaskIds"
          />
          <p>{{ getMasterName(task.master_id) }}</p>
          <p>{{ formatDate(task.dateTime) }}</p>
          <p>{{ formatTime(task.dateTime) }}</p>
          <p class="only-pc-visible">
            {{ getCustomerName(task.customer_id) }}
          </p>
          <p class="only-pc-visible">
            {{ task.service || "—" }}
          </p>
          <p>{{ task.cost || "—" }} ₽</p>
        </div>

        <div
          v-if="filteredTasks.length === 0"
          class="empty-state"
        >
          <p>{{ t("tasks.noTasks") }}</p>
        </div>
      </div>

      <div v-else class="loading">
        {{ t("common.loading") }}
      </div>
    </div>
  </main>
</template>
<style scoped lang="scss">
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

.sidebarred {
  flex: 1;
  padding: 2rem;
  overflow-x: auto;
}

.filters {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.filters select,
.filters input,
.filters button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.tasks-table {
  margin-top: 1rem;
  overflow-x: auto;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 10px repeat(6, 1fr);
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.table-header {
  border-bottom: 2px solid #ccc;
  margin-bottom: 0.5rem;
  font-weight: bold;
  position: sticky;
  top: 0;
  background: var(--light);
  z-index: 10;
}

.table-row:hover {
  background-color: var(--dark-alt);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.loading {
  text-align: center;
  padding: 2rem;
}

@media (max-width: 900px) {
  .table-header,
  .table-row {
    grid-template-columns: 10px repeat(4, 1fr);
  }
  .only-pc-visible {
    display: none;
  }
  .sidebarred {
    padding: 1rem;
  }
  .little {
    padding: 4px;
  }
  .grid-buttons {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Это самое важное - стили для option */
.filters select option {
  background-color: var(--light);
  color: var(--text-color);
}

/* Если не работает в Chrome, добавьте это */
.filters select option:checked,
.filters select option:hover {
  background-color: var(--dark-alt);
  color: var(--text-color);
}

/* Остальные ваши стили остаются без изменений */
.filters select,
.filters input,
.filters button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
