<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="phoenix-accent-text">
          {{ isEdit ? "Редактирование" : "Добавление" }}
          мастера
        </h2>
        <button class="close-btn" @click="closeModal">
          <span class="material-icons">close</span>
        </button>
      </div>

      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="FIO">Фамилия Имя Отчество *</label>
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
          <label for="Login">Логин *</label>
          <input
            id="Login"
            type="text"
            v-model="form.login"
            placeholder="Например: master_ivan"
            :class="{error: errors.login}"
            :disabled="isEdit"
          />
          <span v-if="errors.login" class="error-text">{{
            errors.login
          }}</span>
          <small v-if="isEdit" class="hint-text"
            >Логин нельзя изменить</small
          >
        </div>

        <div class="form-group">
          <label for="Password">
            Пароль
            <span v-if="!isEdit" class="required">*</span>
            <span v-else class="optional"
              >(оставьте пустым, чтобы не менять)</span
            >
          </label>
          <input
            id="Password"
            type="password"
            v-model="form.password"
            :placeholder="
              isEdit ?
                'Введите новый пароль (необязательно)'
              : 'Например: 12345qwerty'
            "
            :class="{error: errors.password}"
          />
          <span v-if="errors.password" class="error-text">{{
            errors.password
          }}</span>
        </div>

        <div class="form-group" v-if="isEdit">
          <label for="Role">Роль</label>
          <select
            id="Role"
            v-model="form.role"
            :class="{error: errors.role}"
          >
            <option value="master">Мастер</option>
            <option value="admin">Администратор</option>
          </select>
          <span v-if="errors.role" class="error-text">{{
            errors.role
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
            <span v-else>{{
              isEdit ? "Сохранить" : "Добавить мастера"
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

const props = defineProps({
  master: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "success"]);

const isEdit = ref(false);
const form = ref({
  fio: "",
  login: "",
  password: "",
  role: "master",
});

const errors = ref({});
const isLoading = ref(false);

// Валидация формы
const validateForm = () => {
  const newErrors = {};

  // Валидация ФИО
  if (!form.value.fio || !form.value.fio.trim()) {
    newErrors.fio = "Введите ФИО мастера";
  } else if (form.value.fio.length < 3) {
    newErrors.fio = "ФИО должно содержать минимум 3 символа";
  } else if (form.value.fio.length > 100) {
    newErrors.fio = "ФИО не должно превышать 100 символов";
  }

  // Валидация логина (только для нового мастера)
  if (!isEdit.value) {
    if (!form.value.login || !form.value.login.trim()) {
      newErrors.login = "Введите логин мастера";
    } else if (form.value.login.length < 3) {
      newErrors.login =
        "Логин должен содержать минимум 3 символа";
    } else if (form.value.login.length > 50) {
      newErrors.login =
        "Логин не должен превышать 50 символов";
    } else if (!/^[a-zA-Z0-9_]+$/.test(form.value.login)) {
      newErrors.login =
        "Логин может содержать только буквы, цифры и знак подчеркивания";
    }
  }

  // Валидация пароля
  if (!isEdit.value) {
    if (!form.value.password) {
      newErrors.password = "Введите пароль";
    } else if (form.value.password.length < 6) {
      newErrors.password =
        "Пароль должен содержать минимум 6 символов";
    }
  } else if (
    form.value.password &&
    form.value.password.length < 6
  ) {
    newErrors.password =
      "Пароль должен содержать минимум 6 символов";
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

// Отправка формы
const submitForm = async () => {
  if (!validateForm()) return;

  isLoading.value = true;

  try {
    let response;

    if (isEdit.value && props.master) {
      // Редактирование мастера
      const masterData = {
        fio: form.value.fio.trim(),
        role: form.value.role,
      };

      // Добавляем пароль только если он указан
      if (form.value.password && form.value.password.trim()) {
        masterData.password = form.value.password.trim();
      }

      response = await api.updateMaster(
        props.master.id,
        masterData,
      );
    } else {
      // Создание нового мастера
      const masterData = {
        fio: form.value.fio.trim(),
        login: form.value.login.trim(),
        password: form.value.password.trim(),
        role: "master",
      };

      response = await api.register(masterData);
    }

    emit("success", response.data);
    closeModal();
  } catch (error) {
    console.error("Failed to save master:", error);
    if (error.response?.data?.detail) {
      alert("Ошибка: " + error.response.data.detail);
    } else {
      alert(
        `Не удалось ${isEdit.value ? "сохранить" : "добавить"} мастера. Проверьте подключение к интернету.`,
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
  if (props.master) {
    isEdit.value = true;
    form.value = {
      fio: props.master.fio || "",
      login: props.master.login || "",
      password: "", // Пароль не заполняем при редактировании
      role: props.master.role || "master",
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

  input,
  select {
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

    &:disabled {
      background: var(--dark-alt);
      cursor: not-allowed;
    }
  }

  .error-text {
    display: block;
    margin-top: 5px;
    font-size: 12px;
    color: var(--error);
  }

  .hint-text {
    display: block;
    margin-top: 5px;
    font-size: 12px;
    color: var(--grey);
  }

  .required {
    color: var(--error);
  }

  .optional {
    font-size: 12px;
    color: var(--grey);
    font-weight: normal;
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
