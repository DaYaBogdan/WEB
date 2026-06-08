<script setup>
import Sidebar from "../components/Sidebar.vue";
import {onMounted, ref, computed} from "vue";
import {useStore} from "vuex";
import NewCustomer from "../components/NewCustomer.vue";

const showAddModal = ref(false);
const isLoading = ref(false);
const selectedClients = ref([]);
const store = useStore();

const clients = computed(() => store.getters.getCustomers);

const selectedCount = computed(
  () => selectedClients.value.length,
);

const toggleClientSelection = (clientId) => {
  const index = selectedClients.value.indexOf(clientId);
  if (index === -1) {
    selectedClients.value.push(clientId);
  } else {
    selectedClients.value.splice(index, 1);
  }
};

const selectAll = () => {
  if (selectedClients.value.length === clients.value.length) {
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
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  showAddModal.value = true;
};

const onClientCreated = async () => {
  await loadClients();
  showAddModal.value = false;
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

onMounted(() => {
  loadClients();
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
          @click="deleteSelectedClients"
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
          :disabled="!clients.length"
        >
          <p
            class="phoenix-accent-text"
            style="margin-top: 4px; padding: 0"
          >
            {{
              selectedCount === clients.length ?
                "Снять все"
              : "Выбрать все"
            }}
          </p>
        </button>
      </div>

      <hr />

      <div class="clients-list">
        <!-- Шапка таблицы - отображается один раз, если есть клиенты -->
        <div
          class="client-item header grid"
          style="grid-template-columns: repeat(2, 1fr) 1fr 1fr"
          v-if="clients.length"
        >
          <p></p>
          <p class="header-text">
            <strong>ФИО</strong>
          </p>
          <p class="header-text">
            <strong>Номер телефона</strong>
          </p>
        </div>

        <!-- Строки с данными клиентов -->
        <div
          class="client-item grid"
          style="grid-template-columns: repeat(2, 1fr) 1fr 1fr"
          v-for="client in clients"
          :key="client.id"
        >
          <input
            type="checkbox"
            :value="client.id"
            :checked="selectedClients.includes(client.id)"
            @change="toggleClientSelection(client.id)"
          />
          <p>{{ client.FIO }}</p>
          <p>{{ client.phone }}</p>
        </div>

        <div v-if="!clients.length" class="empty-state">
          <p>Нет добавленных клиентов</p>
        </div>
      </div>

      <NewCustomer
        v-if="showAddModal"
        @close="showAddModal = false"
        @success="onClientCreated"
      />
    </div>
  </main>
</template>

<style scoped>
.clients-list {
  margin-top: 1rem;
}

.client-item {
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.client-item:hover:not(.header) {
  background-color: #f5f5f5;
}

.client-item.header {
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

/* Дополнительные стили для улучшения внешнего вида */
.grid {
  display: grid;
  gap: 1rem;
}

.bordered {
  margin-right: 0.5rem;
}
</style>
