<script setup>
import {ref, computed} from "vue";
import {useStore} from "vuex";

const store = useStore();

const props = defineProps({
  day: Object,
  selectedTaskIds: Array,
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

// Получить количество выбранных задач в этом дне
const selectedCountInDay = computed(() => {
  if (!props.day?.tasks || !selectedTaskIds.value) return 0;
  const dayTaskIds = props.day.tasks.map((t) => t.id);
  return selectedTaskIds.value.filter((id) =>
    dayTaskIds.includes(id),
  ).length;
});

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
</script>

<template>
  <div class="flex" style="gap: 10px">
    <p class="vertical-text">
      {{ day.formattedDate }} | {{ day?.weekday }}
    </p>
    <div class="day bordered">
      <div class="flex">
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
          <div v-if="day.tasks.length == 0">
            <p class="horizontal-align" style="opacity: 0.4">
              НА ЭТОТ ДЕНЬ КЛИЕНТОВ НЕТ
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
