<script setup>
import Sidebar from "@/views/components/Sidebar.vue";
import {onMounted, ref, computed} from "vue";
import {useStore} from "vuex";
import NewMaster from "@/views/components/NewMaster.vue";
import api from "@/api";

const showAddModal = ref(false);
const selectedMasters = ref([]); // Переименовано с selectedClients
const store = useStore();

const masters = ref([]);
const isLoading = ref(false);

const loadMasters = async () => {
  isLoading.value = true;
  try {
    const response = await api.getMasters();
    masters.value = response.data || [];
    console.log("Masters loaded:", masters.value);
  } catch (error) {
    console.error("Failed to fetch masters:", error);
  } finally {
    isLoading.value = false;
  }
};

const selectedCount = computed(
  () => selectedMasters.value.length,
);

const toggleMasterSelection = (masterId) => {
  const index = selectedMasters.value.indexOf(masterId);
  if (index === -1) {
    selectedMasters.value.push(masterId);
  } else {
    selectedMasters.value.splice(index, 1);
  }
};

const selectAll = () => {
  if (selectedMasters.value.length === masters.value.length) {
    selectedMasters.value = [];
  } else {
    selectedMasters.value = masters.value.map((m) => m.id);
  }
};

const deleteSelectedMasters = async () => {
  if (selectedMasters.value.length === 0) return;

  if (
    !confirm(
      `Вы уверены, что хотите удалить ${selectedMasters.value.length} мастера(ов)?`,
    )
  ) {
    return;
  }

  isLoading.value = true;
  try {
    // ВАЖНО: нужно создать action deleteMasters в store или API
    await Promise.all(
      selectedMasters.value.map((id) => api.deleteMaster(id)),
    );
    selectedMasters.value = [];
    await loadMasters(); // Перезагружаем мастеров
  } catch (error) {
    console.error("Delete failed:", error);
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  showAddModal.value = true;
};

const onMasterCreated = async () => {
  await loadMasters(); // Обновляем список мастеров
  showAddModal.value = false;
};

onMounted(() => {
  loadMasters();
});
</script>

<template>
  <Sidebar />
  <main>
    <div class="column">
      <div class="flex">
        <button class="bordered flex" @click="openAddModal">
          <p
            class="phoenix-accent-text"
            style="margin-top: 4px; padding: 0"
          >
            Добавить
          </p>
          <span class="material-icons little">add</span>
        </button>

        <button
          class="bordered flex"
          @click="deleteSelectedMasters"
          :disabled="selectedCount === 0 || isLoading"
        >
          <p
            class="phoenix-accent-text"
            style="margin-top: 4px; padding: 0"
          >
            Удалить
          </p>
          <span class="material-icons little">delete</span>
        </button>

        <button
          class="bordered flex"
          @click="selectAll"
          :disabled="!masters.length"
        >
          <p
            class="phoenix-accent-text"
            style="margin-top: 4px; padding: 0"
          >
            {{
              selectedCount === masters.length ?
                "Снять все"
              : "Выбрать все"
            }}
          </p>
        </button>
      </div>

      <hr />

      <div class="masters-list">
        <!-- Шапка таблицы -->
        <div
          class="master-item header grid"
          style="grid-template-columns: auto 1fr 1fr"
          v-if="masters.length"
        >
          <p></p>
          <p class="header-text" style="margin-left: 20px">
            <strong>Логин</strong>
          </p>
          <p class="header-text">
            <strong>Роль</strong>
          </p>
        </div>

        <!-- Строки с данными мастеров -->
        <div
          class="master-item grid"
          style="grid-template-columns: auto 1fr 1fr"
          v-for="master in masters"
          :key="master.id"
        >
          <input
            type="checkbox"
            :value="master.id"
            :checked="selectedMasters.includes(master.id)"
            @change="toggleMasterSelection(master.id)"
          />
          <p>{{ master.login }}</p>
          <p>{{ master.role }}</p>
        </div>

        <div v-if="!masters.length" class="empty-state">
          <p>Нет добавленных мастеров</p>
        </div>
      </div>

      <NewMaster
        v-if="showAddModal"
        @close="showAddModal = false"
        @success="onMasterCreated"
      />
    </div>
  </main>
</template>

<style scoped>
.masters-list {
  margin-top: 1rem;
}

.master-item {
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.master-item:hover:not(.header) {
  background-color: #f5f5f5;
}

.master-item.header {
  border-bottom: 2px solid #ccc;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.header-text {
  color: #333;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.grid {
  display: grid;
  gap: 1rem;
}

.bordered {
  margin-right: 0.5rem;
}
</style>
