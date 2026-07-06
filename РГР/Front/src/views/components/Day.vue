<script setup>
import {ref, computed, onMounted, watch} from "vue";
import {useStore} from "vuex";
import {useI18n} from "vue-i18n";

const {t} = useI18n();
const store = useStore();

const props = defineProps({
  day: Object,
  selectedTaskIds: Array,
});

const isWeekend = computed(() => {
  return (
    props.day?.weekend !== undefined &&
    props.day?.weekend !== null
  );
});

const selectedTaskIds = computed(
  () => store.getters.getSelectedTaskIds || [],
);
const customers = computed(
  () => store.getters.getCustomers || [],
);

//---------------------Select All-------------------------
const isAllSelected = computed(() => {
  if (!props.day?.tasks || props.day.tasks.length === 0) {
    return false;
  }
  return props.day.tasks.every((task) =>
    selectedTaskIds.value.includes(task.id),
  );
});

const toggleAllTasks = (event) => {
  const isChecked = event.target.checked;
  const taskIds = props.day.tasks.map((task) => task.id);

  if (isChecked) {
    // Выбираем все задачи
    taskIds.forEach((taskId) => {
      if (!selectedTaskIds.value.includes(taskId)) {
        store.dispatch("toggleTaskSelection", taskId);
      }
    });
  } else {
    // Снимаем все задачи
    taskIds.forEach((taskId) => {
      if (selectedTaskIds.value.includes(taskId)) {
        store.dispatch("removeTaskSelection", taskId);
      }
    });
  }
};

//---------------------DeletingTasks-------------------------
const isTaskSelected = (taskId) => {
  if (
    !selectedTaskIds.value ||
    !Array.isArray(selectedTaskIds.value)
  ) {
    return false;
  }
  return selectedTaskIds.value.includes(taskId);
};

// Обработчик изменения чекбокса
const toggleTask = (taskId, event) => {
  const isChecked = event.target.checked;
  if (isChecked) {
    store.dispatch("toggleTaskSelection", taskId);
  } else {
    store.dispatch("removeTaskSelection", taskId);
  }
};

//---------------------CustomersWork-------------------------
const findCustomer = (customer_id) => {
  if (!customer_id) return t("common.notSpecified");

  const customer = customers.value.find(
    (c) => c.id === customer_id,
  );

  if (customer) {
    return customer.FIO;
  } else {
    console.warn(`Клиент с ID ${customer_id} не найден`);
    return t("common.unknown");
  }
};

const makeWeekend = async () => {
  try {
    const formattedDate = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(
        2,
        "0",
      );
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    };
    await store.dispatch(
      "makeWeekend",
      formattedDate(props.day.date),
    );
    await store.dispatch("getWeekends");
  } catch (e) {
    alert(t("errors.weekendError"));
  }
};

const noWeekend = async () => {
  try {
    await store.dispatch(
      "deleteWeekend",
      props.day.weekend.id,
    );
    await store.dispatch("getWeekends");
  } catch (e) {
    alert(t("errors.weekendError"));
  }
};

const sortTasksByTime = () => {
  if (props.day?.tasks && Array.isArray(props.day.tasks)) {
    props.day.tasks.sort((a, b) => {
      const timeA = a.time?.substring(0, 5) || "00:00";
      const timeB = b.time?.substring(0, 5) || "00:00";
      return timeA.localeCompare(timeB);
    });
  }
};

onMounted(() => {
  sortTasksByTime();
});

watch(
  () => props.day?.tasks,
  () => {
    sortTasksByTime();
  },
  {deep: true},
);
</script>

<template>
  <div class="day-wrapper">
    <div class="vertical-date">
      <p class="vertical-text">
        {{ day.formattedDate }} | {{ day?.weekday }}
      </p>
    </div>

    <div
      class="day bordered"
      :class="{
        'day-weekend': isWeekend,
      }"
    >
      <!-- Выходной день -->
      <div class="none-tasks-content" v-if="isWeekend">
        <p class="phoenix-accent-text base">
          {{ t("diary.weekend") }}
        </p>
        <button class="bordered flex" @click="noWeekend">
          <span class="material-icons little">smoke_free</span>
          <p>{{ t("diary.cancelWeekend") }}</p>
          <span class="material-icons little">no_drinks</span>
        </button>
      </div>

      <!-- Нет задач -->
      <div
        class="none-tasks-content"
        v-else-if="day.tasks.length <= 0"
      >
        <p class="phoenix-accent-text base">
          {{ t("diary.noTasks") }}
        </p>
        <button class="bordered flex" @click="makeWeekend">
          <span class="material-icons little">event</span>
          <p>{{ t("diary.makeWeekend") }}</p>
          <span class="material-icons little"
            >celebration</span
          >
        </button>
      </div>

      <!-- Есть задачи -->
      <div v-else class="tasks-container">
        <!-- Заголовок таблицы -->
        <div class="tasks-header grid">
          <div class="select-all-wrap">
            <input
              type="checkbox"
              :checked="isAllSelected"
              @change="toggleAllTasks"
              class="select-all-checkbox"
            />
          </div>
          <p>{{ t("diary.table.time") }}</p>
          <p>{{ t("diary.table.client") }}</p>
          <p>{{ t("diary.table.service") }}</p>
          <p>{{ t("diary.table.price") }}</p>
        </div>

        <!-- Строки с задачами -->
        <div
          v-for="task in day.tasks"
          :key="task.id"
          class="task-row grid"
        >
          <input
            type="checkbox"
            :checked="isTaskSelected(task.id)"
            @change="(e) => toggleTask(task.id, e)"
          />
          <p>{{ task.time }}</p>
          <p>{{ findCustomer(task.customer_id) }}</p>
          <p>{{ task.service }}</p>
          <p>{{ task.cost }} ₽</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.day-wrapper {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.vertical-date {
  flex-shrink: 0;
}

.vertical-text {
  padding: 10px;
  margin-top: 20px;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  text-align: right;
  font-size: 1.2em;
  font-weight: 500;
  color: var(--primary);
}

.day {
  flex: 1;
  padding: 1rem;
  border-radius: 12px;
  background: var(--light);
  border: 2px solid var(--grey);
}

.day-weekend {
  background: linear-gradient(
    135deg,
    rgba(227, 59, 31, 0.1),
    rgba(255, 106, 19, 0.05)
  );
  border-color: var(--primary);
}

.none-tasks-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  text-align: center;
}

.tasks-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tasks-header {
  display: grid;
  grid-template-columns: 20px repeat(4, 1fr);
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-bottom: 2px solid var(--secondary);
  font-weight: bold;
  color: var(--dark);
  background: var(--light);
  position: sticky;
  top: 0;
}

.tasks-header p {
  margin: 0;
  font-size: 0.9rem;
}

.select-all-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.select-all-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary);
}

.select-all-label {
  font-size: 0.85rem;
  white-space: nowrap;
}

.task-row {
  display: grid;
  grid-template-columns: 20px repeat(4, 1fr);
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid var(--grey);
}

.task-row p {
  margin: 0;
  color: var(--dark);
}

input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary);
}

.bordered {
  padding: 7px 15px;
  border-radius: 12px;
  border: 2px solid var(--secondary);
  background: transparent;
  transition: all 0.3s ease;
}

.flex {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 300px;
}

.column {
  display: flex;
  flex-direction: column;
}

.phoenix-accent-text {
  background: linear-gradient(
    45deg,
    var(--primary),
    var(--secondary),
    var(--accent)
  );
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.base {
  font-size: 1.2rem;
  font-weight: 500;
}

.little {
  font-size: 1.2rem;
}

@media (max-width: 900px) {
  .day-wrapper {
    flex-direction: column;
  }
  .vertical-text {
    writing-mode: horizontal-tb;
    transform: none;
    text-align: center;
    margin-top: 0;
  }

  .tasks-header,
  .task-row {
    grid-template-columns: 20px repeat(4, 1fr);
    gap: 0.5rem;
    font-size: 0.85rem;
  }

  .day {
    padding: 0.75rem;
  }

  .select-all-label {
    font-size: 0.7rem;
  }
}
/* 
@media (max-width: 600px) {
  .tasks-header,
  .task-row {
    grid-template-columns: 20px repeat(4, 1fr);
    font-size: 0.7rem;
    gap: 0.3rem;
  }

  .select-all-wrap {
    gap: 0.2rem;
  }

  .select-all-label {
    font-size: 0.6rem;
  }

  input[type="checkbox"] {
    width: 14px;
    height: 14px;
  }
} */
</style>
