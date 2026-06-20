<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="phoenix-accent-text">
          {{
            isEdit ? t("common.edit") : t("clients.addClient")
          }}
        </h2>
        <button class="close-btn" @click="closeModal">
          <span class="material-icons">close</span>
        </button>
      </div>

      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="FIO">{{ t("clients.fio") }} *</label>
          <input
            id="FIO"
            type="text"
            v-model="form.fio"
            placeholder="Например: Иваненко Иван Иванович"
            :class="{error: errors.fio}"
          />
          <span v-if="errors.fio" class="error-text">{{
            errors.fio
          }}</span>
        </div>

        <div class="form-group">
          <label for="Phone">{{ t("clients.phone") }} *</label>
          <input
            id="Phone"
            type="tel"
            v-model="form.phone"
            placeholder="+7 999 123-45-67"
            :class="{error: errors.phone}"
          />
          <span v-if="errors.phone" class="error-text">{{
            errors.phone
          }}</span>
        </div>

        <div class="form-group">
          <label for="Email">Email</label>
          <input
            id="Email"
            type="email"
            v-model="form.email"
            placeholder="client@example.com"
            :class="{error: errors.email}"
          />
          <span v-if="errors.email" class="error-text">{{
            errors.email
          }}</span>
        </div>

        <div class="form-actions">
          <button
            type="button"
            class="cancel-btn"
            @click="closeModal"
          >
            {{ t("common.cancel") }}
          </button>
          <button
            type="submit"
            class="submit-btn"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>{{
              isEdit ?
                t("common.save")
              : t("clients.addClient")
            }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue";
import api from "@/api";
import {useI18n} from "vue-i18n";
import {useStore} from "vuex";

const {t} = useI18n();

const store = useStore();

const props = defineProps({
  customer: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "success"]);

const isEdit = ref(false);
const form = ref({
  fio: "",
  phone: "",
  email: "",
});

const errors = ref({});
const isLoading = ref(false);

// Валидация формы
const validateForm = () => {
  const newErrors = {};

  if (!form.value.fio || !form.value.fio.trim()) {
    newErrors.fio = t("errors.clients.fio");
  } else if (form.value.fio.length < 3) {
    newErrors.fio = t("errors.clients.fiomin3");
  } else if (form.value.fio.length > 50) {
    newErrors.fio = t("errors.clients.fiomax50");
  }

  if (!form.value.phone || !form.value.phone.trim()) {
    newErrors.phone = t("errors.clients.phone");
  } else {
    // Очищаем номер от лишних символов
    let cleanPhone = form.value.phone.replace(/[^\d+]/g, "");

    // Проверяем формат
    const phoneRegex = /^\+7\d{10}$/;
    const phoneRegexAlt = /^8\d{10}$/;

    if (
      !phoneRegex.test(cleanPhone) &&
      !phoneRegexAlt.test(cleanPhone)
    ) {
      newErrors.phone = t("errors.clients.phoneregex");
    }
  }

  if (form.value.email && form.value.email.trim()) {
    const emailRegex = /^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$/;
    if (!emailRegex.test(form.value.email)) {
      newErrors.email = "Введите корректный email адрес";
    }
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Очистка и форматирование телефона
const formatPhone = (phone) => {
  let cleaned = phone.replace(/\D/g, "");

  if (cleaned.startsWith("8")) {
    cleaned = "+7" + cleaned.substring(1);
  } else if (
    !cleaned.startsWith("7") &&
    !cleaned.startsWith("+")
  ) {
    cleaned = "+7" + cleaned;
  } else if (
    cleaned.startsWith("7") &&
    !cleaned.startsWith("+7")
  ) {
    cleaned = "+7" + cleaned.substring(1);
  }

  return cleaned;
};

// Отправка формы
const submitForm = async () => {
  if (!validateForm()) return;

  isLoading.value = true;

  try {
    const customerData = {
      masterID: store.getters.getID,
      FIO: form.value.fio.trim(),
      phone: formatPhone(form.value.phone),
      email: form.value.email?.trim() || null,
    };

    let response;
    if (isEdit.value && props.customer) {
      response = await api.updateCustomer(
        props.customer.id,
        customerData,
      );
    } else {
      response = await api.addCustomer(customerData);
    }

    emit("success", response.data);
    closeModal();
  } catch (error) {
    console.error("Failed to save customer:", error);
    if (error.response?.data?.detail) {
      alert("Ошибка: " + error.response.data.detail);
    } else {
      alert(
        `Не удалось ${isEdit.value ? "сохранить" : "добавить"} клиента. Проверьте подключение к интернету.`,
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

// Инициализация формы для редактирования
onMounted(() => {
  if (props.customer) {
    isEdit.value = true;
    form.value = {
      fio: props.customer.FIO || "",
      phone: props.customer.phone || "",
      email: props.customer.email || "",
    };
  }
});
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
  background: var(--light);
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
      color: var(--grey);
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

  input {
    width: 100%;
    padding: 10px 12px;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.2s;
    background: var(--light);
    color: var(--text-color);

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
    background: var(--dark-alt);
    color: var(--grey);

    &:hover {
      background: var(--border-color);
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
