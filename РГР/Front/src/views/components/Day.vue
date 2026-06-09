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
      <div class="weekend-content" v-if="isWeekend">
        <p class="phoenix-accent-text base">
          {{ t("diary.weekend") }}
        </p>
        <button class="bordered flex" @click="noWeekend">
          <span class="material-icons little">smoke_free</span>
          <p>{{ t("diary.cancelWeekend") }}</p>
          <span class="material-icons little">no_drinks</span>
        </button>
      </div>

      <!-- Есть задачи -->
      <div
        v-else-if="day.tasks && day.tasks.length > 0"
        class="tasks-container"
      >
        <!-- Заголовок таблицы -->
        <div class="tasks-header grid">
          <p>{{ t("diary.table.select") }}</p>
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

      <!-- Нет задач -->
      <div class="empty-content" v-else>
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

.weekend-content {
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
  grid-template-columns: 80px 100px 1fr 1fr 120px;
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

.task-row {
  display: grid;
  grid-template-columns: 80px 100px 1fr 1fr 120px;
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

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 3rem;
  text-align: center;
  min-height: 200px;
}

.empty-content .base {
  font-size: 1.2rem;
  opacity: 0.7;
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
  gap: 0.5rem;
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
  font-size: 1.1rem;
  font-weight: 500;
}

.little {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
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
    grid-template-columns: 60px 80px 1fr 1fr 100px;
    gap: 0.5rem;
    font-size: 0.85rem;
  }

  .day {
    padding: 0.75rem;
  }
}

@media (max-width: 600px) {
  .tasks-header,
  .task-row {
    grid-template-columns: 50px 70px 1fr 1fr 80px;
    font-size: 0.75rem;
  }
}
</style>
