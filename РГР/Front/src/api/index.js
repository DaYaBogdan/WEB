import axios from "axios";

const apiClient = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "http://localhost:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

//----------------------------------------------------------------------------
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// apiClient.interceptors.request.use((config) => {
//   console.log(
//     `Отправка запроса: ${config.method?.toUpperCase()} ${config.url}`,
//   );
//   return config;
// });

//----------------------------------------------------------------------------
export default {
  // Логин
  login(credentials) {
    return apiClient.post("auth/login", credentials);
  },
  // Регистрация
  register(credentials) {
    return apiClient.post("auth/register", credentials);
  },
  createTask(taskData) {
    return apiClient.post("diary/pushTask", taskData);
  },
  getTasks(userID) {
    return apiClient.get(`diary/getTasks/${userID}`);
  },
  deleteTask(taskId) {
    return apiClient.delete(`diary/deleteTask/${taskId}`);
  },
  addCustomer(data) {
    return apiClient.post("managing/newClient", data);
  },
  getCustomers() {
    return apiClient.get("managing/getAllClients", {
      params: {skip: 0, limit: 100},
    });
  },
  updateCustomer(customer_id, customer_data) {
    return apiClient.put(
      `managing/updateClient/${customer_id}`,
      customer_data,
    );
  },
  // В api/index.js
  deleteCustomer(id) {
    return apiClient.delete(`managing/deleteClient/${id}`);
  },
  makeWeekend(data) {
    return apiClient.post("diary/makeWeekend", data);
  },
  getWeekends(userID) {
    return apiClient.get(`diary/getWeekends/${userID}`);
  },
  deleteWeekend(weekend_id) {
    return apiClient.delete(
      `diary/deleteWeekend/${weekend_id}`,
    );
  },
  getMasters() {
    return apiClient.get("masters/getAllMasters/");
  },
  getMaster(masterId) {
    return apiClient.get(`/masters/getMaster/${masterId}`);
  },
  updateMaster(masterId, masterData) {
    return apiClient.put(
      `/masters/updateMaster/${masterId}`,
      masterData,
    );
  },
  deleteMaster(master_id) {
    return apiClient.delete(
      `masters/deleteMaster/${master_id}`,
    );
  },
  getSettings(user_id) {
    return apiClient.get(`settings/get/${user_id}`);
  },
  updateSettings(user_id, settingsData) {
    return apiClient.put(
      `settings/update/${user_id}`, // Теперь user_id передается правильно
      settingsData,
    );
  },
  getAllTasks() {
    return apiClient.get("/diary/getAllTasks");
  },
};
