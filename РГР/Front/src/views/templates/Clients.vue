<script setup>
import Sidebar from "../components/Sidebar.vue";
import {onMounted, ref, computed} from "vue";
import {useStore} from "vuex";
import NewCustomer from "../components/NewCustomer.vue";
import {useI18n} from "vue-i18n";

const {t} = useI18n();

const showAddModal = ref(false);
const selectedCustomer = ref(null); // Для редактирования
const isLoading = ref(false);
const selectedClients = ref([]);
const store = useStore();

const clients = computed(() => store.getters.getCustomers);

const selectedCount = computed(
  () => selectedClients.value.length,
);
const allSelected = computed(() => {
  return (
    clients.value.length > 0 &&
    clients.value.every((client) =>
      selectedClients.value.includes(client.id),
    )
  );
});

const toggleClientSelection = (clientId) => {
  const index = selectedClients.value.indexOf(clientId);
  if (index === -1) {
    selectedClients.value.push(clientId);
  } else {
    selectedClients.value.splice(index, 1);
  }
};

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedClients.value = [];
  } else {
    selectedClients.value = clients.value.map((c) => c.id);
  }
};

const deleteSelectedClients = async () => {
  if (selectedClients.value.length === 0) return;

  if (
    !confirm(
      `Вы уверены, что хотите удалить ${selectedClients.value.length} клиента(ов)?`,
    )
  ) {
    return;
  }

  isLoading.value = true;
  try {
    await store.dispatch(
      "deleteClients",
      selectedClients.value,
    );
    selectedClients.value = [];
    await loadClients();
  } catch (error) {
    console.error("Delete failed:", error);
    alert("Ошибка при удалении клиентов");
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  selectedCustomer.value = null;
  showAddModal.value = true;
};

const editCustomer = (customer) => {
  selectedCustomer.value = customer;
  showAddModal.value = true;
};

const onClientSaved = async () => {
  await loadClients();
  showAddModal.value = false;
  selectedCustomer.value = null;
};

const loadClients = async () => {
  isLoading.value = true;
  try {
    await store.dispatch("getClients");
    console.log("Clients loaded");
  } catch (error) {
    console.error("Failed to load clients:", error);
  } finally {
    isLoading.value = false;
  }
};

const refreshData = () => {
  loadClients();
};

onMounted(() => {
  loadClients();
});
</script>

<template>
  <Sidebar />
  <main class="sidebarred">
    <div class="column">
      <!-- Заголовок и управление -->
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
            @click="deleteSelectedClients"
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

      <!-- Основная таблица клиентов -->
      <div v-if="!isLoading" class="clients-table">
        <div class="table-header grid">
          <input
            type="checkbox"
            :checked="allSelected"
            @change="toggleSelectAll"
          />
          <p>
            <strong>{{ t("clients.fio") }}</strong>
          </p>
          <p>
            <strong>{{ t("clients.phone") }}</strong>
          </p>
          <p>
            <strong>{{ t("clients.email") }}</strong>
          </p>
          <p>
            <strong>{{ t("clients.edit") }}</strong>
          </p>
        </div>

        <div
          v-for="client in clients"
          :key="client.id"
          class="table-row grid"
        >
          <input
            type="checkbox"
            :value="client.id"
            :checked="selectedClients.includes(client.id)"
            @change="toggleClientSelection(client.id)"
          />
          <p>{{ client.FIO || "—" }}</p>
          <p>{{ client.phone || "—" }}</p>
          <p>{{ client.email || "—" }}</p>
          <div class="actions">
            <span
              class="material-icons little"
              @click="editCustomer(client)"
            >
              edit
            </span>
          </div>
        </div>

        <div v-if="clients.length === 0" class="empty-state">
          <p>{{ t("clients.noClients") }}</p>
        </div>
      </div>

      <div v-else class="loading">
        {{ t("common.loading") }}
      </div>

      <NewCustomer
        v-if="showAddModal"
        :customer="selectedCustomer"
        @close="showAddModal = false"
        @success="onClientSaved"
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

.clients-table {
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
    grid-template-columns: 50px 200px 150px 150px 80px;
    min-width: 630px;
  }

  .sidebarred {
    padding: 1rem;
  }
}
</style>
