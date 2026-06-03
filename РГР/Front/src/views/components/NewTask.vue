<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="phoenix-accent-text">Создание записи</h2>
        <button class="close-btn" @click="closeModal">
          <span class="material-icons">close</span>
        </button>
      </div>

      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="customer">Клиент</label>
          <select
            id="customer"
            v-model="form.customer_id"
            required
            :class="{error: errors.customer_id}"
          >
            <option value="">Выберите клиента</option>
            <option
              v-for="customer in customers"
              :key="customer.id"
              :value="customer.id"
            >
              {{ customer.FIO }} ({{ customer.phone }})
            </option>
          </select>
          <span v-if="errors.customer_id" class="error-text">{{
            errors.customer_id
          }}</span>
        </div>

        <div class="form-group">
          <label for="service">Услуга</label>
          <input
            id="service"
            type="text"
            v-model="form.service"
            placeholder="Например: Маникюр, Стрижка и т.д."
            required
            :class="{error: errors.service}"
          />
          <span v-if="errors.service" class="error-text">{{
            errors.service
          }}</span>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="date">Дата</label>
            <input
              id="date"
              type="date"
              v-model="form.date"
              required
              :class="{error: errors.date}"
            />
            <span v-if="errors.date" class="error-text">{{
              errors.date
            }}</span>
          </div>

          <div class="form-group">
            <label for="time">Время</label>
            <input
              id="time"
              type="time"
              v-model="form.time"
              required
              :class="{error: errors.time}"
            />
            <span v-if="errors.time" class="error-text">{{
              errors.time
            }}</span>
          </div>
        </div>

        <div class="form-group">
          <label for="cost">Стоимость (₽)</label>
          <input
            id="cost"
            type="number"
            v-model="form.cost"
            placeholder="Например: 2000"
            required
            min="0"
            step="100"
            :class="{error: errors.cost}"
          />
          <span v-if="errors.cost" class="error-text">{{
            errors.cost
          }}</span>
        </div>

        <div class="form-actions">
          <button
            type="button"
            class="cancel-btn"
            @click="closeModal"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="submit-btn"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>Создать запись</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from "vue";
import {useStore} from "vuex";
import api from "@/api";

const props = defineProps({
  masterId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["close", "success"]);

const store = useStore();
const customers = computed(
  () => store.getters.getCustomers || [],
);

// Форма
const form = ref({
  customer_id: "",
  service: "",
  date: "",
  time: "",
  cost: "",
});

// Ошибки валидации
const errors = ref({});
const isLoading = ref(false);

// Загружаем клиентов если их нет
onMounted(async () => {
  if (customers.value.length === 0) {
    await store.dispatch("getClients");
  }
});

// Валидация формы
const validateForm = () => {
  const newErrors = {};

  if (!form.value.customer_id) {
    newErrors.customer_id = "Выберите клиента";
  }

  if (
    !form.value.service ||
    form.value.service.trim().length < 2
  ) {
    newErrors.service =
      "Введите название услуги (минимум 2 символа)";
  }

  if (!form.value.date) {
    newErrors.date = "Выберите дату";
  } else {
    const selectedDate = new Date(form.value.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (selectedDate < today) {
      newErrors.date = "Дата не может быть в прошлом";
    }
  }

  if (!form.value.time) {
    newErrors.time = "Выберите время";
  }

  if (!form.value.cost) {
    newErrors.cost = "Введите стоимость";
  } else if (form.value.cost < 0) {
    newErrors.cost = "Стоимость не может быть отрицательной";
  } else if (form.value.cost > 100000) {
    newErrors.cost = "Слишком большая сумма (макс. 100 000 ₽)";
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Отправка формы
const submitForm = async () => {
  if (!validateForm()) return;

  isLoading.value = true;

  try {
    // Формируем datetime из date и time
    const dateTime = new Date(
      `${form.value.date}T${form.value.time}`,
    );

    // Создаем объект задачи
    const taskData = {
      customer_id: parseInt(form.value.customer_id),
      master_id: props.masterId,
      service: form.value.service.trim(),
      datetime: dateTime.toISOString(),
      cost: parseInt(form.value.cost),
    };

    // Отправляем запрос на сервер
    const response = await api.createTask(taskData);

    // Успех - закрываем модалку и обновляем список
    emit("success", response.data);
    closeModal();
  } catch (error) {
    console.error("Failed to create task:", error);
    if (error.response?.data?.detail) {
      alert("Ошибка: " + error.response.data.detail);
    } else {
      alert(
        "Не удалось создать запись. Проверьте подключение к интернету.",
      );
    }
  } finally {
    isLoading.value = false;
  }
};

// Закрытие модального окна
const closeModal = () => {
  emit("close");
};
</script>

<script>
// Метод для API (добавьте в ваш api/index.js)
export const createTask = (taskData) => {
  return apiClient.post("diary/pushTask", taskData);
};
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid var(--secondary);

  h2 {
    margin: 0;
    font-size: 1.5rem;
  }

  .close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;

    &:hover {
      background: rgba(0, 0, 0, 0.05);
      transform: scale(1.1);
    }

    .material-icons {
      font-size: 24px;
      color: #666;
    }
  }
}

form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--primary);
    font-size: 14px;
  }

  input,
  select {
    width: 100%;
    padding: 10px 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.2s;

    &:focus {
      outline: none;
      border-color: var(--secondary);
      box-shadow: 0 0 0 3px rgba(255, 107, 19, 0.1);
    }

    &.error {
      border-color: var(--error);
    }
  }

  .error-text {
    display: block;
    margin-top: 5px;
    font-size: 12px;
    color: var(--error);
  }
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;

  button {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
  }

  .cancel-btn {
    background: #f5f5f5;
    color: #666;

    &:hover {
      background: #e0e0e0;
    }
  }

  .submit-btn {
    background: linear-gradient(
      45deg,
      var(--primary),
      var(--secondary)
    );
    color: white;

    &:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(227, 59, 31, 0.3);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
