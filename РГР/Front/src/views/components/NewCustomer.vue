<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="phoenix-accent-text">Добавление клиента</h2>
        <button class="close-btn" @click="closeModal">
          <span class="material-icons">close</span>
        </button>
      </div>

      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="service">Фамилия Имя Отчество</label>
          <input
            id="FIO"
            type="text"
            v-model="form.fio"
            placeholder="Например: Иваненко Иван Иванович"
            required
            :class="{error: errors.fio}"
          />
          <span v-if="errors.fio" class="error-text">{{
            errors.fio
          }}</span>
        </div>

        <div class="form-group">
          <label for="service">Телефон</label>
          <input
            id="Phone"
            type="text"
            v-model="form.phone"
            placeholder="Например: +79792341234"
            required
            :class="{error: errors.phone}"
          />
          <span v-if="errors.phone" class="error-text">{{
            errors.phone
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
            <span v-else>Добавить Клиента</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import api from "@/api";

const emit = defineEmits(["close", "success"]);

// Форма
const form = ref({
  customer_fio: "",
  customer_phone: "",
});

// Ошибки валидации
const errors = ref({});
const isLoading = ref(false);

// Валидация формы
const validateForm = () => {
  const newErrors = {};

  if (!form.value.fio) {
    newErrors.fio = "Введите ФИО клиента";
  }

  if (
    !form.value.phone ||
    !/^\+7\d{10}$/.test(form.value.phone.trim())
  ) {
    newErrors.service =
      "Введите номер телефона (формат +7XXXXXXXXXX, всего 12 символов)";
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Отправка формы
const submitForm = async () => {
  if (!validateForm()) return;

  isLoading.value = true;

  try {
    // Создаем объект задачи
    const customerData = {
      FIO: form.value.fio.trim(),
      phone: form.value.phone.trim(),
    };

    // Отправляем запрос на сервер
    const response = await api.addCustomer(customerData);

    // Успех - закрываем модалку и обновляем список
    emit("success", response.data);
    closeModal();
  } catch (error) {
    console.error("Failed to addCustomer:", error);
    if (error.response?.data?.detail) {
      alert("Ошибка: " + error.response.data.detail);
    } else {
      alert(
        "Не удалось Добавить клиента. Проверьте подключение к интернету.",
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
