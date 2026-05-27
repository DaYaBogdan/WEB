import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

//----------------------------------------------------------------------------
// apiClient.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem("authToken");
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => Promise.reject(error),
// );

apiClient.interceptors.request.use((config) => {
  console.log(
    `Отправка запроса: ${config.method?.toUpperCase()} ${config.url}`,
  );
  return config;
});

//----------------------------------------------------------------------------
export default {
  // Запрос на получение юзера
  login(credentials) {
    return apiClient.post("/login", credentials);
  },
  // Все посты
  getPosts() {
    return apiClient.get("/posts");
  },
  // Один пост по ID
  getPost(id) {
    return apiClient.get(`/posts/${id}`);
  },
  // Создать новый пост
  createPost(postData) {
    return apiClient.post("/posts", postData);
  },
  // Обновить пост
  updatePost(id, postData) {
    return apiClient.put(`/posts/${id}`, postData);
  },
  // Удалить пост
  deletePost(id) {
    return apiClient.delete(`/posts/${id}`);
  },
};
