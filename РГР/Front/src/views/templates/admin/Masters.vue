<script setup>
import Sidebar from "@/views/components/Sidebar.vue";
import {onMounted, ref, computed} from "vue";
import NewMaster from "@/views/components/NewMaster.vue";
import api from "@/api";
import {useI18n} from "vue-i18n";

const {t} = useI18n();
const showAddModal = ref(false);
const selectedMaster = ref(null); // Для редактирования
const selectedMasters = ref([]);
const masters = ref([]);
const isLoading = ref(false);

const selectedCount = computed(
  () => selectedMasters.value.length,
);
const allSelected = computed(() => {
  return (
    masters.value.length > 0 &&
    masters.value.every((master) =>
      selectedMasters.value.includes(master.id),
    )
  );
});

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

const toggleMasterSelection = (masterId) => {
  const index = selectedMasters.value.indexOf(masterId);
  if (index === -1) {
    selectedMasters.value.push(masterId);
  } else {
    selectedMasters.value.splice(index, 1);
  }
};

const toggleSelectAll = () => {
  if (allSelected.value) {
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
    await Promise.all(
      selectedMasters.value.map((id) => api.deleteMaster(id)),
    );
    selectedMasters.value = [];
    await loadMasters();
  } catch (error) {
    console.error("Delete failed:", error);
    alert("Ошибка при удалении мастеров");
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  selectedMaster.value = null;
  showAddModal.value = true;
};

const editMaster = (master) => {
  selectedMaster.value = master;
  showAddModal.value = true;
};

const onMasterSaved = async () => {
  await loadMasters();
  showAddModal.value = false;
  selectedMaster.value = null;
};

const refreshData = () => {
  loadMasters();
};

onMounted(() => {
  loadMasters();
});
</script>

<template>
  <Sidebar />
  <main class="sidebarred">
    <div class="column">
      <div class="flex">
        <div class="flex">
          <button class="bordered flex" @click="refreshData">
            <p
              class="phoenix-accent-text"
              style="margin-top: 4px; padding: 0"
            >
              {{ t("common.refresh") }}
            </p>
            <span class="material-icons little">refresh</span>
          </button>
        </div>

        <div class="flex">
          <button class="bordered flex" @click="openAddModal">
            <p
              class="phoenix-accent-text"
              style="margin-top: 4px; padding: 0"
            >
              {{ t("common.add") }}
            </p>
            <span class="material-icons little">add</span>
          </button>
        </div>

        <div class="flex">
          <button
            class="bordered flex"
            @click="deleteSelectedMasters"
            :disabled="selectedCount === 0 || isLoading"
          >
            <p
              class="phoenix-accent-text"
              style="margin-top: 4px; padding: 0"
            >
              {{ t("common.deleteSelected") }}
            </p>
            <span class="material-icons little">delete</span>
          </button>
        </div>
      </div>

      <hr />

      <div v-if="!isLoading" class="masters-table">
        <div class="table-header grid">
          <input
            type="checkbox"
            :checked="allSelected"
            @change="toggleSelectAll"
          />
          <p>
            <strong>{{ t("masters.fio") }}</strong>
          </p>
          <p>
            <strong>{{ t("masters.login") }}</strong>
          </p>
          <p>
            <strong>{{ t("masters.role") }}</strong>
          </p>
          <p>
            <strong>{{ t("common.edit") }}</strong>
          </p>
        </div>

        <div
          v-for="master in masters"
          :key="master.id"
          class="table-row grid"
        >
          <input
            type="checkbox"
            :value="master.id"
            :checked="selectedMasters.includes(master.id)"
            @change="toggleMasterSelection(master.id)"
          />
          <p>{{ master.fio || "—" }}</p>
          <p>{{ master.login || "—" }}</p>
          <p>{{ master.role || "—" }}</p>
          <div class="actions">
            <span
              class="material-icons little"
              @click="editMaster(master)"
            >
              edit
            </span>
          </div>
        </div>

        <div v-if="masters.length === 0" class="empty-state">
          <p>{{ t("masters.noMasters") }}</p>
        </div>
      </div>

      <div v-else class="loading">
        {{ t("common.loading") }}
      </div>

      <NewMaster
        v-if="showAddModal"
        :master="selectedMaster"
        @close="showAddModal = false"
        @success="onMasterSaved"
      />
    </div>
  </main>
</template>

<style scoped>
.sidebarred {
  flex: 1;
  padding: 2rem;
  overflow-x: auto;
}

.masters-table {
  margin-top: 1rem;
  overflow-x: auto;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 50px 1fr 1fr 1fr 100px;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.table-header {
  border-bottom: 2px solid var(--secondary);
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

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions .material-icons {
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--primary);
  transition: transform 0.2s;
}

.actions .material-icons:hover {
  transform: scale(1.1);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--grey);
}

.loading {
  text-align: center;
  padding: 2rem;
}

@media (max-width: 900px) {
  .table-header,
  .table-row {
    grid-template-columns: 50px 200px 150px 120px 80px;
    min-width: 600px;
  }

  .sidebarred {
    padding: 1rem;
  }
}
</style>
