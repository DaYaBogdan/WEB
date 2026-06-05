import {createStore} from "vuex";
import router from "@/router";
import api from "@/api";

export default createStore({
  state: {
    user: (() => {
      const userStr = localStorage.getItem("user");
      if (userStr) {
        try {
          return JSON.parse(userStr);
        } catch (e) {
          return null;
        }
      }
      return null;
    })(),
    token: localStorage.getItem("token") || null,
    tasks: (() => {
      const tasksStr = localStorage.getItem("tasks");
      if (tasksStr) {
        try {
          return JSON.parse(tasksStr);
        } catch (e) {
          return [];
        }
      }
      return [];
    })(),
    customers: (() => {
      const customersStr = localStorage.getItem("customers");
      if (customersStr) {
        try {
          return JSON.parse(customersStr);
        } catch (e) {
          return [];
        }
      }
      return [];
    })(),
    weekends: (() => {
      const weekendStr = localStorage.getItem("weekends");
      if (weekendStr) {
        try {
          return JSON.parse(weekendStr);
        } catch (e) {
          return [];
        }
      }
      return [];
    })(),
    selectedTaskIds: [],
    isLoading: false,
    error: null,
  },
  getters: {
    isLogged: (state) => !!state.user,
    userRole: (state) => state.user?.role || "guest",
    getTasks: (state) => state.tasks,
    getCustomers: (state) => state.customers,
    getWeekends: (state) => state.weekends,
    isLoading: (state) => state.isLoading,
    getError: (state) => state.error,
    getSelectedTaskIds: (state) => state.selectedTaskIds,
    getSelectedTasksCount: (state) =>
      state.selectedTaskIds.length,
  },
  mutations: {
    //--------------------------------------------
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    SET_TASKS(state, tasks) {
      state.tasks = tasks;
      if (tasks && tasks.length > 0) {
        localStorage.setItem("tasks", JSON.stringify(tasks));
      } else {
        localStorage.removeItem("tasks");
      }
    },
    SET_CUSTOMERS(state, customers) {
      state.customers = customers;
      if (customers && customers.length > 0) {
        localStorage.setItem(
          "customers",
          JSON.stringify(customers),
        );
      } else {
        localStorage.removeItem("customers");
      }
    },
    SET_WEEKENDS(state, weekends) {
      state.weekends = weekends;
      if (weekends && weekends.length > 0) {
        localStorage.setItem(
          "weekends",
          JSON.stringify(weekends),
        );
      } else {
        localStorage.removeItem("weekends");
      }
    },
    //--------------------------------------------
    ADD_SELECTED_TASK(state, taskId) {
      if (!state.selectedTaskIds.includes(taskId)) {
        state.selectedTaskIds.push(taskId);
      }
    },
    REMOVE_SELECTED_TASK(state, taskId) {
      const index = state.selectedTaskIds.indexOf(taskId);
      if (index !== -1) {
        state.selectedTaskIds.splice(index, 1);
      }
    },
    CLEAR_SELECTED_TASKS(state) {
      state.selectedTaskIds = [];
    },
    SET_SELECTED_TASKS(state, taskIds) {
      state.selectedTaskIds = taskIds;
    },
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    //--------------------------------------------
    SET_USER(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem("user", JSON.stringify(user));
      } else {
        localStorage.removeItem("user");
      }
    },
    LOGOUT(state) {
      state.user = null;
      state.token = null;
      state.tasks = [];
      state.customers = [];
      state.selectedTaskIds = [];
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("tasks");
      localStorage.removeItem("customers");
    },
  },
  actions: {
    // --------------------- SESSION ACTIVITY ACTIONS -----------------------------
    async login({commit}, credentials) {
      try {
        const response = await api.login(credentials);

        const {user, access_token} = response.data;
        commit("SET_USER", user);
        commit("SET_TOKEN", access_token);

        router.push("/Diary");
        return Promise.resolve(user);
      } catch (error) {
        console.error("Login failed:", error);
        return Promise.reject(error);
      }
    },
    async logout({commit}) {
      commit("LOGOUT");
      router.push("/");
    },
    async restoreSession({commit}) {
      const token = localStorage.getItem("token");
      const storedUser = localStorage.getItem("user");
      const storedTasks = localStorage.getItem("tasks");
      if (token && storedUser) {
        commit("SET_TOKEN", token);
        commit("SET_USER", JSON.parse(storedUser));
        if (storedTasks) {
          commit("SET_TASKS", JSON.parse(storedTasks));
        }
      } else {
        commit("LOGOUT");
      }
    },
    // --------------------- GET ACTIONS -----------------------------
    async getTasks({commit, state}) {
      try {
        if (!state.user?.id) {
          console.error("User login not found");
          return Promise.reject(
            new Error("User not authenticated"),
          );
        }

        const response = await api.getTasks(state.user.id);

        const tasks = response.data.tasks || [];

        const tasksWithDateAndTime =
          addDateAndTimeToTasks(tasks);

        commit("SET_TASKS", tasksWithDateAndTime);
        return Promise.resolve(tasksWithDateAndTime);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
        commit("SET_TASKS", []);
        return Promise.reject(error);
      }
    },
    async getClients({commit, state}) {
      try {
        if (!state.user?.id) {
          console.error("User login not found");
          return Promise.reject(
            new Error("User not authenticated"),
          );
        }

        const response = await api.getCustomers();

        const customers = response.data || [];

        commit("SET_CUSTOMERS", customers);
        return Promise.resolve(customers);
      } catch (error) {
        console.error("Failed to fetch clients:", error);
        commit("SET_CUSTOMERS", []);
        return Promise.reject(error);
      }
    },
    async getWeekends({commit, state}) {
      try {
        if (!state.user?.id) {
          console.error("User login not found");
          return Promise.reject(
            new Error("User not authenticated"),
          );
        }

        const response = await api.getWeekends(state.user.id);

        const weekends = response.data.weekends || [];

        commit("SET_WEEKENDS", weekends);
        return Promise.resolve(weekends);
      } catch (error) {
        console.error("Failed to fetch weekends:", error);
        commit("SET_WEEKENDS", []);
        return Promise.reject(error);
      }
    },
    // --------------------- POST ACTIONS -----------------------------
    async makeWeekend({commit, state, dispatch}, day) {
      try {
        const data = {master_id: state.user.id, date: day};
        console.log(data);
        await api.makeWeekend(data);

        await dispatch("getWeekends");

        router.push("/Diary");
        return Promise.resolve();
      } catch (error) {
        console.error("Making weekend failed:", error);
        return Promise.reject(error);
      }
    },
    // --------------------- DELETE ACTIONS -----------------------------
    async deleteWeekend({commit, state, dispatch}, id) {
      try {
        await api.deleteWeekend(id);

        await dispatch("getWeekends");

        router.push("/Diary");
        return Promise.resolve();
      } catch (error) {
        console.error("Making weekend failed:", error);
        return Promise.reject(error);
      }
    },
    async deleteClients({commit, state, dispatch}, clientIds) {
      if (!clientIds || clientIds.length === 0) {
        throw new Error("Выберите клиентов для удаления");
      }

      commit("SET_LOADING", true);
      commit("SET_ERROR", null);

      try {
        // Удаляем клиентов ПОСЛЕДОВАТЕЛЬНО, а не параллельно
        for (const id of clientIds) {
          await api.deleteCustomer(id);
        }

        // Перезагружаем список клиентов
        await dispatch("getClients");

        console.log(`Deleted ${clientIds.length} clients`);
      } catch (error) {
        console.error("Failed to delete clients:", error);
        commit("SET_ERROR", error.message);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },
    async deleteSelectedTasks({commit, state, dispatch}) {
      if (state.selectedTaskIds.length === 0) {
        throw new Error("Выберите задачи для удаления");
      }

      const confirmed = confirm(
        `Удалить ${state.selectedTaskIds.length} задачу(и)?`,
      );
      if (!confirmed) return;

      commit("SET_LOADING", true);
      commit("SET_ERROR", null);

      try {
        // Удаляем все выбранные задачи
        await Promise.all(
          state.selectedTaskIds.map((id) =>
            api.deleteTask(id),
          ),
        );

        // Перезагружаем задачи
        await dispatch("getTasks");

        // Очищаем выбор
        commit("CLEAR_SELECTED_TASKS");

        console.log(
          `Deleted ${state.selectedTaskIds.length} tasks`,
        );
      } catch (error) {
        console.error("Failed to delete tasks:", error);
        commit("SET_ERROR", error.message);
        throw error;
      } finally {
        commit("SET_LOADING", false);
      }
    },
    // --------------------- ESSENTIAL ACTIONS -----------------------------
    toggleTaskSelection({commit}, taskId) {
      commit("ADD_SELECTED_TASK", taskId);
    },
    removeTaskSelection({commit}, taskId) {
      commit("REMOVE_SELECTED_TASK", taskId);
    },
    clearSelectedTasks({commit}) {
      commit("CLEAR_SELECTED_TASKS");
    },
  },
});

function addDateAndTimeToTasks(tasks) {
  return tasks.map((task) => ({
    ...task,
    date:
      task.dateTime ?
        new Date(task.dateTime).toISOString().split("T")[0]
      : null,
    time:
      task.dateTime ?
        new Date(task.dateTime).toLocaleTimeString("ru-RU", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      : null,
  }));
}
