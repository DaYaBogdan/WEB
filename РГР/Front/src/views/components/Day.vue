<script setup>
import {ref, computed, onMounted, watch} from "vue";
import {useStore} from "vuex";

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
  if (!customer_id) return "ID не указан";

  const customer = customers.value.find(
    (c) => c.id === customer_id,
  );

  if (customer) {
    return customer.FIO;
  } else {
    console.warn(`Клиент с ID ${customer_id} не найден`);
    return "Неизвестный клиент";
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
  } catch (e) {
    alert("Weekend ERROR");
  }
};

const noWeekend = async () => {
  try {
    await store.dispatch(
      "deleteWeekend",
      props.day.weekend.id,
    );
  } catch (e) {
    alert("Weekend ERROR");
  }
};

const sortTasksByTime = () => {
  if (props.day?.tasks && Array.isArray(props.day.tasks)) {
    props.day.tasks.sort((a, b) => {
      // Для формата "20:00:00" берем первые 5 символов "HH:MM"
      const timeA = a.time?.substring(0, 5) || "00:00";
      const timeB = b.time?.substring(0, 5) || "00:00";
      return timeA.localeCompare(timeB);
    });
  }
};

// Сортировка при монтировании
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
  <div class="flex" style="gap: 10px">
    <p class="vertical-text">
      {{ day.formattedDate }} | {{ day?.weekday }}
    </p>
    <div
      class="day bordered"
      :class="{
        'day-weekend': isWeekend,
      }"
    >
      <div class="column" v-if="isWeekend">
        <p class="phoenix-accent-text base">ВЫХОДНОЙ</p>
        <button class="bordered flex" @click="noWeekend">
          <span class="material-icons little">smoke_free</span>
          <p>Отменить выходной?</p>
          <span class="material-icons little">no_drinks</span>
        </button>
      </div>
      <div class="flex" v-else-if="day.tasks.length != 0">
        <div class="column" style="gap: 20px">
          <div
            v-if="day.tasks.length != 0"
            class="grid"
            style="grid-template-columns: repeat(5, 1fr) auto"
          >
            <p>Выбрать</p>
            <p>Время</p>
            <p>Клиент</p>
            <p>Услуга</p>
            <p>Цена</p>
          </div>
          <div
            class="grid"
            v-for="task in day.tasks"
            :key="task"
          >
            <input
              type="checkbox"
              :checked="isTaskSelected(task.id)"
              @change="(e) => toggleTask(task.id, e)"
            />
            <div>
              <div class="flex">
                <p>{{ task.time }}</p>
                <p>{{ findCustomer(task.customer_id) }}</p>
                <p>{{ task.service }}</p>
                <p>{{ task.cost }}</p>
              </div>
              <hr />
            </div>
          </div>
        </div>
      </div>
      <div class="column weekEndDialog" v-else>
        <p class="phoenix-accent-text base">КЛИЕНТОВ НЕТ</p>
        <button class="bordered flex" @click="makeWeekend">
          <span class="material-icons little">event</span>
          <p>Выходной?</p>
          <span class="material-icons little"
            >celebration</span
          >
        </button>
      </div>
    </div>
  </div>
</template>
